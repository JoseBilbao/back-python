import pandas as pd
import json

f = open('./data/database.json')

data = json.load(f)

header = 'Symptom'


def unique_symptom(data):
    symptom = []
    for d in data:
        [symptom.append(d[s]) for s in range(len(d)) if s!=0]
    return symptom

def class_counts(rows):
    """Counts the number of each type of example in a dataset."""
    counts = {}  # a dictionary of label -> count.
    for row in rows:
        # in our dataset format, the label is always the first column
        label = row[0]
        if label not in counts:
            counts[label] = 0
        counts[label] += 1
    return counts

def is_numeric(value):
    """Test if a value is numeric."""
    return isinstance(value, int) or isinstance(value, float)

# chance of misclassifying
def gini(data):
    counts = class_counts(data)
    impurtity = 1
    
    for disease in counts:
        prob_of_disease = counts[disease] / float(len(data))
        impurtity -= prob_of_disease**2
    return impurtity

# uncertainy of starting node - the weight impurity of two child nodes
def info_gain (left, right, current_uncertainy):

    p = float(len(left)) / (float(len(left)) + float(len(right))) 

    return current_uncertainy - p * gini(left) -  (1-p) * gini(right)

class Question:
    """A Question is used to partition a dataset.
    """

    def __init__(self, value):
        self.value = value

    def match(self, example):
        # Compare the feature value in an example to the
        # feature value in this question.
        if self.value in example:
            val = example[example.index(self.value)]
        else:
            return False

        if is_numeric(val):
            return val >= self.value
        else:
            return val == self.value

    def __repr__(self):
        # This is just a helper method to print
        # the question in a readable format.
        condition = "=="
        if is_numeric(self.value):
            condition = ">="
        return "Is %s %s %s?" % (
            header, condition, str(self.value))

def find_best_split(data):
    best_info_gain = 0
    best_question = None
    current_uncertainty = gini(data)
    n_symptoms = unique_symptom(data)

    for symptom in n_symptoms:
        question = Question(symptom)
        match_rows, unmatch_rows = partition(data,question)

        if len(match_rows) == 0 or len(unmatch_rows) == 0:
            continue
    
        gain = info_gain(match_rows,unmatch_rows,current_uncertainty)

        if (gain>best_info_gain):
            best_info_gain = gain
            best_question = question
    return best_info_gain, best_question

class Leaf:
    def __init__ (self, data):
        self.predictions = class_counts(data)

class Decision_Nodes:
    
    def __init__ (self, question, true_branch, false_branch):
        self.question = question
        self.true_branch = true_branch
        self.false_branch = false_branch

def partition(rows, question):
    """Partitions a dataset.

    For each row in the dataset, check if it matches the question. If
    so, add it to 'true rows', otherwise, add it to 'false rows'.
    """
    true_rows, false_rows = [], []
    for row in rows:
        if question.match(row):
            true_rows.append(row)
        else:
            false_rows.append(row)
    return true_rows, false_rows

def build_tree(data):

    gain, question = find_best_split(data)

    if question is None:
        for index in range(len(data)-1):
            if set(data[index][1:]) != set(data[index+1][1:]):
                print("test")
        questions  = list(set(data[index][1:]))
        answer =[]
        for d in data:
            answer.append(d[0])
        return questions, answer, []
    else:
        match_rows, unmatch_rows = partition(data, question)
        return question, match_rows,unmatch_rows

def print_tree(node,spacing=""):
    
    if isinstance(node,Leaf):
        print(spacing+"Predict "+ str(node.predictions))
        return

    print(spacing+str(node.question))

    print(spacing+"-->true")
    print_tree(node.true_branch, spacing+" ")

    print(spacing+"-->false")
    print_tree(node.false_branch, spacing+" ")

def classify(data,node):
    
    if isinstance(node,Leaf):
        return node.predictions

    if node.question.match(data):
        return classify(data, node.true_branch)
    else:
        return classify(data, node.false_branch)