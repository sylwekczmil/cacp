===================================================
CACP: Classification Algorithms Comparison Pipeline
===================================================


.. image:: https://img.shields.io/pypi/v/cacp.svg
        :target: https://pypi.python.org/pypi/cacp

.. image:: https://github.com/sylwekczmil/cacp/actions/workflows/tox.yml/badge.svg
        :target: https://github.com/sylwekczmil/cacp/actions/workflows/tox.yml


.. image:: https://readthedocs.org/projects/cacp/badge/?version=latest
        :target: https://cacp.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status

* Free software: MIT license
* Documentation: https://cacp.readthedocs.io.


Installation
--------------

To install cacp, run this command in your terminal:

.. code-block:: console

    pip install cacp


Simple Usage
--------------
An example usage of this library is included in the package:
https://github.com/sylwekczmil/cacp/tree/main/cacp_examples_simple.

.. code:: python3

    from sklearn.ensemble import RandomForestClassifier
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.svm import SVC
    from sklearn.tree import DecisionTreeClassifier

    from cacp import run_experiment, ClassificationDataset

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


Advanced Usage
---------------

An advanced example usage of this library is included in the package:
https://github.com/sylwekczmil/cacp/tree/main/cacp_examples.

.. code:: python3

    from sklearn.neighbors import KNeighborsClassifier
    from skmultiflow.lazy import KNNClassifier
    from skmultiflow.meta import LearnPPNSEClassifier

    from cacp import all_datasets, run_experiment, ClassificationDataset
    from cacp_examples.classifiers import CLASSIFIERS
    from cacp_examples.example_custom_classifiers.xgboost import XGBoost

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



