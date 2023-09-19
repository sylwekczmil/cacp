from pathlib import Path

import pandas as pd

from cacp.util import to_latex


def process_times(result_dir: Path):
    """
    Processes comparison results times.

    :param result_dir: results directory

    """
    df = pd.read_csv(result_dir.joinpath('comparison.csv'))
    time_dir = result_dir.joinpath('time')
    time_dir.mkdir(exist_ok=True, parents=True)
    gb = ['Algorithm']
    dfg = df.groupby(gb)
    df = dfg.mean(numeric_only=True)
    columns = ['Train time [s]', 'Prediction time [s]']
    df_csv = df[columns]
    df_csv = df_csv.sort_values(by=columns, ascending=True)
    df_csv.to_csv(time_dir.joinpath('comparison.csv'))

    df_tex = df_csv.copy(deep=True)
    df_tex.reset_index(drop=False, inplace=True)
    df_tex.index += 1
    tex = to_latex(
        df_tex,
        caption='Results of time comparison',
        label='tab:time_comparison',
    )

    with time_dir.joinpath('comparison.tex').open('w') as f:
        f.write(tex)
