# Dependencies
from flask import Flask, request, jsonify, json
import joblib
import traceback
import pandas as pd
import numpy as np

# Your API definition
app = Flask(__name__)

model = joblib.load("model.pkl")  # Load "model.pkl"
    
model_columns = joblib.load("model_columns.pkl")    # Load "model_columns.pkl"

@app.route('/', methods=['GET'])
def predict():
    if model:
        try:
            json_ = request.json

            print(json_)
            query = pd.get_dummies(pd.DataFrame(json_))

            query = query.reindex(columns=model_columns, fill_value=0)
            query = query.values.tolist()
            # print(query)
            prediction = list(model.predict(query))


            return jsonify({'prediction': str(prediction)})

        except:
            # return jsonify({'trace': json_})
            return jsonify({'trace': traceback.format_exc()})
    else:
        print('Train the model first')
        return ('No model here to use')


if __name__ == '__main__':
    app.run(port=5005, debug=True)
