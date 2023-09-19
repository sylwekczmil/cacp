import typing
from pathlib import Path

import pandas as pd

from cacp.comparison import DEFAULT_METRICS
from cacp.util import to_latex


def process_comparison_result_winners_for_metric(metric: str, result_dir: Path) -> pd.DataFrame:
    """
    Processes comparison results, finds winners for metric.

    :param metric: comparison metric {auc, accuracy, precision, recall, f1}
    :param result_dir: results directory
    :return: DateFrame with winners for metric

    """
    df = pd.read_csv(result_dir.joinpath('comparison.csv'))
    algorithms = df['Algorithm'].unique()
    places = [i for i in range(min(len(algorithms), 3))]

    winner_dir = result_dir.joinpath('winner').joinpath(metric.lower())
    winner_dir.mkdir(exist_ok=True, parents=True)

    def count_places(place=0):
        count = {a: 0 for a in algorithms}
        names = {a: [] for a in algorithms}
        for dataset, df_d in df.groupby('Dataset'):
            df_d_a_m = df_d.groupby('Algorithm').mean(numeric_only=True).sort_values(by=[metric], ascending=False)
            best = df_d_a_m.iloc[place]
            count[best.name] += 1
            names[best.name].append(dataset)

        return count, names

    counts = []
    for c, n in [count_places(i) for i in places]:
        counts.append(c)

    rows = []
    for algorithm in algorithms:
        row = [algorithm]
        for p in places:
            row.append(counts[p][algorithm])
        rows.append(row)

    columns = ['Algorithm'] + ['1st', '2nd', '3rd'][: len(places)]
    df_r = pd.DataFrame(columns=columns, data=rows)
    df_r = df_r.sort_values(by=['1st'], ascending=False)
    df_r.reset_index(drop=True, inplace=True)
    df_r.index += 1
    df_r.to_csv(winner_dir.joinpath('comparison_result.csv'), index=True)
    winner_dir.joinpath('comparison_result.tex').open('w').write(
        to_latex(
            df_r,
            caption=f'Ranking of compared algorithms for {metric}',
            label=f'tab:places_{metric}',
        )
    )

    return df_r


def process_comparison_result_winners(result_dir: Path,
                                      metrics: typing.Sequence[typing.Tuple[str, typing.Callable]] = DEFAULT_METRICS):
    """
    Processes comparison results, finds winners.

    :param result_dir: results directory
    :param metrics: metrics collection

    """
    wins_df = None
    for metric, _ in metrics:
        metric_wins = process_comparison_result_winners_for_metric(metric, result_dir).sort_values(by=['Algorithm'])
        if wins_df is None:
            wins_df = metric_wins[['Algorithm']].copy()

        for c in metric_wins.columns[1:]:
            wins_df[f'{metric} {c}'] = metric_wins[c].values

    winner_dir = result_dir.joinpath('winner')
    winner_dir.mkdir(exist_ok=True, parents=True)
    wins_df = wins_df.sort_values(by=wins_df.columns[1:].values.tolist(), ascending=False)
    wins_df.reset_index(drop=True, inplace=True)
    wins_df.index += 1
    wins_df.to_csv(winner_dir.joinpath('comparison.csv'), index=True)
    winner_dir.joinpath('comparison.tex').open('w').write(
        to_latex(
            wins_df,
            caption='Ranking of compared algorithms',
            label='tab:places',
        )
    )
