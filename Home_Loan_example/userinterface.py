
import json
import warnings

import pandas as pd

import requests
import streamlit as st
from PIL import Image

warnings.filterwarnings('ignore')

st.markdown("<h1 style='text-align: center; color: Green;'>Home Loan Prediction</h1>", unsafe_allow_html=True)
image = Image.open('Home_loan.png')
st.image(image, caption='Home Loan Prediction', width=1000)
st.subheader("Worried about your home loan application and want to know your results right now?")

st.subheader("Not anymore, you can directly check your application status now..")
st.subheader("Wondering how? Do check below for more details")

st.write("If you want to know the prediction of single sample, kindly fill the below form")



Gender = st.radio(
    "Select Gender",
    ('Male', 'Female'))

if Gender == 'Male':
    Gender = 0
else:
    Gender = 1


st.write('Select yes if married, else skip this step')
#Gender = st.selectbox('select Gender', (0, 1))
Married = st.checkbox('Yes')

if Married:
    Married = 1
else:
    Married = 0
#Married = st.selectbox('select Marital status', (1, 0))


Education = st.radio(
    "If the education level is equal to or above batchelors, select Batchelors",
    ('Graduate', 'Not Graduate'))

if Education == 'Not Graduate':
    Education = 0
else:
    Education = 1

#Education = st.selectbox('select Education level', (1, 0))
#Self_Employed = st.selectbox('select Employment status', (1, 0))
Self_Employed = st.radio(
    "Select appropriate option whether self employed or not",
    ('Yes', 'No'))

if Self_Employed == 'Yes':
    Self_Employed = 0
else:
    Self_Employed = 1


ApplicantIncome = (st.number_input(label = "ApplicantIncome"))
CoApplicantIncome = (st.number_input(label = "CoApplicantIncome"))
LoanAmount = (st.number_input(label = "LoanAmount"))
Loan_Amount_Term = (st.number_input(label = "Loan_Amount_Term "))
Credit_History = st.selectbox('select credit history', (0, 1))

Property_Area = st.radio(
    "Select property are where Rural:0, Urban:1, Semi-Urban:2",
    ('Rural', 'Urban', 'Semi-Urban'))

if Property_Area == 'Rural':
    Property_Area = 0
elif Property_Area == 'Urban':
    Property_Area = 1
else:
    Property_Area = 2

inputs = {"Gender" : Gender, "Married" : Married, "Education": Education, "Self_Employed" : Self_Employed,
          "ApplicantIncome" : (ApplicantIncome), "CoApplicantIncome" :(CoApplicantIncome), "LoanAmount" :(LoanAmount), "Loan_Amount_Term": (Loan_Amount_Term),
          "Credit_History" :(Credit_History), "Property_Area": Property_Area}

st.write(inputs)

st.write("please click the single-prediction button below")

if st.button('single-prediction'):
    response = requests.post('http://127.0.0.1:8000/single-prediction', json = (inputs))
    Loan_status = (response.json())
    st.write('Loan Status is  : ', Loan_status)


file_upl = st.file_uploader("select you file here:")
if st.button('multi-predictions'):
    df = pd.read_csv(file_upl)
    df = df.dropna()
    dataframe_input = st.dataframe(df)
    response = requests.post('http://127.0.0.1:8000/multi-predictions',  data = json.dumps(df.to_dict()))
    st.write(response.json())

if st.button('all items'):
    response2 = requests.get('http://127.0.0.1:8000/items')

    st.write(response2.text)
