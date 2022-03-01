from cacp.wilcoxon import process_wilcoxon

CLASSIFIERS = [
    ('XGB', lambda n_inputs, n_classes: None),  # mock this only for tests
    ('SVC', lambda n_inputs, n_classes: None),
    ('DT', lambda n_inputs, n_classes: None),
    ('RF', lambda n_inputs, n_classes: None),
    ('NC', lambda n_inputs, n_classes: None),
    ('KNN', lambda n_inputs, n_classes: None),
    ('MLP', lambda n_inputs, n_classes: None),
    ('AB', lambda n_inputs, n_classes: None),
    ('GNB', lambda n_inputs, n_classes: None),
]


def test_wilcoxon(result_dir_with_data, golden_result_dir):
    process_wilcoxon(CLASSIFIERS, result_dir_with_data)

    for result_winner_dir, expected_winner_dir in [
        (result_dir_with_data.joinpath('wilcoxon'), golden_result_dir.joinpath('wilcoxon')),
        (result_dir_with_data.joinpath('wilcoxon').joinpath('auc'),
         golden_result_dir.joinpath('wilcoxon').joinpath('auc')),
        (result_dir_with_data.joinpath('wilcoxon').joinpath('accuracy'),
         golden_result_dir.joinpath('wilcoxon').joinpath('accuracy')),
    ]:
        for expected_file in expected_winner_dir.glob('*'):
            assert result_winner_dir.joinpath(expected_file.name).exists()
