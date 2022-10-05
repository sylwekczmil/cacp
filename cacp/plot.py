import typing
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from cacp.comparison import DEFAULT_METRICS


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
