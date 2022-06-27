import math
from operator import concat
import random
from itertools import chain, islice
import json
from sre_compile import isstring
#import bplib 
import linecache
from tate_bilinear_pairing import eta
from tate_bilinear_pairing import ecc
import bplib
from bplib.bp import BpGroup

G = bplib.BpGroup()
#print(G)

def toBinary(a):
  l,m=[],[]
  for i in a:
    l.append(ord(i))
  for i in l:
    m.append(int(bin(i)[2:]))
  return m

def KeyGen():
    g = ('{0:05}'.format(random.randint(1, 1)))
    u = ('{0:05}'.format(random.randint(1, 1)))
    x = ('{0:05}'.format(random.randint(1, 1)))
    g = int(g)
    x = int(x)
    X = g**x
    X = str(X)
    X = (X[:16]) if len(X) > 16 else X
    print("Data owner's private key ",x)
    print("Data owner's public key ",X)
    #print(X)
    #print(len(str(X)))
    y = ('{0:05}'.format(random.randint(1, 1)))
    y = int(y)
    Y = g**y
    Y = str(Y)
    Y = (Y[:16]) if len(Y) > 16 else Y
    #print(len(str(Y)))
    print("Verifier's private key ",y)
    print("Verifier's public key ",Y)    
    return g,u,x,X,y,Y


def MainHere(fid):
    with open('test.txt') as f:
        g,u,x,X,y,Y = KeyGen()
        b = 1
        while True:
            c = f.read(1)
            if not c:
                print("End of file")
                break
            if c in set('ABCDEFGH"IJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789}{][,/.1234567890-=qwertyuiop[]asdfghjkl;!@#$%^&*()_+QWERTYUIOP}{ASDFGHJKL:"ZXCVBNM<>?'):
                #print("Read a character: ",b, " -> ", c)
                with open('file.txt', "a") as d:
                    d.write(c)
                    d.close()
                b = int(b)
                b+=1
                Y = int(Y)
                x = int(x)
                enc_kp = hash(Y**x)
                enc_kp = str(enc_kp)
                b = str(b)
                fid = str(fid)
                hoho = str(enc_kp)+str(fid)+str(b)
                hoho = int(hoho)
                #print(hoho)
                u = int(u)
                #c = int(c)
                c = toBinary(c)
                #cc = (','.join(c))
                cc = ( ", ".join( repr(e) for e in c ) )
                print(cc)
                #print(c)
                #math.pi()*()
                cc = (cc[:3]) if len(cc) > 3 else cc
                cc = int(cc)
                tag = hash(hoho*math.pow(u,cc))**x
                #print(tag)
                txt = (f'[{tag}]<[{cc}]>')
                with open('block_tag.txt', "a") as tagpair:
                    tagpair.write(txt+'\n')
                    tagpair.close()
                print(txt)
                print(txt.format(tagg = tag,block = cc))
    pack_key = [g,u,x,X,y,Y]
    return pack_key


def gcd(a, b):
     
    if (a == 0):
        return b
    return gcd(b % a, a)
 
# A simple method to evaluate
# Euler Totient Function
def phi(n):
    result = 1
    for i in range(2, n):
        if (gcd(i, n) == 1):
            result+=1
    return result

def challenge(c):
    k1 = ('{0:05}'.format(random.randint(1, 1)))
    k2 = ('{0:05}'.format(random.randint(1, 1)))
    chal = [c,k1,k2]
    print(chal)
    return tuple(chal)

def ProofGen(T, c, k1, k2):
    TAll = 1
    FAll = 1    
    for i in range(c):
        #print(xx)
        print("========= loop", i ," =========")
        vi = math.pi*int(concat(str(k1),str(i))) # choosing random index
        print("vi ",math.floor(vi))
        ai = phi(int(concat(str(k2),str(i)))) # choose random params
        print("ai ",math.floor(ai))
        line = linecache.getline(r"block_tag.txt", math.floor(vi))
        mvi = line[line.find("<[")+2:line.find("]>")]
        tvi = line[line.find("[")+1:line.find("]")]
        print("mvi ",mvi)
        print("tvi ",tvi)
        TAll = TAll* math.pow((int(tvi)),ai)
        print("TALL: ", TAll)
        FAll += ai*int(mvi)
        i+=1
        P = [FAll, TAll]
    return P

def verify(y,X, g, u, fid, c, k1, k2, FAll, TAll):
    enc_check = hash(math.pow(int(X),int(y)))    
    TAll = 1
    FAll = 1    
    hashcheck = 1
    for i in range(c):
        #print(xx)
        print("========= loop", i ," =========")
        vi = math.pi*int(concat(str(k1),str(i))) # choosing random index
        print("vi ",math.floor(vi))
        ai = phi(int(concat(str(k2),str(i)))) # choose random params
        print("ai ",math.floor(ai))
        line = linecache.getline(r"block_tag.txt", math.floor(vi))
        mvi = line[line.find("<[")+2:line.find("]>")]
        tvi = line[line.find("[")+1:line.find("]")]
        print("mvi ",mvi)
        print("tvi ",tvi)
        TAll = TAll* math.pow((int(tvi)),ai)
        print("TALL: ", TAll)
        FAll += ai*int(mvi)
        hashcheck *= hash(str(enc_check)+str(fid)+str(vi))**ai
        i+=1
    
    b_right = hashcheck*math.pow(u,FAll)
    b_leftside = G.pair(TAll, g) 
    b_rightside = G.pair(b_right, X)
    if(b_leftside == b_rightside):
        return 1
    else:
        return 0

# ==== test =====
#print(c,k1,k2)
g,u,x,X,y,Y = MainHere('1')
c,k1,k2 = challenge(5)
FAll,TAll = ProofGen(1,c,2,3)
verify(y,X,g,u,1,c, k1 ,k2, FAll, TAll)
#print("FAll: ",FAll)
#print("TAll: ",TAll)
# ==== test =====

# k1 = challenge
# k2 = challenge
#print(c,k1,k2)
#ProofGen(T,c,k1,k2)

def shit():    
    with open('test.txt') as infp:
        files = [open('%d.txt' % i, 'w') for i in range(1000)]
        for i, line in enumerate(infp):
            files[i % 1000].write(line)
        for f in files:
            f.close()

f = open("test.txt", "r")
f = str(f)

#KeyGen()

    
