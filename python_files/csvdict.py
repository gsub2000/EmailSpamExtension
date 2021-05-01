import numpy as np
import pandas as pd
import nltk
from nltk.corpus import stopwords
import string
import csv

a_csv_file = open("spamcopy.csv", "r")
dict_reader = csv.DictReader(a_csv_file)
print(dict_reader)
ordered_dict_from_csv = list(dict_reader)

# create function that transforms list of dictionaries to dictionary of lists

# [{text: 'blah blah blah', 'spam': 0},
# {text: 'blah blah blah', 'spam': 1},
# {text: 'blah blah blah', 'spam': 0}]

# {
#   text: ['blah blah', 'blah blah', 'blah blah']
#   spam: [0,1,0]
# }
# temp = [{"text": 'a', "spam": 0}, {"text": 'b', "spam": 1}, {"text": 'c', "spam": 0}]

def transform_dict(data):
    text_list = []
    spam_list = []
    for item in data:
        text_list.append(item['text'])
        spam_list.append(item['spam'])
    
    # create dictionary
    d = {'text': text_list, 'spam': spam_list}

    # return dictionary
    return d

new_data = transform_dict(ordered_dict_from_csv)
# print(new_data)

df = pd.DataFrame.from_dict(new_data)

# check rows/columns
print(df.shape)

# check columns
print(df.columns)

# drop duplicates
df.drop_duplicates(inplace=True)
print(df.shape)

# check if any spaces are blank
print(df.isnull().sum())

# Tokenization Function
def process(text):
    # ITEM 1: Take out punctuation
    # no_punc = []
    # for ch in text:
    #     if ch not in string.punctuation:
    #         no_punc.append(ch)

    no_punc = [ch for ch in text if ch not in string.punctuation]
    no_punc = ''.join(no_punc)

    # ITEM 2: clean up stopwords
    # no_sw = []
    # for word in no_punc.split():
    #     if word.lower() not in stopwords.words('english'):
    #         no_sw.append(word)

    my_list = ['im', 'hes', 'shes', 'dont', 'wont', 'theyll']

    no_sw = [word for word in no_punc.split() if word.lower() not in set(stopwords.words('english'))]
    no_sw = [word for word in no_sw if word.lower() not in my_list]

    # listname = [variable FOR variable IN list_parsed IF variable in/not in/== CONDITION]


    return no_sw

# print(process("Hi! My name is bob and I'm in second grade. I like math and science and i'm also a fan of COD and DOTA!!!!!"))

# apply 'process' function on all text in csv file
print(df['text'].head().apply(process))

# convert words to number equivalent (for AI processing)
from sklearn.feature_extraction.text import CountVectorizer

msgs = CountVectorizer().fit_transform(df['text'])

# split into testing and training data (80/20)
from sklearn.model_selection import train_test_split 
x_train, x_test, y_train, y_test = train_test_split(msgs, df['spam'], test_size=0.21, random_state = 0)

# gets size
print(msgs.shape)

# trains data
from sklearn.naive_bayes import MultinomialNB
classifier = MultinomialNB()
classifier.fit(x_train, y_train)

# compare predicted values against actual y values
pred = classifier.predict(x_train)
print(pred)
print(y_train.values)


# get accuracy percentages to see how the AI is
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix

print(classification_report(y_train, pred))
print('CONFUSION::')
print(confusion_matrix(y_train, pred))
print('ACCURACY::')
print(accuracy_score(y_train, pred))

# repeat process on testing data (rather than training data)
# print("xtest is ", x_test)
pred_test = classifier.predict(x_test)
# print(pred_test)
# print(y_test.values)

# prediction = classifier.predict()

print(classification_report(y_test, pred_test))
print('CONFUSION::')
print(confusion_matrix(y_test, pred_test))
print('ACCURACY::')
print(accuracy_score(y_test, pred_test))