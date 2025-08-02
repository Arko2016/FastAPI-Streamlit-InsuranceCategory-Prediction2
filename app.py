import pandas as pd
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from schema.user_input import user_input
from model.predict import model,MODEL_VERSION,predict_output
from schema.prediction_response import PredictionResponse

#create FastAPI object
app = FastAPI()

#define api endpoint for home page
@app.get('/')
def home():
    return {'message':'Insurance Premium Category home page'}

#add api endpoint for Health check -> recommended while utilizing cloud platforms like AWS for launching the app
#when we use the AWS services, like Elastic Search, it will first hit the '/health' endpoint and will only proceed if status is OK for health api endpoint
@app.get('/health')
def health_check():
    return {
        'status':'OK'
        ,'version': MODEL_VERSION #obtained from predict.py
        ,'model_loaded': model is not None #will load true if model pickle object was loaded properly 
    } 

#define api endpoint to generate production based on user input -> POST request
@app.post('/predict', response_model = PredictionResponse) #the prediction response ensures that prediction is generated, it is first validated using pydantic model from prediction response and then returned to JSON response
def predict_premium(data: user_input):

    #convert the pydantic model object to dataframe for inputing to model object
    input_df = {
        'bmi': data.bmi,
        'age_group': data.age_group,
        'lifestyle_risk': data.lifestyle_risk,
        'city_tier': data.city_tier,
        'income_lpa': data.income_lpa,
        'occupation': data.occupation
    }

    try:
        #generate prediction using the predict output function in predict.py
        prediction = predict_output(input_df)

        #return json response for successful prediction
        return JSONResponse(status_code=200, content={'response': prediction})
    except Exception as e:
        #capture error message during prediction
        return JSONResponse(status_code=500, content=str(e))
