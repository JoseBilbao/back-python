import pandas as pd
import json
import csv
from sklearn.preprocessing import LabelEncoder
from sklearn import tree

def maxLen(data):
    maxLen  = 0
    for disease in data:
        if len(disease) > maxLen:
            maxLen=len(disease)
    return maxLen


def predictionDisease(userInput):
    data = pd.read_csv('./data/disease.csv', na_filter=False)
    symptoms = data.drop('Name', axis='columns')
    target = data['Name']

    drop_label = []
    label_encoder = LabelEncoder()
    for col in symptoms.columns:
        drop_label.append(col)
        symptoms[col] = label_encoder.fit_transform(symptoms[col])
    
    model = tree.DecisionTreeClassifier()
    model.fit(symptoms, target)
    
    encode =  []
    print(len(symptoms.columns))
    for col in symptoms.columns:
        if col in userInput:
            index = userInput.index(col)
            if index!=-1:
                encode.append(1)
        else: encode.append(0)

    y_test = model.predict([encode])
    return y_test

def write_data_csv_tf():
    with open('./data/Symptoms.json') as f:
        symptoms = json.load(f)

    database =[]

    with open('./data/data.json') as f:
        diseases = json.load(f)

    for disease in diseases:
        temp = [disease[0]]
        for symptom in symptoms:
            if symptom in disease:
                temp.append(True)
            else: temp.append(False)
        database.append(temp)

    symptoms.insert(0,"Name")

    with open('disease.csv','w', encoding='UTF8') as w:
        writer = csv.writer(w)
        writer.writerow(symptoms)

        writer.writerows(database)


def write_data_csv():

    with open('./data/data.json') as f:
        diseases = json.load(f)

    maxLength  = maxLen(diseases)
    header = ['Name']
    for count in range(maxLength):
        header.append('symptom_'+str(count))

    with open('diseaseTest.csv','w', encoding='UTF8') as w:
        writer = csv.writer(w)
        writer.writerow(header)

        writer.writerows(diseases)