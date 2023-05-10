"""
Tests of execution of add operation.
"""

import numpy as np
import pytest

import concrete.numpy as cnp


@pytest.mark.parametrize(
    "function",
    [
        pytest.param(
            lambda x: x + 42,
            id="x + 42",
        ),
        pytest.param(
            lambda x: 42 + x,
            id="42 + x",
        ),
        pytest.param(
            lambda x: x + np.array([1, 2, 3]),
            id="x + [1, 2, 3]",
        ),
        pytest.param(
            lambda x: np.array([1, 2, 3]) + x,
            id="[1, 2, 3] + x",
        ),
        pytest.param(
            lambda x: x + np.array([[1, 2, 3], [4, 5, 6]]),
            id="x + [[1, 2, 3], [4, 5, 6]]",
        ),
        pytest.param(
            lambda x: np.array([[1, 2, 3], [4, 5, 6]]) + x,
            id="[[1, 2, 3], [4, 5, 6]] + x",
        ),
    ],
)
@pytest.mark.parametrize(
    "parameters",
    [
        {
            "x": {"range": [0, 85], "status": "encrypted"},
        },
        {
            "x": {"range": [0, 85], "status": "encrypted", "shape": (3,)},
        },
        {
            "x": {"range": [0, 85], "status": "encrypted", "shape": (2, 3)},
        },
        {
            "x": {"range": [-50, 10], "status": "encrypted"},
        },
        {
            "x": {"range": [-50, 10], "status": "encrypted", "shape": (3,)},
        },
        {
            "x": {"range": [-50, 10], "status": "encrypted", "shape": (2, 3)},
        },
        {
            "x": {"range": [0, 1000000], "status": "encrypted"},
        },
        {
            "x": {"range": [0, 1000000], "status": "encrypted", "shape": (3,)},
        },
        {
            "x": {"range": [0, 1000000], "status": "encrypted", "shape": (2, 3)},
        },
    ],
)
def test_constant_add(function, parameters, helpers):
    """
    Test add where one of the operators is a constant.
    """

    parameter_encryption_statuses = helpers.generate_encryption_statuses(parameters)
    configuration = helpers.configuration()

    compiler = cnp.Compiler(function, parameter_encryption_statuses)

    inputset = helpers.generate_inputset(parameters)
    circuit = compiler.compile(inputset, configuration)

    sample = helpers.generate_sample(parameters)
    helpers.check_execution(circuit, function, sample)


@pytest.mark.parametrize(
    "function",
    [
        pytest.param(
            lambda x, y: x + y,
            id="x + y",
        ),
    ],
)
@pytest.mark.parametrize(
    "parameters",
    [
        {
            "x": {"range": [0, 60], "status": "clear"},
            "y": {"range": [0, 60], "status": "encrypted"},
        },
        {
            "x": {"range": [0, 60], "status": "encrypted"},
            "y": {"range": [0, 60], "status": "clear"},
        },
        {
            "x": {"range": [0, 60], "status": "encrypted"},
            "y": {"range": [0, 60], "status": "encrypted"},
        },
        {
            "x": {"range": [0, 60], "status": "clear", "shape": (3,)},
            "y": {"range": [0, 60], "status": "encrypted"},
        },
        {
            "x": {"range": [0, 60], "status": "encrypted", "shape": (3,)},
            "y": {"range": [0, 60], "status": "clear"},
        },
        {
            "x": {"range": [0, 60], "status": "encrypted", "shape": (3,)},
            "y": {"range": [0, 60], "status": "encrypted"},
        },
        {
            "x": {"range": [0, 60], "status": "clear"},
            "y": {"range": [0, 60], "status": "encrypted", "shape": (3,)},
        },
        {
            "x": {"range": [0, 60], "status": "encrypted"},
            "y": {"range": [0, 60], "status": "clear", "shape": (3,)},
        },
        {
            "x": {"range": [0, 60], "status": "encrypted"},
            "y": {"range": [0, 60], "status": "encrypted", "shape": (3,)},
        },
        {
            "x": {"range": [0, 60], "status": "clear", "shape": (3,)},
            "y": {"range": [0, 60], "status": "encrypted", "shape": (3,)},
        },
        {
            "x": {"range": [0, 60], "status": "encrypted", "shape": (3,)},
            "y": {"range": [0, 60], "status": "clear", "shape": (3,)},
        },
        {
            "x": {"range": [0, 60], "status": "encrypted", "shape": (3,)},
            "y": {"range": [0, 60], "status": "encrypted", "shape": (3,)},
        },
        {
            "x": {"range": [0, 60], "status": "clear", "shape": (2, 1)},
            "y": {"range": [0, 60], "status": "encrypted", "shape": (3,)},
        },
        {
            "x": {"range": [0, 60], "status": "encrypted", "shape": (2, 1)},
            "y": {"range": [0, 60], "status": "clear", "shape": (3,)},
        },
        {
            "x": {"range": [0, 60], "status": "encrypted", "shape": (2, 1)},
            "y": {"range": [0, 60], "status": "encrypted", "shape": (3,)},
        },
        {
            "x": {"range": [-30, 30], "status": "encrypted", "shape": (3, 2)},
            "y": {"range": [-30, 30], "status": "encrypted", "shape": (3, 2)},
        },
    ],
)
def test_add(function, parameters, helpers):
    """
    Test add where both of the operators are dynamic.
    """

    parameter_encryption_statuses = helpers.generate_encryption_statuses(parameters)
    configuration = helpers.configuration()

    compiler = cnp.Compiler(function, parameter_encryption_statuses)

    inputset = helpers.generate_inputset(parameters)
    circuit = compiler.compile(inputset, configuration)

    sample = helpers.generate_sample(parameters)
    helpers.check_execution(circuit, function, sample)
