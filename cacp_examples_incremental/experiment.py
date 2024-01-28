import river
from river.forest import ARFClassifier
from river.naive_bayes import GaussianNB
from river.neighbors import KNNClassifier
from river.tree import HoeffdingTreeClassifier

from cacp import run_incremental_experiment, ClassificationDataset

if __name__ == '__main__':
    # select datasets
    experimental_datasets = [
        ClassificationDataset('iris'),
        ClassificationDataset('wisconsin'),
        # you can use datasets from river
        river.datasets.Phishing(),
        river.datasets.Bananas(),

    ]

    # select incremental classifiers
    experimental_classifiers = [
        ('ARF', lambda n_inputs, n_classes: ARFClassifier()),
        ('HAT', lambda n_inputs, n_classes: HoeffdingTreeClassifier()),
        ('KNN', lambda n_inputs, n_classes: KNNClassifier()),
        ('GNB', lambda n_inputs, n_classes: GaussianNB()),
    ]

    # trigger experiment run
    run_incremental_experiment(
        experimental_datasets,
        experimental_classifiers,
        results_directory='./example_result'
    )
