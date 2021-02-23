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
    w = Riffpe(c, l, key)

    message = random_message(c, l)
    print("Message:\t" + str(message))

    enc = w.enc("asdasda", message)

    dec = w.dec("asdasda", enc)

    print("Decrypted:\t" + str(dec))

    assert (message == dec)

