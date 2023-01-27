import numpy as np
from PIL import Image
import numpy.matlib as M
import cv2

def randomPlace(n, recons):
    selectedShares = []
    arr = [i for i in range(n)]
    
    j = n - 1
    while j >= 0:
        rn = np.random.randint(j+1)
        selectedShares.append(arr[rn])
        tmp = arr[rn]
        arr[rn] = arr[j]
        arr[j] = tmp
        j = j - 1


    # for i in range(recons):
    #     selectedShares.append(np.random.randint(n))
    # print(selectedShares)
    return selectedShares

def pixToRGBA(pix, width, height):
    arr = np.zeros([width, height], dtype='u1')
    for i in range(width):
        for j in range(height):
            # print(M.squeeze(pix[i,j,:]))  #ndarray
            temp = M.squeeze(pix[i,j,:])
            temp = [str(value) for value in temp]
            temp = ''.join(temp)

            arr[i][j] = int(temp, 2)

    return arr

def createShares(img = "demo.png", k = 3 ,n=10):
    image = Image.open(img, 'r')
    print("Image is opend :",image)

    # storing height and width of the image
    [width, height] = image.size
    print("Height and width :",width, height)

    if k > n:
        print("No of shares to construct the original image can't be more than total shares of the image")
    else:
        # Array form required to read pixel value
        image = np.array(image, dtype='u1')
        channel = 3  #RGB
        recons = n - k +1
        # global imgShares
        imgShares = np.zeros((n, width, height, channel*8)).astype("u1")

        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                # print(image[i][j])
                a = np.binary_repr(image[i][j][0], width=8)
                b = np.binary_repr(image[i][j][1], width=8)
                c = np.binary_repr(image[i][j][2], width=8)
                # d = np.binary_repr(image[i][j][3], width=8)

                # list of the string 
                pix = np.array((a,b,c))
                # print(pix)
                pix = ''.join(pix)  #string
                # print(pix)

                for k in range(24):
                    if(pix[k] == '1'):
                        selectedShares = randomPlace(n, recons)
                        for m in range(recons):
                            imgShares[selectedShares[m],i,j,k] = 1

        # print(imgShares)
        for i in range(n):
            # print(imgShares[i,:,:,0:8])
            redShare = pixToRGBA(imgShares[i,:,:,0:8].squeeze(), width, height)
            greenShare = pixToRGBA(imgShares[i,:,:,8:16].squeeze(), width, height)
            blueShare = pixToRGBA(imgShares[i,:,:,16:24].squeeze(), width, height)
            # alphaShare = pixToRGBA(imgShares[i,:,:,24:32].squeeze(), width, height)

            ithShare = cv2.merge([redShare, greenShare, blueShare])
            
            ithShare = M.uint8(ithShare)
            # print(ithShare)

            ithShare = Image.fromarray(ithShare)
            ithShare.save(str(i+1)+'.png', "PNG")
            

        # imgCons = []
        # for k1 in range(n):
        #     for k2 in range(image.shape[0]):
        #         for k3 in range(image.shape[1]):
        #             value = ""
        #             for k4 in range(32):
        #                 value += imgShares[k1][k2][k3][k4]
                    

createShares()