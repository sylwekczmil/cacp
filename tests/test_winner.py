import os

import pytest

from cacp.winner import process_comparison_result_winners

IN_GITHUB_ACTIONS = bool(os.getenv("GITHUB_ACTIONS", False))


@pytest.mark.skipif(IN_GITHUB_ACTIONS, reason="Test doesn't work in Github Actions.")
def test_winner_comparison_results(result_dir_with_data, golden_result_dir):
    process_comparison_result_winners(result_dir_with_data)

    result_winner_dir = result_dir_with_data.joinpath('winner')
    expected_winner_dir = golden_result_dir.joinpath('winner')

    assert result_winner_dir.joinpath('comparison.csv').open().read() == expected_winner_dir.joinpath(
        'comparison.csv').open().read()

    assert result_winner_dir.joinpath('comparison.tex').open().read() == expected_winner_dir.joinpath(
        'comparison.tex').open().read()

    for metric in ['accuracy', 'auc', 'f1', 'precision', 'recall']:
        assert result_winner_dir.joinpath(metric).joinpath(
            'comparison_result.csv').open().read() == expected_winner_dir.joinpath(metric).joinpath(
            'comparison_result.csv').open().read()

        assert result_winner_dir.joinpath(metric).joinpath(
            'comparison_result.tex').open().read() == expected_winner_dir.joinpath(metric).joinpath(
            'comparison_result.tex').open().read()
