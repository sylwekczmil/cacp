from cacp.result import process_comparison_results


def test_comparison_results(result_dir_with_data, golden_result_dir):
    process_comparison_results(result_dir_with_data)

    assert result_dir_with_data.joinpath('comparison_result.csv').open().read() == golden_result_dir.joinpath(
        'comparison_result.csv').open().read()

    assert result_dir_with_data.joinpath('comparison_result.tex').open().read() == golden_result_dir.joinpath(
        'comparison_result.tex').open().read()
