import numpy.matlib as M
import numpy as np
from PIL import Image
from localStoragePy import localStoragePy

def mergeShares():
    share1 = Image.open("images/1.png", 'r')
    localStorage = localStoragePy('visual-cryptography', 'sqlite')
    k = localStorage.getItem("noOfShares")
    k = int(k)
    
    [width, height] = share1.size
    share1 = np.array(share1, dtype='u1')
    finalImage = np.zeros(share1.shape).astype("u1")
    isPNG = 1 if finalImage.shape[-1] == 4 else 0
    channel = 3
    if (isPNG):
        channel = 4
    share = np.zeros([k, width, height, channel], dtype='u1')

    print("Inside merge shares")
    isPNG = 1 if finalImage.shape[-1] == 4 else 0

    for i in range(k):
        currImg = Image.open('images/'+str(i+1)+'.png', 'r')
        currImg = np.array(currImg, dtype='u1')

        for j in range(currImg.shape[0]):
            for m in range(currImg.shape[1]):
                share[i, j, m, 0] = currImg[j, m, 0]
                share[i, j, m, 1] = currImg[j, m, 1]
                share[i, j, m, 2] = currImg[j, m, 2]
                if (isPNG):
                    share[i, j, m, 3] = currImg[j, m, 3]

    for i in range(k):
        for j in range(width):
            for m in range(height):
                finalImage[j, m, 0] = M.bitwise_or(
                    finalImage[j, m, 0], share[i, j, m, 0])
                finalImage[j, m, 1] = M.bitwise_or(
                    finalImage[j, m, 1], share[i, j, m, 1])
                finalImage[j, m, 2] = M.bitwise_or(
                    finalImage[j, m, 2], share[i, j, m, 2])
                if (isPNG):
                    finalImage[j, m, 3] = M.bitwise_or(
                        finalImage[j, m, 3], share[i, j, m, 3])

    finalImage = M.uint8(finalImage)

    finalImage = Image.fromarray(finalImage)
    finalImage.save("images/MergedShares.png", "PNG")