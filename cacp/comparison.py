import inspect
import os
import time
import typing
from pathlib import Path

import pandas as pd
from joblib import delayed, Parallel
from tqdm import tqdm

from cacp.dataset import ClassificationDatasetBase, ClassificationFoldData, AVAILABLE_N_FOLDS, \
    ClassificationFoldDataModifierBase, ClassificationFoldDataNormalizer
from cacp.util import accuracy, precision, recall, auc, f1

DEFAULT_METRICS = (('AUC', auc), ('Accuracy', accuracy), ('Precision', precision), ('Recall', recall), ('F1', f1))


def process_comparison_single(classifier_factory, classifier_name,
                              dataset: ClassificationDatasetBase,
                              fold: ClassificationFoldData,
                              metrics: typing.Sequence[typing.Tuple[str, typing.Callable]],
                              ) -> dict:
    """
    Runs comparison on single classifier and dataset.

    :param classifier_factory: classifier factory
    :param classifier_name: classifier name
    :param dataset: single dataset
    :param fold: fold data
    :param metrics: metrics collection
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

    result = {
        'Dataset': dataset.name,
        'Algorithm': classifier_name,
        'Number of classes': len(set(fold.y_train)),
        'Train size': len(fold.x_train),
        'Test size': len(fold.x_test),
        'CV index': fold.index,
        'Train time [s]': train_time,
        'Prediction time [s]': pred_time
    }

    for (metric, metric_fun) in metrics:
        result[metric] = metric_fun(fold.y_test, pred, labels)

    return result


def process_comparison(
    datasets: typing.List[ClassificationDatasetBase],
    classifiers: typing.List[typing.Tuple[str, typing.Callable]],
    result_dir: Path,
    metrics: typing.Sequence[typing.Tuple[str, typing.Callable]] = DEFAULT_METRICS,
    n_folds: AVAILABLE_N_FOLDS = 10,
    custom_fold_modifiers: typing.List[ClassificationFoldDataModifierBase] = None,
    dob_scv: bool = True,
    categorical_to_numerical=True,
    normalized: bool = False
):
    """
    Runs comparison for provided datasets and classifiers.

    :param datasets: dataset collection
    :param classifiers: classifiers collection
    :param result_dir: results directory
    :param metrics: metrics collection
    :param n_folds: number of folds {5,10}
    :param custom_fold_modifiers: custom fold modifiers that can change fold data before usage
    :param dob_scv: if folds distribution optimally balanced stratified cross-validation (DOB-SCV) should be used
    :param categorical_to_numerical: if dataset categorical values should be converted to numerical
    :param normalized: if the data should be normalized in range [0..1]

    """
    count = 0
    records = []
    df = None

    fold_modifiers = []

    if custom_fold_modifiers:
        fold_modifiers.extend(custom_fold_modifiers)

    if normalized:
        fold_modifiers.append(ClassificationFoldDataNormalizer())

    with tqdm(total=len(datasets) * n_folds, desc='Processing comparison', unit='fold') as pbar:
        for dataset_idx, dataset in enumerate(datasets):
            for fold in dataset.folds(n_folds=n_folds, dob_scv=dob_scv,
                                      categorical_to_numerical=categorical_to_numerical):

                modified_fold = fold
                for fold_modifier in fold_modifiers:
                    modified_fold = fold_modifier.modify(modified_fold)

                rows = Parallel(n_jobs=len(classifiers))(
                    delayed(process_comparison_single)(c, c_n, dataset, modified_fold, metrics) for c_n, c in
                    classifiers
                )
                records.extend(rows)
                pbar.update(1)

            df = pd.DataFrame(records)
            df = df.sort_values(by=['Dataset', 'Algorithm', 'CV index'])
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
