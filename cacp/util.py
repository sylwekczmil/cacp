import random

import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn.metrics import roc_auc_score


def seed_everything(seed=1):
    random.seed(seed)
    np.random.seed(seed)


def auc_score(y_true: np.ndarray, y_pred: np.ndarray, average=None, multi_class=None, labels: np.ndarray = None):
    lb = preprocessing.LabelBinarizer()
    lb.fit(labels)
    y_score = lb.transform(y_pred)
    return roc_auc_score(y_true, y_score, average=average, multi_class=multi_class, labels=labels)


def to_latex(df: pd.DataFrame, **kwargs):
    tex = df.style.to_latex(**kwargs)
    tex = tex.replace('_', ' ').replace('\\toprule\n', '').replace('\\midrule\n', '').replace('\\bottomrule\n', '')
    hline = '\\hline'
    lines = tex.split('\n')
    lines.insert(1, '\\footnotesize')
    lines.insert(5, hline)
    lines.insert(7, hline)
    lines.insert(-3, hline)
    tex = '\n'.join(lines)

    tex = tex.replace(' accuracy ', ' ACC ').replace(' auc ', ' AUC ').replace(' algorithm ', ' Algorithm ') \
        .replace(' precision ', ' Pre ').replace(' recall ', ' Sen ').replace(' f1 ', ' F1 ')
    return tex
