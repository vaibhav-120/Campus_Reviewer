import streamlit as st
from streamlit_lottie import st_lottie
import pandas as pd, math
import requests,scraping, sentiment_analyses
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Campus Reviewer", layout="wide")

st.markdown(
    """
    <style>
    header[data-testid="stHeader"] {
        height:0
    }
    body {
        background-color: #f8f9fa;
    }
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
    .info {
        font-size: 1.2rem;
        margin-bottom: 20px;
    }
    .score {
        font-size: 2rem;
        margin-bottom: 20px;
    }
    .input-box {
        width: 80%;
        padding: 10px;
        font-size: 1.2rem;
        border-radius: 10px;
        border: 2px solid #007BFF;
        margin: 10px auto;
    }
    .stRadio > div {
        display: flex;
        flex-direction: row;
        flex-wrap: wrap;
        gap: 15px; /* Adds spacing between options */
    }
    .stRadio div[role='radiogroup'] > label > div:first-child {
        display: none;
    }
    .stRadio label {
        background: rgba(50, 205, 50, 0.2); /* Light green glass effect */
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
    .stRadio label::after {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(144, 238, 144, 0.3), rgba(34, 139, 34, 0.3));
        opacity: 0.7;
        border-radius: 15px;
        z-index: -1;
        transition: all 0.3s ease;
    }
    .stRadio label:hover {
        background: rgba(50, 205, 50, 0.3); /* Slightly darker green */
        border-color: rgba(34, 139, 34, 0.6); /* Darker green border */
        color: #e0f7fa;
        transform: scale(1.05);
        box-shadow: 0px 8px 12px rgba(0, 0, 0, 0.2);
    }
    .stRadio div[role='radiogroup'] > label[data-selected="true"] {
        background: rgba(0, 128, 0, 0.6); /* Deep green for selected */
        border-color: rgba(0, 128, 0, 0.8); /* Stronger green border */
        color: #ffffff;
        box-shadow: 0px 6px 10px rgba(0, 0, 0, 0.2);
    }
    .stRadio div[role='radiogroup'] > label[data-selected="true"]:hover {
        background: rgba(0, 100, 0, 0.8); /* Even deeper green on hover when selected */
        transform: scale(1.05);
        box-shadow: 0px 10px 15px rgba(0, 0, 0, 0.3);
    }
    .card {
        background-color: #f0f8ff;
        padding: 20px;
        margin-bottom: 15px;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s;
    }
    .card:hover {
        transform: scale(1.02);
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
    }
    .card p {
        color: #4b5563;
        margin: 5px 0 0 0;
        font-size: 16px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


@st.cache_data
def load_url(url: str):
    r = requests.get(url)
    return r.json()

df = pd.read_csv('college_data.csv')

st.markdown('<div class="big-title">Campus Reviewer</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-heading">Analyze feedback from various colleges</div>', unsafe_allow_html=True)

col1,col2,col3 = st.columns([1,2,1])
with col2:
    college_names = df['name'].values
    college_input = st.selectbox("", options=college_names, index=None, placeholder="Enter College Name")

def plot(data):
    fig = px.bar(
        data, 
        x='Sentiment',
        color='Sentiment',
        color_discrete_map={'Positive': '#3a5a40', 'Slightly Positive': '#588157', 'Neutral': '#dad7cd','Slightly Negative': '#CB8585' ,'Negative': '#B83737'},
        template='plotly_white',
    )
    fig.update_layout(
        yaxis_title='Number of Reviews',
        margin=dict(l=20, r=20, t=50, b=20)
    )
    fig.update_traces(hovertemplate='Sentiment: %{x}<br>Count: %{y}')
    st.plotly_chart(fig, use_container_width=True)

    option = data['Sentiment'].unique()
    selected_category = st.radio("", options=option,key="Sentiment_choice",index=None,label_visibility='hidden')


    st.subheader("You can see summary of each sentiment here.")
    if selected_category:
        text = data[data['Sentiment'] == selected_category].Text.values

        rowval = min(math.ceil(len(text)/2), 5)
        textcol1, textcol2 = st.columns(2)
        for i in range(min(len(text),10)):
            if i<rowval:
                with textcol1:
                    st.markdown(f"""<div class="card"><p>{text[i]}</p></div>""",unsafe_allow_html=True)
            else:
                with textcol2:
                    st.markdown(f"""<div class="card"><p>{text[i]}</p></div>""",unsafe_allow_html=True)

@st.cache_data
def calculate_all(df):
    total_reviews = len(df)
    positive = len(df[df['Sentiment'] == 'Positive'])
    negative = len(df[df['Sentiment'] == 'Negative'])
    neutral = len(df[df['Sentiment'] == 'Neutral'])
    slight_positive = len(df[df['Sentiment'] == 'Slightly Positive'])
    slight_negative = len(df[df['Sentiment'] == 'Slightly Negative'])
    return total_reviews,positive,negative,neutral,slight_positive,slight_negative

def overview(df,title):
    total_reviews,positive,negative,neutral,slight_positive,slight_negative = calculate_all(df)
    if (positive+slight_positive) == 0:
        positive = 0
    else:
        positive = ((positive+slight_positive)*100)//total_reviews
    if (negative+slight_negative) == 0:
        negative = 0
    else:
        negative = ((negative+slight_negative)* 100)//total_reviews
    if neutral!=0:
        neutral = (neutral* 100)//total_reviews
    st.metric(title, f"{positive}% Positive", f"{neutral}% Neutral, {negative}% Negative")

@st.cache_data
def show_details(df):
    total_reviews,positive,negative,neutral,slight_positive,slight_negative = calculate_all(df)
    st.metric("Total reviews", total_reviews)
    st.metric("Positive", positive)
    st.metric("Negative", negative)
    st.metric("Neutral", neutral)
    st.metric("Slightly Positive", slight_positive)
    st.metric("Slightly Negative", slight_negative)

@st.cache_data
def calculate_main(df1,df2,df3,df4,df5):
    tr1,p1,n1,ne1,sp1,sn1 = calculate_all(df1)
    tr2,p2,n2,ne2,sp2,sn2 = calculate_all(df2)
    tr3,p3,n3,ne3,sp3,sn3 = calculate_all(df3)
    tr4,p4,n4,ne4,sp4,sn4 = calculate_all(df4)
    tr5,p5,n5,ne5,sp5,sn5 = calculate_all(df5)
    p = p1+p2+p3+p4+p5+sp1+sp2+sp3+sp4+sp5
    n = n1+n2+n3+n4+n5+sn1+sn2+sn3+sn4+sn5
    ne = ne1+ne2+ne3+ne4+ne5
    tr = tr1+tr2+tr3+tr4+tr5
    return tr,p,n,ne

def pie(df1,df2,df3,df4,df5):
    tr, p,n,ne = calculate_main(df1,df2,df3,df4,df5)
    values = [p,n,ne]
    fig = go.Figure(data=[go.Pie(
        labels=['Positive','Negative','Neutral'],
        values=values,
    )])
    fig.update_traces(marker=dict(line=dict(color='#000000', width=1.5)))
    st.plotly_chart(fig)

@st.cache_data
def overview_details(Infra_df,Academics_df,Placements_df, Campus_Life_df, Anything_Else_df,college_input):
    st.container(height=30,border=False)
    st.subheader(f"Overview of {college_input}")
    Infracol, Academiccol, Placementcol = st.columns(3)
    with Infracol:
        overview(Infra_df,"Infrastructure")
    with Academiccol:
        overview(Academics_df,"Academics")
    with Placementcol:
        overview(Placements_df,"Placements")
    piecol,extra, statementcol = st.columns([3,1,3])
    with piecol:
        pie(Infra_df,Academics_df,Placements_df, Campus_Life_df, Anything_Else_df)
    with statementcol:
        st.container(height=70,border=False)
        tr, pos, neg, neut = calculate_main(Infra_df,Academics_df,Placements_df, Campus_Life_df, Anything_Else_df)
        if pos!=0:
            overall_percentage = (pos*100)//tr
        else:
            overall_percentage = 0

        st.markdown(f'<div class="info">Overall Score : <div class="score">{overall_percentage}%</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="info">Overall Positive Reviews for {college_input} : {pos}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="info">Overall Negative Reviews for {college_input} : {neg}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="info">Overall Neutral Reviews for {college_input} : {neut}</div>', unsafe_allow_html=True)

if college_input:
    with st.spinner("Collecting Reviews... Please wait."):
        data = scraping.scrap(df[df["name"] == college_input].id.values[0])
    with st.spinner("Analysing Reviews..."):
        Infra_df, Academics_df, Placements_df, Campus_Life_df, Anything_Else_df = sentiment_analyses.sentiment(data)

    overview_details(Infra_df,Academics_df,Placements_df, Campus_Life_df, Anything_Else_df,college_input)
    
    st.subheader(f'Detailed Review Analysis of {college_input}')
    option = st.radio('',('Infrastructure', 'Academics', 'Placements', 'Campus Life', 'Anything Else'),index=0,label_visibility="hidden")


    col_df,col_detail = st.columns([9,1])
    val = Infra_df
    if option == 'Infrastructure':
        val = Infra_df
    elif option == 'Academics':
        val = Academics_df
    elif option == 'Placements':
        val = Placements_df
    elif option == 'Campus Life':
        val = Campus_Life_df
    elif option == 'Anything Else':
        val = Anything_Else_df

    with col_df:
        st.subheader(option)
        plot(val)
    with col_detail:
        show_details(val)

else:
    st.container(height=10,border=False)
    col_file1,x, col_file2,y, col_file3 = st.columns([2,1,2,1,2])
    with col_file1:
        file1 = load_url("https://lottie.host/1d726f97-65e4-4fd5-9522-177894a7a7d9/UoYEEb8rTY.json")
        st_lottie(file1)
        st.markdown('<div class="sub-heading">Search for your favourite Institutes</div>', unsafe_allow_html=True)
    with col_file2:
        st.container(height=50,border=False)
        file2 = load_url("https://lottie.host/cc73783f-90d3-4c13-bb49-6f5a71018e51/twr3psvf4x.json")
        st_lottie(file2)
        st.container(height=45,border=False)
        st.markdown('<div class="sub-heading">Anaylze what others say about the Institute</div>', unsafe_allow_html=True)
    with col_file3:
        file3 = load_url("https://lottie.host/9b3fdd1a-a026-4e72-9c6a-61e7d02f49ad/fdrAxdNkQS.json")
        st_lottie(file3)
        st.markdown('<div class="sub-heading">Select Best Institute for your career</div>', unsafe_allow_html=True)
    


st.markdown('<div style="text-align: center; margin-top: 50px; font-size: 0.9rem; color: #6c757d;">Powered by Streamlit | © 2024 College Reviewer</div>', unsafe_allow_html=True)
