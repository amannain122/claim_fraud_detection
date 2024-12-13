# Insurance Claim Fraud Detection

This project is an **Insurance Claim Fraud Detection** model with two solutions:
1. **Intergrating Google Cloud Platform (GCP)**: Using Google Cloud's AutoML/Vertex AI and Google Cloud Storage to integrate with notebooks to train/deploy a model for fraud detection based on the provided features.
2. **One-Class SVM**: A traditional machine learning approach using One-Class Support Vector Machine (SVM) to detect fraudulent insurance claims.

Both solutions are encapsulated in a **Flask API** for making predictions, and the app is **Dockerized**, making it easy to deploy and run anywhere.

## Features
- **User Input**: The app takes various inputs such as:
  - Age
  - City Code (1to36)
  - Policy Duration
  - Health Indicator (Number of Diseases Diagnosed)
  - Insurance Type (Individual or Joint)
  - Spouse (Whether the user has a spouse)
  - Policy Type (1-4)
  - Accommodation Type (Owned or Rented)
  
- **Prediction**: The app predicts if the claim is fraudulent (Class -1) or not (Class 1).

## Project Setup

### Clone this repository
```bash
git clone https://github.com/amannain122/claim_fraud_detection
```

### Requirements

1. Python 3.10 or higher
2. Docker (for containerization)

### Dependencies
You can install the dependencies by running:

```bash
pip install -r requirements.txt
```
- google-cloud
- Flask
- scikit-learn
- pandas
- joblib
- numpy


### Run the app when in directory using
```bash
python app.py
```
### Docker Setup

1. Build the Image
```bash
docker build -t claim-fraud-prediction .
```
2. Run the Container
```bash
docker run -p 5000:5000 claim-fraud-prediction
```

## Usage
### You can send a POST request to http://127.0.0.1:5000/predict with the following JSON data:

```json
{
  "age": 30,
  "city_code": 3,
  "duration": 5,
  "health_indicator": 2,
  "insurance_type": 1,
  "spouse": 1,
  "policy_type": 2,
  "accommodation": 1
}
```
### Example using Curl:
```
curl -X POST http://127.0.0.1:5000/predict -H "Content-Type: application/json" -d "{\"age\": 30, \"city_code\": 3, \"duration\": 5, \"health_indicator\": 2, \"insurance_type\": 1, \"spouse\": 1, \"policy_type\": 2, \"accommodation\": 1}"
```
