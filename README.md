# Customer Churn Prediction

A web app that predicts customer churn risk and calculates customer lifetime value (CLV) using machine learning.

## What It Does

- **Churn Risk Prediction**: Identifies if a customer is likely to leave (High/Medium/Low risk)
- **Customer Lifetime Value**: Calculates expected revenue from each customer
- **Risk Analysis**: Shows key factors affecting churn (tenure, support calls, payment delays, etc.)
- **Interactive Dashboard**: Enter customer details and get instant predictions

## How It Works

1. Input customer information (tenure, support calls, spending, etc.)
2. ML model predicts churn risk
3. Shows risk level, CLV, and actionable recommendations
4. Flag high-risk customers for retention campaigns

## Tech Stack

- **Backend**: Flask
- **ML Model**: XGBoost (trained on historical data)
- **Data Processing**: Pandas, Scikit-learn
- **Frontend**: HTML/CSS/JavaScript

Check out: [LIVE DEMO](https://customer-churn-pred-5jep.onrender.com/)

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py

# Open http://localhost:5000
```

## Features

- Real-time churn predictions
- Customer risk scoring (High/Medium/Low)
- CLV calculation based on risk level
- Retention recommendations
- Session management (30-min timeout)

## Input Fields

- **Tenure**: Months as customer
- **Monthly Charges**: Amount paid per month
- **Total Spend**: Lifetime spending
- **Support Calls**: Number of support interactions
- **Payment Delays**: Days late on payments
- **Last Interaction**: Days since last contact

## Model Details

- Trained on historical customer data
- Uses feature encoding for categorical data
- Risk calculated using multiple factors
- CLV adjusted based on churn risk
