from PIL import Image
import numpy as np
import numpy.matlib as M

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

    finalImage = M.uint8(finalImage)
    finalImage = Image.fromarray(finalImage)
    finalImage.save("ouput.png", "PNG")

mergeShares(2)