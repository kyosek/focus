import numpy as np
import pytest
from unittest.mock import MagicMock
import tensorflow as tf
import pandas as pd
from focus import Focus


@pytest.fixture
def model():
    return MagicMock()


@pytest.fixture
def X():
    return pd.DataFrame([[1, 2, 3], [4, 5, 6]])


def test_init(self):
    self.assertEqual(self.focus.distance_function, "euclidean")
    self.assertIsInstance(self.focus.optimizer, MagicMock)
    self.assertEqual(self.focus.sigma, 10.0)
    self.assertEqual(self.focus.temperature, 1.0)
    self.assertEqual(self.focus.distance_weight, 0.01)
    self.assertEqual(self.focus.lr, 0.001)
    self.assertEqual(self.focus.num_iter, 100)
    self.assertEqual(self.focus.direction, "both")
    self.assertFalse(self.focus.hyperparameter_tuning)
    self.assertEqual(self.focus.verbose, 1)


def test_generate(self):
    perturbed = self.focus.generate(self.model, self.X)
    self.assertEqual(perturbed.shape, self.X.shape)


def test_prepare_features_by_perturb_direction(model, X):
    focus = Focus()
    direction = "positive"
    prepared_X = focus.prepare_features_by_perturb_direction(model, X, direction)
    assert prepared_X.shape == (0, 3)


def test_compute_gradient(model, X):
    focus = Focus()
    predictions = tf.constant([0, 1])
    to_optimize = [tf.Variable(0.5), tf.Variable(0.7)]
    example_pred_class_index = tf.constant([[0, 0], [1, 1]])
    mask_vector = tf.constant([True, False])
    perturbed = tf.constant([[1, 2, 3], [7, 8, 9]])
    distance_weight = 0.01
    x_train = tf.constant([[1, 2, 3], [4, 5, 6]])
    distance_function = "euclidean"
    sigma = 10.0
    temperature = 1.0
    optimizer = tf.keras.optimizers.Adam()

    gradient = focus.compute_gradient(
        model,
        X,
        predictions,
        to_optimize,
        example_pred_class_index,
        mask_vector,
        perturbed,
        distance_weight,
        x_train,
        distance_function,
        sigma,
        temperature,
        optimizer,
    )

    assert isinstance(gradient, tf.Tensor)


def test_parse_class_tree():
    tree = MagicMock()
    X = np.array([[1, 2, 3], [4, 5, 6]])
    sigma = 0.5

    impurity_values = Focus.parse_class_tree(tree, X, sigma)

    assert isinstance(impurity_values, list)


def test_get_prob_classification_tree():
    tree = MagicMock()
    X = tf.constant([[1, 2, 3], [4, 5, 6]])
    sigma = 0.5

    prob_classification = Focus.get_prob_classification_tree(tree, X, sigma)

    assert isinstance(prob_classification, tf.Tensor)


def test_get_prob_classification_forest(model, X):
    focus = Focus()
    sigma = 0.5
    temperature = 1.0

    prob_classification = focus.get_prob_classification_forest(
        model, X, sigma, temperature
    )

    assert isinstance(prob_classification, tf.Tensor)


def test_filter_hinge_loss(model, X):
    focus = Focus()
    n_class = 2
    mask_vector = np.array([True, False])
    sigma = 0.5
    temperature = 1.0

    hinge_loss = focus.filter_hinge_loss(
        n_class,
        mask_vector,
        X,
        sigma,
        temperature,
        model,
    )

    assert isinstance(hinge_loss, tf.Tensor)
