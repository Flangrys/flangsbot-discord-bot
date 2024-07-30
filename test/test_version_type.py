import unittest

from src.types import version


class TestVersionType(unittest.TestCase):

    def test_version_tuple_with_same_version_expecting_both_equals(self) -> None:
        valid_version__normal_way: tuple[int, int, int, str] = (0, 0, 0, "indev")
        valid_version__typed_way: version.ClientVersion = version.ClientVersion(
            major=0, minor=0, micro=0, level="indev"
        )

        self.assertEqual(valid_version__normal_way, valid_version__typed_way)
