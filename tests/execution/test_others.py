"""
Tests of execution of operations converted to table lookups.
"""

import numpy as np
import pytest

import concrete.numpy as cnp


def fusable_with_bigger_search(x, y):
    """
    Fusable function that requires a single iteration for fusing.
    """

    x = x + 1

    x_1 = x.astype(np.int64)
    x_1 = x_1 + 1.5

    x_2 = x.astype(np.int64)
    x_2 = x_2 + 3.4

    add = x_1 + x_2
    add_int = add.astype(np.int64)

    return add_int + y


def fusable_with_bigger_search_needs_second_iteration(x, y):
    """
    Fusable function that requires more than one iteration for fusing.
    """

    x = x + 1
    x = x + 0.5
    x = np.cos(x)

    x_1 = x.astype(np.int64)
    x_1 = x_1 + 1.5

    x_p = x + 1
    x_p2 = x_p + 1

    x_2 = (x_p + x_p2).astype(np.int64)
    x_2 = x_2 + 3.4

    add = x_1 + x_2
    add_int = add.astype(np.int64)

    return add_int + y


def fusable_with_one_of_the_start_nodes_is_lca_generator():
    """
    Generator of a fusable function that has one of the start nodes as lca.
    """

    # pylint: disable=invalid-name,too-many-locals,too-many-statements

    def subgraph_18(x):
        t0 = 0
        t1 = 3
        t2 = 2
        t3 = 2.4688520431518555
        t4 = 2.4688520431518555
        t5 = x
        t6 = np.multiply(t4, t5)
        t7 = np.true_divide(t6, t3)
        t8 = np.add(t7, t2)
        t9 = np.rint(t8)
        t10 = np.clip(t9, t0, t1)
        t11 = t10.astype(np.int64)
        return t11

    def subgraph_24(x):
        t0 = 0
        t1 = [0.15588106, -0.01305565]
        t2 = 1.3664466152828822
        t3 = [[4, -4]]
        t4 = 0
        t5 = x
        t6 = t5.astype(np.float32)
        t7 = np.add(t6, t4)
        t8 = np.add(t7, t3)
        t9 = np.multiply(t2, t8)
        t10 = np.add(t1, t9)
        t11 = np.greater(t10, t0)
        return t11

    cst0 = np.random.randint(-2, 2, size=(10, 2))
    cst1 = np.random.randint(0, 2, size=(10, 1))

    def function(x):
        t0 = 0
        t1 = 3
        t2 = 1
        t3 = 1.2921873902965313
        t4 = 1.0507009873554805
        t5 = 1
        t6 = 1.7580993408473766
        t7 = [0.15588106, -0.01305565]
        t8 = 1
        t9 = 1.3664466152828822
        t10 = [[4, -4]]
        t11 = 0
        t12 = cst0
        t13 = 0
        t14 = cst1
        t15 = x
        t16 = -2
        t17 = np.add(t15, t16)
        t18 = subgraph_18(t17)
        t19 = np.matmul(t18, t12)
        t20 = np.matmul(t18, t14)
        t21 = np.multiply(t13, t20)
        t22 = np.add(t19, t21)
        t23 = t22.astype(np.float32)
        t24 = subgraph_24(t22)
        t25 = np.add(t23, t11)
        t26 = np.subtract(t5, t24)
        t27 = np.add(t25, t10)
        t28 = np.multiply(t9, t27)
        t29 = np.add(t7, t28)
        t30 = np.multiply(t4, t29)
        t31 = np.exp(t29)
        t32 = np.multiply(t24, t30)
        t33 = np.subtract(t31, t8)
        t34 = np.multiply(t6, t33)
        t35 = np.multiply(t26, t34)
        t36 = np.add(t32, t35)
        t37 = np.true_divide(t36, t3)
        t38 = np.add(t37, t2)
        t39 = np.rint(t38)
        t40 = np.clip(t39, t0, t1)
        t41 = t40.astype(np.int64)
        return t41

    return function

    # pylint: enable=invalid-name,too-many-locals,too-many-statements


def deterministic_unary_function(x):
    """
    An example deterministic unary function.
    """

    def per_element(element):
        result = 0
        for i in range(element):
            result += i
        return result

    return np.vectorize(per_element)(x)


@pytest.mark.parametrize(
    "function,parameters",
    [
        pytest.param(
            lambda x: x // 3,
            {
                "x": {"status": "encrypted", "range": [0, 127]},
            },
            id="x // 3",
        ),
        pytest.param(
            lambda x: 127 // x,
            {
                "x": {"status": "encrypted", "range": [1, 127]},
            },
            id="127 // x",
        ),
        pytest.param(
            lambda x: (x / 3).astype(np.int64),
            {
                "x": {"status": "encrypted", "range": [0, 127]},
            },
            id="(x / 3).astype(np.int64)",
        ),
        pytest.param(
            lambda x: (127 / x).astype(np.int64),
            {
                "x": {"status": "encrypted", "range": [1, 127]},
            },
            id="(127 / x).astype(np.int64)",
        ),
        pytest.param(
            lambda x: x**2,
            {
                "x": {"status": "encrypted", "range": [0, 11]},
            },
            id="x ** 2",
        ),
        pytest.param(
            lambda x: 2**x,
            {
                "x": {"status": "encrypted", "range": [0, 6]},
            },
            id="2 ** x",
        ),
        pytest.param(
            lambda x: x % 10,
            {
                "x": {"status": "encrypted", "range": [0, 127]},
            },
            id="x % 10",
        ),
        pytest.param(
            lambda x: 121 % x,
            {
                "x": {"status": "encrypted", "range": [1, 127]},
            },
            id="121 % x",
        ),
        pytest.param(
            lambda x: +x,
            {
                "x": {"status": "encrypted", "range": [0, 127]},
            },
            id="+x",
        ),
        pytest.param(
            lambda x: abs(42 - x),
            {
                "x": {"status": "encrypted", "range": [0, 84]},
            },
            id="abs(64 - x)",
        ),
        pytest.param(
            lambda x: ~x,
            {
                "x": {"status": "encrypted", "range": [0, 16]},
            },
            id="~x",
        ),
        pytest.param(
            lambda x: x & 10,
            {
                "x": {"status": "encrypted", "range": [0, 16]},
            },
            id="x & 10",
        ),
        pytest.param(
            lambda x: 5 & x,
            {
                "x": {"status": "encrypted", "range": [0, 16]},
            },
            id="5 & x",
        ),
        pytest.param(
            lambda x: x | 6,
            {
                "x": {"status": "encrypted", "range": [0, 16]},
            },
            id="x | 6",
        ),
        pytest.param(
            lambda x: 11 | x,
            {
                "x": {"status": "encrypted", "range": [0, 16]},
            },
            id="11 | x",
        ),
        pytest.param(
            lambda x: x ^ 9,
            {
                "x": {"status": "encrypted", "range": [0, 16]},
            },
            id="x ^ 9",
        ),
        pytest.param(
            lambda x: 13 ^ x,
            {
                "x": {"status": "encrypted", "range": [0, 16]},
            },
            id="13 ^ x",
        ),
        pytest.param(
            lambda x: x << 2,
            {
                "x": {"status": "encrypted", "range": [0, 16]},
            },
            id="x << 2",
        ),
        pytest.param(
            lambda x: 2 << x,
            {
                "x": {"status": "encrypted", "range": [0, 5]},
            },
            id="2 << x",
        ),
        pytest.param(
            lambda x: x >> 2,
            {
                "x": {"status": "encrypted", "range": [0, 120]},
            },
            id="x >> 2",
        ),
        pytest.param(
            lambda x: 120 >> x,
            {
                "x": {"status": "encrypted", "range": [0, 16]},
            },
            id="120 >> x",
        ),
        pytest.param(
            lambda x: x > 50,
            {
                "x": {"status": "encrypted", "range": [0, 100]},
            },
            id="x > 50",
        ),
        pytest.param(
            lambda x: 50 > x,  # pylint: disable=misplaced-comparison-constant
            {
                "x": {"status": "encrypted", "range": [0, 100]},
            },
            id="50 > x",
        ),
        pytest.param(
            lambda x: x < 50,
            {
                "x": {"status": "encrypted", "range": [0, 100]},
            },
            id="x < 50",
        ),
        pytest.param(
            lambda x: 50 < x,  # pylint: disable=misplaced-comparison-constant
            {
                "x": {"status": "encrypted", "range": [0, 100]},
            },
            id="50 < x",
        ),
        pytest.param(
            lambda x: x >= 50,
            {
                "x": {"status": "encrypted", "range": [0, 100]},
            },
            id="x >= 50",
        ),
        pytest.param(
            lambda x: 50 >= x,  # pylint: disable=misplaced-comparison-constant
            {
                "x": {"status": "encrypted", "range": [0, 100]},
            },
            id="50 >= x",
        ),
        pytest.param(
            lambda x: x <= 50,
            {
                "x": {"status": "encrypted", "range": [0, 100]},
            },
            id="x <= 50",
        ),
        pytest.param(
            lambda x: 50 <= x,  # pylint: disable=misplaced-comparison-constant
            {
                "x": {"status": "encrypted", "range": [0, 100]},
            },
            id="50 <= x",
        ),
        pytest.param(
            lambda x: x == 50,
            {
                "x": {"status": "encrypted", "range": [0, 100]},
            },
            id="x == 50",
        ),
        pytest.param(
            lambda x: 50 == x,  # pylint: disable=misplaced-comparison-constant
            {
                "x": {"status": "encrypted", "range": [0, 100]},
            },
            id="50 == x",
        ),
        pytest.param(
            lambda x: x != 50,
            {
                "x": {"status": "encrypted", "range": [0, 100]},
            },
            id="x != 50",
        ),
        pytest.param(
            lambda x: 50 != x,  # pylint: disable=misplaced-comparison-constant
            {
                "x": {"status": "encrypted", "range": [0, 100]},
            },
            id="50 != x",
        ),
        pytest.param(
            lambda x: x.clip(5, 10),
            {
                "x": {"status": "encrypted", "range": [0, 15]},
            },
            id="x.clip(5, 10)",
        ),
        pytest.param(
            lambda x: (60 * np.sin(x)).astype(np.int64) + 60,
            {
                "x": {"status": "encrypted", "range": [0, 127]},
            },
            id="(60 * np.sin(x)).astype(np.int64) + 60",
        ),
        pytest.param(
            lambda x: ((np.sin(x) ** 2) + (np.cos(x) ** 2)).astype(np.int64),
            {
                "x": {"status": "encrypted", "range": [0, 127]},
            },
            id="((np.sin(x) ** 2) + (np.cos(x) ** 2)).astype(np.int64)",
        ),
        pytest.param(
            lambda x: np.maximum(x, [[10, 20], [30, 40], [50, 60]]),
            {
                "x": {"status": "encrypted", "range": [0, 127], "shape": (3, 2)},
            },
            id="np.maximum(x, [[10, 20], [30, 40], [50, 60]])",
        ),
        pytest.param(
            fusable_with_bigger_search,
            {
                "x": {"status": "encrypted", "range": [5, 10]},
                "y": {"status": "encrypted", "range": [5, 10]},
            },
            id="fusable_with_bigger_search",
        ),
        pytest.param(
            fusable_with_bigger_search_needs_second_iteration,
            {
                "x": {"status": "encrypted", "range": [5, 10]},
                "y": {"status": "encrypted", "range": [5, 10]},
            },
            id="fusable_with_bigger_search_needs_second_iteration",
        ),
        pytest.param(
            fusable_with_one_of_the_start_nodes_is_lca_generator(),
            {
                "x": {"status": "encrypted", "range": [0, 4], "shape": (1, 10)},
            },
            id="fusable_with_one_of_the_start_nodes_is_lca",
        ),
        pytest.param(
            lambda x: x + x.shape[0] + x.ndim + x.size,
            {
                "x": {"status": "encrypted", "range": [0, 15], "shape": (3, 2)},
            },
            id="x + shape[0] + x.ndim + x.size",
        ),
        pytest.param(
            lambda x: (100 * np.sin(x.transpose())).astype(np.int64),
            {
                "x": {"status": "encrypted", "range": [0, 15], "shape": (3, 2)},
            },
            id="(100 * np.sin(x.transpose())).astype(np.int64)",
        ),
        pytest.param(
            lambda x: np.where(x < 5, x * 3, x),
            {
                "x": {"status": "encrypted", "range": [0, 10]},
            },
            id="np.where(x < 5, x * 3, x)",
        ),
        pytest.param(
            lambda x: x + np.ones_like(x),
            {
                "x": {"status": "encrypted", "range": [0, 10]},
            },
            id="x + np.ones_like(x)",
        ),
        pytest.param(
            lambda x: x + np.zeros_like(x),
            {
                "x": {"status": "encrypted", "range": [0, 10]},
            },
            id="x + np.zeros_like(x)",
        ),
        pytest.param(
            lambda x: cnp.univariate(deterministic_unary_function)(x),
            {
                "x": {"status": "encrypted", "range": [0, 10]},
            },
            id="cnp.univariate(deterministic_unary_function)(x)",
        ),
    ],
)
def test_others(function, parameters, helpers):
    """
    Test others.
    """

    # scalar
    # ------

    if "shape" not in parameters["x"]:
        parameter_encryption_statuses = helpers.generate_encryption_statuses(parameters)
        configuration = helpers.configuration()

        compiler = cnp.Compiler(function, parameter_encryption_statuses)

        inputset = helpers.generate_inputset(parameters)
        circuit = compiler.compile(inputset, configuration)

        sample = helpers.generate_sample(parameters)
        helpers.check_execution(circuit, function, sample, retries=10)

    # tensor
    # ------

    if "shape" not in parameters["x"]:
        parameters["x"]["shape"] = (3, 2)

    parameter_encryption_statuses = helpers.generate_encryption_statuses(parameters)
    configuration = helpers.configuration()

    compiler = cnp.Compiler(function, parameter_encryption_statuses)

    inputset = helpers.generate_inputset(parameters)
    circuit = compiler.compile(inputset, configuration)

    sample = helpers.generate_sample(parameters)
    helpers.check_execution(circuit, function, sample, retries=10)


def test_others_bad_fusing(helpers):
    """
    Test others with bad fusing.
    """

    configuration = helpers.configuration()

    # two variable inputs
    # -------------------

    @cnp.compiler({"x": "encrypted", "y": "clear"})
    def function1(x, y):
        return (10 * (np.sin(x) ** 2) + 10 * (np.cos(y) ** 2)).astype(np.int64)

    with pytest.raises(RuntimeError) as excinfo:
        inputset = [(i, i) for i in range(100)]
        function1.compile(inputset, configuration)

    helpers.check_str(
        # pylint: disable=line-too-long
        """

Function you are trying to compile cannot be converted to MLIR

 %0 = 10                             # ClearScalar<uint4>
 %1 = 10                             # ClearScalar<uint4>
 %2 = 2                              # ClearScalar<uint2>
 %3 = 2                              # ClearScalar<uint2>
 %4 = x                              # EncryptedScalar<uint7>
 %5 = y                              # ClearScalar<uint7>
 %6 = sin(%4)                        # EncryptedScalar<float64>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ only integer operations are supported
 %7 = cos(%5)                        # ClearScalar<float64>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ only integer operations are supported
 %8 = power(%6, %2)                  # EncryptedScalar<float64>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ only integer operations are supported
 %9 = power(%7, %3)                  # ClearScalar<float64>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ only integer operations are supported
%10 = multiply(%0, %8)               # EncryptedScalar<float64>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ only integer operations are supported
%11 = multiply(%1, %9)               # ClearScalar<float64>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ only integer operations are supported
%12 = add(%10, %11)                  # EncryptedScalar<float64>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ only integer operations are supported
%13 = astype(%12, dtype=int_)        # EncryptedScalar<uint4>
return %13

        """,  # noqa: E501
        # pylint: enable=line-too-long
        str(excinfo.value),
    )

    # big intermediate constants
    # --------------------------

    @cnp.compiler({"x": "encrypted"})
    def function2(x):
        return (np.sin(x) * [[1, 2], [3, 4]]).astype(np.int64)

    with pytest.raises(RuntimeError) as excinfo:
        inputset = range(100)
        function2.compile(inputset, configuration)

    helpers.check_str(
        # pylint: disable=line-too-long
        """

Function you are trying to compile cannot be converted to MLIR

%0 = [[1 2] [3 4]]                 # ClearTensor<uint3, shape=(2, 2)>
%1 = x                             # EncryptedScalar<uint7>
%2 = sin(%1)                       # EncryptedScalar<float64>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ only integer operations are supported
%3 = multiply(%2, %0)              # EncryptedTensor<float64, shape=(2, 2)>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ only integer operations are supported
%4 = astype(%3, dtype=int_)        # EncryptedTensor<int3, shape=(2, 2)>
return %4

        """,  # noqa: E501
        # pylint: enable=line-too-long
        str(excinfo.value),
    )

    # intermediates with different shape
    # ----------------------------------

    @cnp.compiler({"x": "encrypted"})
    def function3(x):
        return np.abs(np.sin(x)).reshape((2, 3)).astype(np.int64)

    with pytest.raises(RuntimeError) as excinfo:
        inputset = [np.random.randint(0, 2**7, size=(3, 2)) for _ in range(100)]
        function3.compile(inputset, configuration)

    helpers.check_str(
        # pylint: disable=line-too-long
        """

Function you are trying to compile cannot be converted to MLIR

%0 = x                                   # EncryptedTensor<uint7, shape=(3, 2)>
%1 = sin(%0)                             # EncryptedTensor<float64, shape=(3, 2)>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ only integer operations are supported
%2 = absolute(%1)                        # EncryptedTensor<float64, shape=(3, 2)>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ only integer operations are supported
%3 = reshape(%2, newshape=(2, 3))        # EncryptedTensor<float64, shape=(2, 3)>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ only integer operations are supported
%4 = astype(%3, dtype=int_)              # EncryptedTensor<uint1, shape=(2, 3)>
return %4

        """,  # noqa: E501
        # pylint: enable=line-too-long
        str(excinfo.value),
    )


def test_others_bad_univariate(helpers):
    """
    Test univariate with bad function.
    """

    configuration = helpers.configuration()

    def bad_univariate(x):
        return np.array([x, x, x])

    @cnp.compiler({"x": "encrypted"})
    def f(x):
        return cnp.univariate(bad_univariate)(x)

    with pytest.raises(ValueError) as excinfo:
        inputset = range(10)
        f.compile(inputset, configuration)

    helpers.check_str(
        "Function bad_univariate cannot be used with cnp.univariate",
        str(excinfo.value),
    )
