from cacp.comparison import DEFAULT_METRICS
from cacp.plot import process_comparison_results_plots


def test_plot(result_dir_with_data):
    process_comparison_results_plots(result_dir_with_data)

    plot_dir = result_dir_with_data.joinpath('plot')

    for extension in ['eps', 'png']:
        for kind in ['dataset', 'fold']:
            for metric, _ in DEFAULT_METRICS:
                assert plot_dir.joinpath(f'comparison_{metric.lower()}_per_{kind}.{extension}').exists()
