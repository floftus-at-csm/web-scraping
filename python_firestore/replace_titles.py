import json


json_file_path = "./result4.json" 
with open(json_file_path, 'r') as j:
    contents = json.loads(j.read())
val = 0
dict1 = {}
for key, value in contents.items():
    id = list(contents.keys())[val]
    print(list(contents.keys())[val])
    print(type(list(contents.keys())[val]))
    id = id.replace("/", "-")
    if(id == ""):
        id = "untitled"
    print(id)
    # list(contents.keys())[val] = id
    dict1[id] = value
    val = val+1

json_object = json.dumps(dict1, indent=4)
with open("sample.json", "w") as outfile:
    outfile.write(json_object)
# contents.sa