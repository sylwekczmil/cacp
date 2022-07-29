from cacp import run_experiment
from cacp.run import run_incremental_experiment


def count_by_extension(result_dir, extension: str):
    file_count = 0
    for p in result_dir.glob(f'**/*.{extension}'):
        if p.is_file():
            file_count += 1

    return file_count


def test_run_happy_path(datasets, classifiers, result_dir):
    run_experiment(datasets, classifiers, result_dir)

    png_file_count = count_by_extension(result_dir, 'png')
    eps_file_count = count_by_extension(result_dir, 'eps')
    csv_file_count = count_by_extension(result_dir, 'csv')
    tex_file_count = count_by_extension(result_dir, 'tex')

    assert png_file_count == 10
    assert eps_file_count == 10
    assert csv_file_count == 17
    assert tex_file_count == 16


def test_run_incremental_happy_path(incremental_datasets, incremental_classifiers, result_dir):
    run_incremental_experiment(incremental_datasets, incremental_classifiers, result_dir)

    png_file_count = count_by_extension(result_dir, 'png')
    eps_file_count = count_by_extension(result_dir, 'eps')
    csv_file_count = count_by_extension(result_dir, 'csv')
    tex_file_count = count_by_extension(result_dir, 'tex')

    assert png_file_count == 70
    assert eps_file_count == 70
    assert csv_file_count == 26
    assert tex_file_count == 16
