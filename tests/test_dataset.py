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
