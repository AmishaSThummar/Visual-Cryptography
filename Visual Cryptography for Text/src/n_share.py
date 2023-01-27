import numpy as np
from PIL import Image

# RSA algorithm for pixel encryption
def squareAndMultiply(n, a, b):
    res = 1
    while b != 0:
        if (b & 1):
            res = (res * a) % n
        b = int(b/2)
        a = (a*a) % n
    return res


def extendedEuclidean(n, a):
    r1 = n
    r2 = a
    s1 = 1
    s2 = 0
    t1 = 0
    t2 = 1

    res = []

    while r2 > 0:
        q = (int)(r1/r2)
        r = r1 - (q*r2)
        t = t1 - (q*t2)
        s = s1 - (q*s2)
        r1 = r2
        r2 = r
        s1 = s2
        s2 = s
        t1 = t2
        t2 = t

    res.append(r1)
    res.append(s1)
    res.append(t1)

    # for inverse of the number
    while (res[2] < 0):
        res[2] += n

    return res


def keyGeneration(p, q):
    res = []
    # print("inside key generation")
    n = p*q
    maxEle = (p-1)*(q-1)
    e = 0
    while (True):
        e = np.random.randint(maxEle-2) + 2
        temp = extendedEuclidean(maxEle, e)
        # #print("\nvalue of e :",e)
        # print(temp)
        if (temp[0] == 1):
            # print("Calculated e")
            res.append(e)
            res.append(temp[2])
            break
    # print("key generation end")
    return res


def RSAEncryption(originalPix, e, n):
    originalPix = squareAndMultiply(n, originalPix, e)
    return originalPix


def RSADecryption(cipherPix, d, n):
    cipherPix = squareAndMultiply(n, cipherPix, d)
    return cipherPix


# data has newly genrerated image


def generate_shares(data, share=2):
    data = np.array(data, dtype='u1')
    # print("inside generate shares")
    # Generate image of same size
    # np.zeros => ndarray of zeros having given shape, order and datatype.
    img1 = np.zeros(data.shape).astype("u1")
    img3 = np.zeros(data.shape).astype("u1")
    # #print(img1)
    img2 = np.zeros(data.shape).astype("u1")
    p = 17
    q = 19
    res = keyGeneration(p, q)
    print("After key generation")
    # print(res)
    global publicKey
    global num
    publicKey = res[1]
    # print(publicKey)
    num = p*q
    # Set random factor

    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            for k in range(data.shape[2]):
                n = int(np.random.randint(data[i, j, k] + 1))
                # print(n , " ")
                foo = RSAEncryption(n, res[0], num)

                if foo >= 255:
                    img3[i, j, k] = foo - 255
                    img1[i, j, k] = 255
                else:
                    img1[i, j, k] = foo
                    img3[i, j, k] = 0
                img2[i, j, k] = data[i, j, k] - n

    # print("After Rsa")
    # print(img1)
    # Saving shares
    img1 = img1.astype(np.dtype('u1'))
    img2 = img2.astype(np.dtype('u1'))
    img3 = img3.astype(np.dtype('u1'))
    img1 = Image.fromarray(img1)
    img2 = Image.fromarray(img2)
    img3 = Image.fromarray(img3)

    img1.save("images/pic1.png", "PNG")
    img2.save("images/pic2.png", "PNG")
    img3.save("images/pic3.png", "PNG")


def compress_shares(img1="images/share1.png", img2="images/share2.png", img3="images/share3.png"):
    # Read images
    img1 = np.asarray(Image.open(img1)).astype('u1')
    img2 = np.asarray(Image.open(img2)).astype('u1')
    img3 = np.asarray(Image.open(img3)).astype('u1')

    # print("Inside decryption",img1)
    # shape means dimensions of the image
    img = np.zeros(img1.shape)
    # print("\n")

    # Fit to range
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            for k in range(img.shape[2]):
                cipherPix1 = int(img1[i, j, k])
                cipherPix2 = int(img3[i, j, k])
                n = RSADecryption(cipherPix1 + cipherPix2, publicKey, num)
                # #print(n, " ")
                img[i, j, k] = n + img2[i, j, k]

    # Save compressed image
    # print("After decryption")
    # print(img)
    img = img.astype(np.dtype('u1'))

    img = Image.fromarray(img)
    img.save("images/compress.png", "PNG")
