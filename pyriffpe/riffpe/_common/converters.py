import collections
import functools
import itertools
import math
import operator

from typing import Dict, List


def int_to_digits(x: int, ndigits: int, base=10, order='big'):
    result = [0 for _ in range(ndigits)]
    x_curr = x
    for i in range(ndigits):
        x_curr, x_part = divmod(x_curr, base)
        result[i] = x_part

    if x_curr > 0:
        raise ValueError(f"{x} doesn't fit in {ndigits} digits of base {base} (remainder: {x_curr}).")

    if order == 'big':
        result.reverse()
    return result


def digits_to_int(digits, base=10, order='big'):
    iterator = digits if order == 'big' else reversed(digits)
    result = 0
    for digit in iterator:
        result *= base
        result += digit
    return result


def int_to_bases(x: int, bases: List[int], order='big'):
    ndigits = len(bases)
    result = [0 for _ in range(ndigits)]
    x_curr = x
    ibases = reversed(bases) if order == 'big' else bases
    for i, base in enumerate(ibases):
        x_curr, x_part = divmod(x_curr, base)
        result[i] = x_part

    if x_curr > 0:
        raise ValueError(f"{x} doesn't fit in {ndigits} digits of bases {bases} (remainder: {x_curr}).")

    if order == 'big':
        result.reverse()
    return result


def _is_probable_prime(x):
    from Crypto.Util.number import isPrime
    return isPrime(x, 1e-10)


def _pollard_rho_f(n, s=2):
    x = s
    y = s
    d = 1

    g = lambda a: (a*a+1) % n

    while True:
        x = g(x)
        y = g(g(y))
        d = math.gcd(abs(x-y), n)

        if d == n:
            return _pollard_rho_f(n, s+1)
        if d > 1:
            return d


def _simple_factorize(x: int):
    c = collections.Counter()
    from Crypto.Util.number import sieve_base
    for d in sieve_base:
        if x == 1:
            break
        while x % d == 0:
            c[d] += 1
            x //= d
    
    while x > 1:
        if _is_probable_prime(x):
            c[x] += 1
            break
        else:
            k = _pollard_rho_f(x)
            c[k] += 1
            x //= k
    return c


def find_best_bases(x: int = None, threshold: int = 36, xfactors: Dict[int, int] = None):
    """
    Find best bases that would describe range(x), with each base >= threshold.
    """
    if xfactors is None:
        if x is None:
            raise ValueError("Exactly one: x or xfactors must be provided, got none")
        else:
            # optional integer factorization of x (using precomputed sieve + pollard rho)
            xfactors = _simple_factorize(x)
    elif x is not None:
            raise ValueError("Exactly one: x or xfactors must be provided, got both")

    primes = list(xfactors.keys())
    i_exps = list(xfactors.values())
    
    best = None
    best_w = None
    
    def incr_w(value):
        return value * math.log2(value)
    
    been_there = set()

    def naive_iter(remaining, selected, rem, selected_w):
        """
        :param remaining: remaining exponents
        :param selected: list of selected factors (as values)
        :param rem: remaining value (should be prod of p**e for p, e in zip(primes, remaining))
        :param selected_w: shoudl be equal to sum(incr_w(x) for x in selected)
        
        :yields: selected tuples and their weights.
        """
        
        # dead branch; not enough remaining; 
        # this branch should never be executed due to the
        # `value < threshold` and `nrem < threshold`
        # conditions down the line, but we check for it regardless
        if rem < threshold:
            return
        # if rem < threshold^2, then there are no partitions of exps s.t. both values are >= threshold,
        # so remaining is the only possible selection
        if rem < threshold**2:
            value = rem
            value_w = incr_w(value)
            selected.append(value)
            nselected_w = selected_w + value_w
            yield tuple(selected), nselected_w
            selected.pop()
            return
        
        # Iterate over the possible choices of the first element,
        # this generates a lot of repeats in the general,
        # since both (a, b) and (b, a) are allowed to be in selected;
        # we try to circumvent this with been_there, but value gets recomputed regardless
        for first in itertools.product(*(range(e+1) for e in remaining)):
            # try..finally to ensure state is reverted on short-circuiting conditions
            try:
                # modify state (begin)
                value = 1
                for i, (p, e) in enumerate(zip(primes, first)):
                    remaining[i] -= e
                    value *= pow(p, e)
                selected.append(value)
                # modify state (end)
                
                # if the current value is not enough, skip
                if value < threshold:
                    continue
                
                nrem = rem // value
                # if the remaining factors are not enough, skip
                if 1 < nrem < threshold:
                    continue

                # if we've been here, skip
                sit_hash = hash(tuple(sorted(selected)))
                if sit_hash in been_there:
                    continue
                been_there.add(sit_hash)

                value_w = incr_w(value)
                nselected_w = selected_w + value_w
                    
                # if the current selection is worse than best, skip
                if best_w and best_w < nselected_w:
                    continue

                # all the digits used up:
                if not any(remaining):
                    yield tuple(selected), nselected_w
                else:
                    yield from naive_iter(remaining, selected, nrem, nselected_w)

            finally:
                # undo modify state (begin)
                selected.pop()
                for i, e in enumerate(first):
                    remaining[i] += e
                # undo modify state (end)

    rem = functools.reduce(operator.mul, (pow(p, e) for p, e in zip(primes, i_exps)), 1)
    for sol, sol_w in naive_iter(i_exps, [], rem, 0):
        if best is None or sol_w < best_w:
            best, best_w = sol, sol_w
    return tuple(sorted(best))
