emails = [{'email': "hi@uci.edu", 'id': 3, 'selected': False}, {'email': "hi3@uci.edu", 'id': 2, 'selected': False}, {'email': "hello@uci.edu", 'id': 7, 'selected': False}]
selectedEmail = [{'email': "hi@uci.edu", 'id': 3}, {'email': "hi2@uci.edu", 'id': 4}, {'email': "hi3@uci.edu", 'id': 5}]

# if email in emails is part of the selected list, then go ahead and change the 'selected' attribute to True 


# 50
# 5 = 250

# 5
# 50 = 55
# for i in selectedEmail:
#     email = i['email']
#     for i in emails:
#         if i['email'] == email:
#             i['selected'] = True

# print(emails)

# print(set())
# print(dict())

unique_mails = set()
for i in selectedEmail:
    unique_mails.add(i["email"])
for i in emails:
    if i["email"] in unique_mails:
        i["selected"] = True
print(emails)
