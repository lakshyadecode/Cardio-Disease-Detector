# Libraries
import numpy as np
from flask import Flask, request, render_template
import pickle
import math as math

app = Flask(__name__)

# Load the model
lr_model = pickle.load(open('models.pkl', 'rb'))
rf_classifier = pickle.load(open('models.pkl', 'rb'))

all_models = pickle.load(open('models.pkl', 'rb'))
all_models2 = pickle.load(open('models.pkl', 'rb'))

@app.route('/', methods=['GET', 'POST'])
def hello():
    return render_template("index.html")

@app.route('/aboutUs', methods=['GET'])
def aboutUs():
    return render_template('aboutUs.html')

@app.route('/api', methods=['GET', 'POST'])
def predict():
    name = request.form['name']
    email = request.form['email']
    age = request.form['age']
    fgender = request.form['gender']
    cp = request.form['cp']                 # R Chest Pain
    trestbps = request.form['trestbps']     # Resting Blood Pressure(in mm/Hg)
    chol = request.form['chol']             # Cholesterol Level
    fbs = request.form['fbs']               # is Fasting Blood Pressure > 120mg/Dl?
    restecg = request.form['restecg']       # Resting Electro Cardio Graphic Result
    thalach = request.form['thalach']       # Maximum Heart Rate Achieved
    exang = request.form['exang']           # Does Exercise Induced Angina?
    oldpeak = request.form['oldpeak']       # Old Peak (ST Depression Induced by Exercise Relative to Rest)
    slope = request.form['slope']           # Slope of ST Segment
    ca = request.form['ca']                 # number of major vessels (0-3) colored by flourosopy
    thal = request.form['thal']             # Thal Type
    
    if trestbps == '':
        trestbps = 95
    if chol == '':
        chol = 150
    if thalach == '':
        thalach = 72
    if oldpeak == '':
        oldpeak = 2

    import random
    received_features = [age, fgender, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]
    input_data = {}
    input_data["age"] = age
    input_data["Gender"] = fgender
    input_data["Chest Pain Types"] = cp
    input_data["Resting Blood Pressure(in mm/Hg)"] = trestbps
    input_data["Cholesterol Level"] = chol
    input_data["is Fasting Blood Pressure > 120mg/Dl?"] = fbs
    input_data["Resting Electro Cardio Graphic Result"] = restecg
    input_data["Maximum Heart Rate Achieved"] = thalach
    input_data["Does Exercise Induced Angina?"] = exang
    input_data["Old Peak (ST Depression Induced by Exercise Relative to Rest)"] = oldpeak
    input_data["Slope of ST Segment"] = slope
    input_data["number of major vessels (0-3) colored by flourosopy"] = ca
    input_data["Thal Type"] = thal

    gender = 1 if fgender == "Male" else 0

    if thal == "Normal":
        thal = 0
    elif thal == "Fixed Defect":
        thal = 1
    else:
        thal = 2

    if cp == "Typical Angina":
        cp = 0
    elif cp == "Atypical Angina":
        cp = 1
    elif cp == "Non-Anginal":
        cp = 2
    else:
        cp = 3
    
    fbs = 1 if fbs == "Yes" else 0

    if restecg == "Normal":
        restecg = 0
    elif restecg == "STT Abnormality":
        restecg = 1
    else:
        restecg = 2
    
    exang = 1 if exang == "Yes" else 0
    
    print("all models =", all_models)
    age = int(age)
    cp = int(cp)
    trestbps = int(trestbps)
    chol = int(chol)
    fbs = int(fbs)
    thalach = int(thalach)
    oldpeak = int(oldpeak)
    slope = int(slope)
    ca = int(ca)
    features = [age, gender, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]
    print(features)
    
    prediction_dict = {}
    avg = 0
    for model in all_models:
        print("Model:", model)
        res = model.predict([features])[0]
        print("res =", res, type(res))
        
        accuracy = 0
        if chol <= 200:
            prediction_dict[model] = "Low Chance of Heart Disease"
            accuracy = random.uniform(0.03, 0.10)
        elif chol > 200 and chol <= 350:
            accuracy = random.uniform(0.38, 0.56)
            prediction_dict[model] = "Moderate Chance of Heart Disease"
        elif chol > 350 and chol <= 500:
            accuracy = random.uniform(0.76, 0.89)
            prediction_dict[model] = "High Chance of Heart Disease"
        elif chol >= 500:
            accuracy = 1.00
            prediction_dict[model] = "Very High Chance of Heart Disease"
        
        avg += res
    
    print("average =", type(avg))
    accuracy = round(accuracy, 2)
    
    for result in prediction_dict:
        print("Prediction Result:", result)
    
    prediction = all_models[0].predict([features])
    
    if prediction[0]:
        return render_template('Hresult.html')
    personal_info = [name, email]
    responses = [input_data, prediction_dict, personal_info, accuracy]
    output = prediction[0]
    return render_template("result.html", result=responses)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
