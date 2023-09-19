import typing

import numpy as np
from sklearn.model_selection import KFold

from cacp import ClassificationDatasetBase, ClassificationFoldData
from cacp.dataset import AVAILABLE_N_FOLDS


class RandomDataset(ClassificationDatasetBase):
    def folds(
        self,
        n_folds: AVAILABLE_N_FOLDS = 10,
        dob_scv: bool = True,
        categorical_to_numerical=True
    ) -> typing.Iterable[ClassificationFoldData]:
        labels = np.array([label for label in range(self.classes)])
        x = np.random.rand(self.instances, self.features)
        y = np.random.choice(self.classes, self.instances)
        kf = KFold(n_splits=n_folds)

        folds = []

        for i, (train_index, test_index) in enumerate(kf.split(x), start=1):
            x_train, x_test = x[train_index], x[test_index]
            y_train, y_test = y[train_index], y[test_index]

            folds.append(ClassificationFoldData(
                index=i,
                labels=labels,
                x_test=x_test,
                y_test=y_test,
                x_train=x_train,
                y_train=y_train
            ))

        return iter(folds)

    @property
    def name(self) -> str:
        return 'RandomDataset'

    @property
    def instances(self) -> int:
        return 100

    @property
    def features(self) -> int:
        return 5

    @property
    def classes(self) -> int:
        return 2


if __name__ == '__main__':
    ds = RandomDataset()
    for fold in ds.folds():
        print(fold)
