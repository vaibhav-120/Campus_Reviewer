import streamlit as st
import pandas as pd, joblib, random
st.set_page_config(page_title="Campus Reviewer", layout="wide")

scaler = joblib.load('pages/scaler.pkl')
model = joblib.load('pages/kmeans_model.pkl')
label_encoders = joblib.load('pages/label_encoders.pkl')
data1 = pd.read_csv('pages/data1.csv')

def recommend_colleges(stream,degree,location,fee_range):
    fee = fee_range[1]
    fee = scaler.transform([[fee]])[0][0]
    stream = label_encoders['Stream'].transform([stream])[0]
    degree = label_encoders['Degree'].transform([degree])[0]
    location = label_encoders['State'].transform([location])[0]

    user_features = [location,stream,degree,fee]
    cluster = model.predict([user_features])[0]
    recommendations = data1[data1['cluster'] == cluster]
    collegees = []
    colleges_in_state = data1[data1['State'] == location].College_Name.values.tolist()
    for i in colleges_in_state:
        if i in recommendations['College_Name'].values.tolist() and recommendations[recommendations['Fee'] < fee].College_Name.values.tolist():
            collegees.append(i)
    return collegees

data = pd.read_csv('pages/College_details.csv')

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

st.markdown('<div class="big-title">College Recommender</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-heading">Suggesting college according to prefrences</div>', unsafe_allow_html=True)

st.write("### Select Your Stream")
streams_available = data['Stream'].unique()


stream = st.radio('d',streams_available,index=None,label_visibility="hidden")
if stream:
    st.success(f"{stream} selected")


st.markdown("---")

st.write("### Select Your Degree Type")
degree_available = ["UG", "PG"]
degree = st.radio('d',degree_available,index=None,label_visibility="hidden")
if degree:
    st.success(f"{degree} selected")

st.markdown("---")

st.write("### Select Your Location")
location_available = data['State'].unique()
location = st.selectbox('d',options=location_available,index=None,label_visibility='hidden')

st.markdown("---")

fee_range = st.slider(
    "Select Fee Range",
    min_value=0,
    max_value=3500000,
    value=(5000, 20000),
    step=1000
)

if st.button("Find Colleges"):
    clgs = recommend_colleges(stream,degree,location,fee_range)
    clg = clgs[random.randint(0,len(clgs))]
    st.success(clg)


st.markdown("---")
st.markdown('<div style="text-align: center; margin-top: 50px; font-size: 0.9rem; color: #6c757d;">Powered by Streamlit | © 2024 College Reviewer</div>', unsafe_allow_html=True)
