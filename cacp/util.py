import random

import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn.metrics import roc_auc_score


def seed_everything(seed=1):
    """
    Sets up seed for random and numpy random.

    :param seed: random seed

    """
    random.seed(seed)
    np.random.seed(seed)


def auc_score(y_true: np.ndarray, y_pred: np.ndarray, average=None, multi_class=None,
              labels: np.ndarray = None) -> float:
    """
    Calculates multiclass AUC score.

    :param y_true: real labels
    :param y_pred: predicted labels
    :param average: sklearn roc_auc_score param
    :param multi_class: sklearn roc_auc_score param
    :param labels: sklearn roc_auc_score param
    :return: AUC value

    """
    lb = preprocessing.LabelBinarizer()
    lb.fit(labels)
    y_score = lb.transform(y_pred)
    return roc_auc_score(y_true, y_score, average=average, multi_class=multi_class, labels=labels)


def to_latex(df: pd.DataFrame, **kwargs) -> str:
    """
    Converts Pandas DateFrame to latex table string.

    :param df: Pandas DateFrame with data to be converted
    :param kwargs: other pandas df.to_latex args
    :return: Latex string

    """
    tex = df.style.to_latex(**kwargs)
    tex = tex.replace('_', ' ').replace('\\toprule\n', '').replace('\\midrule\n', '').replace('\\bottomrule\n', '')
    hline = '\\hline'
    lines = tex.split('\n')
    lines.insert(1, '\\footnotesize')
    lines.insert(5, hline)
    lines.insert(7, hline)
    lines.insert(-3, hline)

    # this fixes difference between python 3.7 and later versions
    lines[6] = lines[6].replace('{', '').replace('}', '')

    tex = '\n'.join(lines)

    tex = tex.replace(' accuracy ', ' ACC ').replace(' auc ', ' AUC ').replace(' algorithm ', ' Algorithm ') \
        .replace(' precision ', ' Pre ').replace(' recall ', ' Sen ').replace(' f1 ', ' F1 ')
    return tex
