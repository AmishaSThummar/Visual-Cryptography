import numpy as np
from PIL import Image
import numpy.matlib as M
import cv2
from Crypto.Cipher import AES
from secrets import token_bytes
from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage.io import imread
from skimage.metrics import structural_similarity as ssim

# Resize the image and again remake the image -----------------------------------------?????????????????????


def randomPlace(n, recons):
    selectedShares = []
    arr = [i for i in range(n)]

    j = n - 1
    while recons > 0:
        rn = np.random.randint(j+1)
        selectedShares.append(arr[rn])
        tmp = arr[rn]
        arr[rn] = arr[j]
        arr[j] = tmp
        j -= 1
        recons -= 1

    # for i in range(recons):
    #     selectedShares.append(np.random.randint(n))
    # print(selectedShares)
    return selectedShares


def pixToRGBA(pix, width, height):
    arr = np.zeros([width, height], dtype='u1')
    for i in range(width):
        for j in range(height):
            # print(M.squeeze(pix[i,j,:]))  #ndarray
            temp = M.squeeze(pix[i, j, :])
            temp = [str(value) for value in temp]
            temp = ''.join(temp)

            arr[i][j] = int(temp, 2)

    return arr


def createShares(img="cipherImage.png", k=3, n=10):
    image = Image.open(img, 'r')

    print("Image is opend :", image)

    # storing height and width of the image
    [width, height] = image.size
    print("Height and width :", width, height)

    if k > n:
        print("No of shares to construct the original image can't be more than total shares of the image")
    else:
        # Array form required to read pixel value
        image = np.array(image, dtype='u1')
        channel = 3  # RGB
        if(image.shape[-1] == 4):
            channel = 4
        recons = n - k + 1
        # global imgShares
        imgShares = np.zeros((n, width, height, channel*8)).astype("u1")

        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                # print(image[i][j])
                a = np.binary_repr(image[i][j][0], width=8)
                b = np.binary_repr(image[i][j][1], width=8)
                c = np.binary_repr(image[i][j][2], width=8)
                d = ''
                if (image.shape[-1] == 4):
                    d = np.binary_repr(image[i][j][3], width=8)

                # list of the string
                pix = np.array((a, b, c))
                if (image.shape[-1] == 4):
                    pix = np.array((a, b, c, d))
                # print(pix)
                pix = ''.join(pix)  # string
                # print(pix)

                if (image.shape[-1] == 4):
                    for k in range(32):
                        if (pix[k] == '1'):
                            selectedShares = randomPlace(n, recons)
                            for m in range(recons):
                                imgShares[selectedShares[m], i, j, k] = 1
                else:
                    for k in range(24):
                        if (pix[k] == '1'):
                            selectedShares = randomPlace(n, recons)
                            for m in range(recons):
                                imgShares[selectedShares[m], i, j, k] = 1

        # print(imgShares)
        for i in range(n):
            # print(imgShares[i,:,:,0:8])
            redShare = pixToRGBA(
                imgShares[i, :, :, 0:8].squeeze(), width, height)
            greenShare = pixToRGBA(
                imgShares[i, :, :, 8:16].squeeze(), width, height)
            blueShare = pixToRGBA(
                imgShares[i, :, :, 16:24].squeeze(), width, height)
            alphaShare = []
            if(image.shape[-1] == 4):
                alphaShare = pixToRGBA(imgShares[i,:,:,24:32].squeeze(), width, height)

            if(image.shape[-1] == 4):
                ithShare = cv2.merge([redShare, greenShare, blueShare, alphaShare])
            else:
                ithShare = cv2.merge([redShare, greenShare, blueShare])

            ithShare = M.uint8(ithShare)
            # print(ithShare)

            ithShare = Image.fromarray(ithShare)
            ithShare.save(str(i+1)+'.png', "PNG")
        print("outside create shares")
        # imgCons = []
        # for k1 in range(n):
        #     for k2 in range(image.shape[0]):
        #         for k3 in range(image.shape[1]):
        #             value = ""
        #             for k4 in range(32):
        #                 value += imgShares[k1][k2][k3][k4]


def AESEncryption(img="demo.png"):
    image = Image.open(img, 'r')
    print("Image is opend :", image)
    image = np.array(image, dtype='u1')
    # channel = 3  #RGB
    # # global imgShares
    # imgShares = np.zeros((n, width, height, channel*8)).astype("u1")
    # imgIterator = iter(image)
    key = token_bytes(16)
    cipherEncry = AES.new(key, AES.MODE_EAX)
    nonce = cipherEncry.nonce
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

            # print("before enc")
            # print(inputForAes)

            # print("Cipher")
            ciphertext = cipherEncry.encrypt(bytes(inputForAes))
            # print(ciphertext)
            temp = list(ciphertext)
            # print(image.shape[-1])
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

            # print(temp)
            # print("after aes dec")
            # plainText = cipherDecry.decrypt(ciphertext)
            # print(list(plainText))

    cipherImage = cipherImage.astype(np.dtype('u1'))
    # print("cipher image :\n", cipherImage)
    cipherImage = Image.fromarray(cipherImage)
    cipherImage.save("cipherImage.png", "PNG")
    print("Outside encryption\n")
    return key, nonce


def mergeShares(k):
    share1 = Image.open("1.png", 'r')
    [width, height] = share1.size
    share1 = np.array(share1, dtype='u1')
    finalImage = np.zeros(share1.shape).astype("u1")
    isPNG = 1 if finalImage.shape[-1] == 4 else 0
    channel = 3
    if(isPNG):
        channel = 4
    share = np.zeros([k, width, height, channel], dtype='u1')
    # finalImage = np.zeros([width, height, channel], dtype='u1')

    print("Inside decryption")
    isPNG = 1 if finalImage.shape[-1] == 4 else 0

    for i in range(k):
        currImg = Image.open(str(i+1)+'.png', 'r')
        currImg = np.array(currImg, dtype='u1')

        for j in range(currImg.shape[0]):
            for m in range(currImg.shape[1]):
                share[i, j, m, 0] = currImg[j, m, 0]
                share[i, j, m, 1] = currImg[j, m, 1]
                share[i, j, m, 2] = currImg[j, m, 2]
                if(isPNG):
                    share[i,j,m,3] = currImg[j,m,3]

    for i in range(k):
        for j in range(width):
            for m in range(height):
                finalImage[j, m, 0] = M.bitwise_or(
                    finalImage[j, m, 0], share[i, j, m, 0])
                finalImage[j, m, 1] = M.bitwise_or(
                    finalImage[j, m, 1], share[i, j, m, 1])
                finalImage[j, m, 2] = M.bitwise_or(
                    finalImage[j, m, 2], share[i, j, m, 2])
                if(isPNG):
                    finalImage[j,m,3] = M.bitwise_or(finalImage[j,m,3], share[i,j,m,3])

    # finalImage = M.uint8(finalImage)
    # finalImage = Image.fromarray(finalImage)
    # finalImage.save("ouput.png", "PNG")\r

    finalImage = M.uint8(finalImage)
    # print("Merged shares :\n", finalImage)
    finalImage = Image.fromarray(finalImage)
    finalImage.save("MergedShares.png", "PNG")


def AESDecryption(key, nonce):
    image = Image.open("MergedShares.png", 'r')
    image = np.array(image, dtype='u1')
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
    temp = AESEncryption()
    print(temp[0])
    createShares()
    mergeShares(3)
    AESDecryption(temp[0], temp[1])
    img_orig = imread('demo.png', as_gray=False)
    img_recon = imread('decryptedImg.png', as_gray=False)
    psnr_value = psnr(img_orig, img_recon)

    print('PSNR:', psnr_value)

    # Calculate the SSIM between the two images
    img_orig = imread('demo.png', as_gray=True)
    img_recon = imread('decryptedImg.png', as_gray=True)
    ssim_value = ssim(img_orig, img_recon)

    print('SSIM:', ssim_value)

kOutOfNShares()
