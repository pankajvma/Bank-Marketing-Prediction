import numpy as np
from flask import Flask, request, jsonify, render_template, json
import requests

app = Flask(__name__)
# model = pickle.load(open('model.pkl', 'rb'))

int_vars = ['age', 'pdays', 'previous']
float_vars = ['cons.conf.idx', 'cons.price.idx', 'emp.var.rate', 'euribor3m', 'nr.employed']

def get_data(data):

    education = data['education']

    education = education.replace(".", " ")

    education = education.replace("y", " Years")

    poutcome = data['poutcome']
    if poutcome == 'nonexistent': poutcome = 'Non-Existent' 

    pdays = data['pdays']
    pdays = 'Yes' if pdays else 'No'

    return [data['age'], data['job'], data['marital'], education, data['default'], 
            data['housing'], data['loan'], data['contact'], pdays, data['previous'], poutcome, 
            data['emp.var.rate'], data['cons.price.idx'], data['cons.conf.idx'], data['euribor3m'], data['nr.employed']]

@app.route('/')
def home():
    return render_template('index.html', title_text="Bank Marketing Prediction")

@app.route('/prediction_form')
def prediction_form():
    return render_template('predict.html', title_text="Get a Prediction")

@app.route('/predict',methods=['GET'])
def predict():
    json_ = [{x: y for x , y in request.args.items()}]

    for i in int_vars:
        json_[0][i] = int(json_[0][i])

    for i in float_vars:
        json_[0][i] = float(json_[0][i])

    # json_ = json.dumps(json_)

    data = json_[0]

    age, job, marital, education, default, housing, loan, contact, pdays, previous, poutcome, emp_var_rate, cons_price_idx, cons_conf_idx, euribor3m, nr_employed = get_data(data)
    

    # resp = requests.request('GET', 'http://127.0.0.1:5000/', json = json_)
    resp = requests.request('Post', 'https://bank-marketing-prediction.herokuapp.com/', json = json_)
    
    prediction = eval(resp.json()['prediction'])[0]

    output = 'is more likely to' if prediction == 1 else 'might not'

    return render_template('prediction.html', age_text = age, education_text = education.title(), previous_text = previous, 
                            housing_text = housing.title(), loan_text = loan.title(), default_text = default.title(), contact_text = contact.title(), 
                            pdays_text = pdays, poutcome_text = poutcome.title(), job_text = job.title(), marital_text = marital.title(),
                           emp_var_rate_text = emp_var_rate, cons_price_text = cons_price_idx, cons_conf_idx_text = cons_conf_idx, euribor3m_text = euribor3m, 
                           nr_employed_text = nr_employed, prediction_text= f'This customer {output} Subscribe to the Term Deposit.', title_text = "Prediction Report")


if __name__ == "__main__":
    app.run(debug=True, port=5010)