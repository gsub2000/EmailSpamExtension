import nltk
from nltk.corpus import stopwords
import string
emails = [{'email': "hi@uci.edu", 'subject': 'Welcome back to COMPSCI 161- read syllabus', 'selected': False}, 
    {'email': "hi3@uci.edu", 'subject': 'Barack Obama has tweeted regarding the US Supreme Court', 'selected': False}, 
    {'email': "hello@uci.edu", 'subject': 'Hello, I was reaching out to see if you wanted to', 'selected': False},
    {'email': "test@uci.edu", 'subject': 'Redeem you $50 gift card today! Call this number', 'selected': False}]
selectedEmail = [{'email': "hi@uci.edu", 'subject': 'Welcome back to COMPSCI 161- read syllabus'}, 
    {'email': "hi2@uci.edu", 'subject': 'Quiz Statistics: Global Forums #1'}, 
    {'email': "hi3@uci.edu", 'subject': "NBA tweeted Klay Thompson out with a torn ACL during Finals"},
    {'email': "anon@uci.edu", 'subject': "Call this number to get your $50 gift card for free"}]

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

# ("hi@uci.edu", "hello I wanted to reach out for a job")

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


print(emails)
