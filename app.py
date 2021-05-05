import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

def get_full_data(form_input):
    # form_input = [23, 1, 15, 125, 5, 1, 0, 0, 0]

    add_data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    add_data[form_input[8]] = 1
    add_data[form_input[9] + 11] = 1

    model_input = form_input[: 8]
    model_input.extend(add_data)

    return model_input

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    int_features = [int(x) for x in request.form.values()]

    print(int_features) 

    all_int_features = get_full_data(int_features)

    print(all_int_features) 

    final_features = [np.array(all_int_features)]
    prediction = model.predict(final_features)

    edu = ['Primary', 'Secondary', 'Tertiary']
    house = ['No', 'Yes']
    loan = ['No', 'Yes']
    job = ['admin', 'blue-collar', 'entrepreneur', 'housemaid', 'management', 
            'retired', 'self-employed', 'services', 'student', 'technician', 'unemployed']

    marital = ['Divorced', 'Married', 'Single']

    age, edu_ind, bal, house_ind, loan_ind, dur, co_count, days_passed, job_ind, marital_ind = int_features

    edu = edu[edu_ind]
    house = house[house_ind]
    loan = loan[loan_ind]
    job = job[job_ind]
    marital = marital[marital_ind]

    output = 'is more likely to' if prediction == 1 else 'might not'

    return render_template('index.html', age_text = age, education_text = edu, balance_text = bal, 
                            housing_text = house, loan_text = loan, duration_text = dur, contacted_text = co_count, 
                            days_passed_text = days_passed, job_text = job, marital_text = marital,
                            prediction_text= f'This customer {output} Subscribe to the Term Deposit.',
                            display_none = "none")


if __name__ == "__main__":
    app.run(debug=True)