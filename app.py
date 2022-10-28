import streamlit as st
from PIL import Image
import numpy as np
from model import search_video

def search():
    st.write('Input query:', query)
    return search_video(query)


st.image(Image.open(f'img/logo{np.random.choice(3) + 1}.png'), use_column_width=True)
with st.expander("About"):
    st.text("""Profit Autumn Code 2022 Video Generator""")


query = st.text_input('Input query', 'Cats playing with dolphin')

if st.button("run"):
    res_path = search()
#     st.video("https://youtu.be/yVV_t_Tewvs")
    
    video_file = open(res_path, 'rb')
    video_bytes = video_file.read()
    st.video(video_bytes)
