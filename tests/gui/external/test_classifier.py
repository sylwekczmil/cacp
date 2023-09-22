from cacp.gui.external.classifier import parse_classifier, RIVER_CLASSIFIERS, SKLEARN_CLASSIFIERS


def test_parse_sklearn_classifier():
    classifier = parse_classifier({
        "init_values": {
            "criterion": "gini",
            "splitter": "best",
            "min_samples_split": 2,
            "min_samples_leaf": 1,
            "min_weight_fraction_leaf": 0,
            "min_impurity_decrease": 0,
            "ccp_alpha": 0,
            "max_depth": 1,
        },
        "#": 8,
        "docs_url": "https://scikit-learn.org/1.0/modules/generated/sklearn.tree.DecisionTreeClassifier.html",
        "json_schema": {
            "title": "DecisionTreeClassifier",
            "type": "object",
            "properties": {
                "criterion": {"title": "Criterion", "default": "gini", "type": "string"},
                "splitter": {"title": "Splitter", "default": "best", "type": "string"},
                "max_depth": {"title": "Max Depth", "type": "integer"},
                "min_samples_split": {
                    "title": "Min Samples Split",
                    "default": 2,
                    "type": "integer",
                },
                "min_samples_leaf": {
                    "title": "Min Samples Leaf",
                    "default": 1,
                    "type": "integer",
                },
                "min_weight_fraction_leaf": {
                    "title": "Min Weight Fraction Leaf",
                    "default": 0.0,
                    "type": "number",
                },
                "max_features": {"title": "Max Features", "type": "integer"},
                "random_state": {"title": "Random State", "type": "integer"},
                "max_leaf_nodes": {"title": "Max Leaf Nodes", "type": "integer"},
                "min_impurity_decrease": {
                    "title": "Min Impurity Decrease",
                    "default": 0.0,
                    "type": "number",
                },
                "ccp_alpha": {"title": "Ccp Alpha", "default": 0.0, "type": "number"},
            },
        },
        "id": "sklearn.tree._classes.DecisionTreeClassifier",
        "name": "DecisionTreeClassifier",
    })
    assert classifier(1, 1).max_depth == 1


def test_list_river_classifiers():
    assert len(RIVER_CLASSIFIERS) == 24


def test_list_sklearn_classifiers():
    assert len(SKLEARN_CLASSIFIERS) == 34
