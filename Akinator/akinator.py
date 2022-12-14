from flask import Blueprint
from flask import request
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn import tree
import pyttsx3
from sklearn import preprocessing
from sklearn.tree import DecisionTreeClassifier,_tree
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.svm import SVC
import csv
import warnings
import re
from Akinator.chatbot import *
from Akinator.decisionTree import *

akinator = Blueprint('akinator', __name__)

@akinator.route("/", methods=["GET"])
def test():
    return "akinator";

def check_pattern(dis_list,inp):
    pred_list=[]
    inp=inp.replace(' ','_')
    patt = f"{inp}"
    regexp = re.compile(patt)
    pred_list=[item for item in dis_list if regexp.search(item)]
    if(len(pred_list)>0):
        return 1,pred_list
    else:
        return 0,[]
def sec_predict(symptoms_exp):
    df = pd.read_csv('data/diseasePrediction.csv')
    X = df.iloc[:, :-1]
    y = df['prognosis']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=20)
    rf_clf = DecisionTreeClassifier()
    rf_clf.fit(X_train, y_train)

    symptoms_dict = {symptom: index for index, symptom in enumerate(X)}
    input_vector = np.zeros(len(symptoms_dict))
    for item in symptoms_exp:
        input_vector[[symptoms_dict[item.capitalize()]]] = 1

    return rf_clf.predict([input_vector])
def print_disease(node,le):
    node = node[0]
    val  = node.nonzero() 
    disease = le.inverse_transform(val[0])
    presentD  = list(map(lambda x:x.strip(),list(disease)))
    return list(map(lambda x:x.strip(),list(disease)))
def tree_train():
    training= open('./data/data.json')
    data = json.load(training)

    unique_disease  = []
    unique_symptoms = []
    for d in data:
        unique_disease.append(d[0])
        unique_symptoms += d[1:]

    return data,unique_disease,list(set(unique_symptoms))
def sec_predict_chatbot1(symptoms_exp):
    df = pd.read_csv('./Akinator/data/Training.csv')
    X = df.iloc[:, :-1]
    y = df['prognosis']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=20)
    rf_clf = DecisionTreeClassifier()
    rf_clf.fit(X_train, y_train)

    symptoms_dict = {symptom: index for index, symptom in enumerate(X)}
    input_vector = np.zeros(len(symptoms_dict))
    for item in symptoms_exp:
        input_vector[[symptoms_dict[item]]] = 1

    return rf_clf.predict([input_vector])
def tree_to_code(tree, feature_names,disease_input,reduced_data,le):
    tree_ = tree.tree_
    feature_name = [
        feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
        for i in tree_.feature
    ]

    chk_dis=",".join(feature_names).split(",")
    symptoms_present = []
    data = []
    conf,cnf_dis=check_pattern(chk_dis,disease_input)
    disease_input=cnf_dis[0]
    print(disease_input)
    def recurse(node, depth,le):
        indent = "  " * depth
        if tree_.feature[node] != _tree.TREE_UNDEFINED:
            name = feature_name[node]
            threshold = tree_.threshold[node]

            if name == disease_input:
                val = 1
            else:
                val = 0
            if  val <= threshold:
                recurse(tree_.children_left[node], depth + 1,le)
            else:
                symptoms_present.append(name)
                recurse(tree_.children_right[node], depth + 1,le)
        else:
            present_disease = print_disease(tree_.value[node],le)
            # print( "You may have " +  present_disease )
            red_cols = reduced_data.columns 
            symptoms_given = red_cols[reduced_data.loc[present_disease].values[0].nonzero()]
            data.append(list(symptoms_given))
            data.append(present_disease)
    recurse(0, 1,le)
    return data

@akinator.route("/chatbotInput",methods=["POST"])
def chatbot():
    userInput = request.get_data(as_text=True)
    print(userInput)
    data,unique_disease,unique_symptoms=tree_train()
    conf,cnf_dis=check_pattern(unique_symptoms,userInput)
    # userInput=cnf_dis[0]
    question = Question(userInput)
    # Air fluid level
    match_rows, unmatch_rows = partition(data, question)
    print(match_rows)
    if len(match_rows)==1:
        return {"data":match_rows[0][0],"match":match_rows[0]}
    decision, true_branch, false_branch = build_tree(match_rows)
    if len(false_branch)==0:
        false_branch = ''
    if isinstance(decision, list) or type(decision) is list:
        return {"questions":decision, "answer":true_branch}
    elif isinstance(decision, Question):
        return {"question":decision.value, "match":true_branch,'unmatch':false_branch}
    # return {"question":decision.value, "match":true_branch,'unmatch':false_branch}

@akinator.route("/chatbotQuestion",methods=["POST"])
def split():
    userInput = request.get_json()
    ans = userInput['ans']
    true_branch = userInput['match']

    if len(true_branch)==1:
        first_prediction = true_branch[0][0]
        return {"data":first_prediction}
    else:
        decision, true_branch, false_branch  = build_tree(true_branch)
        if isinstance(decision, list) or type(decision) is list:
            return {"questions":decision, "answer":true_branch}
        elif isinstance(decision, Question):
            return {"question":decision.value, "match":true_branch,'unmatch':false_branch}

    return ''
    
@akinator.route("/chatbotSecondPrediction",methods=["POST"])   
def secondPrediction():
    userInput = request.get_data(as_text=True)
    userInput = userInput.strip('[]').replace('"','').split(",")
    predict = sec_predict(userInput)
    print(predict[0])
    return predict[0]

@akinator.route("/symptoms",methods=["POST"])
def symptoms():
    userInput = request.get_data(as_text=True)

    training = pd.read_csv('./Akinator/data/Training.csv')
    testing= pd.read_csv('./Akinator/data/Testing.csv')
    cols= training.columns
    cols= cols[:-1]
    x = training[cols]
    y = training['prognosis']
    y1= y


    reduced_data = training.groupby(training['prognosis']).max()

    #mapping strings to numbers
    le = preprocessing.LabelEncoder()
    le.fit(y)
    y = le.transform(y)


    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.33, random_state=42)
    testx    = testing[cols]
    testy    = testing['prognosis']  
    testy    = le.transform(testy)


    clf1  = DecisionTreeClassifier()
    clf = clf1.fit(x_train,y_train)

    model=SVC()
    model.fit(x_train,y_train)

    importances = clf.feature_importances_
    indices = np.argsort(importances)[::-1]
    features = cols

    data = tree_to_code(clf,cols,userInput,reduced_data,le)
    print(data[0])
    print(data[1])
    return {"data":data[0],"result":data[1]}

@akinator.route("/predict",methods=["POST"])
def predict():
    data = request.get_json(force=True)
    print(data)
    symptoms_exp=[]
    for syptom in data.keys():
        if data[syptom]=="yes" and syptom!='result':
            symptoms_exp.append(syptom)
    second_prediction=sec_predict_chatbot1(symptoms_exp)

    if(data['result']==second_prediction[0]):
        print("You may have ", data['result'])
    else:
        print("You may have ",data['result'], "or ", second_prediction[0])

    return {'prediction':data['result'], 'prediction2':second_prediction[0]}

@akinator.route("/prediction", methods=["POST"])
def prediction():
    userInput = request.get_data(as_text=True)
    userInput = userInput.strip('[]').replace('"','').split(",")
    print(userInput)
    predict  = predictionDisease(userInput).tolist()
    return ''.join(predict)