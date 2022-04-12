import argparse
import random

from riffpe.riffpe import Riffpe

from urllib import parse
import json
import requests
from pathlib import Path
#from Crypto.Cipher import AES
#from Crypto.Util.Padding import pad
from ff3 import FF3Cipher
import pyffx

from time import perf_counter_ns

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
    parser.add_argument("--compare", help="Reads test data from a file", type=str)
    parser.add_argument("--generate", help="Generates test data and saves them in a file", type=int)

    args, args_unknown = parser.parse_known_args()

    n = 10
    l = 2
    chops = 2

    key = b'\xefTT\xc89\xd0ap\xd7M\x97V\xd3\x82h\xeb'
    tag = "exmil@am"


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
        start = perf_counter_ns()
        c = Riffpe(n, l, key, tag, chops)
        enc = c.enc(plaintext)
        end = perf_counter_ns()
        print(args.encrypt)
        print(str(enc))
        print("time: %s" % (end - start))
    elif args.decrypt:
        ciphertext = args.decrypt
        #mode = "decrypt"
        l = len(ciphertext)
        c = Riffpe(n, l, key, tag, chops)
        dec = c.dec(ciphertext)
        print(str(dec))
    elif args.test:
        tests = args.test
        l = 2
        n = 10
        c = Riffpe(n, l, key, tag, chops)
        w = {}

        for m in range(tests):
            x = [random.randint(0, n - 1) for iter in range(l)]
            #print("mesage: " + str(x))
            ency = c.enc(x)
            #print(str(ency))
            w[m] = ency

        #print(str(w))
    elif args.generate:
        tests = args.generate
        fl = {}
        n = 10
        l = 2
        #n = 10
        #l = 4
        for m in range(tests):
            x = [random.randint(0, n - 1) for iter in range(l)]
            fl[m] = x
        save("data.json", fl)

    elif args.read:
        fl = read("data.json")
        n = 10
        l = 4
        c = Riffpe(n, l, key, tag, chops)
        w = {}
        for m in fl:
            x = fl[m]
            #print(str(x))
            ency = c.enc(x)
            w[m] = ency

    elif args.compare:
        fl = read("data.json")
        key = "EF4359D8D580AA4F7F036D6F04FC6A94"
        tweak = "D8E7920AFA330A73"

        #n = 100
        #l = 3
        #c = Riffpe(n, l, key, chops)
        l = 2
        n = 10
        c = Riffpe(n, l, key.encode(), tag, chops)
        w = {}
        tot_time = 0
        for m in fl:
            x = fl[m]
            pt = x[0] + x[1] # + x[2] + x[3]
            #print("w " + pt)
            #print(m)
            #c = FF3Cipher(10, key, tweak)
            #cipher = AES.new(key, AES.MODE_CBC, bytearray(AES.block_size))
            #print(str(pt))
            start = perf_counter_ns()

            if args.compare == "ffx":
                c = pyffx.Integer(key.encode(), length=16)
                encrypted = c.encrypt(str(pt))
                w[m] = encrypted
            else:
                # riffpe part
                ency = c.enc(x)
                #print(ency)
                w[m] = ency
                #print("w[%s] = %s" % (m, w[m]))

            end = perf_counter_ns()

            tot_time = tot_time + end - start

            #print(str(x))
            #ency = c.enc("tag", x)

            #w[m] = ct

        print(len(w))
        re = random.randint(0, len(w))
        print("w[%s] = %s" % (re, w[str(re)]))
        print(tot_time / len(w))
