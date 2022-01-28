import streamlit as st
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from plotly import graph_objs as go 
from sklearn.linear_model import LinearRegression


# Title of the App

st.title ('Salary Predictor')
st.image ('data//sal.jpg')

# Importing Data

data = pd.read_csv('data//Salary_data.csv')

# Navigation bar

navigation_bar = st.sidebar.radio('Navigation', ['Home', 'Predictions', 'Contribute'])

# Working through Navigation 
# first Step if visitor selects Home.

if navigation_bar == 'Home':

# We are going to give two options 
# 1. Want to see the salary table 
# 2. Show Graphs
#    In graphs it will show two more options 
#    a) Interactive graph
#    b) Non-Interactive graph

# For option 1 showing table

    if st.checkbox('Show Table', value = False):
        st.write(data)
        
# for option two we have graph of two types
    
    graph = st.selectbox ('What kind of Graph?', ['None','Non-Interactive', 'Interactive'] , index = 0 )
    val = st.slider ('Filter data using Years of Experience', 0,20)                   
    data = data.loc[data['YearsExperience']>= val] # I didnt understand right now why he did it 
    
    # Now for Option 1 in graph i.e Non-Interactive
    
    if graph == 'Non-Interactive':
        fig, ax = plt.subplots(figsize = (10, 5))
        ax.scatter(data['YearsExperience'], data['Salary'])
        plt.ylim(0)
        plt.xlabel('Years Of Experience')
        plt.ylabel('Salray')
        plt.tight_layout()
        st.pyplot(fig)
    
    # If Option two selected i.e Interactive
    
    if graph == 'Interactive':
    
        layout = go.Layout(
            xaxis = dict(range = [0, 18]), 
            yaxis = dict(range = [0, 240000])
        )
        fig = go.Figure(data = go.Scatter(x=data["YearsExperience"], y=data["Salary"], mode = 'markers'), layout = layout)
        st.plotly_chart(fig)

# Getting Data ready and fitting Linear Rigression on Data if Prediction is selected in Navigation Bar

X = np.array(data['YearsExperience'])
X = X.reshape(-1, 1)
y = np.array(data['Salary'])
model_LR = LinearRegression()
model_LR.fit(X, y)

# if Prediction is selected in Navigation Bar

if navigation_bar == 'Predictions':
    st.header ('Know Your Salary')
    val = st.number_input('Enter your Exprerience', 0.00, 20.00, step = 0.25)
    val = np.array(val).reshape(-1,1)
    preds = model_LR.predict(val)[0]
    
    if st.button('Predict'):
        st.success(f'Your Predicted Salary is {round(preds)}')
        
# If Contribute is selected in the Navigation bar

if navigation_bar == 'Contribute':
    st.header('Contribure to our Dataset')
    experience = st.number_input('Enter your Years of Experience', 0.00, 20.0, step = 0.5)
    Salary = st.number_input('Enter your salary', 0, 1000000, step = 10000)
    if st.button('Submit'):
        to_add = {"YearsExperience":[experience], "Salary": [Salary]}
        to_add = pd.DataFrame(to_add)
        to_add.to_csv('data//Salary_Data.csv', mode = 'a' , header = False, index = False)
        st.success('Submitted')
