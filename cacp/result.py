from pathlib import Path

import pandas as pd

from cacp.util import to_latex


def process_comparison_results(result_dir: Path):
    """
    Processes comparison results, computes mean values for all metrics.

    :param result_dir: results directory

    """
    df = pd.read_csv(result_dir.joinpath('comparison.csv'))

    gb = ['algorithm']
    dfg = df.groupby(gb)
    df = dfg.mean()
    dfg_std = dfg.std()

    metrics = ['auc', 'accuracy', 'precision', 'recall', 'f1']
    df_csv = df.copy(deep=True)
    for metric in metrics:
        df_csv.insert(list(df_csv.columns).index(metric) + 1, f'{metric} +/-', dfg_std[metric])

    columns = ['auc', 'auc +/-', 'accuracy', 'accuracy +/-',
               'precision', 'precision +/-', 'recall', 'recall +/-', 'f1', 'f1 +/-']
    df_csv = df_csv[columns]
    df_csv = df_csv.sort_values(by=['auc', 'accuracy'], ascending=False)

    df_csv.reset_index(inplace=True)
    df_csv.index += 1
    df_csv.to_csv(result_dir.joinpath('comparison_result.csv'))

    df_tex = df_csv.copy(deep=True)
    for metric in metrics:
        metric_pm = metric + ' +/-'
        df_tex[metric] = df_tex[metric].apply(lambda x: "{:1.3f}".format(x))
        df_tex[metric_pm] = df_tex[metric_pm].apply(lambda x: "{:1.3f}".format(x))
        df_tex[metric] = df_tex[metric].astype(str) + r'$\pm$' + df_tex[metric_pm].astype(str)
        del df_tex[metric_pm]

    f = result_dir.joinpath('comparison_result.tex').open('w')
    tex = to_latex(
        df_tex,
        caption='Results of comparison',
        label='tab:comparison',
    )
    f.write(tex)
