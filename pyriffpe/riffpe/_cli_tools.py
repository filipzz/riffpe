from . import Riffpe

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

    # Parameter validation
    assert len(args.key) in (16, 24, 32)

    instance = Riffpe(args.base,
                      args.length,
                      args.key,
                      args.tag,
                      args.chops)
    
    message_split = [0 for _ in range(args.length)]
    message_curr = args.message
    for i in range(args.length):
        message_curr, message_part = divmod(message_curr, args.base)
        message_split[i] = message_part
    
    # Remainder must be 0
    assert message_curr == 0

    if args.big_endian:
        message_split.reverse()
    process_func = instance.dec if is_decrypt else instance.enc
    output_split = process_func(message_split)
    # In recombination we iterate in reverse, so only revert on little-endian
    if not args.big_endian:
        output_split.reverse()
    # TODO: it should be possible to fully skip .reverse() calls and instead use iterator reversals.
    # To be checked.

    output_curr = 0
    for split_part in output_split:
        output_curr *= args.base
        output_curr += split_part
    
    # Count number of digits for the max value
    # and ensure the printed value is properly padded

    no_digits = math.ceil(math.log10(pow(args.base, args.length)))
    
    print(format(output_curr, f'0{no_digits}d'))
