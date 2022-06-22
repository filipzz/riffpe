# To force pure Python implementation instead of native (if/when available),
# set the following line to "True":
force_fallback = False

# Try to import native implementation, use fallback (pure Python) otherwise.
try:
    if force_fallback: raise ImportError

    from ._native import Riffpe, CBCTweakablePRNG

except ImportError:
    import warnings
    warnings.warn("Using fallback Riffpe implementation")

    from ._fallback.Riffpe import Riffpe
    from ._fallback.CBCTweakablePRNG import CBCTweakablePRNG

__all__ = ('Riffpe', 'CBCTweakablePRNG')
