import pytest
from idealforms.formatters import Formatter, \
    default_formatter, thousands_formatter, money_formatter


class TestMoneyFormatter:
    def test_format_2000_get_2K(self):
        assert money_formatter(2000, 1) == '$2K'

    def test_thosuands_floor(self):
        assert money_formatter(2500, 1) == '$2K'

    def test_unexpected(self):
        assert money_formatter(2500, 1) != '$2.5K'

    def test_millions(self):
        assert money_formatter(2500000, 1) == '$2.5M'

    def test_billions(self):
        assert money_formatter(2500000000, 1) == '$2.5B'


class TestThousandsFormatter:
    def test_expected(self):
        assert thousands_formatter(2000, 1) == '2.0'

    def test_format_two_million_get_2000_point_0(self):
        assert thousands_formatter(2000000, 1) == '2000.0'

    def test_unexpected(self):
        assert thousands_formatter(2500000, 1) != '2.5'


@pytest.mark.parametrize("fn", [money_formatter,
                                thousands_formatter,
                                default_formatter]
                         )
def test_formatter_is_protocol(fn):
    assert isinstance(fn, Formatter)
