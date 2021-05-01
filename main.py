from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import json
from sklearn import svm
import pandas
import pymongo
import nltk
from nltk.corpus import stopwords
import string

nltk.download('stopwords')

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = "Content-Type"

def process(text):
    # ITEM 1: Take out punctuation
    no_punc = [ch for ch in text if ch not in string.punctuation]
    no_punc = ''.join(no_punc)

    # ITEM 2: clean up stopwords
    my_list = ['im', 'hes', 'shes', 'dont', 'wont', 'theyll']

    no_sw = [word for word in no_punc.split() if word.lower() not in set(stopwords.words('english'))]
    no_sw = [word for word in no_sw if word.lower() not in my_list]

    # listname = [variable FOR variable IN list_parsed IF variable in/not in/== CONDITION]
    return set(no_sw)

# this is to find what emails in the inbox have been selected
def mergeEmails(selectedEmail, emails):
    unique_mails = set()
    mail_subjects = []
    for i in selectedEmail:
        unique_mails.add(i["email"])
        mail_subjects.append(process(i["subject"]))
    for i in emails:
        if i["email"] in unique_mails:
            i["selected"] = True
        for sub in mail_subjects:
            my_tokens = process(i['subject'])
            if len(my_tokens.intersection(sub))/len(my_tokens) > 0.5:
                i['selected'] = True
                break

@app.route('/test', methods=["POST"])
def sendData():
    selected = request.get_json(force=True)['items']

    client = pymongo.MongoClient("mongodb+srv://gayatrs:CodingMinds!@spambotdata.muyzy.mongodb.net/EmailsData?retryWrites=true&w=majority")
    db = client['EmailsData']
    col = db['Selected']
    for email in selected:
        col.insert_one(email)

    return json.dumps('It worked')

#AI MODEL STILL IN PROGRESS (WILL BE UPDATED)
@app.route('/data', methods=["POST"])
def example():
    email_data = request.get_json(force=True)['msg']

    emails = []

    while len(email_data) > 3:
        try:
            ind1 = email_data.index('{')
            ind2 = email_data.index('}')

            emails.append( json.loads(email_data[ind1:ind2+1]) )
            email_data = email_data[ind2+1:]
        except:
            break

    # grab the data from the selected database table
    # grab the data from the emails database table
    client = pymongo.MongoClient("mongodb+srv://gayatrs:CodingMinds!@spambotdata.muyzy.mongodb.net/EmailsData?retryWrites=true&w=majority")
    db = client['EmailsData']
    col = db['Selected']
    selectedEmails = list(col.find())
    
    # emails -> [{'email': hi@uci.edu, 'id': 3, 'selected': false}, {'email': hi@uci.edu, 'id': 2, 'selected': false}]
    # selectedEmail ->[{'email': hi@uci.edu, 'id': 3}, {'email': hi@uci.edu, 'id': 4}, {'email': hi@uci.edu, 'id': 5}]

    # loop through selected emails and check if email exists in the list of dictionaries called 'emails', if it does, make its element 'selected' = true
    
    # flagged = [email['email'] for email in emails if email['selected'] == True]

    def checkSelected(index, emailsList):
        if emailsList[index]['selected']:
            return 0
        else:
            return 1
    
    # find simiarity between sender names
    def getSenderSimilarity(selectedEmails, emails):
        unique_mails = set()
        return_list = []
        for i in selectedEmails:
            unique_mails.add(i["sender"])
        for i in emails:
            if i["sender"] in unique_mails:
                return_list.append(0)
            else:
                return_list.append(1)
        return return_list
                
    mergeEmails(selectedEmails, emails)
    # [subject/email, sender]
    
    data = [
        [0, 0],
        [1, 0],
        [0, 1],
        [1, 1]
    ]

    s = ['flag', 'flag', 'flag', 'safe']

    rec_model = svm.SVC()
    rec_model.fit(data, s)

    data_list = getSenderSimilarity(selectedEmails, emails)
    print(data_list)

    flagged = []
    for i in range(len(emails)):
        values = [data_list[i],checkSelected(i, emails)]
        print(values)
        process = rec_model.predict([values])
        if process[0] == 'flag':
            flagged.append(emails[i]['email'])

    print(flagged)
    return json.dumps(flagged)

if __name__ == "__main__":
    app.run()
    
# app.run(host="127.0.0.1")