import sys
sys.path.insert(0, './src')
import streamlit as st
from ImageCryptography import imageCrptography
from TextCryptography import TextCryptography

menu = st.sidebar.radio('Options', ['Text Cryptography', 'Image Cryptography'])


if menu == 'Text Cryptography':
    st.title('Text Cryptography')
    TextCryptography()
    

elif menu == 'Image Cryptography':
    st.title('Image Cryptography')
    imageCrptography()
