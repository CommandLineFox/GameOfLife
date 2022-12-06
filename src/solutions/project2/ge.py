import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sn
import functools
from itertools import groupby
import math 


#   ZADATAK   1.1


def fun1(array, x):
    array.append(array[-1]+float(x[2]))
    return array

def SrednjaVrednost11(data):
    tiplets=[]
    b = groupby(data, key=lambda x: x[0])
    
    for k, v in b:
        temp=list(v)
        d = functools.reduce(fun1, temp, [0.0])
        tuple=(k,d[-1]/(len(d)-1))
        tiplets.append(tuple)
    
    return tiplets



#  ZADATAK   1.2


def fun2(array):
    cell, gene, value = array
    global my_dictionary
    return cell, gene, round(value-my_dictionary[cell], 2)
    
def CentriranjeEkspresije12(data):
    b = map(fun2, data)
    return list(b)



#  ZADATAK   1.3

def fun3(array, x):
    array.append(array[-1]+(float(x[2])-my_dictionary[x[0]])**2)
    return array

def Varijansa13(data):

    tiplets=[]
    b = groupby(data, key=lambda x: x[0])

    for k, v in b:
        temp=list(v)
        d = functools.reduce(fun3, temp, [0.0])
        tuple=(k,d[-1]/(len(d)-2))
        tiplets.append(tuple)

    return tiplets



#  ZADATAK   1.4

#ulaz iz tacke 1.3
def fun4(data):
    cell, value = data
    global my_dictionary
    return cell, math.sqrt(value) 

def standardnaDevijacija14(data):
    
    d=list(map(fun4, data))  
    return d
    

#  ZADATAK   1.5



def fun5(data):
    cell, gene, value = data
    global my_dictionary
    global my_dictionary_dev
    return cell, gene, (value-my_dictionary[cell])/my_dictionary_dev[cell]


def standardnavrednost15(data):
    res=map(fun5, data)
    return list(res)


#  ZADATAK   2.1



def fun6(array, x):
    array.append(array[-1]+(float(x[2])-my_dictionary[x[0]])**2)
    return array

def zamenigencelija(data):
    cell,gene,value=data
    return gene,cell,value


def varijansagena21(data):
   
    a_sort = sorted(data, key=lambda x: x[1])

    b = list(map(zamenigencelija,a_sort))
    
    tuples=SrednjaVrednost11(b)
    global my_dictionary
    my_dictionary = {k: v for k, v in tuples}  #Postaje   gen vrednost
    return Varijansa13(CentriranjeEkspresije12(b)) 

    #for k, v in b:
    #    temp=list(v)
    #    d = functools.reduce(fun6, temp, [0.0])
    #    tuple=(k,d[-1]/(len(d)-2))
    #    tiplets.append(tuple)

    #return a_sort


#  ZADATAK   2.2

def fun7(array,x):
    array.append(array[-1]+float(x[1]))
    return array



def standDevGena22(data):

    tiplets=[]

    b = groupby(data, key=lambda x: x[0])
    
    for k, v in b:
        temp=list(v)
        print(temp[0])
        d = functools.reduce(fun7, temp, [0.0])
        tuple=(k,d[-1]/(len(d)-1))
        tiplets.append(tuple)

    return(sorted(tiplets, key = lambda x : x[1])[:500])



#  ZADATAK 2.3

def fun8(array,x):
    global my_dictionarygene
    if x[1] in my_dictionarygene:
        array.append(x)

    return array

def filtriratiniz23(data):
    tuples=standDevGena22(data)
    global my_dictionarygene
    my_dictionarygene = {k: v for k, v in tuples}
    d = functools.reduce(fun8, data, [])


#  ZADATAK 2.4

def sortvrednosti24(data):
    list1 = sorted(data, key = lambda x: (x[0], -x[2]))
    return list1

#  ZADATAK 2.5


def fun10(array,x):
    cell,gene,value=x
    tuptup=cell,gene,value,(array[-1])[3]-1
    array.append(tuptup)
def ranknormalizacija25(data):
    tiplets=[]
    
    b = groupby(data, key=lambda x: x[1])
    for k, v in b:
        temp=list(v)
        d = functools.reduce(fun10, temp, ["G","C",0,len(temp)+1])
        d.pop(0)
        tiplets.append(d)
    
    return tiplets
#  ZADATAK 2.6

def fun9(data):
    celija, gen, originalnavrednost, rankvrednost=data
    return celija, gen, rankvrednost

def izbaciorig26(data):
    res=map(fun9, data)




df = pd.read_table('ekspresije.tsv', index_col=0)
data = [(cell, gene, value) for cell in df.columns 
                            for gene, value in df[cell].items()]

embedding = pd.read_table('umap.tsv')
embedding['cluster'] = 0
plt.figure(figsize=(8, 6))
plt.scatter(
    embedding.umap1,
    embedding.umap2,
    c=[sn.color_palette()[x] for x in embedding.cluster]
)


def pozivanje20(data):
    tuples1=SrednjaVrednost11(data)
    global my_dictionary
    my_dictionary = {k: v for k, v in tuples1}
    data=CentriranjeEkspresije12(data)
    tuples2=standardnaDevijacija14(Varijansa13(data))  
    global my_dictionary_dev
    my_dictionary_dev = {k: v for k, v in tuples2}
    return standardnavrednost15(data)


#POZIVI
#1 ZADATAK
ulaz = input()
global my_dictionary
global my_dictionary_dev
global my_dictionarygene

if(ulaz=="1.1"):
   print(SrednjaVrednost11(data))
elif(ulaz=="1.2"):
    tuples=SrednjaVrednost11(data)
    my_dictionary = {k: v for k, v in tuples}
    print(CentriranjeEkspresije12(data))              #Mozda treba apsolutna od rezultata
elif(ulaz=="1.3"):
    tuples=SrednjaVrednost11(data)
    my_dictionary = {k: v for k, v in tuples}
    print(Varijansa13(CentriranjeEkspresije12(data))) 
elif(ulaz=="1.4"):
    tuples=SrednjaVrednost11(data)
    my_dictionary = {k: v for k, v in tuples}
    print(standardnaDevijacija14(Varijansa13(data)))  
elif(ulaz=="1.5"):
    tuples1=SrednjaVrednost11(data)
    my_dictionary = {k: v for k, v in tuples1}
    data=CentriranjeEkspresije12(data)
    tuples2=standardnaDevijacija14(Varijansa13(data))  
    my_dictionary_dev = {k: v for k, v in tuples2}
    print(standardnavrednost15(data))
      

#2 ZADATAK

elif(ulaz=="2.1"):
    data=pozivanje20(data)
    print(varijansagena21(data))                      # da li se koristi za jos nesto?
elif(ulaz=="2.2"):
    data=pozivanje20(data)
    print(standDevGena22(varijansagena21(data)))  
elif(ulaz=="2.3"):
    data=pozivanje20(data)
    tuples3=standDevGena22(varijansagena21(data))
    my_dictionarygene = {k: v for k, v in tuples3}
    print(filtriratiniz23(data))
elif(ulaz=="2.4"):
    data=pozivanje20(data)
    tuples3=standDevGena22(varijansagena21(data))
    my_dictionarygene = {k: v for k, v in tuples3}
    print(sortvrednosti24(filtriratiniz23(data)))  
elif(ulaz=="2.5"):
    data=pozivanje20(data)
    tuples3=standDevGena22(varijansagena21(data))
    my_dictionarygene = {k: v for k, v in tuples3}
    print(ranknormalizacija25(sortvrednosti24(filtriratiniz23(data))))  
elif(ulaz=="2.6"):
    data=pozivanje20(data)
    tuples3=standDevGena22(varijansagena21(data))
    my_dictionarygene = {k: v for k, v in tuples3}
    print(izbaciorig26(ranknormalizacija25(sortvrednosti24(filtriratiniz23(data)))))    

     