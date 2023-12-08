import streamlit as st
import pandas as pd
import os
import base64

st.set_page_config(page_title="Free FPL points predictor")


#@st.cache_data
def read_data():
   return pd.read_csv("./data/player_scores.csv")

df = read_data()


st.title('FPL points predictor')

st.sidebar.title("GW 16")

st.write('A free and straightforward tool for helping with your FPL team selection.')

st.write('Make your selections on the left to update the table (if you\'re on a mobile device click the little arrow at the top left). Note that the underlying model doesn\'t know when a player is injured, or about things like cup matches or internationlal tournaments')


price = st.sidebar.number_input('budget', value = 15.0, step = 0.1)

position = st.sidebar.radio(
    'Position',
     ['gk', 'df', 'mf', 'st'])

metric = st.sidebar.radio(
    'Priority',
     ['This game week', 'Long term'])

sv='long_term_value_rating'
if metric == 'This game week':
    sv = 'predicted_score'

st.dataframe(df[(df['position'] == position) & (df['price'] <= price)].sort_values(sv, ascending = False)[0:10], hide_index=True)




@st.cache_data
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

@st.cache_data
def get_img_with_href(local_img_path, target_url):
    img_format = os.path.splitext(local_img_path)[-1].replace('.', '')
    bin_str = get_base64_of_bin_file(local_img_path)
    html_code = f'''
        <a href="{target_url}">
            <img src="data:image/{img_format};base64,{bin_str}" />
        </a>'''
    return html_code

#gif_html = get_img_with_href('./assets/coffee_pic.png', 'https://docs.streamlit.io')
#st.markdown(gif_html, unsafe_allow_html=True)


url = "https://donate.stripe.com/aEUcOI09M9LVeEE3cc"
st.sidebar.markdown("Found this useful? [Buy me a coffee](%s)" % url)
st.sidebar.image("./assets/coffee_pic.png")

st.markdown("Models are built from the data curated in the [excellent vaastav github repo](%s)" % "https://github.com/vaastav/Fantasy-Premier-League/")

st.write("The predictions are the averages of two models - a lightGBM model that relies on historical form, and a deep learning approach that utilises embeddings to capture player ability")

st.write("The long-term value predictions are created by applying the model to all future matches and adding up the scores. Matches further into the future are downweighted relative to those that are happening soon. The scores are normalised so that 100 is the highest and 0 is the lowest")