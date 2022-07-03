from array import array
import json,math, timeit
import random
start = timeit.default_timer()
filename = "p01000.json"
for i in range(1000,10001,1000):
    numattr = i
    j = str(i)
    while(len(j) < 5):
        j = "0"+ j
    with open('./testpatient/p{}.txt'.format(j),'r') as file:
        doc = file.read()

    # filename = "file.txt"
    # with open('file.json','r') as file:
    #     doc = file.read()
    #doc = json.loads(doc)
    id = int(j)
    #doc = json.dumps(doc)
    # with open('file.txt','r') as file:
    #     doc = file.read()
    numblock = i*10
    array_blocks = []

    #convert doc to byte
    doc_byte = str.encode(doc)
    doc_Binary = ''.join([bin(b)[2:] for b in doc_byte])
    #print(len(doc_Binary))
    lenperblock = math.ceil(len(doc_Binary) / numblock)
    #print(lenperblock)
    temp_doc_Binary = doc_Binary

    while(temp_doc_Binary != ""):
        array_blocks.append(temp_doc_Binary[:lenperblock])
        temp_doc_Binary = temp_doc_Binary[lenperblock:]
    #print(array_blocks)
    #print(len(array_blocks))
    j = random.randint(0,len(array_blocks))
    #randomly pick 1 block
    mj = array_blocks[j]
    mj = int(mj,2)
    # generate Zq*
    ZqStar = []
    k = random.randint(0,len(array_blocks))
    for i in range(k):
        pickchoice = random.randint(0,len(array_blocks)-1)
        #print(pickchoice)
        #print(array_blocks[pickchoice])
        ZqStar.append(array_blocks[pickchoice])
    si_index = random.randint(0,len(ZqStar)-1)
    #print(xi_index)
    si = ZqStar[si_index]
    #print("Si: ",si)
    s = int(si,2)
    #print("S: ",s)
    Di = hash(id**s)
    #print("Di: ",Di)
    #Generate wj
    # filename_byte = str.encode(filename)
    # filename_Binary = ''.join([bin(b)[2:] for b in filename_byte])
    #Fid = int(filename_Binary,2)
    #print("Fid: ",Fid)
    wj = filename + str(len(array_blocks)) + str(j)
    #print("wj: ",wj)
    #Calculate Tj
    Tj = (Di**mj) + hash(wj)**s
    stop = timeit.default_timer()
    runtime = stop-start
    #print("Tag: ",Tj)
    print("Time({}): ".format(numattr),runtime)
