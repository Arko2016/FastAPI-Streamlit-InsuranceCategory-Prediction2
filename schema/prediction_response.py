'''
Create Pydantic object to validate model output 
'''
from pydantic import BaseModel, Field
from typing import Dict

class PredictionResponse(BaseModel):
    #this will contain definitions for each of the model output components
    predicted_class : str = Field(

        ...,
        description = "this will capture the predicted class (High/Medium/Low)",
        example = "High"
    )

    confidence: float = Field(

        ...,
        description= "Model's confidence for the prediction class (range 0 to 1)",
        example = "0.60"

    )

    class_probabilities: Dict[str,float] = Field(

        ...,
        description="Probability distribution across all possible classes",
        example={"Low": 0.01, "Medium": 0.15, "High": 0.84}
    )