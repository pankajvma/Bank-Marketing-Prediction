import joblib
import numpy as np
import pandas as pd
import pickle
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline

df = pd.read_csv('notebook/bank/bank-additional-full.csv')

include = ['age', 'job', 'marital', 'education', 'default', 'housing', 'loan',
           'contact', 'pdays', 'previous', 'poutcome', 'emp.var.rate',
           'cons.price.idx', 'cons.conf.idx', 'euribor3m', 'nr.employed',
           'subscribed']

df = df[include]

# Data Preprocessing
def preprocess_data():
    df['pdays'] = (df.pdays != 999).astype('uint8')
    df['subscribed'] = (df.subscribed == 'yes').astype('uint8')
    categoricals = []
    for col, col_type in df.dtypes.iteritems():
        if col_type == 'O':
            categoricals.append(col)

    df_ohe = pd.get_dummies(df, columns=categoricals)



    dependent_variable = 'subscribed'
    x = df_ohe[df_ohe.columns.difference([dependent_variable])]
    y = df_ohe[dependent_variable]

    #Oversampling the train data
    from imblearn.over_sampling import RandomOverSampler, SMOTE

    os=RandomOverSampler()
    x,y=os.fit_resample(x,y)

    # Saving the data columns
    model_columns = list(x.columns)
    joblib.dump(model_columns, 'model_columns.pkl')
    print("Model columns dumped!")

    return [x, y]


def pipe_line(x, y):
    # Creating ML Pipeline
    pipeline_lr = Pipeline([('scaler', StandardScaler()),
                        ('pca', PCA(n_components = 10)),
                        ('lr', LogisticRegression(n_jobs=-1, C= 0.1, penalty= 'l2', solver= 'newton-cg'))])

    pipeline_lr.fit(x,  y)

    # Saving pipeline
    joblib.dump(pipeline_lr, 'model.pkl')
    print("Model dumped!")

def test_pipeline(x, y):

    # Load the saved model
    model = joblib.load('model.pkl')

    # test
    print(model.predict(x[y==1].tail(20)))


def launch():
    x, y = preprocess_data()
    pipe_line(x, y)
    test_pipeline(x, y)

launch()