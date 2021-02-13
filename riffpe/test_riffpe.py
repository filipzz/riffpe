import random

from riffpe import Riffpe


def test_rs():
    c = random.randint(10, 100)
    l = random.randint(3, 10)
    print("Generated parameters: %s %s" % (c + 1, l))

    w = Riffpe(c, l)

    message = random_message(c, l)
    print("Testing for message: " + str(message))

    for i in range(l):
        prev = message[0:i]
        x = message[i]
        next = message[i + 1:]
        # print("%s %s %s" % (prev, x, next))
        enc = w.rs("asdasd", "asdasd", prev, x, next, 0)
        dec = w.rs("asdasd", "asdasd", prev, enc, next, 1)
        print("%s %s %s" % (x, enc, dec))
        assert (x == dec)


def random_message(c:int, l:int):
    return [random.randint(0, c) for iter in range(l)]


def test_enc():
    c = random.randint(10, 100)
    l = random.randint(3, 10)
    print("Generated parameters: %s %s" % (c + 1, l))

    w = Riffpe(c, l)

    message = random_message(c, l)
    print("Message:\t" + str(message))

    enc = w.enc("asdasd", "asdasda", message)

    dec = w.dec("asdasd", "asdasda", enc)

    print("Decrypted:\t" + str(dec))

    assert (message == dec)

