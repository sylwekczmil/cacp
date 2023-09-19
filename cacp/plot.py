import typing
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from cacp.comparison import DEFAULT_METRICS, DEFAULT_INCREMENTAL_METRICS


def process_comparison_results_plots(result_dir: Path,
                                     metrics: typing.Sequence[typing.Tuple[str, typing.Callable]] = DEFAULT_METRICS):
    """
    Generates plots from comparison results.

    :param result_dir: results directory
    :param metrics: metrics collection

    """
    df_results = pd.read_csv(result_dir.joinpath('comparison.csv'))
    plot_dir = result_dir.joinpath('plot')
    plot_dir.mkdir(exist_ok=True, parents=True)

    def boxplot_sorted(df, by, column, file_suffix):
        df2 = pd.DataFrame({col: vals[column] for col, vals in df.groupby(by)})
        meds = df2.median().sort_values(ascending=False)
        df2[meds.index].boxplot(return_type="axes")
        plt.title('')
        plt.suptitle('')
        plt.ylabel(column)
        plt.xlabel('Algorithm')
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.savefig(plot_dir.joinpath(f'comparison_{column.lower()}{file_suffix}.eps'))
        plt.savefig(plot_dir.joinpath(f'comparison_{column.lower()}{file_suffix}.png'))
        plt.close()

    for metric, _ in metrics:
        boxplot_sorted(df_results, column=metric, by='Algorithm', file_suffix='_per_fold')
        boxplot_sorted(df_results.groupby(['Algorithm', 'Dataset']).mean().reset_index(level=0),
                       column=metric, by='Algorithm', file_suffix='_per_dataset')


@dataclass
class Line:
    x: np.ndarray
    y: np.ndarray
    label: str = ''


def process_comparison_results_incremental_plot(file_name: str, y_label: str, lines: typing.List[Line], plot_dir: Path):
    for line in lines:
        plt.plot(line.x, line.y, label=line.label)
    plt.xlabel('Number of samples')
    plt.ylabel(y_label)
    ax = plt.gca()
    if len(lines) > 1:
        ax.legend()
    ax.set_ylim([-0.05, 1.05])
    plt.savefig(plot_dir.joinpath(f'{file_name}.eps'))
    plt.savefig(plot_dir.joinpath(f'{file_name}.png'))
    plt.close()


def process_comparison_results_single_incremental_plot(classifier_name: str, dataset_name: str, metric: str,
                                                       df: pd.DataFrame, incremental_plot_dir: Path):
    """
    Generates plots from single incremental comparison results.

    :param classifier_name: classifier name
    :param dataset_name: dataset name
    :param metric: metric name
    :param df: result dataframe
    :param incremental_plot_dir: output plot directory

    """

    incremental_classifier_single_plot_dir = incremental_plot_dir.joinpath('single').joinpath(classifier_name)
    incremental_classifier_single_plot_dir.mkdir(exist_ok=True, parents=True)
    line = Line(df['index'], df[metric])
    process_comparison_results_incremental_plot(
        f"{classifier_name}_{dataset_name}_{metric.lower()}",
        metric,
        [line],
        incremental_classifier_single_plot_dir
    )


def process_comparison_results_incremental_plots(
    result_dir: Path,
    metrics: typing.Sequence[typing.Tuple[str, typing.Callable]] = DEFAULT_INCREMENTAL_METRICS
):
    """
    Generates plots from incremental comparison results.

    :param result_dir: results directory
    :param metrics: metrics collection

    """
    incremental_comparison_dir = result_dir.joinpath('incremental').joinpath('result')
    incremental_plot_dir = result_dir.joinpath('incremental').joinpath('plot')
    incremental_plot_dir.mkdir(exist_ok=True, parents=True)

    dataset_dfs = defaultdict(list)
    classifier_names = []
    metrics_names = [m for m, _ in metrics]

    for classifier_dir in incremental_comparison_dir.glob("*"):
        classifier_name = classifier_dir.stem
        classifier_names.append(classifier_name)
        for classifier_dataset_file in classifier_dir.glob("*.csv"):
            dataset_name = classifier_dataset_file.stem
            df = pd.read_csv(classifier_dataset_file)
            dataset_dfs[dataset_name].append(df)
            for metric in metrics_names:
                process_comparison_results_single_incremental_plot(
                    classifier_name,
                    dataset_name,
                    metric,
                    df,
                    incremental_plot_dir
                )

    for dataset_name, dfs in dataset_dfs.items():
        for metric in metrics_names:
            lines = [Line(df['index'], df[metric], classifier_names[i]) for i, df in enumerate(dfs)]
            process_comparison_results_incremental_plot(
                f"{dataset_name}_{metric.lower()}",
                metric,
                lines,
                incremental_plot_dir
            )
