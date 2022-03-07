import pathlib
import typing
from pathlib import Path

import pandas as pd

from cacp.dataset import ClassificationDataset
from cacp.util import to_latex


def dataset_info(datasets: typing.Iterable[ClassificationDataset], result_dir: Path):
    """
    Produces results files with list of all datasets used in experiment alog with their attributes.

    :param datasets: dataset collection
    :param result_dir: results directory

    """
    records = []
    for dataset_idx, dataset in enumerate(datasets):
        row = {
            'Dataset': dataset.name,
            'Instances': dataset.instances,
            'Features': dataset.features,
            'Classes': dataset.classes,
        }
        records.append(row)

    df = pd.DataFrame(records)
    df.index += 1
    info_dir = result_dir.joinpath('info')
    info_dir.mkdir(exist_ok=True, parents=True)
    df.to_csv(info_dir.joinpath('datasets.csv'), index=True)
    f = info_dir.joinpath('datasets.tex').open('w')
    tex = to_latex(
        df,
        caption='Datasets used to perform experiments',
        label='tab:datasets'
    )
    f.write(tex)


def classifier_info(classifiers: typing.Iterable[typing.Tuple[str, typing.Callable]], result_dir: pathlib.Path):
    """
    Produces results files with list of all classifiers used in experiment along with their attributes.

    :param classifiers: classifiers collection
    :param result_dir: results directory

    """
    records = []
    for cn, c in classifiers:
        cz = c(2, 2).__class__
        library = cz.__module__.split('.')[0]
        name = cz.__name__
        if cn == 'XGB':
            library = 'xgboost'
        name = name.replace('Classifier', '')
        if cn != 'SEVQ':
            row = {
                'Acronym': cn,
                'Name': name,
                'Library': library,
                'Type': 'offline' if (library == 'sklearn' or library == 'xgboost') else 'incremental'
            }
            records.append(row)

    df = pd.DataFrame(records)
    df = df.drop_duplicates()
    df.sort_values(['Type', 'Acronym'], inplace=True)
    df = df.reset_index(drop=True)
    df.index += 1
    info_dir = result_dir.joinpath('info')
    info_dir.mkdir(exist_ok=True, parents=True)
    df.to_csv(info_dir.joinpath('classifiers.csv'), index=True)
    f = info_dir.joinpath('classifiers.tex').open('w')
    tex = to_latex(
        df,
        caption='Classifiers used to perform experiments',
        label='tab:algorithm'
    )
    f.write(tex)
