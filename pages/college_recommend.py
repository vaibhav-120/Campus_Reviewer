import streamlit as st
import pandas as pd, joblib, random, os
st.set_page_config(page_title="Campus Reviewer", layout="wide")


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_RELATIVE_PATH = "kmeans_model.pkl"
SCALER_RELATIVE_PATH = "scaler.pkl"
ENCODER_RELATIVE_PATH = "label_encoders.pkl"
DATA1_RELATIVE_PATH = "data.csv"
DATA_RELATIVE_PATH = "College_details.csv"
MODEL_PATH = os.path.join(BASE_DIR, MODEL_RELATIVE_PATH)
SCALER_PATH = os.path.join(BASE_DIR, SCALER_RELATIVE_PATH)
ENCODER_PATH = os.path.join(BASE_DIR, ENCODER_RELATIVE_PATH)
DATA1_PATH = os.path.join(BASE_DIR, DATA1_RELATIVE_PATH)
DATA_PATH = os.path.join(BASE_DIR, DATA_RELATIVE_PATH)

def load_model(model_path):
    try:
        if os.path.exists(model_path):
            model = joblib.load(model_path)
            return model
        else:
            raise FileNotFoundError(f"Model file not found at: {model_path}")
    except Exception as e:
        raise

def load_file(file_path):
    try:
        if os.path.exists(file_path):
            file = pd.read_csv(file_path)
            return file
        else:
            raise FileNotFoundError(f"File file not found at: {file_path}")
    except Exception as e:
        raise

model = load_model(MODEL_PATH)
scaler = load_model(SCALER_PATH)
label_encoders = load_model(ENCODER_PATH)
data1 = load_file(DATA1_PATH)
data = load_file(DATA_PATH) 

def recommend_colleges(user_input):
    for col in ['State', 'Stream', 'Degree']:
        user_input[col] = label_encoders[col].transform([user_input[col]])[0]

    user_features = [user_input[col] for col in ['State', 'Stream', 'Degree']]
    cluster = model.predict([user_features])[0]

    recommendations = data1[data1['cluster'] == cluster]
    return recommendations[['College_Name','State','Stream']]

def find_closest_fee(lst,fee):
    fee_diffs = abs(lst.Fee - fee)
    min_diff_index = fee_diffs.idxmin()
    return data.loc[min_diff_index]

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
    input = [location,stream,degree]
    user_input = {
        'State': input[0],
        'Stream': input[1],
        'Degree': input[2]
    }
    clgs = recommend_colleges(user_input)
    fee = scaler.transform([[fee_range[1]]])[0][0]

    recommended_college_names = clgs['College_Name'].tolist()
    indices = []
    for i in range(len(data)):
        if data1.loc[i, 'College_Name'] in recommended_college_names:
            indices.append(i)

    s = pd.DataFrame(data1.iloc[indices].State == user_input['State'])
    lst = data1.iloc[s[s['State'] == True].index.tolist()]
    lst = lst[lst.Stream == user_input['Stream']]
    lst = lst[lst.Degree == user_input['Degree']]
    
    closest_college = find_closest_fee(lst,fee)
    st.success(closest_college.College_Name)


st.markdown("---")
st.markdown('<div style="text-align: center; margin-top: 50px; font-size: 0.9rem; color: #6c757d;">Powered by Streamlit | © 2024 College Reviewer</div>', unsafe_allow_html=True)
