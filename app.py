import streamlit as st
import pickle
import pandas as pd

teams = ['Chennai Super Kings',
 'Delhi Capitals',
 'Gujarat Titans',
 'Punjab Kings',
 'Kolkata Knight Riders',
 'Lucknow Super Giants',
 'Mumbai Indians',
 'Rajasthan Royals',
 'Royal Challengers Bangalore',
 'Sunrisers Hyderabad']

Cities = ['Bangalore', 'Delhi', 'Kolkata', 'Mumbai', 'Hyderabad', 'Chennai',
       'Jaipur', 'Ahmedabad', 'Cuttack', 'Nagpur', 'Visakhapatnam', 'Pune',
       'Raipur', 'Ranchi', 'Abu Dhabi',  'Dubai', 'Navi Mumbai', 'Lucknow', 'Guwahati']


try:
    with open('pipe.pkl', 'rb') as file:
        pipe = pickle.load(file)
except FileNotFoundError:
    print("File not found. Check the file path.")
except Exception as e:
    print("Error loading pickled file:", e)



st.title('IPL WIN PREDICTOR')

col1, col2 = st.columns(2)

with col1:
    batting_team = st.selectbox('Select the Batting Team', teams )



with col2:
        bowling_team_options = [team for team in teams if team != batting_team]
        bowling_team = st.selectbox('Select the Bowling Team', bowling_team_options)



selected_city = st.selectbox('Select the Host city', sorted(Cities))

target = st.number_input('Target')


col3, col4, col5 = st.columns(3)

with col3:
    score = st.number_input('Score')
with col4:
    overs = st.number_input('Overs Completed')
with col5:
    wickets = st.number_input('Wickets out')

if st.button('Predict Probability'):
    runs_left = target - score
    balls_left = 120 - (overs*6)
    wickets = 10 - wickets
    crr = score/overs
    rrr = (runs_left*6)/ balls_left

    input_df = pd.DataFrame({'batting_team': [batting_team], 'bowling_team': [bowling_team],
                            'city':[selected_city], 'runs_left':[runs_left], 'balls_left': [balls_left],
                            'wickets': [wickets], 'total_runs_x': [target], 'crr': [crr], 'rrr': [rrr]})

    result = pipe.predict_proba(input_df)
    loss = result[0][0]
    win = result[0][1]
    st.header(batting_team + " - " + str(round(win * 100))+ "%" )
    st.header(bowling_team + " - " + str(round(loss * 100))+ "%" )
