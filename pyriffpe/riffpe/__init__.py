# To force pure Python implementation instead of native (if/when available),
# set the following line to "True":
force_fallback = False

from ._common import TweakablePRNG, int_to_digits, digits_to_int, int_to_bases

# Try to import native implementation, use fallback (pure Python) otherwise.
try:
    if force_fallback: raise ImportError

    from ._native import Riffpe, RiffpeX, CBCTweakablePRNG

except ImportError:
    import warnings
    warnings.warn("Using fallback Riffpe implementation")

    from ._fallback import Riffpe, RiffpeX, CBCTweakablePRNG

__all__ = ('TweakablePRNG', 'int_to_digits', 'digits_to_int', 'int_to_bases', 
           'Riffpe', 'RiffpeX', 'CBCTweakablePRNG')
