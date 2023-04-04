# PIL is the Python Imaging Library which provides the python interpreter with image editing capabilities.
from PIL import Image
import numpy as np

# Convert encoding data into 8-bit binary
# form using ASCII value of characters
def genData(data):

        # list of binary codes
        # of given data
        newd = []

        for i in data:
            newd.append(format(ord(i), '08b'))
        return newd

# Pixels are modified according to the
# 8-bit binary data and finally returned
def modPix(image, data):
    
    datalist = genData(data)
    # print(datalist)
    lendata = len(datalist)

    # returns iterator to collection pix
    imgIterator = iter(image)   #<iterator object at 0x00000160CB05F460>
    
    print("inside lsb_stegnography encoding :")
    # print(imgIterator.__next__())

    for i in range(lendata):

        # Extracting 3 pixels at a time => hence we need image of size of multiple of 3
        #__next__() => by default it will split array of size 3
        # This method returns the next item from the container. If there are no further items, raise the StopIteration exception. 
        pix = [value for value in imgIterator.__next__()+
                                  imgIterator.__next__()+
                                  imgIterator.__next__()]
        # print(pix)
        # Pixel value should be made
        
        for j in range(0, 8):
            if (datalist[i][j]=='0') and (pix[j]% 2 != 0):

                if (pix[j]% 2 != 0):
                    pix[j] -= 1

            elif (datalist[i][j] == '1') and (pix[j] % 2 == 0):
                pix[j] -= 1

        # Eigh^th pixel of every set tells
        # whether to stop ot read further.
        # 0 means keep reading; 1 means the
        # message is over.
        # [-1] means last index in the list
        if (i == lendata - 1):
            if (pix[-1] % 2 == 0):
                pix[-1] -= 1
        else:
            if (pix[-1] % 2 != 0):
                pix[-1] -= 1

        pix = tuple(pix)
        yield pix[0:3]
        yield pix[3:6]
        yield pix[6:9]

def encode_enc(newimg, data):
    # size function will return height and width of the image
    w = newimg.size[0]
    
    (x, y) = (0, 0)

    # getdata() Returns the contents of this image as a sequence object containing pixel values.
    for pixel in modPix(newimg.getdata(), data):
        # print(pixel)
        # print("*********")
        # print(x,y)


        # Putting modified pixels in the new image
        # puttng pixels height wise
        newimg.putpixel((x, y), pixel)
        if (x == w - 1):
            x = 0
            y += 1
        else:
            x += 1

# Encode data into image
# here data has a text which you want to hide
def lsb_encode(data):
    # Entered image by user is already stored in images folder by name "img"
    try:
        image = Image.open('images/img.jpg', 'r')
    except:
        image = Image.open('images/img.png', 'r')

    newimg = image.copy()

    # this method will hide text into image
    encode_enc(newimg, data)
    
    print(newimg.histogram())
    return newimg

# Decode the data in the image
def lsb_decode(file_name):
    image = Image.open(file_name, 'r')

    data = ''
    
    imgdata = iter(image.getdata())

    while (True):
        pixels = [value for value in imgdata.__next__()[:3] +
                                  imgdata.__next__()[:3] +
                                  imgdata.__next__()[:3]]
        # string of binary data
        binstr = ''

        for i in pixels[:8]:
            if (i % 2 == 0):
                binstr += '0'
            else:
                binstr += '1'

        # convert binary to int => ASCII to character
        data += chr(int(binstr, 2))
        # print("lsb stegnography decoding :")
        # print(pixels[-1])
        if (pixels[-1] % 2 != 0):
            return data
