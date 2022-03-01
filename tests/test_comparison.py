import pytest

from cacp.comparison import process_comparison
from cacp.util import seed_everything


@pytest.mark.parametrize("test_input",
                         [
                             (5, True, False), (5, False, False),
                             (10, True, False), (10, False, False),
                             (5, False, True)
                         ])
def test_comparison(result_dir, datasets, classifiers, test_input):
    n_folds, dob_scv, normalized = test_input
    seed_everything()
    process_comparison(
        datasets, classifiers, result_dir,
        n_folds=n_folds,
        dob_scv=dob_scv,
        normalized=normalized
    )
    assert result_dir.joinpath('comparison.csv').exists()
