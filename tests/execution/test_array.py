"""
Tests of execution of array operation.
"""

import pytest

import concrete.numpy as cnp


@pytest.mark.parametrize(
    "function,parameters",
    [
        pytest.param(
            lambda x: cnp.array([x, x + 1, 1]),
            {
                "x": {"range": [0, 10], "status": "encrypted", "shape": ()},
            },
            id="cnp.array([x, x + 1, 1])",
        ),
        pytest.param(
            lambda x, y: cnp.array([x, y]),
            {
                "x": {"range": [0, 10], "status": "encrypted", "shape": ()},
                "y": {"range": [0, 10], "status": "clear", "shape": ()},
            },
            id="cnp.array([x, y])",
        ),
        pytest.param(
            lambda x, y: cnp.array([[x, y], [y, x]]),
            {
                "x": {"range": [0, 10], "status": "encrypted", "shape": ()},
                "y": {"range": [0, 10], "status": "clear", "shape": ()},
            },
            id="cnp.array([[x, y], [y, x]])",
        ),
        pytest.param(
            lambda x, y, z: cnp.array([[x, 1], [y, 2], [z, 3]]),
            {
                "x": {"range": [0, 10], "status": "encrypted", "shape": ()},
                "y": {"range": [0, 10], "status": "clear", "shape": ()},
                "z": {"range": [0, 10], "status": "encrypted", "shape": ()},
            },
            id="cnp.array([[x, 1], [y, 2], [z, 3]])",
        ),
    ],
)
def test_array(function, parameters, helpers):
    """
    Test array.
    """

    parameter_encryption_statuses = helpers.generate_encryption_statuses(parameters)
    configuration = helpers.configuration()

    compiler = cnp.Compiler(function, parameter_encryption_statuses)

    inputset = helpers.generate_inputset(parameters)
    circuit = compiler.compile(inputset, configuration)

    sample = helpers.generate_sample(parameters)
    helpers.check_execution(circuit, function, sample)
