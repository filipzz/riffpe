import argparse

from riffpe.riffpe import Riffpe


if __name__ == '__main__':

    info_text = 'Riffpe prototype'
    parser = argparse.ArgumentParser(description=info_text)

    parser.add_argument("-n", help="Space size", type=int)
    parser.add_argument("-l", help="Number of slices", type=int)
    parser.add_argument("-p", "--plaintext", help="Message to encrypt", nargs="*", type=int)
    parser.add_argument("-c", "--ciphertext", help="Ciphertext to decrypt", nargs="*", type=int)
    parser.add_argument("-t", "--tag", help="Tag", type=str)

    args, args_unknown = parser.parse_known_args()

    n = 100
    l = 0
    key = "abc"
    tag = "bcd"
    plaintext = ""
    ciphertext = ""
    mode = "encrypt"

    if args.tag:
        tag = args.tag


    if args.plaintext:
        plaintext = args.plaintext
        l = len(plaintext)
        mode = "encrypt"
        c = Riffpe(n, l)
        enc = c.enc(key, tag, plaintext)
        print(str(enc))
    elif args.ciphertext:
        ciphertext = args.ciphertext
        mode = "decrypt"
        l = len(ciphertext)
        c = Riffpe(n, l)
        dec = c.dec(key, tag, ciphertext)
        print(str(dec))






        message = [6, 2, 10, 11, 4, 9, 9, 10]
        enc = c.enc("asdasd", "asdasda", message)

        dec = c.dec("asdasd", "asdasda", enc)