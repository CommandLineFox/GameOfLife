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
    tiplets = []
    b = groupby(data, key=lambda x: x[0])

    for k, v in b:
        temp = list(v)
        d = functools.reduce(fun1, temp, [0.0])
        tuple = (k, d[-1]/(len(d)-1))
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

    tiplets = []
    b = groupby(data, key=lambda x: x[0])

    for k, v in b:
        temp = list(v)
        d = functools.reduce(fun3, temp, [0.0])
        tuple = (k, d[-1]/(len(d)-2))
        tiplets.append(tuple)

    return tiplets


#  ZADATAK   1.4

# ulaz iz tacke 1.3
def fun4(data):
    cell, value = data
    global my_dictionary
    return cell, math.sqrt(value)


def standardnaDevijacija14(data):
    d = list(map(fun4, data))
    return d


#  ZADATAK   1.5


def fun5(data):
    cell, gene, value = data
    global my_dictionary
    global my_dictionary_dev
    return cell, gene, (value-my_dictionary[cell])/my_dictionary_dev[cell]


def standardnavrednost15(data):
    res = map(fun5, data)
    return list(res)


#  ZADATAK   2.1


def fun6(array, x):
    array.append(array[-1]+(float(x[2])-my_dictionary[x[0]])**2)
    return array


def zamenigencelija(data):
    cell, gene, value = data
    return gene, cell, value


def varijansagena21(data):

    tuples = SrednjaVrednost11(data)
    global my_dictionary
    my_dictionary = {k: v for k, v in tuples}  # Postaje gen vrednost
    return Varijansa13(CentriranjeEkspresije12(data))

    # for k, v in b:
    #    temp=list(v)
    #    d = functools.reduce(fun6, temp, [0.0])
    #    tuple=(k,d[-1]/(len(d)-2))
    #    tiplets.append(tuple)

    # return a_sort


#  ZADATAK   2.2

def fun7(array, x):
    if(array[0] < 500):
        array[0] += 1
        array.append(x[0])
    return array


def standDevGena22(data):
    data = sorted(data, key=lambda x: x[1])
    d = functools.reduce(fun7, data, [0])
    d.pop(0)
    return d


#  ZADATAK 2.3

def fun8(array, x):
    global my_dictionarygene
    if x[0] in my_dictionarygene:
        array.append(x)

    return array


def filtriratiniz23(data):
    d = functools.reduce(fun8, data, [])
    return d

#  ZADATAK 2.4


def sortvrednosti24(data):
    list1 = sorted(data, key=lambda x: (x[0], -x[2]))
    return list1

#  ZADATAK 2.5


def fun10(array, x):
    cell, gene, value = x
    vrednost = ((array[-1])[3])-1
    tuptup = cell, gene, value, vrednost
    array.append(tuptup)
    return array


def ranknormalizacija25(data):
    tiplets = []

    b = groupby(data, key=lambda x: x[0])
    for k, v in b:
        temp = list(v)

        d = functools.reduce(fun10, temp, [("G", "C", 0, len(temp)+1)])
        if d is None:
            continue
        d.pop(0)
        tiplets += d

    return tiplets
#  ZADATAK 2.6


def fun9(data):
    q, b, c, d = data
    return q, b, d


def izbaciorig26(data):
    res = list(map(fun9, data))
    return res


#  ZADATAK 3.1

def fun11(array, x):
    cell, gene, value = x
    tuptup = gene, value
    array.append(tuptup)
    return array


def grupisicelija31(data):
    tiplets = []

    data = groupby(data, key=lambda x: x[1])
    for k, v in data:
        temp = list(v)

        d = functools.reduce(fun10, temp, [])
        tipl = k, d
        tiplets.append(tipl)
    return tiplets


#  ZADATAK 3.2


df = pd.read_table('ekspresije.tsv', index_col=0)
data = [(cell, gene, value) for cell in df.columns
        for gene, value in df[cell].items()]

embedding = pd.read_table('umap.tsv')
embedding['cluster'] = 0
palette = [(0.12156862745098039, 0.4666666666666667, 0.7058823529411765),
           (1.0, 0.4980392156862745, 0.054901960784313725),
           (0.17254901960784313, 0.6274509803921569, 0.17254901960784313),
           (0.8392156862745098, 0.15294117647058825, 0.1568627450980392),
           (0.5803921568627451, 0.403921568627451, 0.7411764705882353),
           (0.5490196078431373, 0.33725490196078434, 0.29411764705882354),
           (0.8901960784313725, 0.4666666666666667, 0.7607843137254902),
           (0.4980392156862745, 0.4980392156862745, 0.4980392156862745),
           (0.7372549019607844, 0.7411764705882353, 0.13333333333333333),
           (0.09019607843137255, 0.7450980392156863, 0.8117647058823529)]

plt.figure(figsize=(8, 6))
plt.scatter(
    embedding.umap1,
    embedding.umap2,
    c=list(palette[x] for x in embedding.cluster)
)


def pozivanje20(data):
    tuples1 = SrednjaVrednost11(data)
    global my_dictionary
    my_dictionary = {k: v for k, v in tuples1}
    data = CentriranjeEkspresije12(data)
    tuples2 = standardnaDevijacija14(Varijansa13(data))
    global my_dictionary_dev
    my_dictionary_dev = {k: v for k, v in tuples2}
    data = standardnavrednost15(data)
    a_sort = sorted(data, key=lambda x: x[1])
    data = list(map(zamenigencelija, a_sort))
    return data


# POZIVI
# 1 ZADATAK
ulaz = input()
global my_dictionary
global my_dictionary_dev
global my_dictionarygene

if(ulaz == "1.1"):
    print(SrednjaVrednost11(data))
elif(ulaz == "1.2"):
    tuples = SrednjaVrednost11(data)
    my_dictionary = {k: v for k, v in tuples}
    print(CentriranjeEkspresije12(data))  # Mozda treba apsolutna od rezultata
elif(ulaz == "1.3"):
    tuples = SrednjaVrednost11(data)
    my_dictionary = {k: v for k, v in tuples}
    print(Varijansa13(CentriranjeEkspresije12(data)))
elif(ulaz == "1.4"):
    tuples = SrednjaVrednost11(data)
    my_dictionary = {k: v for k, v in tuples}
    print(standardnaDevijacija14(Varijansa13(data)))
elif(ulaz == "1.5"):
    tuples1 = SrednjaVrednost11(data)
    my_dictionary = {k: v for k, v in tuples1}
    data = CentriranjeEkspresije12(data)
    tuples2 = standardnaDevijacija14(Varijansa13(data))
    my_dictionary_dev = {k: v for k, v in tuples2}
    print(standardnavrednost15(data))


# 2 ZADATAK

elif(ulaz == "2.1"):
    data = pozivanje20(data)
    print(varijansagena21(data))
elif(ulaz == "2.2"):
    data = pozivanje20(data)
    print(standDevGena22(varijansagena21(data)))
elif(ulaz == "2.3"):
    data = pozivanje20(data)
    my_dictionarygene = standDevGena22(varijansagena21(data))
    print(filtriratiniz23(data))
elif(ulaz == "2.4"):
    data = pozivanje20(data)
    my_dictionarygene = standDevGena22(varijansagena21(data))
    print(sortvrednosti24(filtriratiniz23(data)))
elif(ulaz == "2.5"):
    data = pozivanje20(data)
    my_dictionarygene = standDevGena22(varijansagena21(data))
    print(ranknormalizacija25(sortvrednosti24(filtriratiniz23(data))))
elif(ulaz == "2.6"):
    data = pozivanje20(data)
    my_dictionarygene = standDevGena22(varijansagena21(data))
    print(izbaciorig26(ranknormalizacija25(sortvrednosti24(filtriratiniz23(data)))))


# 3 ZADATAK

elif(ulaz == "3.1"):
    data = pozivanje20(data)
    my_dictionarygene = standDevGena22(varijansagena21(data))
    print(grupisicelija31(izbaciorig26(ranknormalizacija25(
        sortvrednosti24(filtriratiniz23(data))))))
