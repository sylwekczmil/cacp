import os
import typing
from pathlib import Path

from cacp.comparison import process_comparison
from cacp.dataset import ClassificationDataset, AVAILABLE_N_FOLDS
from cacp.info import dataset_info, classifier_info
from cacp.plot import process_comparison_results_plots
from cacp.result import process_comparison_results
from cacp.time import process_times
from cacp.util import seed_everything
from cacp.wilcoxon import process_wilcoxon
from cacp.winner import process_comparison_result_winners


def run_experiment(
    datasets: typing.List[ClassificationDataset],
    classifiers: typing.List[typing.Tuple[str, typing.Callable]],
    results_directory: typing.Union[str, os.PathLike] = './result',
    n_folds: AVAILABLE_N_FOLDS = 10,
    dob_scv: bool = True,
    categorical_to_numerical=True,
    normalized: bool = False,
    seed: int = 1
):
    """
    [Main CACP Function] Runs automatic comparison of the performance evaluation of supervised classification
    algorithms by evaluating metrics on multiple datasets.

    :param datasets: dataset collection
    :param classifiers: classifiers collection
    :param results_directory: results directory
    :param n_folds: number of folds {5,10}
    :param dob_scv: if folds distribution optimally balanced stratified cross-validation (DOB-SCV) should be used
    :param categorical_to_numerical: if dataset categorical values should be converted to numerical
    :param normalized: if the data should be normalized in range [0..1]
    :param seed: random seed value

    """
    seed_everything(seed)
    result_dir = Path(results_directory)
    result_dir.mkdir(exist_ok=True, parents=True)

    dataset_info(datasets, result_dir)
    classifier_info(classifiers, result_dir)
    process_comparison(
        datasets, classifiers, result_dir,
        n_folds=n_folds,
        dob_scv=dob_scv,
        categorical_to_numerical=categorical_to_numerical,
        normalized=normalized
    )
    process_comparison_results(result_dir)
    process_comparison_results_plots(result_dir)
    process_comparison_result_winners(result_dir)
    process_times(result_dir)
    process_wilcoxon(classifiers, result_dir)
