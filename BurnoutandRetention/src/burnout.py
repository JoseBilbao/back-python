import pandas as pd
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# get data
url = "./BurnoutandRetention/data/data.csv"
burnout = pd.read_csv(url)

X = burnout.drop(['Id','Disengagement','Exhaustion','Burnout index','Recieved','Hierarchical Level'], axis='columns')
y = burnout[['Burnout index']]

# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

regressor = LinearRegression()
regressor.fit(X,y)  

def predict_index(data):
    data = pd.DataFrame(data)
    y_pred = regressor.predict(data)
    return y_pred[0];


X_dis = burnout.drop(['Id','Disengagement','Exhaustion','Burnout index','Recieved','Reciprocity','Ratio','Hierarchical Level'], axis='columns')
y_dis = burnout[['Disengagement']]

regressor_dis = LinearRegression()
regressor_dis.fit(X_dis,y_dis)  

def predict_dis(data):
    data = pd.DataFrame(data)
    y_pred = regressor_dis.predict(data)
    return y_pred[0];


X_ex = burnout.drop(['Id','Disengagement','Exhaustion','Burnout index','Sent','Ratio','Hierarchical Level'], axis='columns')
y_ex = burnout[['Exhaustion']]

regressor_ex = LinearRegression()
regressor_ex.fit(X_ex,y_ex)  

def predict_ex(data):
    data = pd.DataFrame(data)
    y_pred = regressor_ex.predict(data)
    return y_pred[0];