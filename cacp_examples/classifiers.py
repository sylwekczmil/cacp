from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import NearestCentroid, KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from skmultiflow.bayes import NaiveBayes
from skmultiflow.lazy import KNNClassifier
from skmultiflow.meta import AdaptiveRandomForestClassifier, \
    AdditiveExpertEnsembleClassifier, OzaBaggingClassifier, \
    DynamicWeightedMajorityClassifier, LearnPPNSEClassifier
from skmultiflow.trees import HoeffdingTreeClassifier, HoeffdingAdaptiveTreeClassifier, \
    ExtremelyFastDecisionTreeClassifier

from cacp_examples.example_custom_classifiers.xgboost import XGBoost

CLASSIFIERS = [
    ('XGB', lambda n_inputs, n_classes: XGBoost()),
    ('SVC', lambda n_inputs, n_classes: SVC()),
    ('DT', lambda n_inputs, n_classes: DecisionTreeClassifier(max_depth=5)),
    ('RF', lambda n_inputs, n_classes: RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1)),
    ('NC', lambda n_inputs, n_classes: NearestCentroid()),
    ('KNN', lambda n_inputs, n_classes: KNeighborsClassifier(3)),
    ('MLP', lambda n_inputs, n_classes: MLPClassifier(alpha=1, max_iter=10000)),
    ('AB', lambda n_inputs, n_classes: AdaBoostClassifier()),
    ('GNB', lambda n_inputs, n_classes: GaussianNB()),
]

# Note that some of these classifiers require normalized data
INCREMENTAL_CLASSIFIERS = [
    ('HT', lambda n_inputs, n_classes: HoeffdingTreeClassifier()),
    ('HAT', lambda n_inputs, n_classes: HoeffdingAdaptiveTreeClassifier()),
    ('EFDT', lambda n_inputs, n_classes: ExtremelyFastDecisionTreeClassifier()),
    ('DWM', lambda n_inputs, n_classes: DynamicWeightedMajorityClassifier()),
    ('NB', lambda n_inputs, n_classes: NaiveBayes()),
    ('KNNI', lambda n_inputs, n_classes: KNNClassifier()),
    ('ARF', lambda n_inputs, n_classes: AdaptiveRandomForestClassifier()),
    ('AEE', lambda n_inputs, n_classes: AdditiveExpertEnsembleClassifier()),
    ('OB', lambda n_inputs, n_classes: OzaBaggingClassifier()),
    ('LPPNSEC', lambda n_inputs, n_classes: LearnPPNSEClassifier())
]
