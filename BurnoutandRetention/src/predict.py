import pandas as pd
import numpy as np
from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import OneHotEncoder
from sksurv.ensemble import RandomSurvivalForest
from sksurv.linear_model import CoxPHSurvivalAnalysis

url = "./BurnoutandRetention/data/job_retention.csv"
job_retention = pd.read_csv(url)

field_str = job_retention.loc[:, "field"].astype(object).values[:, np.newaxis]
field_num = OrdinalEncoder(categories=[['Finance', 'Health', 'Law', 'Education_and_Training', 'Sales_Marketing', 'Public_Government']]).fit_transform(field_str)

X_no_field = job_retention.drop("field", axis=1)

level_str = job_retention.loc[:, "level"].astype(object).values[:, np.newaxis]
level_num = OrdinalEncoder(categories=[['Low', 'Medium', 'High']]).fit_transform(level_str)

X_no_field = X_no_field.drop("level", axis=1)

Xt=pd.get_dummies(X_no_field,columns=['gender'],drop_first=True)

Xt.loc[:,"field"] = field_num
Xt.loc[:,"level"] = level_num

Xt = Xt.drop(["left",'month'], axis=1)

y = [(d['left'],d['month']) for d in job_retention.to_dict('records')]

y = np.array(y, dtype=[('left', '?'), ('month', '<f8')])

estimator = CoxPHSurvivalAnalysis().fit(Xt, y)

def risk_score(data):
    data = pd.DataFrame(data)
    r = estimator.predict(data)
    return r

def rate(data):
    data = pd.DataFrame(data)
    r = estimator.predict_survival_function(data)
    data = {}
    i=0
    for result in r:
        data[i]=(np.array(result.y).tolist())
        i+=1
    return data