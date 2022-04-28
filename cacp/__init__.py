"""Top-level package for cacp."""

__author__ = """Sylwester Czmil"""
__email__ = 'sylwekczmil@gmail.com'
__version__ = '0.1.4'

from cacp.dataset import \
    ClassificationDatasetBase, \
    ClassificationDataset, \
    LocalClassificationDataset, \
    ClassificationFoldData, \
    all_datasets

from cacp.run import run_experiment

__all__ = [
    'ClassificationDatasetBase',
    'ClassificationDataset',
    'LocalClassificationDataset',
    'ClassificationFoldData',
    'all_datasets',
    'run_experiment'
]
