import numpy as np
from flask import Flask, request, jsonify
import joblib
import os  

app = Flask(__name__)

# Check if the app is running inside a Docker container
if os.path.exists('/app/models'):
    # If inside Docker, use the Docker container path
    model_path = '/app/models/'
else:
    # If running locally, use the local path
    model_path = './models/'

# Load the models
model = joblib.load(os.path.join(model_path, 'best_model.pkl'))  # One Class SVM


def calculate_premium(age):
    """
    Calculate the premium based on the user's age.
    Modify this function if you have a specific formula.
    """
    if age < 20:
        raise ValueError("Age cannot be below 20.")
    premium = 1000 + (age - 20) * 100  # Example premium calculation
    return premium

def process_input_data(age, city_code, duration, health_indicator, insurance_type, spouse, policy_type, accommodation):
    """
    Process input data into the format expected by the model.
    """
    # Process city code (one-hot encoding) excluding city_code 1 (as it is not used by the model)
    city_codes = [0] * 35  # 35 cities, excluding C1
    city_codes[city_code - 2] = 1 if city_code != 1 else 0  # Adjust for index shift

    # Process age group
    age_group = (age - 20) // 10 + 1  # Dividing into age groups of 10 years starting from 20
    
    # Calculate premium
    premium = calculate_premium(age)
    
    # Map inputs to a feature vector
    features = [
        *city_codes,        # City Codes (35 values instead of 36)
        age_group,          # Age Group
        duration,           # Policy Duration
        health_indicator,   # Health Indicator
        insurance_type,     # Insurance Type (0 or 1)
        spouse,             # Spouse (0 or 1)
        policy_type,        # Policy Type (1, 2, 3, 4)
        accommodation,      # Accommodation Type (0 or 1)
        premium             # Premium (calculated based on age)
    ]
    
    return np.array(features).astype(int).reshape(1, -1)  # Ensure all values are standard Python int

@app.route('/predict', methods=['POST'])
def predict():
    """
    API endpoint that receives input data, processes it, and returns a prediction.
    """
    try:
        # Get the JSON data from the request
        data = request.get_json()

        # Extract values from the request data
        age = data.get('age')
        city_code = data.get('city_code')
        duration = data.get('duration')
        health_indicator = data.get('health_indicator')
        insurance_type = data.get('insurance_type')
        spouse = data.get('spouse')
        policy_type = data.get('policy_type')
        accommodation = data.get('accommodation')

        # Process the input data
        input_data = process_input_data(age, city_code, duration, health_indicator, insurance_type, spouse, policy_type, accommodation)
        
        # Make the prediction
        prediction = model.predict(input_data)
        
        # Return the prediction as a JSON response (convert prediction to int)
        return jsonify({'prediction': int(prediction[0])})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True)
