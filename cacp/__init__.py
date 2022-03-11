"""Top-level package for cacp."""

__author__ = """Sylwester Czmil"""
__email__ = 'sylwekczmil@gmail.com'
__version__ = '0.1.2'

from cacp.dataset import ClassificationDataset, ClassificationFoldData, all_datasets
from cacp.run import run_experiment

__all__ = ['ClassificationDataset', 'ClassificationFoldData', 'all_datasets', 'run_experiment']
