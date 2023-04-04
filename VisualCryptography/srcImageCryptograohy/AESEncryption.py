import base64
from secrets import token_bytes
from Crypto.Cipher import AES
import datetime
import numpy as np
from PIL import Image
import streamlit as st
import extra_streamlit_components as stx
from localStoragePy import localStoragePy


def AESEncryption():
    localStorage = localStoragePy('visual-cryptography', 'sqlite')

    image = Image.open('images/userGivenImage.png', 'r')
    print("Image is opend :", image)
    image = np.array(image, dtype='u1')

    key = token_bytes(16)
    cipherEncry = AES.new(key, AES.MODE_EAX)
    nonce = cipherEncry.nonce
    print("Inside encryption nonce:", nonce)

    key = base64.b64encode(key).decode()
    nonce = base64.b64encode(nonce).decode()

    localStorage.setItem("nonce", nonce)
    localStorage.setItem("key",key)

    print("Inside encryption nonce:", nonce)

    cipherImage = np.zeros(image.shape).astype("u1")
    print(image.shape[-1])
    for i in range(image.shape[0]):
        for j in range(0, image.shape[1], 4):
            inputForAes = []
            inputForAes.append(image[i][j][0])
            inputForAes.append(image[i][j][1])
            inputForAes.append(image[i][j][2])
            if (image.shape[-1] == 4):
                inputForAes.append(image[i][j][3])

            if (j+1 < image.shape[1]):
                inputForAes.append(image[i][j+1][0])
                inputForAes.append(image[i][j+1][1])
                inputForAes.append(image[i][j+1][2])
                if (image.shape[-1] == 4):
                    inputForAes.append(image[i][j+1][3])

            if (j+2 < image.shape[1]):
                inputForAes.append(image[i][j+2][0])
                inputForAes.append(image[i][j+2][1])
                inputForAes.append(image[i][j+2][2])
                if (image.shape[-1] == 4):
                    inputForAes.append(image[i][j+2][3])

            if (j+3 < image.shape[1]):
                inputForAes.append(image[i][j+3][0])
                inputForAes.append(image[i][j+3][1])
                inputForAes.append(image[i][j+3][2])
                if (image.shape[-1] == 4):
                    inputForAes.append(image[i][j+3][3])

            # doing encryption of 16 bytes at a time
            ciphertext = cipherEncry.encrypt(bytes(inputForAes))

            temp = list(ciphertext)

            if (image.shape[-1] == 4):
                cipherImage[i][j] = temp[0:4]
                if (j+1 < image.shape[1]):
                    cipherImage[i][j+1] = temp[4:8]
                if (j+2 < image.shape[1]):
                    cipherImage[i][j+2] = temp[8:12]
                if (j+3 < image.shape[1]):
                    cipherImage[i][j+3] = temp[12:16]
            else:
                cipherImage[i][j] = temp[0:3]
                if (j+1 < image.shape[1]):
                    cipherImage[i][j+1] = temp[3:6]
                if (j+2 < image.shape[1]):
                    cipherImage[i][j+2] = temp[6:9]
                if (j+3 < image.shape[1]):
                    cipherImage[i][j+3] = temp[9:12]

    cipherImage = cipherImage.astype(np.dtype('u1'))

    cipherImage = Image.fromarray(cipherImage)
    cipherImage.save("images/cipherImage.png", "PNG")
    print("Outside encryption\n")
    return key, nonce
