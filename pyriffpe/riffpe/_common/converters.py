from typing import List


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

