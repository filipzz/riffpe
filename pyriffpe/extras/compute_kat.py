"""
Compute Known Answer Test resutls step-by-step
"""

import struct
from typing import Sequence
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

def byte_xor(a: bytes, b: bytes) -> bytes: return bytes(x^y for x, y in zip(a, b))

def cbc_absorb(function: str, cipher, input: bytes, state: bytes = bytes(AES.block_size)) -> bytes: 
    for i in range(0, len(input), AES.block_size):
        block = input[i:i+AES.block_size]
        output = cipher.encrypt(byte_xor(block, state))
        print(f"{function}: cbc_absorb: {i=:3} {state.hex()=} {block.hex()=} {output.hex()=}")
        state = output
    return state

def cbc_squeeze(function: str, cipher, state: bytes, bytes_to_produce: int) -> bytes:
    print(f"{function}: cbc_squeeze: {bytes_to_produce=}")
    blocks = (bytes_to_produce + AES.block_size - 1) // AES.block_size
    result = b''
    for i in range(blocks):
        output = cipher.encrypt(state)
        print(f"{function}: cbc_squeeze: {i=:3} {state.hex()=} {output.hex()=}")
        state = output
        result += output
    return result[:bytes_to_produce]

def compute_tweak_iv(cipher, tweak: bytes, radix: int, digits: int) -> bytes:
    print(f"compute_tweak_iv: {tweak.hex()=}, {radix=}, {digits=}")
    tweak_pfx = struct.pack('<IIQ', radix, digits, len(tweak))
    print(f"compute_tweak_iv: {tweak_pfx.hex()=}")
    kdf_pfx = pad(tweak_pfx + tweak, AES.block_size, 'pkcs7')
    print(f"compute_tweak_iv: {kdf_pfx.hex()=}")
    tweak_iv = cbc_absorb("compute_tweak_iv", cipher, kdf_pfx)
    print(f"compute_tweak_iv: {tweak_iv.hex()=}")
    return tweak_iv

def compute_round_tweak(cipher, tweak_iv: bytes, input: Sequence[int], idx: int, phase: int) -> bytes:
    # TODO: we currently assume <256 radix here for B packing
    assert idx < len(input)
    state = [*input, idx]
    state[idx] = phase
    struct_def = "<" + "B"*len(state)
    print(f"compute_round_tweak: {input=}, {idx=}, {phase=}")
    print(f"compute_round_tweak: {struct_def=!r}, {state=}")
    encoded_state = struct.pack(struct_def, *state)
    print(f"compute_round_tweak: {encoded_state.hex()=}")
    padded_state = pad(encoded_state, AES.block_size, 'pkcs7')
    print(f"compute_round_tweak: {padded_state.hex()=}")
    print(f"compute_round_tweak: {tweak_iv.hex()=}")
    round_tweak = cbc_absorb("compute_round_tweak", cipher, padded_state, tweak_iv)
    print(f"compute_round_tweak: {round_tweak.hex()=}")
    return round_tweak

def compute_round_perm(cipher, radix: int, round_tweak: bytes, bytes_per_value=16) -> dict[int, int]:
    print(f"compute_round_perm: {radix=}, {round_tweak.hex()=}, {bytes_per_value=}")
    total_bytes = radix * bytes_per_value
    print(f"compute_round_perm: {total_bytes=}")
    stream = cbc_squeeze("compute_round_perm", cipher, round_tweak, total_bytes)
    print(f"compute_round_perm: {stream.hex()=}")
    vks = [
        (stream[k*bytes_per_value:(k+1)*bytes_per_value], k)
        for k in range(radix)
    ]
    print("compute_round_perm: kvs (unsorted)")
    for v, k in vks:
        print(f"    {k=:4} {v.hex()=}")
    vks.sort()
    print("compute_round_perm: kvs (sorted)")
    for v, k in vks:
        print(f"    {k=:4} {v.hex()=}")
    perm = [(i, k) for i, (_v, k) in enumerate(vks)]
    print("compute_round_perm: perm (forward)")
    for i, k in perm:
        print(f"    {i=:4} {k=:4}")
    return dict(perm)

def print_highlighted_state(state: list[int], idx: int, label: str = 'state'):
    state_tmp = state[:idx] + [[state[idx]]] + state[idx+1:]
    print(f"  {label}: {state_tmp!r}")


def do_phase_element(radix: int, idx: int, phase: int, state_ref: list[int], cipher, tweak_iv: bytes, bpv: int):
    print("="*80)
    print(f"Phase {phase} Element {idx}")
    print("-"*80)
    print_highlighted_state(state_ref, idx)
    round_tweak = compute_round_tweak(cipher, tweak_iv, state_ref, idx, phase)
    perm = compute_round_perm(cipher, radix, round_tweak, bpv)
    print(f"  Element {state_ref[idx]} -> {perm[state_ref[idx]]}")
    state_ref[idx] = perm[state_ref[idx]]
    print_highlighted_state(state_ref, idx)


def main():
    key = bytes.fromhex("00112233445566778899aabbccddeeff")
    tweak = b"Alice"
    aes_ecb = AES.new(key, AES.MODE_ECB)
    bpv = 16

    # Keep the input small, otherwise it's hard to reason about it:
    radix = 5
    digits = 3
    input = [2, 3, 4]

    # Compute tweak_iv, a common state for all further computations
    tweak_iv = compute_tweak_iv(aes_ecb, tweak, radix, digits)
    state = list(input)

    for i in range(digits):
        do_phase_element(radix, i, 0, state, aes_ecb, tweak_iv, bpv)
    for i in range(digits):
        do_phase_element(radix, i, 1, state, aes_ecb, tweak_iv, bpv)

    output = list(state)

    print("="*80)
    print(f"{input=}")
    print(f"{output=}")

   
if __name__ == "__main__":
    main()

