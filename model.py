import numpy as np
import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier

df = pd.read_csv('model.csv')

x = df.drop('subscribed',axis = 1).values
y = df['subscribed'].values

#We are training our model with all availabe data.

rfc = RandomForestClassifier(n_estimators = 10)

#Fitting model with trainig data
rfc.fit(x, y)

# Saving model to disk
pickle.dump(rfc, open('model.pkl','wb'))

# Loading model to compare the results
model = pickle.load(open('model.pkl','rb'))

# test
print(model.predict([[59.0,2,2343,1,0,1042.0,1.0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0]]))