from ..exp.patchers.assign import PatchAssignment, QuoteType
import textwrap


def test_assignment_patch_extract_original_value():
    source = textwrap.dedent(
        """\
        a = '10'
        """
    )

    patcher = PatchAssignment()
    _, original_value = patcher(source, "b")

    assert original_value == None

    _, original_value = patcher(source, "a")

    assert original_value == "10"


def test_assignment_patch_shell_script():
    test_cases = [
        (
            textwrap.dedent(
                """\
                a=1
                b=2
                """
            ),
            "a",
            "3",
            textwrap.dedent(
                """\
                a=3
                b=2
                """
            ),
        ),
        (
            textwrap.dedent(
                """\
                a=1
                 b = 2
                """  # noqa
            ),
            "b",
            "10",
            textwrap.dedent(
                """\
                a=1
                 b = 10
                """
            ),
        ),
        (
            textwrap.dedent(
                """\
                a=1
                b ='2'
                """
            ),
            "b",
            "10",
            textwrap.dedent(
                """\
                a=1
                b ='10'
                """
            ),
        ),
        (
            textwrap.dedent(
                """\
                a=1
                export b ='2'
                """
            ),
            "b",
            "10",
            textwrap.dedent(
                """\
                a=1
                export b ='10'
                """
            ),
        ),
        (
            textwrap.dedent(
                """\
                # Comment
                a=1
                export b ='2' # Comment
                """
            ),
            "b",
            "10",
            textwrap.dedent(
                """\
                # Comment
                a=1
                export b ='10' # Comment
                """
            ),
        ),
        (
            # Ignore commented
            textwrap.dedent(
                """\
                # Comment
                a=1
                # b=3
                export b ="2" # Comment
                """
            ),
            "b",
            "10",
            textwrap.dedent(
                """\
                # Comment
                a=1
                # b=3
                export b ="10" # Comment
                """
            ),
        ),
        (
            # Append if not available
            textwrap.dedent(
                """\
                a=1
                b=2
                """
            ),
            "c",
            "3",
            textwrap.dedent(
                """\
                a=1
                b=2

                c=3"""
            ),
        ),
        (
            # Escape double quotes
            textwrap.dedent(
                """\
                a=1.1
                b=2
                """
            ),
            "c",
            '"3"',
            textwrap.dedent(
                """\
                a=1.1
                b=2

                c="\\\"3\\\"\""""
            ),
        ),
        (
            # Obtaining space
            textwrap.dedent(
                """\
                a=1.1
                b=2
                """
            ),
            "a",
            "3 4",
            textwrap.dedent(
                """\
                a="3 4"
                b=2
                """
            ),
        ),
    ]

    patcher = PatchAssignment()

    for content, variable, replace, expected in test_cases:
        result, _ = patcher(content, variable, replace)
        assert result == expected


def test_assignment_patch_pod_spec():
    source = textwrap.dedent(
        """\
        Pod::Spec.new do |spec|
        spec.name         = 'Reachability'
        spec.version      = '3.1.0'
        spec.license      = { :type => 'BSD' }
        spec.homepage     = 'https://github.com/tonymillion/Reachability'
        spec.authors      = { 'Tony Million' => 'tonymillion@gmail.com' }
        spec.summary      = 'ARC and GCD Compatible Reachability Class for iOS and OS X.'
        spec.source       = { :git => 'https://github.com/tonymillion/Reachability.git', :tag => 'v3.1.0' }
        spec.source_files = 'Reachability.{h,m}'
        spec.framework    = 'SystemConfiguration'
        end
        """
    )

    expected = textwrap.dedent(
        """\
        Pod::Spec.new do |spec|
        spec.name         = 'Reachability'
        spec.version      = '3.1.1'
        spec.license      = { :type => 'BSD' }
        spec.homepage     = 'https://github.com/tonymillion/Reachability'
        spec.authors      = { 'Tony Million' => 'tonymillion@gmail.com' }
        spec.summary      = 'ARC and GCD Compatible Reachability Class for iOS and OS X.'
        spec.source       = { :git => 'https://github.com/tonymillion/Reachability.git', :tag => 'v3.1.0' }
        spec.source_files = 'Reachability.{h,m}'
        spec.framework    = 'SystemConfiguration'
        end
        """
    )

    patcher = PatchAssignment()
    result, _ = patcher(source, "spec.version", "3.1.1")
    assert result == expected


def test_assignment_patch_python():
    source = textwrap.dedent(
        """\
        __VERSION__ ='3.1.0'
        """
    )

    expected = textwrap.dedent(
        """\
        __VERSION__ ='3.2.0'
        """
    )

    patcher = PatchAssignment()
    result, _ = patcher(source, "__VERSION__", "3.2.0")
    assert result == expected


def test_assignment_normalize():
    patcher = PatchAssignment()

    assert patcher.normalize("a") == "a"

    assert patcher.normalize("a b") == '"a b"'

    assert patcher.normalize("a", quote=QuoteType.Double) == '"a"'

    assert patcher.normalize("a", quote=QuoteType.Single) == "'a'"
    assert patcher.normalize("'a'", quote=QuoteType.Single) == "'\\'a\\''"
