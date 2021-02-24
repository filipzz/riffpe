import argparse
import random

from riffpe.riffpe import Riffpe

from urllib import parse
import json
import requests
from pathlib import Path


def random_message(c:int, l:int):
    """
    Generates a random message from **Z_c^l**
    :param c:
    :param l:
    :return:
    """
    return [random.randint(0, c-1) for iter in range(l)]


def read(file_name: str):
    try:
        parsed = parse.urlparse(file_name)
        if all([parsed.scheme, parsed.netloc, parsed.path]):
            data = json.loads(requests.get(file_name).text)
        else:
            with open(file_name, 'r') as f:
                data = json.load(f)
    except:
        raise Exception("Read error")

    return data


def save(file_name: str, data: dict):
    path = Path(file_name)
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(file_name, 'w') as f:
            json.dump(data, f, indent=2)
    except:
        raise Exception("Write error")


if __name__ == '__main__':

    info_text = 'Riffpe prototype'
    parser = argparse.ArgumentParser(description=info_text)

    parser.add_argument("-n", "--base", help="Space size", type=int)
    parser.add_argument("-l", help="Number of slices", type=int)
    parser.add_argument("-e", "--encrypt", help="Message to encrypt", nargs="*", type=int)
    parser.add_argument("-d", "--decrypt", help="Ciphertext to decrypt", nargs="*", type=int)
    parser.add_argument("-t", "--tag", help="Tag", type=str)
    parser.add_argument("--test", help="Performs efficiency test", type=int)
    parser.add_argument("--chops", help="lenght of the random walk is 32//chops", type=int)
    parser.add_argument("--read", help="Reads test data from a file", type=str)
    parser.add_argument("--generate", help="Generates test data and saves them in a file", type=int)

    args, args_unknown = parser.parse_known_args()

    n = 10000
    l = 0
    chops = 1

    key = b'\xefTT\xc89\xd0ap\xd7M\x97V\xd3\x82h\xeb'
    tag = "email@example.com"

    plaintext = ""
    ciphertext = ""
    mode = "encrypt"

    if args.base:
        n = args.base

    if args.tag:
        tag = args.tag

    if args.chops:
        chops = args.chops

    #print(str(args.encrypt))


    if args.encrypt:
        plaintext = args.encrypt
        l = len(plaintext)
        #mode = "encrypt"
        c = Riffpe(n, l, key, chops)
        enc = c.enc(tag, plaintext)
        print(str(enc))
    elif args.decrypt:
        ciphertext = args.decrypt
        #mode = "decrypt"
        l = len(ciphertext)
        c = Riffpe(n, l, key, chops)
        dec = c.dec(tag, ciphertext)
        print(str(dec))
    elif args.test:
        tests = args.test
        l = 16
        n = 10
        c = Riffpe(n, l, key, chops)
        w = {}

        for m in range(tests):
            x = [random.randint(0, n - 1) for iter in range(l)]
            #print("mesage: " + str(x))
            ency = c.enc("tag", x)
            #print(str(ency))
            w[m] = ency

        #print(str(w))
    elif args.generate:
        tests = args.generate
        fl = {}
        n = 100
        l = 3
        for m in range(tests):
            x = [random.randint(0, n - 1) for iter in range(l)]
            fl[m] = x
        save("data.json", fl)

    elif args.read:
        fl = read("data.json")
        n = 100
        l = 3
        c = Riffpe(n, l, key, chops)
        w = {}
        for m in fl:
            x = fl[m]
            #print(str(x))
            ency = c.enc("tag", x)
            w[m] = ency

