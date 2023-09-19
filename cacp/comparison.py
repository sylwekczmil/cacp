import inspect
import os
import typing
from pathlib import Path
from timeit import default_timer as timer

import pandas as pd
import river
from joblib import delayed, Parallel
from river import metrics as river_metrics, stream, utils
from river.datasets.base import Dataset
from tqdm import tqdm

from cacp.dataset import ClassificationDatasetBase, ClassificationFoldData, AVAILABLE_N_FOLDS, \
    ClassificationFoldDataModifierBase, ClassificationFoldDataNormalizer
from cacp.util import accuracy, precision, recall, auc, f1

DEFAULT_METRICS = (('AUC', auc), ('Accuracy', accuracy), ('Precision', precision), ('Recall', recall), ('F1', f1))

DEFAULT_INCREMENTAL_METRICS = (
    ('AUC', river_metrics.ROCAUC), ('Accuracy', river_metrics.Accuracy), ('Precision', river_metrics.Precision),
    ('Recall', river_metrics.Recall), ('F1', river_metrics.F1)
)


def process_comparison_single(
    classifier_factory, classifier_name,
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
    model = classifier_factory(fold.x_train.shape[1], len(fold.labels))
    train_start_time = timer()
    labels = fold.labels
    pred = None
    try:
        if 'classes' in inspect.getfullargspec(model.fit).args:
            model.fit(fold.x_train, fold.y_train, classes=labels.tolist())
        else:
            model.fit(fold.x_train, fold.y_train)
        train_time = timer() - train_start_time
        pred_start_time = timer()
        pred = model.predict(fold.x_test)
        pred_time = timer() - pred_start_time
    except Exception as e:
        train_time = 9999
        pred_time = 9999
        print(f"Error while running {classifier_name}, metrics will be set to 0", e)

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
        try:
            result[metric] = metric_fun(fold.y_test, pred, labels)
        except Exception as e:
            result[metric] = 0.
            print(f"Error while calculating {metric} for {classifier_name}, value will be set to 0", e)

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
    normalized: bool = False,
    progress=lambda progress, total: None,
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
    :param progress: function that can be used to monitor progress

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
        progress(pbar.n, pbar.total)
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
                progress(pbar.n, pbar.total)

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


def process_incremental_comparison_single(classifier_factory, classifier_name,
                                          dataset: typing.Union[
                                              ClassificationDatasetBase, Dataset
                                          ], number_of_classes: int, incremental_comparison_dir: Path,
                                          metrics: typing.Sequence[
                                              typing.Tuple[str, typing.Callable]] = DEFAULT_INCREMENTAL_METRICS
                                          ) -> dict:
    """
    Runs comparison on single classifier and dataset.

    :param classifier_factory: classifier factory
    :param classifier_name: classifier name
    :param dataset: single dataset
    :param number_of_classes: number of classes
    :param incremental_comparison_dir: incremental single results directory
    :param metrics: metrics collection
    :return: dictionary of calculated metrics and metadata

    """

    incremental_comparison_classifier_dir = incremental_comparison_dir.joinpath(classifier_name)
    incremental_comparison_classifier_dir.mkdir(exist_ok=True, parents=True)

    train_time = 0
    pred_time = 0

    train_size = 0
    dataset_name = "-"

    metric = river_metrics.base.Metrics([])

    try:
        dataset_type = type(dataset)
        if issubclass(dataset_type, ClassificationDatasetBase):
            dataset_name = dataset.name
            train_size = dataset.instances
        elif issubclass(dataset_type, Dataset):
            dataset_name = dataset.__class__.__name__.lower()
            train_size = dataset.n_samples

        metric = river_metrics.base.Metrics([m() for _, m in metrics])
        model = classifier_factory(train_size, number_of_classes)

        # Determine if predict_one or predict_proba_one should be used in case of a classifier
        if utils.inspect.isclassifier(model) and not metric.requires_labels:
            pred_func = model.predict_proba_one
        else:
            pred_func = model.predict_one

        records = []
        y_pred = None

        for i, x, y, *kwargs in stream.simulate_qa(dataset, None, None, copy=True):

            kwargs = kwargs[0] if kwargs else {}

            if y is None:
                # no ground truth, just make a prediction
                pred_start_time = timer()
                # predict
                y_pred = pred_func(x=x, **kwargs)
                pred_time_diff = timer() - pred_start_time
                pred_time += pred_time_diff
            else:
                # there's a ground truth, model and metric can be updated

                # update the metrics
                if y_pred != {} and y_pred is not None:
                    metric.update(y_true=y, y_pred=y_pred)
                    y_pred = max(y_pred, key=y_pred.get) if type(y_pred) is dict else y_pred
                    record = {
                        'index': i,
                        'y_true': y,
                        'y_pred': y_pred
                    }
                    for metric_idx, (metric_name, _) in enumerate(metrics):
                        record[metric_name] = metric.data[metric_idx].get()
                    records.append(record)

                learn_one_start_time = timer()
                # learn
                model.learn_one(x=x, y=y, **kwargs)
                learn_time_diff = timer() - learn_one_start_time
                train_time += learn_time_diff

        df = pd.DataFrame(records)
        df.to_csv(incremental_comparison_classifier_dir.joinpath(f'{dataset_name}.csv'), index=False)

    except Exception as e:
        print(f"Error while running {classifier_name}, metrics will be set to 0", e)

    result = {
        'Dataset': dataset_name,
        'Algorithm': classifier_name,
        'Number of classes': number_of_classes,
        'Train size': train_size,
        'Test size': train_size,
        'Train time [s]': train_time,
        'Prediction time [s]': pred_time
    }

    for metric_idx, (metric_name, _) in enumerate(metrics):
        try:
            value = metric.data[metric_idx].get()
            result[metric_name] = float(value)
        except Exception as e:
            print(f"Error while calculating {metric} for {classifier_name}, value will be set to 0", e)
            result[metric_name] = 0.

    return result


def process_incremental_comparison(
    datasets: typing.List[typing.Union[ClassificationDatasetBase, river.datasets.base.Dataset]],
    classifiers: typing.List[typing.Tuple[str, typing.Callable]],
    result_dir: Path,
    metrics: typing.Sequence[typing.Tuple[str, typing.Callable]] = DEFAULT_INCREMENTAL_METRICS,
    progress=lambda progress, total: None,
):
    """
    Runs comparison for provided datasets and incremental classifiers.

    :param datasets: dataset collection
    :param classifiers: classifiers collection
    :param result_dir: results directory
    :param metrics: metrics collection
    :param progress: function that can be used to monitor progress

    """

    incremental_comparison_dir = result_dir.joinpath('incremental').joinpath('result')
    incremental_comparison_dir.mkdir(exist_ok=True, parents=True)
    count = 0
    records = []
    df = None

    with tqdm(total=len(datasets), desc='Processing comparison', unit='dataset') as pbar:
        progress(pbar.n, pbar.total)
        for dataset_idx, dataset in enumerate(datasets):

            # preload dataset to prevent race conditions on file savings and count classes
            labels = set()
            for x, y in dataset:
                labels.add(y)
            number_of_classes = len(labels)

            rows = Parallel(n_jobs=len(classifiers))(
                delayed(process_incremental_comparison_single)(c, c_n, dataset, number_of_classes,
                                                               incremental_comparison_dir, metrics) for
                c_n, c in
                classifiers
            )
            records.extend(rows)
            pbar.update(1)
            progress(pbar.n, pbar.total)

            df = pd.DataFrame(records)
            df = df.sort_values(by=['Dataset', 'Algorithm'])
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
