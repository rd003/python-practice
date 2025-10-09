import json

data = {"name":"Gauraj","age":34}

# with open('sample1.json','w') as f:
#     json.dump(data,f,indent=4)

# with open('sample2.json','r') as f:
#     data=f.read()
#     print(data["name"]) # error



with open('sample2.json','r') as f:
    data=json.load(f)    
    print(data["name"])