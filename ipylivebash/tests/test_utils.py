from ipylivebash.exp.scaffold.utils import inspect_arg_name


def test_inspect_arg_name_by_kwarg():
    def func(a, b, c):
        return inspect_arg_name(2, "c")

    A = 1
    C = 4
    res = func(A, c=C, b="3")

    assert res == "C"


def test_inspect_arg_name_by_pos():
    def func(a, b, c):
        return inspect_arg_name(2, "c")

    A = 1
    D = 4
    res = func(A, "b", D)

    assert res == "D"


def test_inspect_arg_name_not_found():
    def func(a, b, c):
        return inspect_arg_name(4, "k")

    A = 1
    D = 4
    res = func(A, "b", D)
    assert res == None


def test_inspect_arg_name_not_varible():
    def func(a, b, c):
        return inspect_arg_name(0, "a")

    D = 4
    res = func("1===2", "b", D)
    assert res == None


def test_inspect_arg_name_can_not_accpt_func():
    def func(a, b, c):
        return inspect_arg_name(0, "a")

    def func2():
        return "a"

    D = 4
    res = func(func2(), "b", D)
    assert res == None
