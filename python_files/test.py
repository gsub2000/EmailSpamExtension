# Imports
# users -> name -> AppData -> Local -> Programs -> Python -> Python32-38 -> Scripts
import numpy as np
import pandas as pd
import nltk
from nltk.corpus import stopwords
import string
import csv
# nltk.download('stopwords')

a_csv_file = open("spam_ham_dataset.csv", "r")
dict_reader = csv.DictReader(a_csv_file)
ordered_dict_from_csv = list(dict_reader)[0]
dict_from_csv = dict(ordered_dict_from_csv)
print(dict_from_csv)



# load file and read data
df = pd.read_csv("spam_ham_dataset.csv")

# print(df.head(5))

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
x_train, x_test, y_train, y_test = train_test_split(msgs, df['spam'], test_size=0.20, random_state = 0)

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





