from flask import Flask, redirect, url_for, render_template, request, session, flash
import pandas as pd
import pickle
import os
from datetime import timedelta

port = int(os.environ.get('PORT', 5000))
app = Flask(__name__)
app.secret_key = os.urandom(24) 
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)  # Set session timeout duration

with open("pred_churn.pkl", "rb") as f:
    model = pickle.load(f)
with open("ohe_encoder.pkl", "rb") as f:
    ohe = pickle.load(f)

def calculate_risk_level(features):
    risk_score = 0
    if features['tenure'] < 12:
        risk_score += 2
    if features['support_calls'] > 5:
        risk_score += 2
    if features['payment_delay'] > 10:
        risk_score += 2
    if features['last_interaction'] > 30:
        risk_score += 1
    return "High" if risk_score >= 5 else "Medium" if risk_score >= 3 else "Low"

def calculate_clv(features):
    avg_monthly_revenue = features['total_spend'] / features['tenure'] if features['tenure'] > 0 else 0
    expected_lifetime = 12  # Assume 1 year as default
    
    if features['risk_level'] == "High":
        expected_lifetime = 6  # Shorter lifetime for high-risk customers
    elif features['risk_level'] == "Medium":
        expected_lifetime = 1
    elif features['risk_level'] == "Low":
        expected_lifetime = 24  # Longer lifetime for low-risk customers

    clv = avg_monthly_revenue * expected_lifetime
    return round(clv, 2)


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/predict", methods=['POST', 'GET'])
def predict():
    print("Route hit: /predict") # Add this line to confirm the route is hit
    if request.method == 'POST':
        session.permanent = True
        try:
            print("POST request received") # Confirm it's a POST request

            user_data = {
                'age': int(request.form['age']),
                'gender': request.form['gender'],
                'tenure': int(request.form['tenure']),
                'usage_frequency': int(request.form['usage_freq']),
                'support_calls': int(request.form['support_calls']),
                'payment_delay': int(request.form['pay_delay']),
                'subscription_type': request.form['sub_type'],
                'contract_length': request.form['con_len'],
                'total_spend': float(request.form['total_sp']),
                'last_interaction': int(request.form['last_int'])
            }

            user_df = pd.DataFrame([user_data])
            categorical_features = ['gender', 'subscription_type', 'contract_length']
            user_encoded = ohe.transform(user_df[categorical_features])
            user_df_encoded = pd.DataFrame(user_encoded, columns=ohe.get_feature_names_out(categorical_features))
            final_df = pd.concat([user_df.drop(categorical_features, axis=1).reset_index(drop=True), user_df_encoded.reset_index(drop=True)], axis=1)
            final_df = final_df.reindex(columns=model.feature_names_in_, fill_value=0)

            user_data['risk_level'] = calculate_risk_level(user_data)
            clv = calculate_clv(user_data)

            prediction = model.predict(final_df)[0]

            session['res'] = "Churned" if prediction == 1 else "Not Churned"
            session['risk_level'] = user_data['risk_level']
            session['clv'] = clv

            print(f"Session Data: {session['res']}, {session['risk_level']}, {session['clv']}")
            flash(f"Customer churn: {session['res']}, Risk Level: {session['risk_level']}, CLV: ${session['clv']:.2f}", "success")
            return redirect(url_for("result"))
        except Exception as e:
            print(f"Error: {str(e)}")  # Add this line to print the error message
            flash(f"Error: {str(e)}")
            return render_template('predict.html', error=str(e), form_data=request.form)
    else:
        return render_template('predict.html')


@app.route('/result')
def result():
    print("Route hit: /result")  # Confirm the route is hit
    res = session.get("res")
    rl = session.get("risk_level")
    clv = session.get("clv")
    print(f"Session data: res={res}, risk_level={rl}, clv={clv}")  # Print session data to debug

    if res is None or rl is None or clv is None:
        flash("Error: No result data found. Please try submitting the form again.", "danger")
        return redirect(url_for("predict"))
    return render_template('result.html', res=res, risk_level=rl, clv=clv)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=port)
