import streamlit as st
import pickle
import pandas as pd

teams = [
    'Sunrisers Hyderabad','Mumbai Indians','Royal Challengers Bangalore',
    'Kolkata Knight Riders','Kings XI Punjab','Chennai Super Kings',
    'Rajasthan Royals','Delhi Capitals'
]

cities = [
    'Hyderabad','Bangalore','Mumbai','Indore','Kolkata','Delhi',
    'Chandigarh','Jaipur','Chennai','Cape Town','Port Elizabeth',
    'Durban','Centurion','East London','Johannesburg','Kimberley',
    'Bloemfontein','Ahmedabad','Cuttack','Nagpur','Dharamsala',
    'Visakhapatnam','Pune','Raipur','Ranchi','Abu Dhabi',
    'Sharjah','Mohali','Bengaluru'
]

pipe = pickle.load(open("pipe.pkl",'rb'))
st.title('IPL Win Predictor')

# --- Inputs ---
col1, col2 = st.columns(2)
with col1:
    batting_team = st.selectbox('Select the batting team', sorted(teams))
with col2:
    bowling_team = st.selectbox('Select the bowling team', sorted(teams))

selected_city = st.selectbox('Select host city', sorted(cities))
target = st.number_input('Target', min_value=1)

col3, col4, col5 = st.columns(3)
with col3:
    score = st.number_input('Score', min_value=0)
with col4:
    overs = st.number_input('Overs completed', min_value=0.0, step=0.1)
with col5:
    wickets_out = st.number_input('Wickets out', min_value=0, max_value=10)

# --- Prediction ---
if st.button('Predict Probability'):
    # feature engineering
    runs_left   = target - score
    balls_left  = 120 - (overs * 6)
    wickets_left = 10 - wickets_out
    # avoid division by zero
    crr = (score / overs) if overs > 0 else 0
    rrr = (runs_left * 6) / balls_left if balls_left > 0 else 0

    # build DataFrame with the exact column names the pipeline expects
    input_df = pd.DataFrame({
        'batting_team': [batting_team],
        'bowling_team': [bowling_team],
        'city': [selected_city],
        'runs_left': [runs_left],
        'balls_left': [balls_left],
        'wickets_left': [wickets_left],       # <-- key fix here
        'total_runs_x': [target],
        'crr': [crr],
        'rrr': [rrr]
    })

    # predict
    result = pipe.predict_proba(input_df)
    loss, win = result[0]

    st.header(f"{batting_team} - {round(win*100)}%")
    st.header(f"{bowling_team} - {round(loss*100)}%")


