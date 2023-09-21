.. highlight:: shell

========================
Graphical User Interface
========================

Set up a custom dataset
-----------------------

#. Click the ``Datasets`` navigation button in the left menu.

#. Click the ``Add custom dataset`` button at the top of the page.

#. In the ``Name`` section, enter the name of your dataset. It should be unique.

#. Choose the type of the dataset in section ``Type``.

   * ``Custom code`` – it allows to create your own custom dataset,

   * ``CSV file (last column will be treated as class column)`` - it allows to use a file with your own dataset.
     If you chose this option, you should set a path to the file on your computer in the ``Path`` input.

   * ``Keel files (should have KEEL datasets structure)`` - it allows to use files with KEEL datasets structure.
     If you chose this option, you should set a directory to the KEEL files on your computer in the ``Path`` input.

Set up a custom classifier
--------------------------

#. Click the ``Classifiers`` navigation button in the left menu.

#. Click the ``Add custom classifier`` button at the top of the page.

#. In the ``Name`` section, enter the name of your classifier. It should be unique.

#. Choose the type of the classifier in section ``Type``.

   * ``Batch learning`` – represents the training of machine learning models in a batch manner. The system is not capable of learning incrementally.
   * ``Incremental learning`` - model learns and enhances its knowledge progressively, without forgetting previously acquired information.

.. note::
   Implemented classifier should have a similar interface to those provided by the Scikit-learn library. Please do not change the class declaration.

Set up a custom metric
----------------------

#. Click the ``Metrics`` navigation button in the left menu.

#. Click the ``Add custom metric`` button at the top of the page.

#. In the ``Name`` section, enter the name of your metric. It should be unique.

#. Choose the type of the metric in section ``Type``.

   * ``Batch learning``– metric prepared for non-incremental datasets,

   * ``Incremental learning`` - metric prepared for incremental datasets.

.. note::
   Implemented evaluation metrics should have a similar interface to those provided by the Scikit-learn library. Please do not change the function declaration.


Create a new experiment
-----------------------

#. Click the ``Create new experiment`` button at the bottom of left menu.

#. In the ``Name`` section, enter the name of your experiment. It should be unique.

#. Choose the type of the experiment in the ``Type`` section.

   * ``Batch learning`` – prepare an experiment for machine learning models learned in a batch manner.

   * ``Incremental learning`` - model learns and enhances its knowledge progressively, without forgetting previously acquired information.

#. Select datasets for your experiment.

   * If you want to add a custom dataset, click on the ``Add Custom dataset`` button and select the appropriate dataset in the modal window.

   * If you want to add a KEEL dataset, click on the ``Add KEEL dataset`` button and select the appropriate dataset in the modal window.

   * If you creating an incremental learning experiment, you can also add dataset from River clicking on ``Add River dataset``.

    You can add all datasets at once by clicking on ``Submit all using default properties`` or add them one at a time.
    It is also possible to remove the selected dataset from the ``Selected datasets`` section using the ``Delete`` button.

#. Select classifiers for your experiment.

   * If you want to add custom classifier, click on the ``Add Custom classifiers`` button and select the appropriate classifier in the modal window.

   * If you creating a batch learning experiment, you can choose classifiers from the Scikit-learn library for your comparisons.
     Click on the ``Add Sklearn classifier`` button and select the appropriate classifier in the modal window.

   * If you creating an incremental learning experiment, you can choose classifiers from the River library for your comparisons.
     Click on the ``Add River classifier`` button and select the appropriate classifier in the modal window.

    You can add all classifiers at once by clicking on ``Submit all using default properties`` or add them one at a time adjust its parameters individually.
    It is also possible to remove the selected classifier from the ``Selected classifiers`` section using the ``Delete`` button.

#. Select metrics for your experiment.

   * If you want to add custom metric, click on the ``Add Custom metric`` button and select the appropriate metric in the modal window.

   * If you creating a batch learning experiment, you can choose metrics from the Scikit-learn library for your comparisons.
     Click on the ``Add Sklearn metric`` button and select the appropriate metric in the modal window.

   * If you creating an incremental learning experiment, you can choose metrics from the River library for your comparisons.
     Click on the ``Add River metric`` button and select the appropriate metric in the modal window.

    You can add all metrics at once by clicking on ``Submit all using default properties`` or add them one at a time.
    It is also possible to remove the selected metric from the ``Selected metrics`` section using the ``Delete`` button.

#. Click the ``Create`` button and wait for the experiment to complete.

#. Once your experiment is complete, you can view the results by clicking on the ``Experiment`` navigation button in the left menu
   by clicking on the ``Open`` button in the row of the selected experiment. To delete the results of a performed experiment,
   click the ``Delete`` button on the selected experiment.


