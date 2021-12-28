from typing import Protocol, Optional, runtime_checkable


@runtime_checkable
class Formatter(Protocol):
    def __call__(self, x: float, pos: Optional[float]) -> str:
        ...  # pragma: no cover


def default_formatter(x: float, pos: Optional[float]) -> str:
    return str(x)


def thousands_formatter(x: float, pos: Optional[float]) -> str:
    s = '{:1.1f}'.format(x*1e-3)
    return s


def money_formatter(x: float, pos: Optional[float]) -> str:
    if x >= 1e9:
        s = '${:1.1f}B'.format(x*1e-9)
    elif x >= 1e6:
        s = '${:1.1f}M'.format(x*1e-6)
    else:
        s = '${:1.0f}K'.format(x*1e-3)
    return s
