import cv2
import numpy.matlib as M
import numpy as np
from PIL import Image
from localStoragePy import localStoragePy

# select the shares
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


def createShares(img="images/cipherImage.png",  n=10):
    image = Image.open(img, 'r')
    localStorage = localStoragePy('visual-cryptography', 'sqlite')
    k = localStorage.getItem("noOfShares")
    k = int(k)
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
        if (image.shape[-1] == 4):
            channel = 4

        # randomnly select n-k+1 shares and hide information
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
            if (image.shape[-1] == 4):
                alphaShare = pixToRGBA(
                    imgShares[i, :, :, 24:32].squeeze(), width, height)

            if (image.shape[-1] == 4):
                ithShare = cv2.merge(
                    [redShare, greenShare, blueShare, alphaShare])
            else:
                ithShare = cv2.merge([redShare, greenShare, blueShare])

            ithShare = M.uint8(ithShare)

            ithShare = Image.fromarray(ithShare)
            ithShare.save('images/'+str(i+1)+'.png', "PNG")
        print("outside create shares")