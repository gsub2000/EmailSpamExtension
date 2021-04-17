from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import json
from sklearn import svm
import pandas
import pymongo


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = "Content-Type"

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
        values = [getNum(email)]
        print(values)
        process = rec_model.predict([values])
        if process[0] == 'flag':
            flagged.append(email['email'])

    # print(flagged)
    return json.dumps(flagged)

def getNum(email):
    return 0

if __name__ == "__main__":
    app.run()
    
# app.run(host="127.0.0.1")