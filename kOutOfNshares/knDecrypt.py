from PIL import Image
import numpy as np
import numpy.matlib as M
from Crypto.Cipher import AES
from secrets import token_bytes

import knEncrypt

def mergeShares(k):
    share1 = Image.open("1.png",'r')
    [width, height] = share1.size
    channel = 3
    share = np.zeros([k,width,height, channel], dtype='u1')
    finalImage = np.zeros([width,height, channel], dtype='u1')
    print("Inside decryption")

    for i in range(k):
        currImg = Image.open(str(i+1)+'.png', 'r')
        currImg = np.array(currImg, dtype='u1')

        for j in range(currImg.shape[0]):
            for m in range(currImg.shape[1]):
                share[i,j,m,0] = currImg[j,m,0]
                share[i,j,m,1] = currImg[j,m,1]
                share[i,j,m,2] = currImg[j,m,2]
                # share[i,j,m,3] = currImg[j,m,3]

    for i in range(k):
        for j in range(width):
            for m in range(height):
                finalImage[j,m,0] = M.bitwise_or(finalImage[j,m,0], share[i,j,m,0])
                finalImage[j,m,1] = M.bitwise_or(finalImage[j,m,1], share[i,j,m,1])
                finalImage[j,m,2] = M.bitwise_or(finalImage[j,m,2], share[i,j,m,2])
                # finalImage[j,m,3] = M.bitwise_or(finalImage[j,m,3], share[i,j,m,3])

    # finalImage = M.uint8(finalImage)
    # finalImage = Image.fromarray(finalImage)
    # finalImage.save("ouput.png", "PNG")\r
    finalImage = M.uint8(finalImage)
    finalImage = Image.fromarray(finalImage)
    finalImage.save("MergedShares.png", "PNG")

def AESDecryption():
    image = Image.open("MergedShares.png", 'r')
    image = np.array(image, dtype='u1')
    cipherDecry = AES.new(knEncrypt.key, AES.MODE_EAX, nonce=knEncrypt.nonce)
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
            # print(ciphertext)
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
            # print("in decryption")
            # print(temp)
            # print("after aes dec")
            # plainText = cipherDecry.decrypt(ciphertext)
            # print(list(plainText))

    cipherImage = cipherImage.astype(np.dtype('u1'))
    cipherImage = Image.fromarray(cipherImage)
    cipherImage.save("decryptedImg.png", "PNG")
    print("Complete the AES decryption")


def kOutOfNShares():
    mergeShares(3)
    AESDecryption()

kOutOfNShares()