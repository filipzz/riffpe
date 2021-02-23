import argparse
import random

from riffpe.riffpe import Riffpe

def random_message(c:int, l:int):
    """
    Generates a random message from **Z_c^l**
    :param c:
    :param l:
    :return:
    """
    return [random.randint(0, c-1) for iter in range(l)]



if __name__ == '__main__':

    info_text = 'Riffpe prototype'
    parser = argparse.ArgumentParser(description=info_text)

    parser.add_argument("-n", "--base", help="Space size", type=int)
    parser.add_argument("-l", help="Number of slices", type=int)
    parser.add_argument("-e", "--encrypt", help="Message to encrypt", nargs="*", type=int)
    parser.add_argument("-d", "--decrypt", help="Ciphertext to decrypt", nargs="*", type=int)
    parser.add_argument("-t", "--tag", help="Tag", type=str)
    parser.add_argument("--test", help="Performs efficiency test", type=int)

    args, args_unknown = parser.parse_known_args()

    n = 10000
    l = 0

    key = b'\xefTT\xc89\xd0ap\xd7M\x97V\xd3\x82h\xeb'
    tag = "email@example.com"

    plaintext = ""
    ciphertext = ""
    mode = "encrypt"

    if args.base:
        n = args.base

    if args.tag:
        tag = args.tag

    #print(str(args.encrypt))


    if args.encrypt:
        plaintext = args.encrypt
        l = len(plaintext)
        #mode = "encrypt"
        c = Riffpe(n, l, key)
        enc = c.enc(tag, plaintext)
        print(str(enc))
    elif args.decrypt:
        ciphertext = args.decrypt
        #mode = "decrypt"
        l = len(ciphertext)
        c = Riffpe(n, l, key)
        dec = c.dec(tag, ciphertext)
        print(str(dec))
    elif args.test:
        tests = args.test
        l = 8
        n = 100
        c = Riffpe(n, l, key)
        w = {}

        for m in range(tests):
            x = [random.randint(0, n - 1) for iter in range(l)]
            #print("mesage: " + str(x))
            ency = c.enc("tag", x)
            #print(str(ency))
            w[m] = ency

        #print(str(w))

