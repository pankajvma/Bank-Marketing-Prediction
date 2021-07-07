import joblib
import numpy as np
import pandas as pd
import pickle
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier

df = pd.read_csv('notebook/bank/bank-additional-full.csv')

include = ['age', 'job', 'marital', 'education', 'default', 'housing', 'loan',
           'contact', 'pdays', 'previous', 'poutcome', 'emp.var.rate',
           'cons.price.idx', 'cons.conf.idx', 'euribor3m', 'nr.employed',
           'subscribed']

df = df[include]

# Data Preprocessing
df['pdays'] = (df.pdays != 999).astype('uint8')
df['subscribed'] = (df.subscribed == 'yes').astype('uint8')
categoricals = []
for col, col_type in df.dtypes.iteritems():
    if col_type == 'O':
        categoricals.append(col)

df_ohe = pd.get_dummies(df, columns=categoricals)

df_ohe.to_csv('model.csv', index=False)
df.to_json('model.json', orient='table', index=False)


dependent_variable = 'subscribed'
x = df_ohe[df_ohe.columns.difference([dependent_variable])]
y = df_ohe[dependent_variable]

#Oversampling the train data
from imblearn.over_sampling import RandomOverSampler, SMOTE

os=RandomOverSampler()
x,y=os.fit_resample(x,y)


abc = RandomForestClassifier(n_estimators=10)

abc.fit(x, y)

# Save your model
joblib.dump(abc, 'model.pkl')
print("Model dumped!")

# Load the model that you just saved
model = joblib.load('model.pkl')

# Saving the data columns from training
model_columns = list(x.columns)
joblib.dump(model_columns, 'model_columns.pkl')
print("Models columns dumped!")

# test
print(abc.predict(x[y==0].tail(20)))