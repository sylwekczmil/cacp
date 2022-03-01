from cacp.info import dataset_info, classifier_info


def test_dataset_info(datasets, result_dir):
    dataset_info(datasets, result_dir)

    csv_p = result_dir.joinpath('info').joinpath('datasets.csv')
    tex_p = result_dir.joinpath('info').joinpath('datasets.tex')

    for p in [csv_p, tex_p]:
        with p.open('r') as f:
            content = f.read()
            for ds in datasets:
                assert ds.name in content
                assert str(ds.instances) in content
                assert str(ds.features) in content
                assert str(ds.classes) in content


def test_classifier_info(classifiers, result_dir):
    classifier_info(classifiers, result_dir)

    csv_p = result_dir.joinpath('info').joinpath('classifiers.csv')
    tex_p = result_dir.joinpath('info').joinpath('classifiers.tex')

    for p in [csv_p, tex_p]:
        with p.open('r') as f:
            content = f.read()
            for cn, _ in classifiers:
                assert cn in content
