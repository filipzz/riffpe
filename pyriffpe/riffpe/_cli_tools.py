from . import Riffpe, int_to_digits, digits_to_int

import argparse
import math


def add_common_cli_arguments(parser: argparse.ArgumentParser):
    parser.add_argument("-n", "--radix", help="Space size", type=int, default=100)
    parser.add_argument("-l", "--digits", help="Number of slices", type=int, default=8)
    parser.add_argument("-t", "--tweak", help="Hex-encoded tweak (tag)", type=bytes.fromhex, default=b"")
    parser.add_argument("-b", "--bytes-per-value", help="lenght of the random walk is 8-bit increments", type=int, default=16)

def add_crypt_cli_arguments(parser: argparse.ArgumentParser, is_decrypt: bool):
    add_common_cli_arguments(parser)
    parser.add_argument("-B", "--big-endian", action='store_true', help="Use big-endian order of slices in the message, default is little-endian.")
    parser.add_argument("-k", "--key", type=bytes.fromhex, help="Hex-encoded underlying AES key (must be 16, 24 or 32-bytes long).", required=True)
    parser.add_argument("message", type=int, help=f"Message to be processed ({'de' if is_decrypt else 'en'}crypted). "
                                                   "At the moment, must be an integer from range [0, n^l) "
                                                   "(with n = space size, l = number of slices).")

def crypt_main(parser: argparse.ArgumentParser, is_decrypt: bool):
    """
    Universal function for both encryption and decryption
    """
    args = parser.parse_args()
    order = 'big' if args.big_endian else 'little'

    # Parameter validation
    assert len(args.key) in (16, 24, 32)

    instance = Riffpe(
        radix=args.radix,
        digits=args.digits,
        key=args.key,
        tweak=args.tweak,
        bytes_per_value=args.bytes_per_value,
    )
    
    message_split = int_to_digits(args.message, args.digits, args.radix, order)
    process_func = instance.decrypt if is_decrypt else instance.encrypt
    output_split = process_func(message_split)
    output = digits_to_int(output_split, args.radix, order)
    
    # Count number of digits for the max value
    # and ensure the printed value is properly padded

    no_digits = math.ceil(math.log10(pow(args.radix, args.digits)))
    
    print(format(output, f'0{no_digits}d'))
