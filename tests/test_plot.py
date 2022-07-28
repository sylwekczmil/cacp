from cacp.comparison import DEFAULT_METRICS
from cacp.plot import process_comparison_results_incremental_plots
from cacp.plot import process_comparison_results_plots


def test_plot(result_dir_with_data):
    process_comparison_results_plots(result_dir_with_data)

    plot_dir = result_dir_with_data.joinpath('plot')

    for extension in ['eps', 'png']:
        for kind in ['dataset', 'fold']:
            for metric, _ in DEFAULT_METRICS:
                assert plot_dir.joinpath(f'comparison_{metric.lower()}_per_{kind}.{extension}').exists()


def test_plot_incremental(result_dir_with_incremental_data):
    process_comparison_results_incremental_plots(result_dir_with_incremental_data)

    classifier_names = ['ARF', 'HAT', 'KNN']
    dataset_names = ['phishing', 'pima', 'wisconsin']
    metrics = ['auc', 'accuracy', 'precision', 'recall', 'f1']

    plot_dir = result_dir_with_incremental_data.joinpath('incremental').joinpath('plot')
    single_plot_dir = result_dir_with_incremental_data.joinpath('incremental').joinpath('plot').joinpath('single')
    for classifier_name in classifier_names:
        single_classifier_plot_dir = single_plot_dir.joinpath(classifier_name)
        for dataset_name in dataset_names:
            for metric in metrics:
                assert single_classifier_plot_dir.joinpath(f'{classifier_name}_{dataset_name}_{metric}.png').exists()
                assert single_classifier_plot_dir.joinpath(f'{classifier_name}_{dataset_name}_{metric}.eps').exists()

    for dataset_name in dataset_names:
        for metric in metrics:
            assert plot_dir.joinpath(f'{dataset_name}_{metric}.png').exists()
