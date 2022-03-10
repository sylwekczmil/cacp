from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

from cacp import run_experiment, ClassificationDataset

if __name__ == '__main__':
    # select datasets
    experimental_datasets = [
        ClassificationDataset('iris'),
        ClassificationDataset('wisconsin'),
        ClassificationDataset('pima'),
        ClassificationDataset('wdbc'),
    ]

    # select classifiers
    experimental_classifiers = [
        ('SVC', lambda n_inputs, n_classes: SVC()),
        ('DT', lambda n_inputs, n_classes: DecisionTreeClassifier(max_depth=5)),
        ('RF', lambda n_inputs, n_classes: RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1)),
        ('KNN', lambda n_inputs, n_classes: KNeighborsClassifier(3)),
    ]

    # trigger experiment run
    run_experiment(
        experimental_datasets,
        experimental_classifiers,
        results_directory='./example_result'
    )
