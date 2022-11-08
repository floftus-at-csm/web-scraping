import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json
from datetime import date

today = date.today()
d1 = today.strftime("%d.%m.%Y")

json_file_path = "./sample.json" 

with open(json_file_path, 'r') as j:
    contents = json.loads(j.read())

# # 1. This will be the criteria to sort each inner list
# # first by ID, then by date, ascending
# def _sort(item):
#     return (item['id'], item['date'])

# # 2. Sorting my json file lists, in place
# for lista in contents.values():
#     lista.sort(key=_sort)

cred = credentials.Certificate("serviceAccount.json")
firebase_admin.initialize_app(cred)
# firebase_admin.initialize_app(cred, {
# 'projectId': "1:657928510466:web:faf980580c1b19d9f25b1b",
# })    

db = firestore.client()

# Inside the collection Objects, I create a document for each object key,
# Then set the inner list as an inner document, with value equals to the list.
val = 0
for key, value in contents.items():
    id = list(contents.keys())[val]
    print(list(contents.keys())[val])
    val = val + 1
    # id = value.pop('id', None)
    # print(type(id))
    if id:
        print("in if")
        db.collection("ubuweb").document(id).set(value, merge=True)

    else:
        db.collection("ubuweb").document(id).add(value)
    # doc_ref = db.document('Objects/' + key).set({'value': value})