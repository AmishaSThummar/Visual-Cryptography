import sys
sys.path.insert(0, './src')
# import streamlit as st
from PIL import Image
from srcImageCryptograohy.AESEncryption import st
from srcImageCryptograohy.AESEncryption import AESEncryption
from srcImageCryptograohy.AESDecryption import AESDecryption
from srcImageCryptograohy.kOutOfNSharesEncryption import createShares
from srcImageCryptograohy.kOutOfNSharesDecryption import mergeShares
from skimage.io import imread
from skimage.metrics import peak_signal_noise_ratio as psnr
from localStoragePy import localStoragePy
from SSIM_PIL import compare_ssim


def imageCrptography():
    
    menu = st.sidebar.radio('Options', ['Encode', 'Decode'])

    if menu == 'Encode':
        st.title('Encoding')

        # Image
        img = st.file_uploader('Upload image file', type=['jpg', 'png', 'jpeg'])
        if img is not None:
            img = Image.open(img)

            img.save('images/userGivenImage.png')
            st.image(img, caption='Selected image to use for data encoding', width=250)
            
        noOfShares = st.text_input("Enter the no of images wants to divide out of 10")
        # Encode message
        if st.button('Encode data and Generate shares'):

            if len(noOfShares) == 0:
                st.warning("Enter the no of shares.")
            elif img is None:
                st.warning("No image file is selected.")
            print("Inside k out of n shares \n")
            localStorage = localStoragePy('visual-cryptography', 'sqlite')
            localStorage.setItem("noOfShares",noOfShares)
            AESEncryption()
            createShares()
            st.success('Image encoded, Shares generated in folder [images]')



    elif menu == 'Decode':
        st.title('Decoding')
        localStorage = localStoragePy('visual-cryptography', 'sqlite')

        if st.button('Compress shares and Decode message'):
            mergeShares()

            key = localStorage.getItem("key")
            nonce = localStorage.getItem("nonce")
            AESDecryption(key, nonce)
            st.success('Image decrypted and stored in folder [images]')
            img = Image.open("images/decryptedImg.png")
            st.image(img, caption='Image after merging the given shares', use_column_width=True)


            # error calculation
            img_orig = imread('images/userGivenImage.png', as_gray=False)
            img_recon = imread('images/decryptedImg.png', as_gray=False)
            psnr_value = psnr(img_orig, img_recon)
            st.write("Pick signal to noise ratio: ",psnr_value)
            print('PSNR:', psnr_value)

            # Calculate the SSIM between the two images
            img_orig = Image.open('images/userGivenImage.png')
            img_recon = Image.open('images/decryptedImg.png')
            
            ssim_value = compare_ssim(img_orig, img_recon)
            st.write('Structural similarity:', ssim_value)
            print('SSIM:', ssim_value)


