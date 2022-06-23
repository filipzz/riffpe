# To force pure Python implementation instead of native (if/when available),
# set the following line to "True":
force_fallback = False

from ._common import TweakablePRNG, int_to_digits, digits_to_int

# Try to import native implementation, use fallback (pure Python) otherwise.
try:
    if force_fallback: raise ImportError

    from ._native import Riffpe, CBCTweakablePRNG

except ImportError:
    import warnings
    warnings.warn("Using fallback Riffpe implementation")

    from ._fallback import Riffpe, CBCTweakablePRNG

__all__ = ('TweakablePRNG', 'int_to_digits', 'digits_to_int', 'Riffpe', 'CBCTweakablePRNG')
