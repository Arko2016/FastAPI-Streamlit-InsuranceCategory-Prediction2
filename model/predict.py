import pandas as pd
import pickle

#import the model pickle created in mlmodel.py
with open('./model/model.pkl','rb') as f:
    model = pickle.load(f)

#get output class labels from model
class_labels = model.classes_.tolist()

#a temporary model version is entered manually, to be designed later using MLFlow
MODEL_VERSION = '1.0.0'

#define function to predict output based on user input
def predict_output(user_input:dict):
    #convert the dictionary to pandas dataframe
    #note: we will first need to convert the user input to a list and then to dataframe to avoid error
    input_df = pd.DataFrame([user_input])
    
    #predict output class
    predicted_class = model.predict(input_df)[0]
    
    #get probabilities for all classes (in this case: High/Medium/Low)
    probabilities = model.predict_proba(input_df)[0]
    confidence = max(probabilities)

    #create mapping: class labels -> probabilities
    class_probs = dict(zip(class_labels, map(lambda p:round(p,4), probabilities)))

    #return all model outputs captured above
    return {
        'predicted_class':predicted_class
        ,'confidence': round(confidence,4)
        ,'class_probabilities':class_probs
    }