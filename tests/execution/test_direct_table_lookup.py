"""
Tests of execution of direct table lookup operation.
"""

import numpy as np
import pytest

import concrete.numpy as cnp


def identity_table_lookup_generator(n):
    """
    Get identity table lookup function.
    """

    return lambda x: cnp.LookupTable(range(2**n))[x]


def random_table_lookup_1b(x):
    """
    Lookup on a random table with 1-bit input.
    """

    # fmt: off
    table = cnp.LookupTable([10, 12])
    # fmt: on

    return table[x]


def random_table_lookup_2b(x):
    """
    Lookup on a random table with 2-bit input.
    """

    # fmt: off
    table = cnp.LookupTable([3, 8, 22, 127])
    # fmt: on

    return table[x]


def random_table_lookup_3b(x):
    """
    Lookup on a random table with 3-bit input.
    """

    # fmt: off
    table = cnp.LookupTable([30, 52, 125, 23, 17, 12, 90, 4])
    # fmt: on

    return table[x]


def random_table_lookup_4b(x):
    """
    Lookup on a random table with 4-bit input.
    """

    # fmt: off
    table = cnp.LookupTable([30, 52, 125, 23, 17, 12, 90, 4, 21, 51, 22, 15, 53, 100, 75, 90])
    # fmt: on

    return table[x]


def random_table_lookup_5b(x):
    """
    Lookup on a random table with 5-bit input.
    """

    # fmt: off
    table = cnp.LookupTable(
        [
            1, 5, 2, 3, 10, 2, 4, 8, 1, 12, 15, 12, 10, 1, 0, 2,
            4, 3, 8, 7, 10, 11, 6, 13, 9, 0, 2, 1, 15, 11, 12, 5
        ]
    )
    # fmt: on

    return table[x]


def random_table_lookup_6b(x):
    """
    Lookup on a random table with 6-bit input.
    """

    # fmt: off
    table = cnp.LookupTable(
        [
            95, 74, 11, 83, 24, 116, 28, 75, 26, 85, 114, 121, 91, 123, 78, 69,
            72, 115, 67, 5, 39, 11, 120, 88, 56, 43, 74, 16, 72, 85, 103, 92,
            44, 115, 50, 56, 107, 77, 25, 71, 52, 45, 80, 35, 69, 8, 40, 87,
            26, 85, 84, 53, 73, 95, 86, 22, 16, 45, 59, 112, 53, 113, 98, 116
        ]
    )
    # fmt: on

    return table[x]


def random_table_lookup_7b(x):
    """
    Lookup on a random table with 7-bit input.
    """

    # fmt: off
    table = cnp.LookupTable(
        [
            13, 58, 38, 58, 15, 15, 77, 86, 80, 94, 108, 27, 126, 60, 65, 95,
            50, 79, 22, 97, 38, 60, 25, 48, 73, 112, 27, 45, 88, 20, 67, 17,
            16, 6, 71, 60, 77, 43, 93, 40, 41, 31, 99, 122, 120, 40, 94, 13,
            111, 44, 96, 62, 108, 91, 34, 90, 103, 58, 3, 103, 19, 69, 55, 108,
            0, 111, 113, 0, 0, 73, 22, 52, 81, 2, 88, 76, 36, 121, 97, 121,
            123, 79, 82, 120, 12, 65, 54, 101, 90, 52, 84, 106, 23, 15, 110, 79,
            85, 101, 30, 61, 104, 35, 81, 30, 98, 44, 111, 32, 68, 18, 45, 123,
            84, 80, 68, 27, 31, 38, 126, 61, 51, 7, 49, 37, 63, 114, 22, 18,
        ]
    )
    # fmt: on

    return table[x]


def negative_identity_table_lookup_generator(n):
    """
    Get negative identity table lookup function.
    """

    return lambda x: cnp.LookupTable([-i for i in range(2**n)])[x]


@pytest.mark.parametrize(
    "bits,function",
    [
        pytest.param(1, identity_table_lookup_generator(1)),
        pytest.param(2, identity_table_lookup_generator(2)),
        pytest.param(3, identity_table_lookup_generator(3)),
        pytest.param(4, identity_table_lookup_generator(4)),
        pytest.param(5, identity_table_lookup_generator(5)),
        pytest.param(6, identity_table_lookup_generator(6)),
        pytest.param(7, identity_table_lookup_generator(7)),
        pytest.param(1, random_table_lookup_1b),
        pytest.param(2, random_table_lookup_2b),
        pytest.param(3, random_table_lookup_3b),
        pytest.param(4, random_table_lookup_4b),
        pytest.param(5, random_table_lookup_5b),
        pytest.param(6, random_table_lookup_6b),
        pytest.param(7, random_table_lookup_7b),
        pytest.param(1, negative_identity_table_lookup_generator(1)),
        pytest.param(2, negative_identity_table_lookup_generator(2)),
        pytest.param(3, negative_identity_table_lookup_generator(3)),
        pytest.param(4, negative_identity_table_lookup_generator(4)),
        pytest.param(5, negative_identity_table_lookup_generator(5)),
        pytest.param(6, negative_identity_table_lookup_generator(6)),
    ],
)
def test_direct_table_lookup(bits, function, helpers):
    """
    Test direct table lookup.
    """

    configuration = helpers.configuration()

    # scalar
    # ------

    compiler = cnp.Compiler(function, {"x": "encrypted"})

    inputset = range(2**bits)
    circuit = compiler.compile(inputset, configuration)

    sample = int(np.random.randint(0, 2**bits))
    helpers.check_execution(circuit, function, sample)

    # tensor
    # ------

    compiler = cnp.Compiler(function, {"x": "encrypted"})

    inputset = [np.random.randint(0, 2**bits, size=(3, 2)) for _ in range(100)]
    circuit = compiler.compile(inputset, configuration)

    sample = np.random.randint(0, 2**bits, size=(3, 2))
    helpers.check_execution(circuit, function, sample)

    # negative scalar
    # ---------------

    compiler = cnp.Compiler(function, {"x": "encrypted"})

    inputset = range(-(2 ** (bits - 1)), 2 ** (bits - 1))
    circuit = compiler.compile(inputset, configuration)

    sample = int(np.random.randint(-(2 ** (bits - 1)), 2 ** (bits - 1)))
    helpers.check_execution(circuit, function, sample)

    # negative tensor
    # ---------------

    compiler = cnp.Compiler(function, {"x": "encrypted"})

    inputset = [
        np.random.randint(-(2 ** (bits - 1)), 2 ** (bits - 1), size=(3, 2)) for _ in range(100)
    ]
    circuit = compiler.compile(inputset, configuration)

    sample = np.random.randint(-(2 ** (bits - 1)), 2 ** (bits - 1), size=(3, 2))
    helpers.check_execution(circuit, function, sample)


def test_direct_multi_table_lookup(helpers):
    """
    Test direct multi table lookup.
    """

    configuration = helpers.configuration()

    square = cnp.LookupTable([i * i for i in range(4)])
    cube = cnp.LookupTable([i * i * i for i in range(4)])

    table = cnp.LookupTable(
        [
            [square, cube],
            [cube, square],
            [square, cube],
        ]
    )

    def function(x):
        return table[x]

    compiler = cnp.Compiler(function, {"x": "encrypted"})

    inputset = [np.random.randint(0, 2**2, size=(3, 2)) for _ in range(100)]
    circuit = compiler.compile(inputset, configuration)

    sample = np.random.randint(0, 2**2, size=(3, 2))
    helpers.check_execution(circuit, function, sample)


def test_bad_direct_table_lookup(helpers):
    """
    Test direct table lookup with bad parameters.
    """

    configuration = helpers.configuration()

    # empty table
    # -----------

    with pytest.raises(ValueError) as excinfo:
        cnp.LookupTable([])

    assert str(excinfo.value) == "LookupTable cannot be constructed with []"

    # invalid table
    # -------------

    with pytest.raises(ValueError) as excinfo:
        cnp.LookupTable([[0, 1], [2, 3]])

    assert str(excinfo.value) == "LookupTable cannot be constructed with [[0, 1], [2, 3]]"

    # invalid multi table
    # -------------------

    with pytest.raises(ValueError) as excinfo:
        cnp.LookupTable(["abc", 3.2])

    assert str(excinfo.value) == "LookupTable cannot be constructed with ['abc', 3.2]"

    # simulation with float value
    # ---------------------------

    with pytest.raises(ValueError) as excinfo:
        random_table_lookup_3b(1.1)

    assert str(excinfo.value) == "LookupTable cannot be looked up with 1.1"

    # simulation with invalid shape
    # -----------------------------

    square = cnp.LookupTable([i * i for i in range(4)])
    cube = cnp.LookupTable([i * i * i for i in range(4)])

    table = cnp.LookupTable(
        [
            [square, cube],
            [cube, square],
            [square, cube],
        ]
    )

    with pytest.raises(ValueError) as excinfo:
        _ = table[np.array([1, 2])]

    assert str(excinfo.value) == "LookupTable of shape (3, 2) cannot be looked up with [1 2]"

    # compilation with float value
    # ----------------------------

    compiler = cnp.Compiler(random_table_lookup_3b, {"x": "encrypted"})

    inputset = [1.5]
    with pytest.raises(ValueError) as excinfo:
        compiler.compile(inputset, configuration)

    assert str(excinfo.value) == "LookupTable cannot be looked up with EncryptedScalar<float64>"

    # compilation with invalid shape
    # ------------------------------

    compiler = cnp.Compiler(lambda x: table[x], {"x": "encrypted"})

    inputset = [10, 5, 6, 2]
    with pytest.raises(ValueError) as excinfo:
        compiler.compile(inputset, configuration)

    assert str(excinfo.value) == (
        "LookupTable of shape (3, 2) cannot be looked up with EncryptedScalar<uint4>"
    )
