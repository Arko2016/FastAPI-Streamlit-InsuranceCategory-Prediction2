'''
Create Pydantic object to capture user input
'''

from pydantic import BaseModel, Field, computed_field, field_validator
from typing import Literal, Annotated
from config.city_tiers import tier_1_cities,tier_2_cities

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