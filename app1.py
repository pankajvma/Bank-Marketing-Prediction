import numpy as np
from flask import Flask, request, jsonify, render_template, json, send_from_directory, current_app, send_file, Response, make_response
import requests, os, io, csv

app = Flask(__name__)

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

@app.route('/prediction_multiple')
def prediction_multiple():
    return render_template('predict_multiple.html', title_text="Get a Prediction")

@app.route('/predict',methods=['GET'])
def predict():
    json_ = [{x: y for x , y in request.args.items()}]

    for i in int_vars:
        json_[0][i] = int(json_[0][i])

    for i in float_vars:
        json_[0][i] = float(json_[0][i])


    data = json_[0]

    age, job, marital, education, default, housing, loan, contact, pdays, previous, poutcome, emp_var_rate, cons_price_idx, cons_conf_idx, euribor3m, nr_employed = get_data(data)


    # resp = requests.request('GET', 'http://127.0.0.1:5000/', json = json_)
    resp = requests.request('GET', 'https://bank-marketing-prediction.herokuapp.com/', json = json_)
    
    prediction = eval(resp.json()['prediction'])[0]

    output = 'is more likely to' if prediction == 1 else 'might not'

    return render_template('prediction.html', age_text = age, education_text = education.title(), previous_text = previous, 
                            housing_text = housing.title(), loan_text = loan.title(), default_text = default.title(), contact_text = contact.title(), 
                            pdays_text = pdays, poutcome_text = poutcome.title(), job_text = job.title(), marital_text = marital.title(),
                           emp_var_rate_text = emp_var_rate, cons_price_text = cons_price_idx, cons_conf_idx_text = cons_conf_idx, euribor3m_text = euribor3m, 
                           nr_employed_text = nr_employed, prediction_text= f'This customer {output} Subscribe to the Term Deposit.', title_text = "Prediction Report")


@app.route("/get_csv")
def get_csv():
    csv = 'age,job,marital,education,default,housing,loan,contact,pdays,previous,poutcome,emp.var.rate,cons.price.idx,cons.conf.idx,euribor3m,nr.employed'
    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=predict.csv"})

@app.route("/get_readme")
def get_readme():
    csv = 'Columns description for csv-\n\n\
          age: Age of the Customer\n\
          job: Customer\'s Profession (housemaid, services, admin., blue-collar, technician,retired, management, unemployed, self-employed, unknown,entrepreneur, student)\n\
          marital: Marital status (married, single, divorced, unknown) \n\
          education: Customers education (basic.4y, high.school, basic.6y, basic.9y, professional.course, unknown, university.degree, illiterate) \n\
          default: Does the customer have a credit (yes, no, unknown) \n\
          housing: Has the customer taken any personal loan (yes, no, unknown) \n\
          loan: Has the customer taken any personal loan (yes, no, unknown)\n\
          contact: Medium of contact (telephone, cellular)\n\
          pdays: if the customer was contacted in any earlier campaign (0 if No else 1)\n\
          previous:  Number of Contacts before this campaign \n\
          poutcome: Outcome of previous contacts (nonexistent, failure, success)\n\
          emp.var.rate: Employment variation rate \n\
          cons.price.idx: Consumer price index\n\
          cons.conf.idx: Consumer connfidence index\n\
          euribor3m: Euribor3m\n\
          nr.employed: Number of employees\n\n\
After filling the file please upload it and wait till the predictions are generated.\n\n\
The predictions file contains only one column by name "Predictions", it contains the predictions in the form of 0 and 1.\n\
Here 1 denotes a potential subscriber and 0 is Non-Subscriber.'
    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=ReadMe.txt"})

@app.route('/transform', methods=["POST"])
def transform_view():
    f = request.files['data_file']
    # create a list
    data = []
    if not f:
        return "No file"

    stream = io.StringIO(f.stream.read().decode("UTF8"), newline=None)

    csv_input = csv.DictReader(stream)

    for row in csv_input:
        data.append(row)
            
    for dt in data:
        for i in int_vars:
            dt[i] = int(dt[i])

        for i in float_vars:
            dt[i] = float(dt[i])


    # resp = requests.request('GET', 'http://127.0.0.1:5005/', json = data)
    resp = requests.request('GET', 'https://bank-marketing-prediction.herokuapp.com/', json = data)
    prediction = eval(resp.json()['prediction'])

    print(prediction)

    final_prediction = "Prediction"

    for p in prediction:
        final_prediction += f'\n{p}'

    response = make_response(final_prediction)
    response.headers["Content-Disposition"] = "attachment; filename=result.csv"

    return response

if __name__ == "__main__":
    app.run(debug=True, port=5000)
