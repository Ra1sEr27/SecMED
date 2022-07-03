import json
with open('./testpatient/p00000.json','r') as file:
    doc = file.read()
doc = json.loads(doc)
for i in range(1,10001):
    j = str(i)
    while(len(j) < 5):
        j = "0"+ j
    # while(len(certid) < 5):
    #     certid = "0" + certid
    # certid = "DO" + certid
    # print(certid)
    #print(j)
    id = "p"+j
    doc["id"] = "p{}".format(j)
    #print(doc['id'])
    if i > 1:
        doc["id{}".format(i)] = "p00001"
    if i % 1000 == 0:
        doc_string = json.dumps(doc)
        with open('./testpatient/{}.txt'.format(id),'w') as file:
            file.write(doc_string)
