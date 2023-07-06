import typing
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import wilcoxon

from cacp.comparison import DEFAULT_METRICS
from cacp.util import to_latex


def bold_large_p_value(data: float, format_string="%.4f") -> str:
    """
    Makes large p-value in Latex table bold

    :param data: value
    :param format_string:
    :return: bolded values string

    """
    if data > 0.05:
        return "\\textbf{%s}" % format_string % data

    return "%s" % format_string % data


def process_wilcoxon_for_metric(current_algorithm: str, metric: str, result_dir: Path) -> pd.DataFrame:
    """
    Calculates the Wilcoxon signed-rank test for comparison results single metric.

    :param current_algorithm: current algorithm
    :param metric: comparison metric {auc, accuracy, precision, recall, f1}
    :param result_dir: results directory
    :return: DateFrame with wilcoxon values for metric

    """
    wilcoxon_dir = result_dir.joinpath('wilcoxon')
    wilcoxon_dir.mkdir(exist_ok=True, parents=True)
    metric_dir = wilcoxon_dir.joinpath(metric.lower())
    metric_dir.mkdir(exist_ok=True, parents=True)

    records = []
    df = pd.read_csv(result_dir.joinpath('comparison.csv'))
    algorithms = list(df['Algorithm'].unique())
    algorithms.remove(current_algorithm)
    current_alg_df = df[df['Algorithm'] == current_algorithm]
    for algorithm in algorithms:
        a_df = df[df['Algorithm'] == algorithm]
        alg1_values = current_alg_df[metric].values
        alg2_values = a_df[metric].values
        diff = alg1_values - alg2_values
        if np.all(diff == 0):
            w, p = 'invalid-data', 1
        else:
            w, p = wilcoxon(alg1_values, alg2_values)
        row = {
            current_algorithm: current_algorithm,
            'Algorithm': algorithm,
            'p-value': p,
        }
        records.append(row)

    df_r = pd.DataFrame(records)
    df_r.reset_index(drop=True, inplace=True)
    df_r.index += 1
    df_r.to_csv(metric_dir.joinpath(f'comparison_{current_algorithm}_result.csv'), index=True)
    f = metric_dir.joinpath(f'comparison_{current_algorithm}_result.tex').open('w')
    f.write(
        to_latex(df_r,
                 caption=f"Comparison of classifiers and {current_algorithm} "
                         f"using Wilcoxon signed-rank test for {metric}",
                 label=f'tab:{current_algorithm}_wilcoxon_{metric}_comparison',
                 )
    )
    return df_r


def process_wilcoxon(classifiers: typing.List[typing.Tuple[str, typing.Callable]], result_dir: Path,
                     metrics: typing.Sequence[typing.Tuple[str, typing.Callable]] = DEFAULT_METRICS):
    """
    Calculates the Wilcoxon signed-rank test for comparison results.

    :param classifiers: classifiers collection
    :param result_dir: results directory
    :param metrics: metrics collection

    """
    for current_algorithm, _ in classifiers:
        with warnings.catch_warnings():
            warnings.simplefilter(action='ignore', category=UserWarning)
            r_df = None
            for metric, _ in metrics:
                metric_wilcoxon = process_wilcoxon_for_metric(current_algorithm, metric, result_dir)
                if metric_wilcoxon.empty:
                    continue
                metric_wilcoxon = metric_wilcoxon.sort_values(by=['Algorithm'])
                if r_df is None:
                    r_df = metric_wilcoxon[['Algorithm']].copy()

                for c in metric_wilcoxon.columns[2:]:
                    r_df[f'{metric} {c}'] = metric_wilcoxon[c].values

            wilcoxon_dir = result_dir.joinpath('wilcoxon')
            wilcoxon_dir.mkdir(exist_ok=True, parents=True)

            if r_df is None:
                return

            r_df.reset_index(drop=True, inplace=True)
            r_df.index += 1
            r_df.to_csv(wilcoxon_dir.joinpath(f'comparison_{current_algorithm}.csv'), index=True)

            for metric, _ in metrics:
                col = f'{metric} p-value'
                r_df[col] = r_df[col].apply(lambda data: bold_large_p_value(data))

            wilcoxon_dir.joinpath(f'comparison_{current_algorithm}.tex').open('w').write(
                to_latex(r_df,
                         caption=f"Comparison of classifiers and {current_algorithm} using Wilcoxon signed-rank test",
                         label='tab:wilcoxon_comparison',
                         ))
