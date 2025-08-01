import pandas as pd
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field, field_validator
from typing import Literal, Annotated
import pickle

#import the model pickle created in mlmodel.py
with open('./model/model.pkl','rb') as f:
    model = pickle.load(f)

#create FastAPI object
app = FastAPI()

#specify tiering for cities
tier_1_cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune"]
tier_2_cities = [
    "Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi", "Visakhapatnam", "Coimbatore",
    "Bhopal", "Nagpur", "Vadodara", "Surat", "Rajkot", "Jodhpur", "Raipur", "Amritsar", "Varanasi",
    "Agra", "Dehradun", "Mysore", "Jabalpur", "Guwahati", "Thiruvananthapuram", "Ludhiana", "Nashik",
    "Allahabad", "Udaipur", "Aurangabad", "Hubli", "Belgaum", "Salem", "Vijayawada", "Tiruchirappalli",
    "Bhavnagar", "Gwalior", "Dhanbad", "Bareilly", "Aligarh", "Gaya", "Kozhikode", "Warangal",
    "Kolhapur", "Bilaspur", "Jalandhar", "Noida", "Guntur", "Asansol", "Siliguri"
]

#create Pydantic model to validate incoming data from user
class user_input(BaseModel):
    age: Annotated[int, Field(...,gt = 0, lt = 120, description='age of patinet')]
    weight: Annotated[float, Field(..., gt = 0, description='Weight of patient in kg')]
    height: Annotated[float, Field(..., gt = 0 , description='height of patient in meters')]
    income_lpa: Annotated[float, Field(...,gt = 0, description='income of the patient in lakhs per annum')]
    smoker: Annotated[bool, Field(...,description='Is user a smoker (True/False)')]
    city: Annotated[str, Field(..., description='city where patient resides')]
    occupation: Annotated[Literal['retired', 'freelancer','student', 'government_job','business_owner', 'unemployed', 'private_job'], Field(...,description='occupation of patient')]


    #calculate bmi
    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight/(self.height ** 2),2)
    
    #calculate life risk
    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        if self.smoker and self.bmi > 30:
            return 'high'
        elif self.smoker and self.bmi > 27:
            return 'medium'
        else:
            return 'low'
    
    #define age bucket
    @computed_field
    @property
    def age_group(self) -> str:
        if self.age < 25:
            return 'young'
        elif self.age < 40:
            return 'adult'
        elif self.age < 65:
            return 'middle-aged'
        else:
            return 'senior'
    
    #convert city to Title case (first alphabet should be capital)
    #helps to capture cases when the city string is standardized to be be correctly mapped to city tiers
    @field_validator('city')
    @classmethod
    def normalize_city(cls, v: str) -> str:
        v = v.strip().title() #remove any white spaces and convert to Title case
        return v

    #define city tiers
    @computed_field
    @property
    def city_tier(self) -> str:
        if self.city in tier_1_cities:
            return 'tier1'
        elif self.city in tier_2_cities:
            return 'tier2'
        else:
            return 'tier3'

#define api path for home page
@app.get('/')
def home():
    return {'message':'Insurance Premium Category home page'}

#define api path to generate production based on user input -> POST request
@app.post('/predict')
def predict_premium(data: user_input):

    #convert the pydantic model object to dataframe for inputing to model object
    input_df = pd.DataFrame([{
        'bmi': data.bmi,
        'age_group': data.age_group,
        'lifestyle_risk': data.lifestyle_risk,
        'city_tier': data.city_tier,
        'income_lpa': data.income_lpa,
        'occupation': data.occupation
    }])

    #generate prediction
    prediction = model.predict(input_df)[0]

    #return json response for successful prediction
    return JSONResponse(status_code=200, content={'predicted_category': prediction})
