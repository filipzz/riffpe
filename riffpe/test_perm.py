import random
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad


from riffpe.perm import Perm


def test_perm():

    c = random.randint(10, 10000)

    key = get_random_bytes(16)
    #key = b'\xefTT\xc89\xd0ap\xd7M\x97V\xd3\x82h\xeb'



    a = Perm(c, key)


    iv = pad("This is tag".encode(), AES.block_size)

    x = random.randint(0, c)

    pi_x = a.perm(iv, x, 0)

    pi_inv_x = a.perm(iv, pi_x, 1)

    print(str(pi_x))

    print(str(pi_inv_x))

    assert(x == pi_inv_x)