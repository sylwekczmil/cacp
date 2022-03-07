from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def process_comparison_results_plots(result_dir: Path):
    """
    Generates plots from comparison results.

    :param result_dir: results directory

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
        y_label = 'AUC' if metric == 'auc' else metric.capitalize()
        plt.ylabel(y_label)
        plt.xlabel('Algorithm')
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.savefig(plot_dir.joinpath(f'comparison_{metric}{file_suffix}.eps'))
        plt.savefig(plot_dir.joinpath(f'comparison_{metric}{file_suffix}.png'))
        plt.close()

    for metric in ['auc', 'accuracy', 'precision', 'recall', 'f1']:
        boxplot_sorted(df_results, column=metric, by='algorithm', file_suffix='_per_fold')
        boxplot_sorted(df_results.groupby(['algorithm', 'dataset']).mean().reset_index(level=0),
                       column=metric, by='algorithm', file_suffix='_per_dataset')
