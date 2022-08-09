import pandas as pd
import json
from sklearn.ensemble import RandomForestClassifier
import statsmodels.api as sm
import statsmodels.formula.api as smf 
from sklearn.model_selection import train_test_split
import numpy as np

data = pd.read_csv('./Culture/data/output.csv')
employees = pd.read_csv('./Culture/data/hrdata_OSF.csv')

employees_dict = {}
for emp in employees.to_dict('records'):
    name = emp['name']
    employees_dict[name] = {
        'acquired':emp['acquired'],
        'tenure':emp['tenure'],
        'title_status':emp['title_status'],
        'male':emp['male'],
        'rating':emp['rating'],
        'branch_id':emp['branch_id']
    }

retention = data.drop(columns=['Unnamed: 0','month','diff','n_emails','innov'])
reformation = data.drop(columns=['Unnamed: 0','month','diff','n_emails','ret'])

# retention = retention.to_dict('records')
retentions = {}
for r in retention.to_dict('records'):
    retentions[r['sender']] = r['ret']

reformations = {}
for r in reformation.to_dict('records'):
    reformations[r['sender']] = r['innov']

df = []
for emp in employees_dict:
    if emp in retentions and emp in reformations:

        temp = employees_dict[emp]
        temp['ret'] = retentions[emp]
        temp['innov'] = reformations[emp]
        temp['name'] = emp

        df.append(employees_dict[emp])

df = pd.DataFrame(df)
df.fillna(0, inplace=True)
X_train, X_test= train_test_split(df, test_size=0.33, random_state=42)

retentions_X_train = X_train.drop(columns=['innov','name'], axis=1)
reformations_X_train = X_train.drop(columns=['ret','name'], axis=1)

retentions_X_train = sm.add_constant(retentions_X_train) 

retentions_y_train = X_train['ret']
reformations_y_train = X_train['innov']

olsmod = smf.ols(formula='ret ~ acquired + tenure + title_status + male + rating + branch_id', data=retentions_X_train)
olsres = olsmod.fit()

olsmod_innov = smf.ols(formula='innov ~ acquired + tenure + title_status + male + rating + branch_id', data=reformations_X_train)
olsres_innov = olsmod_innov.fit()

def prediction(data):
    data = pd.DataFrame(data)
    data["acquired"] = data.acquired.astype(int)
    data["tenure"] = data.acquired.astype(float)
    data["title_status"] = data.acquired.astype(int)
    data["rating"] = data.acquired.astype(float)
    data["male"] = data.acquired.astype(int)
    data["branch_id"] = data.acquired.astype(int)
    ypred = olsres.predict(data)
    ypred_innov = olsres_innov.predict(data)
    return {'ret':ypred[0], 'innov':ypred_innov[0]}