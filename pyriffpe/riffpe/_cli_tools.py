from . import Riffpe, int_to_digits, digits_to_int

import argparse
import math


def add_common_cli_arguments(parser: argparse.ArgumentParser):
    parser.add_argument("-n", "--base", help="Space size", type=int, default=100)
    parser.add_argument("-l", "--length", help="Number of slices", type=int, default=8)
    parser.add_argument("-t", "--tag", help="Hex-encoded tag", type=bytes.fromhex, default="")
    # FIXME: check if this is correct, fix otherwise
    parser.add_argument("--chops", help="lenght of the random walk is 32//chops", type=int, default=1)

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

    instance = Riffpe(args.base,
                      args.length,
                      args.key,
                      args.tag,
                      args.chops)
    
    message_split = int_to_digits(args.message, args.length, args.base, order)
    process_func = instance.decrypt if is_decrypt else instance.encrypt
    output_split = process_func(message_split)
    output = digits_to_int(output_split, args.base, order)
    
    # Count number of digits for the max value
    # and ensure the printed value is properly padded

    no_digits = math.ceil(math.log10(pow(args.base, args.length)))
    
    print(format(output, f'0{no_digits}d'))
