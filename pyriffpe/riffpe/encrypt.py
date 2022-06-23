from ._cli_tools import add_crypt_cli_arguments, crypt_main
import argparse


parser = argparse.ArgumentParser(description="Riffpe Encryption Command-Line Tool")
add_crypt_cli_arguments(parser, is_decrypt=False)


if __name__ == '__main__':
    crypt_main(parser, is_decrypt=False)
