from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import json
import sklearn
import pandas
import pymongo

db = dict()

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = "Content-Type"

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

    
    client = pymongo.MongoClient("mongodb+srv://gayatrs:Gs191052044!@spambotdata.muyzy.mongodb.net/EmailsData?retryWrites=true&w=majority")
    db = client['EmailsData']
    collection = db['Emails']

    # doc = {
    #     "sender": "me",
    #     "email" : "me@gmail.com"
    # }
    for e in emails:
        collection.insert_one(e)



    return json.dumps("message")


app.run(host="127.0.0.1")