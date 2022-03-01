import shutil
from pathlib import Path

import pytest
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

from cacp.dataset import ClassificationDataset

files_cache_path = Path(__file__).parent.joinpath('files_cache')


@pytest.fixture()
def result_dir() -> Path:
    p = Path(__file__).parent.joinpath('results')
    p.mkdir(exist_ok=True, parents=True)
    return p


@pytest.fixture()
def golden_result_dir() -> Path:
    return Path(__file__).parent.joinpath('golden_result')


@pytest.fixture()
def result_dir_with_data(result_dir, golden_result_dir) -> Path:
    shutil.copy(golden_result_dir.joinpath('comparison.csv'), result_dir.joinpath('comparison.csv'))
    return result_dir


@pytest.fixture()
def example_result_dir() -> Path:
    p = Path(__file__).parent.joinpath('example_results')
    p.mkdir(exist_ok=True, parents=True)
    return p


@pytest.fixture()
def datasets():
    return [
        ClassificationDataset('iris', files_cache_path=files_cache_path),
        ClassificationDataset('wisconsin', files_cache_path=files_cache_path),
        ClassificationDataset('pima', files_cache_path=files_cache_path),
    ]


@pytest.fixture()
def classifiers():
    return [
        ('SVC', lambda n_inputs, n_classes: SVC()),
        ('DT', lambda n_inputs, n_classes: DecisionTreeClassifier(max_depth=5)),
        ('RF', lambda n_inputs, n_classes: RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1)),
    ]


@pytest.fixture(autouse=True)
def run_before_and_after_tests(result_dir):
    # before
    yield
    # after
    shutil.rmtree(result_dir, ignore_errors=True)


def pytest_sessionstart(session):
    files_cache_path.mkdir(exist_ok=True, parents=True)


def pytest_sessionfinish(session, exitstatus):
    shutil.rmtree(files_cache_path, ignore_errors=True)
