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


def reduceSrednjaVrednost(data):
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
    return cell, gene, abs(value-my_dictionary[cell])


def mapCentriranjeEkspresije(data):
    tuples = reduceSrednjaVrednost(data)
    global my_dictionary
    my_dictionary = {k: v for k, v in tuples}
    #dic = dict(map(lambda kv: (kv[0]+" "+kv[1], my_dictionary[kv[0]]), data))
    b = map(fun2, data)
    print(list(b))


#  ZADATAK   1.3


def fun3(array, x):
    array.append(array[-1]+(float(x[2])-my_dictionary[x[0]])**2)
    return array


def reduceVarijansa(data):
    tuples = reduceSrednjaVrednost(data)
    global my_dictionary
    my_dictionary = {k: v for k, v in tuples}

    tiplets = []
    b = groupby(data, key=lambda x: x[0])

    for k, v in b:
        temp = list(v)
        d = functools.reduce(fun3, temp, [0.0])
        tuple = (k, math.sqrt(d[-1]/(len(d)-1)))  # Mozda treba -2
        tiplets.append(tuple)

    return tiplets


#  ZADATAK   1.4


def fun4(data):
    tuples = reduceSrednjaVrednost(data)


def mapstandardnaDevijacija(data):
    tuples = reduceSrednjaVrednost(data)
    global my_dictionary
    my_dictionary = {k: v for k, v in tuples}

    tiplets = []
    b = groupby(data, key=lambda x: x[0])
    k, v = b
    for k, v in b:
        temp = list(v)
        d = map(fun4, temp)


df = pd.read_table('ekspresije.tsv', index_col=0)
data = [(cell, gene, value) for cell in df.columns
        for gene, value in df[cell].items()]

print(reduceVarijansa(data))
