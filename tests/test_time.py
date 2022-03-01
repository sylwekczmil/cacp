from cacp.time import process_times


def test_time(result_dir_with_data, golden_result_dir):
    process_times(result_dir_with_data)

    assert result_dir_with_data.joinpath('time').joinpath('comparison.csv').open().read() == golden_result_dir.joinpath(
        'time').joinpath('comparison.csv').open().read()

    assert result_dir_with_data.joinpath('time').joinpath('comparison.tex').open().read() == golden_result_dir.joinpath(
        'time').joinpath('comparison.tex').open().read()
