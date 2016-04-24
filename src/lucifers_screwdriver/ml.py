"""
Machine learning.
"""
import numpy as np
from sklearn.neighbors import KNeighborsClassifier

from . import enums as _e


def performance(y_true, y_pred):
    true_positives  = np.count_nonzero( y_true &  y_pred)
    false_positives = np.count_nonzero(~y_true &  y_pred)
    false_negatives = np.count_nonzero( y_true & ~y_pred)

    completeness  = true_positives  / (true_positives + false_negatives)
    contamination = false_positives / (true_positives + false_positives)

    return completeness, contamination


def features(object_params):
    X = np.empty((len(object_params), 6), dtype=float)

    X[:,0] = object_params[_e.H]
    X[:,1] = object_params[_e.A]
    X[:,2] = object_params[_e.E]
    X[:,3] = object_params[_e.I]
    X[:,4] = object_params[_e.ARG_PERI]
    X[:,5] = object_params[_e.LONG_ASC_NODE]

    return X


def train(object_params, PHAs, **kwargs):
    X = features(object_params)

    clf = KNeighborsClassifier(**kwargs)
    clf.fit(X, PHAs)

    return clf
