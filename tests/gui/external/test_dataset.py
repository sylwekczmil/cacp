from river.datasets.synth import AnomalySine

from cacp import ClassificationDataset
from cacp.gui.external.dataset import parse_dataset


def test_parse_keel_dataset():
    dataset = parse_dataset({
        "init_values": {},
        "#": 27,
        "Name": "iris",
        "Instances": 150,
        "Features": 4,
        "Classes": 3,
        "docs_url": "[https://sci2s.ugr.es/keel/dataset/data/classification/iris-names.txt](https://sci2s.ugr.es/keel/dataset/data/classification/iris-names.txt)",
        "json_schema": {"title": "iris", "type": "object", "properties": {}},
        "id": "cacp.dataset.ClassificationDataset",
        "name": "iris",
    })
    assert dataset.name == "iris"
    assert type(dataset) == ClassificationDataset


def test_parse_river_dataset():
    dataset = parse_dataset({
        "init_values": {
            "n_samples": 3333,
            "n_anomalies": 2500,
            "contextual": False,
            "n_contextual": 2500,
            "shift": 4,
            "noise": 0.5,
            "replace": True,
        },
        "#": 1,
        "id": "river.datasets.synth.anomaly_sine.AnomalySine",
        "name": "AnomalySine",
        "type": "Synthetic",
        "task": "Binary classification",
        "samples": 10000,
        "features": 2,
        "outputs": 1,
        "classes": 1,
        "docs_url": "[https://riverml.xyz/0.11.1/api/synth/AnomalySine](https://riverml.xyz/0.11.1/api/synth/AnomalySine)",
        "json_schema": {
            "title": "AnomalySine",
            "type": "object",
            "properties": {
                "n_samples": {
                    "title": "N Samples",
                    "default": 10000,
                    "type": "integer",
                },
                "n_anomalies": {
                    "title": "N Anomalies",
                    "default": 2500,
                    "type": "integer",
                },
                "contextual": {
                    "title": "Contextual",
                    "default": False,
                    "type": "boolean",
                },
                "n_contextual": {
                    "title": "N Contextual",
                    "default": 2500,
                    "type": "integer",
                },
                "shift": {"title": "Shift", "default": 4, "type": "integer"},
                "noise": {"title": "Noise", "default": 0.5, "type": "number"},
                "replace": {"title": "Replace", "default": True, "type": "boolean"},
                "seed": {"title": "Seed", "type": "integer"},
            },
        },
    })
    assert type(dataset) == AnomalySine
    assert dataset.n_samples == 3333
