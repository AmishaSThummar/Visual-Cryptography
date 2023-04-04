import os
import sys
sys.path.insert(0, './src')
import streamlit as st
from PIL import Image
from srcTextCryptography.lsb_stegno import lsb_encode, lsb_decode
from srcTextCryptography.n_share import generate_shares, compress_shares
from SSIM_PIL import compare_ssim
from skimage.io import imread
from skimage.metrics import peak_signal_noise_ratio as psnr


def TextCryptography():
    menu = st.sidebar.radio('Options', ['Encode', 'Decode'])

    if menu == 'Encode':
        st.title('Encoding')

        # Image
        img = st.file_uploader('Upload image file', type=['png'])
        if img is not None:
            img = Image.open(img)
            newsize = (120, 120)
            img = img.resize(newsize)
            
            img.save('images/img.png')
            st.image(img, caption='Selected image to use for data encoding',
                    width=250)

        # Data
        txt = st.text_input('Message to hide')

        # Encode message
        if st.button('Encode data and Generate shares'):

            # Checks
            if len(txt) == 0:
                st.warning('No data to hide')
            elif img is None:
                st.warning('No image file selected')

            # Generate splits
            else:
                generate_shares(lsb_encode(txt))
                st.success('Data encoded, Shares generated in folder [images]')

    elif menu == 'Decode':
        st.title('Decoding')

        # Share 1
        img1 = st.file_uploader('Upload Share 1', type=['png'])
        if img1 is not None:
            img1 = Image.open(img1)
            img1.save('images/share1.png')
            st.image(img1, caption='Share 1', use_column_width=True)

        # Share 2
        img2 = st.file_uploader('Upload Share 2', type=['png'])
        if img2 is not None:
            img2 = Image.open(img2)
            img2.save('images/share2.png')
            st.image(img2, caption='Share 2', use_column_width=True)
        
        # Share 3
        img3 = st.file_uploader('Upload Share 3', type=['png'])
        if img3 is not None:
            img3 = Image.open(img3)
            img3.save('images/share3.png')
            st.image(img3, caption='Share 3', use_column_width=True)

        # Decode message
        if st.button('Compress shares and Decode message'):

            # Check
            if img1 is None or img2 is None:
                st.warning('Upload both shares')

            # Compress shares
            else:
                compress_shares()
                os.remove('images/share1.png')
                os.remove('images/share2.png')
                os.remove('images/share3.png')
                st.success('Decoded message: ' + lsb_decode('images/compress.png'))

                # error calculation
                img_orig = imread('images/img.png', as_gray=False)
                img_recon = imread('images/compress.png', as_gray=False)
                psnr_value = psnr(img_orig, img_recon)
                st.write("PSNR :", psnr_value)
                print('PSNR:', psnr_value)

                # Calculate the SSIM between the two images
                img_orig = Image.open('images/img.png')
                img_recon = Image.open('images/compress.png')
                
                ssim_value = compare_ssim(img_orig, img_recon)
                st.write('Structural similarity:', ssim_value)
                print('SSIM:', ssim_value)


# abcdefghijklmnopqrstuvwxyz
# Lorem ipsum dolor sit amet consectetur adipisicing elit. Neque, odio!
# "Hard work beats talent when talent doesn't work hard." ―Tim Notke
# @suhani -> #Hello $Fine