# Import the necessary packages
from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler

# Configuring the Flask environment and loading the pickle file
app = Flask(__name__)
model = pickle.load(open('Random_forest_regression_model.pkl', 'rb'))
@app.route('/', methods = ['GET'])
def Home():
    return render_template('index.html')

@app.route("/predict", methods = ['POST'])
def predict():
    Fuel_Type_Diesel = 0
    
    # Getting the form information
    if (request.method == "POST"):
        Year = int(request.form['Year'])
        Present_Price = float(request.form['Present_Price'])
        Kms_Driven = int(request.form['Kms_Driven'])
        Owner = int(request.form['Owner'])
        
        # Checking for fuel type information
        Fuel_Type_Petrol = request.form['Fuel_Type_Petrol']
        if (Fuel_Type_Petrol == "Petrol"):
            Fuel_Type_Petrol = 1
            Fuel_Type_Diesel = 0
        elif(Fuel_Type_Diesel == "Diesel"):
            Fuel_Type_Petrol = 1
            Fuel_Type_Diesel = 0
        else:
            Fuel_Type_Petrol = 0
            Fuel_Type_Diesel = 0
            
        # Converting the Year to Number of Years
        Year = 2021 - Year
        
        # Getting Seller Type information
        Seller_Type_Individual = request.form['Seller_Type_Individual']
        if (Seller_Type_Individual == "Individual"):
            Seller_Type_Individual = 1
        else:
            Seller_Type_Individual = 0
        
        # Transmission Type
        Transmission_Manual = request.form['Transmission_Manual']
        if (Transmission_Manual == "Manual"):
            Transmission_Manual = 1
        else:
            Transmission_Manual = 0
        
        # Predicting the price of the car with the given inputs
        Prediction = model.predict([[Present_Price, Kms_Driven, Owner, Year, Fuel_Type_Diesel, Fuel_Type_Petrol, Seller_Type_Individual, Transmission_Manual]])
        output = round(Prediction[0], 2)
        
        # Displaying the output dependino upon the predictions
        if (output < 0):
            return render_template('index.html', prediction_text = "Sorry you cannot sell this car.")
        else:
            return render_template('index.html', prediction_text = f"You can sell this car for Rs. {output} Lakhs.")
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(debug = True)
            
                                        