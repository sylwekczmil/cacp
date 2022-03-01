from sklearn.neighbors import KNeighborsClassifier
from skmultiflow.lazy import KNNClassifier
from skmultiflow.meta import LearnPPNSEClassifier

from cacp import all_datasets, run_experiment, ClassificationDataset
from cacp_examples.classifiers import CLASSIFIERS
from cacp_examples.example_custom_classifiers.xgboost import XGBoost

if __name__ == '__main__':
    # you can specify datasets by name, all of them will be automatically downloaded
    experimental_datasets_example = [
        ClassificationDataset('iris'),
        ClassificationDataset('wisconsin'),
        ClassificationDataset('pima'),
        ClassificationDataset('sonar'),
        ClassificationDataset('wdbc'),
    ]
    # or use all datasets
    experimental_datasets = all_datasets()

    # same for classifiers, you can specify list of classifiers
    experimental_classifiers_example = [
        ('KNN_3', lambda n_inputs, n_classes: KNeighborsClassifier(3)),
        # you can define classifiers multiple times with different parameters
        ('KNN_5', lambda n_inputs, n_classes: KNeighborsClassifier(5)),
        # you can use classifiers from any lib that
        # supports fit/predict methods eg. scikit-learn/scikit-multiflow
        ('KNNI', lambda n_inputs, n_classes: KNNClassifier(n_neighbors=3)),
        # you can also use wrapped algorithms from other libs or custom implementations
        ('XGB', lambda n_inputs, n_classes: XGBoost()),
        ('LPPNSEC', lambda n_inputs, n_classes: LearnPPNSEClassifier())
    ]
    # or you can use predefined ones
    experimental_classifiers = CLASSIFIERS

    # this is how you trigger experiment run
    run_experiment(
        experimental_datasets,
        experimental_classifiers,
        results_directory='./example_result'
    )
