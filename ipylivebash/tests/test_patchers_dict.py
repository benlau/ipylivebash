from ..exp.patchers.dict import PatchDict


def test_dict_read():
    test_cases = [
        ({"a": "b"}, "a", "b"),
        ({"a": {"b": "c"}}, "a.b", "c"),
        ({"a": {}}, "a", "{}"),
        ({"a": "b"}, "a.b.c", None),
    ]

    for input, path, expected in test_cases:
        patcher = PatchDict()
        actual = patcher.read(input, path)
        assert actual == expected


def test_dict_write():
    test_cases = [
        ({"a": "b"}, "a", "c", {"a": "c"}),
        ({"a": {"b": "c"}}, "a.b", "d", {"a": {"b": "d"}}),
        ({"a": {"b": "c"}}, "a", "d", {"a": "d"}),
        ({"a": "b"}, "a.b.c", "d", {"a": {"b": {"c": "d"}}}),
        ([], "a.b.c", "d", {"a": {"b": {"c": "d"}}}),
        ({"a": []}, "a.b.c", "d", {"a": {"b": {"c": "d"}}}),
    ]

    for input, path, value, expected in test_cases:
        patcher = PatchDict()
        actual = patcher.write(input, path, value)
        assert actual == expected
