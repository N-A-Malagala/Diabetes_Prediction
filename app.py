from flask import Flask, render_template, request
import pickle
from datetime import datetime

app = Flask(__name__)

def prediction(lst):
    filename = 'model/diabetes_predictor.pickle'
    with open(filename, 'rb') as file:
        model = pickle.load(file)
    pred_value = model.predict([lst])
    return pred_value

@app.route('/',methods=['POST', 'GET'])

def index():
  result = None
  if request.method == 'POST':
    dob = request.form['dob']
    hypertension = request.form['hypertension']
    heart_disease = request.form['heart_disease']
    weight = request.form['weight']
    height = request.form['height']
    HbA1c_level = request.form['HbA1c_level']
    blood_glucose_level = request.form['blood_glucose_level']

    dob_date = datetime.strptime(dob, "%Y-%m-%d")
    today = datetime.now()
    age = round((today - dob_date).days / 365.25, 1)  # Corrected age calculation

    height_m = float(height) / 100  # Convert height to meters
    bmi = round(float(weight) / (height_m ** 2), 1)

    feature_list = []
    feature_list.append(float(age))
    feature_list.append(int(hypertension))
    feature_list.append(int(heart_disease))
    feature_list.append(float(bmi)) 
    feature_list.append(float(HbA1c_level))
    feature_list.append(int(blood_glucose_level))
    
    pred = prediction(feature_list)
      
    if pred is not None:
      result = "Yes" if pred >= 0.5 else "No"
    
  return render_template("index.html", result=result)

if __name__ == '__main__':
    app.run(debug=True)