from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import json
from sklearn import svm
import pandas
import pymongo


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = "Content-Type"

# this is to find what emails in the inbox have been selected
def mergeEmails(selectedEmail, emails):
    unique_mails = set()
    for i in selectedEmail:
        unique_mails.add(i["email"])
    for i in emails:
        if i["email"] in unique_mails:
            i["selected"] = True

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
    mergeEmails(selectedEmails, emails)
    print(emails)
    # merge data




    # transform data
    # parse and tokenize data
    # get predictive model
    # make predictions

    data = [
        [0],
        [1]
    ]

    s = ['flag', 'safe']

    rec_model = svm.SVC()
    rec_model.fit(data, s)

    flagged = []
    for email in emails:
        values = [getNum(email['email'])]
        print(email, values)
        process = rec_model.predict([values])
        if process[0] == 'flag':
            flagged.append(email['email'])

    # print(flagged)
    return json.dumps(flagged)

def getNum(email):
    if "notifications@instructure.com" in email:
        return 0
    return 0

if __name__ == "__main__":
    app.run()
    
# app.run(host="127.0.0.1")