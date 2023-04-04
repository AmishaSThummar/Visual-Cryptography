import base64
from Crypto.Cipher import AES
import numpy as np
from PIL import Image

def AESDecryption(key, nonce):
    image = Image.open("images/MergedShares.png", 'r')
    image = np.array(image, dtype='u1')

    print("Inside decryption :", key)
    nonce = base64.b64decode(nonce)
    key = base64.b64decode(key)
    print("Inside decryption nonce:", nonce)
    cipherDecry = AES.new(key, AES.MODE_EAX, nonce=nonce)
    cipherImage = np.zeros(image.shape).astype("u1")

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

            ciphertext = cipherDecry.decrypt(bytes(inputForAes))

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
    cipherImage.save("images/decryptedImg.png", "PNG")
    print("Complete the AES decryption")