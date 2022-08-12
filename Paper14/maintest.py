from array import array
import json,math, timeit
import random
from decimal import Decimal
from sympy import airyaiprime
from sympy.ntheory.factor_ import totient
import linecache
from bplib.bp import BpGroup
from operator import concat
G = BpGroup()
# def gcd(a, b):
#     if (a == 0):
#         return b
#     return gcd(b % a, a)

def phi(n):
    result = 1
    for i in range(2, n):
        if (math.gcd(i, n) == 1):
            result+=1
    return result

def TagGen(filename, array_blocks,Di,mj,s):
        #Generate wj
        wj = filename + str(len(array_blocks)) + str(j)
        #Calculate Tj
        Tj = (Di**mj) + hash(wj)**s
        return wj,Tj

def challenge(numblock):
    c = random.randint(0,numblock)
    #print(len(ZqStar))
    k1 = random.randint(0,math.floor(len(ZqStar)/100))
    k2 = random.randint(0,math.floor(len(ZqStar)/100))
    #k1 = ('{0:20}'.format(random.randint(1, 1)))
    #k2 = ('{0:20}'.format(random.randint(1, 1)))
    # chal = [c,k1,k2]
    # return chal
    #k1 = ('{0:05}'.format(random.randint(1, 1)))
    #k2 = ('{0:05}'.format(random.randint(1, 1)))
    chal = [c,k1,k2]
    #print(chal)
    return chal

def ProofGen(chal):
    C=[]
    #print(int(chal[0],2))
    P = []
    TBar = []
    FBar = []
    Tj = 1
    Fj = 1
    TAll = 1
    FAll = 1
    #print(type(chal[1]))
    #print(int(chal[0],2))
    for i in range(1,2,1):
        vi = math.pi*chal[1]*i # choosing random index
        ai = phi(chal[2]*i)# choose random params
        #print("vi: ",vi)
        #print('vi,ai: ',vi,ai)
        line = linecache.getline(r"block_tag.txt", 1)
        #print(line)
        #print(line)
        mvi = line[line.find("<[")+2:line.find("]>")]
        tvi = line[line.find("[")+1:line.find("]")]
        #print(tvi)
        mvi = int(Decimal(mvi))
        tvi = int(Decimal(tvi))

        #print("mvi :",mvi)
        #print("tvi :",tvi)
        TAll = math.pow((int(tvi)),int(ai))
        #print("TALL: ", TAll)
        FAll += ai*int(mvi)
        #print("FALL: ", FAll)
        i+=1
        P = [FAll, TAll]
    return P,ai,vi

def verify(wj,PKi,ID,mj,P0,ai,vi,P,g,numblock):
    eq2left = 1
    eq2leftbool = 1
    total_Tmul = 0
    total_Texp = 0
    total_Tpair = 0
    for i in range(1):
        Tmulstart = timeit.default_timer()
        #print(P[0])
        for i in range(P[0]):
            eq2left *= P[0]
        Tmulstop = timeit.default_timer()
        Tmul = Tmulstop - Tmulstart
        total_Tmul += Tmul
        if eq2left != g:
            eq2leftbool = 0
        #FBar = 0
        # print(P[1])
        # for i in range(int(P[1])):
        #     FBar += P[1]
        Texpstart = timeit.default_timer()
        eq2middle = hash(wj)**ai
        eq2right = hash(ID)+P[0]
        Texpstop = timeit.default_timer()
        Texp = Texpstop - Texpstart
        total_Texp += Texp
        if eq2middle == PKi:
            eq2middlebool = 1
        else:
            eq2middlebool = 0
        
        if eq2right == P0:
            eq2rightbool = 1
        else: eq2rightbool = 0
        #print("eq2left: ",eq2leftbool)
        #print("eq2mid: ",eq2middlebool)
        #print("eq2right: ",eq2rightbool)
        result = 0
        Tpairstart = timeit.default_timer()
        if eq2leftbool == eq2middlebool:
            if eq2middlebool == eq2rightbool:
                result = 1
            else: result = 0
        else: result = 0
        Tpairstop = timeit.default_timer()
        Tpair = Tpairstop-Tpairstart
        total_Tpair += Tpair
    return total_Tmul,total_Texp,total_Tpair, result
        #     #print("True")
        #     return True
        # #print("False")
        # return False

patient_list = []
runtimelist = []
for i in range (0,81):
    if i < 10:
        temp = "p000" + str(i)
        patient_list.append(temp)
    elif (i < 100) and (i >= 10):
        temp = "p00" + str(i)
        patient_list.append(temp)
    elif (i <1000 ) and (i >= 100):
        temp = "p0" + str(i)
        patient_list.append(temp)

filename = "p01000.json"
prevLeastRuntime = 0
array_request = [1,5,10,20,40,80]
for k2 in array_request:
    for k1 in range(10):
        runtime_total = 0
        for k3 in range (0,k2):

            with open('./Patient160/{}.json'.format(patient_list[k3]),'r') as file:
                doc = file.read()
            doc = json.dumps(doc)

            # filename = "file.txt"
            # with open('file.json','r') as file:
            #     doc = file.read()
            #doc = json.loads(doc)
            id = int(patient_list[k2][1:])
            #doc = json.dumps(doc)
            # with open('file.txt','r') as file:
            #     doc = file.read()
            start = timeit.default_timer()
            numblock = 10000 # 1000 Attributes -> 1000*10 = 10000
            stop = timeit.default_timer()
            runtimemul1 = stop-start
            array_blocks = []

            #convert doc to byte
            doc_byte = str.encode(doc)
            doc_Binary = ''.join([bin(b)[2:] for b in doc_byte])
            #print(len(doc_Binary))
            lenperblock = math.ceil(len(doc_Binary) / numblock)
            #print(lenperblock)
            temp_doc_Binary = doc_Binary
            #cut part of binary and put into the block
            while(temp_doc_Binary != ""): 
                array_blocks.append(temp_doc_Binary[:lenperblock])
                temp_doc_Binary = temp_doc_Binary[lenperblock:]
            #print(array_blocks)
            #print(len(array_blocks))
            #--pick index of array blocks
            j = random.randint(0,len(array_blocks)-1)
            #pick block at index j
            mj = array_blocks[j]
            mj = int(mj,2)
            # generate Zq*
            ZqStar = []
            k = random.randint(0,len(array_blocks))
            for i in range(k):
                pickchoice = random.randint(0,len(array_blocks)-1)
                ZqStar.append(array_blocks[pickchoice])
            #--Get secert key (Si)
            si_index = random.randint(0,len(ZqStar)-1)
            #print(xi_index)
            si = ZqStar[si_index]
            #print("Si: ",len(si))
            s = int(si,2)
            #print("S: ",s)

            P0 = int(array_blocks[si_index],2)**s
            #print("P0: ",P0)
            start = timeit.default_timer()
            Di = hash(id**s)
            stop = timeit.default_timer()
            runtimeexp1 = stop-start
            #--Generate PKi
            g = random.randint(1,5)
            PKi = g**s
            start = timeit.default_timer()
            wj,Tj = TagGen(filename, array_blocks,Di,mj,s)
            stop = timeit.default_timer()
            runtimeexp2 = stop-start
            
            chal = challenge(numblock)
            P,ai,vi = ProofGen(chal)

            start = timeit.default_timer()
            Tmul,Texp,Tpair, result = verify(wj,PKi,id,mj,P0,ai,vi,P,g,numblock)
            stop = timeit.default_timer()
            runtimeexp2 = stop-start
            #totalruntime = 2*(runtimeexp1+runtimeexp2)
            runtimetagver = (3*Tpair) + Tmul + Texp
            runtime_total += runtimetagver
        runtimelist.append(runtime_total)
    runtimelist.sort()
    for i2 in range(len(runtimelist)):
        if runtimelist[i2] > prevLeastRuntime:
            print('Time({})(ms): '.format(k2), runtimelist[i2]*10000000)
            #print('DSRR1Time({}): '.format(i), runtime_list[i1])
            prevLeastRuntime = runtimelist[i2]
            break
        #print("Time({}): ".format(i1),runtime1+runtime2+runtime3)