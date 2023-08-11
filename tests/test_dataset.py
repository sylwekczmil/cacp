from pathlib import Path

import numpy as np

from cacp import all_datasets, LocalClassificationDataset
from cacp_examples.example_custom_datasets.random_dataset import RandomDataset


def test_dataset_all():
    datasets = all_datasets()
    assert len(datasets) == 69


def test_dataset_0(datasets):
    ds = datasets[0]
    assert ds.name == 'iris'
    assert ds.output_name == 'Class'
    assert ds.origin == 'Real world'
    assert ds.features == 4
    assert ds.classes == 3
    assert ds.instances == 150


def test_dataset_1(datasets):
    ds = datasets[1]
    assert ds.name == 'wisconsin'
    assert ds.output_name == 'Class'
    assert ds.origin == 'Real world'
    assert ds.features == 9
    assert ds.classes == 2
    assert ds.instances == 683


def test_dataset_2(datasets):
    ds = datasets[2]
    assert ds.name == 'pima'
    assert ds.output_name == 'Class'
    assert ds.origin == 'Real world'
    assert ds.features == 8
    assert ds.classes == 2
    assert ds.instances == 768


def test_custom_dataset():
    ds = RandomDataset()
    assert ds.name == 'RandomDataset'
    assert ds.features == 5
    assert ds.classes == 2
    assert ds.instances == 100

    for i, fold in enumerate(ds.folds()):
        assert fold.index == i
        assert np.all(fold.labels == np.array([0, 1]))
        assert fold.x_train.shape == (90, 5)
        assert fold.y_train.shape == (90,)
        assert fold.x_test.shape == (10, 5)
        assert fold.y_test.shape == (10,)


def test_local_dataset():
    ds_path = Path(__file__).parent.parent. \
        joinpath('cacp_examples') \
        .joinpath('example_custom_datasets') \
        .joinpath('local_dataset')
    ds = LocalClassificationDataset('iris', ds_path)
    assert ds.name == 'iris'
    assert ds.output_name == 'Class'
    assert ds.origin == 'Real world'
    assert ds.features == 4
    assert ds.classes == 3
    assert ds.instances == 150


def test_dataset_folds(datasets):
    ds = datasets[0]
    index = 0
    for index, fold in enumerate(ds.folds(), 1):
        assert fold.index == index
        assert fold.x_train.shape == (135, 4)
        assert fold.x_test.shape == (15, 4)
        assert fold.y_train.shape == (135,)
        assert fold.y_test.shape == (15,)
    assert index == 10


def test_dataset_iter(datasets):
    ds = datasets[0]
    index = 0
    for index, (x, y) in enumerate(ds, 1):
        assert np.issubdtype(type(y), np.integer)
        assert type(x) is dict
        assert len(x) == 4
        assert list(x.keys()) == [0, 1, 2, 3]
    assert index == 150
