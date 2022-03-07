import inspect
import os
import time
import typing
from pathlib import Path

import pandas as pd
from joblib import delayed, Parallel
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from tqdm import tqdm

from cacp.dataset import ClassificationDataset, AVAILABLE_N_FOLDS, ClassificationFoldData
from cacp.util import auc_score


def process_comparison_single(classifier_factory, classifier_name,
                              dataset: ClassificationDataset,
                              fold: ClassificationFoldData) -> dict:
    """
    Runs comparison on single classifier and dataset.

    :param classifier_factory: classifier factory
    :param classifier_name: classifier name
    :param dataset: single dataset
    :param fold: fold data
    :return: dictionary of calculated metrics and metadata

    """
    cls = classifier_factory(fold.x_train.shape[1], len(fold.labels))
    train_start_time = time.time()
    labels = fold.labels
    if 'classes' in inspect.getfullargspec(cls.fit).args:
        cls.fit(fold.x_train, fold.y_train, classes=labels.tolist())
    else:
        cls.fit(fold.x_train, fold.y_train)
    train_time = (time.time() - train_start_time)
    pred_start_time = time.time()
    pred = cls.predict(fold.x_test)
    pred_time = (time.time() - pred_start_time)

    return {
        'dataset': dataset.name,
        'algorithm': classifier_name,
        'number_of_classes': len(set(fold.y_train)),
        'train_size': len(fold.x_train),
        'test_size': len(fold.x_test),
        'cv_idx': fold.index,
        'accuracy': accuracy_score(fold.y_test, pred),
        'precision': precision_score(fold.y_test, pred, average='weighted', labels=labels, zero_division=0),
        'recall': recall_score(fold.y_test, pred, average='weighted', labels=labels, zero_division=0),
        'f1': f1_score(fold.y_test, pred, average='weighted', labels=labels, zero_division=0),
        'auc': auc_score(fold.y_test, pred, average='weighted', multi_class='ovo', labels=labels),
        'train_time': train_time,
        'pred_time': pred_time
    }


def process_comparison(
    datasets: typing.List[ClassificationDataset],
    classifiers: typing.List[typing.Tuple[str, typing.Callable]],
    result_dir: Path,
    n_folds: AVAILABLE_N_FOLDS = 10,
    dob_scv: bool = True,
    categorical_to_numerical=True,
    normalized: bool = False,
):
    """
    Runs comparison for provided datasets and classifiers.

    :param datasets: dataset collection
    :param classifiers: classifiers collection
    :param result_dir: results directory
    :param n_folds: number of folds {5,10}
    :param dob_scv: if folds distribution optimally balanced stratified cross-validation (DOB-SCV) should be used
    :param categorical_to_numerical: if dataset categorical values should be converted to numerical
    :param normalized: if the data should be normalized in range [0..1]

    """
    count = 0
    records = []
    df = None

    with tqdm(total=len(datasets) * n_folds, desc='Processing comparison', unit='fold') as pbar:
        for dataset_idx, dataset in enumerate(datasets):
            for fold in dataset.folds(n_folds=n_folds, dob_scv=dob_scv,
                                      categorical_to_numerical=categorical_to_numerical):
                if normalized:
                    fold.normalize()
                rows = Parallel(n_jobs=len(classifiers))(
                    delayed(process_comparison_single)(c, c_n, dataset, fold) for c_n, c in classifiers)
                records.extend(rows)
                pbar.update(1)

            df = pd.DataFrame(records)
            df = df.sort_values(by=['dataset', 'algorithm', 'cv_idx'])
            count += 1
            df.to_csv(result_dir.joinpath(f'comparison_{count}.csv'), index=False)
            if count > 1:
                prev_file = result_dir.joinpath(f'comparison_{count - 1}.csv')
                if os.path.isfile(prev_file):
                    os.remove(prev_file)

    if df is not None:
        prev_file = result_dir.joinpath(f'comparison_{count}.csv')
        if os.path.isfile(prev_file):
            os.remove(prev_file)
        df.to_csv(result_dir.joinpath('comparison.csv'), index=False)
