## Simple script converting benchmark.py results to a Benchmark.md-compatible GFM Markdown table

import re
import sys

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <output of benchmark.py>")

ifname = sys.argv[1]

standard_unit = 'us'

re_dataset = re.compile(r"Dataset (\[[^\]]+\]) (.+)")
re_average = re.compile(r"average ((en|de)crypt) time: (.+?)ns")
re_riffpe = re.compile(r"Riffpe\((\d+), (\d+)\) (.+)")

with open(ifname, 'r') as f:
    curr_dataset = None
    curr_impl = None

    matrix = {}

    for line in f:
        m_dataset = re_dataset.match(line)
        m_average = re_average.match(line)
        if m_dataset:
            curr_dataset = m_dataset.group(1)
            curr_impl = m_dataset.group(2)
            # Collapse common Riffpe configurations
            m_riffpe = re_riffpe.match(curr_impl)
            if m_riffpe:
                curr_impl = f"Riffpe(n={m_riffpe.group(1)}) {m_riffpe.group(3)}"
        elif m_average:
            try:
                tentry = matrix[curr_impl]
            except KeyError:
                tentry = matrix[curr_impl] = {}
            try:
                entry = tentry[curr_dataset]
            except KeyError:
                entry = tentry[curr_dataset] = {'encrypt': 0, 'decrypt': 0}
            avg_type = m_average.group(1)
            avg_time = m_average.group(3)
            entry[avg_type] = float(avg_time)

impls = list(matrix.keys())
datasets = set(ds for imp in impls for ds in matrix[imp])


def ns_to_unit(unit, time_ns):
    if unit == 'ns':
        return f"{time_ns:f} ns"
    elif unit == 'us':
        return f"{time_ns/1000:f} us"
    elif unit == 'ms':
        return f"{time_ns/1000_000:f} ms"
    elif unit == 's':
        return f"{time_ns/1000_000_000:f} s"
    else:
        raise ValueError("Unrecognized unit: " + unit)


def make_array(type: str):
    max_string_lens = {ds: len(ds) for ds in datasets}
    max_string_lens['Implementation'] = len('Implementation')
    array = []
    for imp in impls:
        row = [imp]
        max_string_lens['Implementation'] = max(max_string_lens['Implementation'], len(imp))
        for ds in datasets:
            try:
                time_ns = matrix[imp][ds][type]
                cell = ns_to_unit(standard_unit, time_ns)
                if time_ns < 1000 and standard_unit != 'ns':
                    cell += f" ({ns_to_unit('ns', time_ns)})"
                elif 1000 <= time_ns < 1000_000 and standard_unit != 'us':
                    cell += f" ({ns_to_unit('us', time_ns)})"
                elif 1000_000 <= time_ns < 1000_000_000 and standard_unit != 'ms':
                    cell += f" ({ns_to_unit('ms', time_ns)})"
                elif 1000_000_000 <= time_ns and standard_unit != 's':
                    cell += f" ({ns_to_unit('s', time_ns)})"
            except KeyError:
                cell = "*N/A*"
            max_string_lens[ds] = max(max_string_lens[ds], len(cell))
            row.append(cell)
        array.append(row)
    col_lens = [max_string_lens[ds] for ds in ['Implementation', *datasets]]
    return array, col_lens


enc_array, enc_col_lens = make_array('encrypt')
dec_array, dec_col_lens = make_array('decrypt')


def print_array(array, col_lens, heading):
    print(heading)
    # Print heading row
    row = ['Implementation', *datasets]
    print(' | '.join(s.ljust(l) for s, l in zip(row, col_lens)))
    print('-|-'.join('-'*l for l in col_lens))
    for row in array:
        print(' | '.join(s.ljust(l) for s, l in zip(row, col_lens)))


print_array(enc_array, enc_col_lens, "**Encryption time**")
print_array(dec_array, dec_col_lens, "**Decryption time**")
