from Crypto.Random import get_random_bytes
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


def test_enc():
    c = random.randint(10, 100)
    l = random.randint(3, 10)
    print("Generated parameters: %s %s" % (c, l))

    key = get_random_bytes(16)
    #key = b'\xefTT\xc89\xd0ap\xd7M\x97V\xd3\x82h\xeb'
    tweak = "momo"
    w = Riffpe(c, l, key, tweak, 1)

    message = random_message(c, l)
    print("Message:\t" + str(message))

    enc = w.enc(message)

    dec = w.dec(enc)

    print("Decrypted:\t" + str(dec))

    assert (message == dec)

