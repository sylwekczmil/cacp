import warnings

import numpy as np

with warnings.catch_warnings():
    warnings.simplefilter(action='ignore', category=FutureWarning)
    import xgboost as xgb


class XGBoost:

    def __init__(self, max_depth=5):
        self.bst = None
        self.max_depth = max_depth

    def fit(self, x, y, param=None, feature_names=None):
        if param is None:
            param = {
                'max_depth': self.max_depth,
                'objective': 'multi:softprob',
                'eval_metric': 'mlogloss',
                'num_class': len(set(y))
            }
        dtrain = xgb.DMatrix(x, label=y, feature_names=feature_names)
        self.bst = xgb.train(param, dtrain)

    def predict(self, x):
        return np.argmax(self.bst.predict(xgb.DMatrix(x)), axis=1)
