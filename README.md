# Home-Loan-prediction

A bank's profit or a loss depends to a large extent on loans i.e. whether the customers are paying back the loan or defaulting. By predicting the loan defaulters, the bank can reduce its Non- Performing Assets. This makes the study of this phenomenon very important.

It is a classification problem where we have to predict whether a loan would be approved or not. 

We have considered 3 mains tools to accomplish this project
1. Streamlit(User Interface)

  Streamlit is used as user interface where the users can do a pre check of what could be their loan status if applied.
  
2. FastAPI(Backend)

  Considering the user input, we predict whether the user get approval for the loan or not using FastAPI as our backend.
  
3. PostgreSQL(Database)

  All the data that was given by the user whether it could be form data(for single sample) or file data(for predicting multiple samples) along with the prediction is stored in PostgreSQL database.

### Streamlit:
  #### single sample: 
          This part is mainly to take input from the user for different features such as: Gender(of the applicant), Married(marital status), Education(Graduate or not), Self_Employed, ApplicantIncome, CoApplicantIncome, LoanAmount, Loan_Amount_Term, Credit_History, Property_Area. This is a form that has to be submitted by the user to get the prediction.
  
  #### Multiple samples: 
           In this case, the user has to upload a csv file that contains multiple samples with different features to get the prediction of all the samples at a time. 
  
  #### Get past predictions: 
           This will display the past prediction along with the features from postgresql database.
  
### FastAPI:
    There are total of 3 endpoints here: a) single-prediction(prediction for one sample), b) multi-predictions(for multiple samples), c) all items(to return features from database).
    
    To start FastAPI: uvicorn main:app --reload
    
    Pre-processing and all the necessary quality checks have also been done in this stage.
    
    
### Machine learning model:
     For this classification problem we have used logistic regression to make predictions.
     
### PostgreSQL:
      This is used to stored the data.
      
### Airflow:
      For scheduling and monitoring the workflows.



