"""
Test the decoder module
"""

# Author: Andres Hoyos-Idrobo
# License: simplified BSD

from nose.tools import (assert_equal, assert_true, assert_false,
                        assert_raises)
import warnings
import os
import numpy as np
import nibabel
from sklearn.svm import LinearSVC, SVR
from sklearn.linear_model import (LogisticRegression, RidgeClassifier,
                                  Ridge)
from sklearn.base import BaseEstimator
from sklearn.datasets import load_iris
from sklearn.metrics import accuracy_score

from nilearn.input_data import NiftiMasker
from nilearn.decoding.tests.test_same_api import to_niimgs
# from nilearn.image import index_img
from nilearn._utils.testing import assert_warns
from nilearn.decoding.decoder import (Decoder, DecoderRegressor,
                                      _check_param_grid)


# Crate a test dataset
rand = np.random.RandomState(0)
X = rand.rand(100, 10)
# Create different targets
y_regression = rand.rand(100)
y_classif = np.hstack([[-1] * 50, [1] * 50])
y_classif_str = np.hstack([['face'] * 50, ['house'] * 50])
y_multiclass = np.hstack([[0] * 35, [1] * 30, [2] * 35])


# Test estimators
# Regression
ridge = Ridge()
svr = SVR(kernel='linear')
# Classification
svc = LinearSVC()
logistic_l1 = LogisticRegression(penalty='l1')
logistic_l2 = LogisticRegression(penalty='l2')
ridge_classifier = RidgeClassifier()


def test_check_param_grid():

    # testing several estimators, each one with its specific regularization
    # parameter
    regressors = {'ridge': (ridge, 'alpha'),
                  'svr': (svr, 'C')}
    classifiers = {'svc': (svc, 'C'),
                   'logistic_l1': (logistic_l1, 'C'),
                   'logistic_l2': (logistic_l2, 'C'),
                   'ridge_classifier': (ridge_classifier, 'alpha')}

    # Regression
    for _, (regressor, param) in regressors.items():
        param_grid = _check_param_grid(regressor, X, y_regression, None)
        assert_equal(list(param_grid.keys())[0], param)
    # Classification
    for _, (classifier, param) in classifiers.items():
        param_grid = _check_param_grid(classifier, X, y_classif, None)
        assert_equal(list(param_grid.keys())[0], param)