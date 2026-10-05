from math import sqrt  # noqa: I001

from . import expose_config  # noqa: F401
from config import SHOULD_KEYTRACK_EXTRA


def if_keytrack_extra (keytrack: float, default: float = 0) -> float:
    return keytrack if SHOULD_KEYTRACK_EXTRA else default


def remap (x: float, min: float, max: float) -> float:
   return x*(max-min) + min


def hex_to_text (hex: str) -> str:
    return bytes.fromhex(hex).decode('utf-8')

def text_to_hex (text: str) -> str:
    return text.encode('utf-8').hex().upper()


C3 = 60
def tinker_formula (tracking: float, inv_tracking: float) -> str:
    offset = C3 * inv_tracking - 36.0
    return f"(({offset}+A*127)*{tracking})"



TEMPLATE_HELPERS = {
    func.__name__: func for func in [
        sqrt,
        if_keytrack_extra,
        remap,
        text_to_hex,
        tinker_formula,
    ]
}
