import numpy as np
import pandas as pd
import pickle
from sklearn.ensemble import AdaBoostClassifier

df = pd.read_csv('model.csv')

x = df.drop('subscribed',axis = 1).values
y = df['subscribed'].values

#We are training our model with all availabe data.

abc = AdaBoostClassifier(n_estimators= 150, learning_rate= 1.0, algorithm= 'SAMME')

#Fitting model with trainig data
abc.fit(x, y)

# Saving model to disk
pickle.dump(abc, open('model.pkl','wb'))

# Loading model to compare the results
model = pickle.load(open('model.pkl','rb'))

# test
print(model.predict([[59.0,2,2343,1,0,1042.0,1.0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0]]))