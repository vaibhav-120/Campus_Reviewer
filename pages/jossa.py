import streamlit as st
import pandas as pd, joblib, numpy as np
import os
st.set_page_config(page_title="Campus Reviewer", layout="wide")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_RELATIVE_PATH = "model.pkl"
MODEL_PATH = os.path.join(BASE_DIR, MODEL_RELATIVE_PATH)

def load_model(model_path):
    try:
        if os.path.exists(model_path):
            model = joblib.load(model_path)
            return model
        else:
            raise FileNotFoundError(f"Model file not found at: {model_path}")
    except Exception as e:
        raise

model = load_model(MODEL_PATH)
details = pd.read_csv('pages/detail.csv')

def encoded_value(df,val):
    for i in range(len(df)):
        if df[i] == val:
            return i

def predict_colleges(program,gender,seat,quota,rank):
    ENC_Program = encoded_value(details['Program'],program)
    ENC_Gender = encoded_value(details['Gender'],gender)
    ENC_Seat_Type = encoded_value(details['Seat Type'],seat)
    ENC_Quota = encoded_value(details['Quota'],quota)
    predict = model.predict([[ENC_Program,ENC_Quota,ENC_Seat_Type,ENC_Gender,rank]])
    return details['Colleges'][predict[0]]


st.markdown(
    '''
    <style>
        .big-title {
        font-size: 3rem;
        color: #007BFF;
        font-weight: bold;
        text-align: center;
        margin-bottom: 10px;
    }
    .sub-heading {
        font-size: 1.5rem;
        text-align: center;
        margin-top: 0;
        margin-bottom: 20px;
    }
    .stRadio > div {
        display: flex;
        flex-direction: row;
        gap: 15px;
    }
    .stRadio div[role='radiogroup'] > label > div:first-child {
        display: none;
    }
    .stRadio label {
        background: rgba(20, 20, 20, 0.2);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        color: #ffffff;
        padding: 12px 25px;
        border-radius: 15px;
        border: 1px solid rgba(50, 205, 50, 0.4);
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        cursor: pointer;
        transition: all 0.3s ease;
        text-align: center;
        font-weight: 500;
        background-clip: padding-box;
        position: relative;
    }
    .stRadio label:hover {
        background: rgba(50, 205, 50, 0.3);
        border-color: rgba(34, 139, 34, 0.6);
        transform: scale(1.05);
        box-shadow: 0px 8px 12px rgba(0, 0, 0, 0.2);
    }
    </style>
    ''',
    unsafe_allow_html=True
)

st.markdown('<div class="big-title">College Predictor</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-heading">Predicting college you will get according to your rank</div>', unsafe_allow_html=True)

st.write("### Enter Your Rank")
rank = st.number_input('d',1,200000,label_visibility='hidden')
if rank:
    st.success(f"Your rank is {rank}")


st.markdown("---")

st.write("### Select Your Quota Type")
quota_available = details['Quota'].unique()
quota = st.radio('d',quota_available[:-1],index=None,label_visibility="hidden")
if quota:
    st.success(f"{quota} selected")

st.markdown("---")

st.write("### Select Your Gender")
gender_available = details['Gender'].unique()
gender = st.radio('d',gender_available[:-1],index=None,label_visibility="hidden")
if gender:
    st.success(f"{gender} selected")


st.markdown("---")


st.write("### Select Your Seat Type")
seat_available = details['Seat Type'].unique()
seat = st.radio('d',seat_available[:-1],index=None,label_visibility="hidden")
if seat:
    st.success(f"{seat} selected")
    
st.markdown("---")


st.write("### Select Your Program")
program_available = details['Program'].unique()
program = st.selectbox('d',program_available,index=None,label_visibility='hidden')
if program:
    st.success(f"{program} selected")


if st.button("Find College"):
    if program and gender and seat and quota and rank:
        clg = predict_colleges(program,gender,seat,quota,rank)
        st.success(clg)
    else:
        st.warning("Fill all values")


st.markdown("---")
st.markdown('<div style="text-align: center; margin-top: 50px; font-size: 0.9rem; color: #6c757d;">Powered by Streamlit | © 2024 College Reviewer</div>', unsafe_allow_html=True)
