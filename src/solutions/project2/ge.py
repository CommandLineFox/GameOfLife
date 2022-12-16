import pandas as pd
import matplotlib.pyplot as plt
import functools
from itertools import groupby
import math
import random
import csv


#   ZADATAK   1.1
def reduce_srednja_vrednost(niz, x):
    niz.append(niz[-1]+float(x[2]))
    return niz


def srednja_vrednost_11(data):
    tupleti = []
    b = groupby(data, key=lambda x: x[0])

    for k, v in b:
        temp = list(v)
        d = functools.reduce(reduce_srednja_vrednost, temp, [0.0])
        tuple = (k, d[-1]/(len(d)-1))
        tupleti.append(tuple)

    return tupleti


#  ZADATAK   1.2
def map_centriranje_ekspresija(niz):
    celija, gen, vrednost = niz
    global vrednosti
    return celija, gen, round(vrednost-vrednosti[celija], 2)


def centriranje_ekspresija_12(data):
    b = map(map_centriranje_ekspresija, data)
    return list(b)


#  ZADATAK   1.3
def reduce_varijansa(niz, x):
    niz.append(niz[-1]+(float(x[2])-vrednosti[x[0]])**2)
    return niz


def varijansa_13(data):
    tupleti = []
    b = groupby(data, key=lambda x: x[0])

    for k, v in b:
        temp = list(v)
        d = functools.reduce(reduce_varijansa, temp, [0.0])
        tuple = (k, d[-1]/(len(d)-2))
        tupleti.append(tuple)

    return tupleti


#  ZADATAK   1.4
# ulaz iz tacke 1.3
def map_standardna_devijacija(data):
    celija, vrednost = data
    global vrednosti
    return celija, math.sqrt(vrednost)


def standardna_devijacija_14(data):
    d = list(map(map_standardna_devijacija, data))
    return d


#  ZADATAK   1.5
def map_standardna_vrednost(data):
    celija, gen, vrednost = data
    global vrednosti
    global vrednosti_dev
    return celija, gen, (vrednost-vrednosti[celija])/vrednosti_dev[celija]


def standardna_vrednost_15(data):
    rezultat = map(map_standardna_vrednost, data)
    return list(rezultat)


#  ZADATAK   2.1
def zameni_gen_celija(data):
    celija, gen, vrednost = data
    return gen, celija, vrednost


def varijansa_gena_21(data):
    tuples = srednja_vrednost_11(data)
    global vrednosti
    vrednosti = {k: v for k, v in tuples}  # Postaje gen vrednost
    return varijansa_13(centriranje_ekspresija_12(data))


#  ZADATAK   2.2
def reduce_standardna_devijacija_gena(niz, x):
    if(niz[0] < 500):
        niz[0] += 1
        niz.append(x[0])
    return niz


def standardna_devijacija_gena_22(data):
    data = sorted(data, key=lambda x: x[1])
    d = functools.reduce(reduce_standardna_devijacija_gena, data, [0])
    d.pop(0)
    return d


#  ZADATAK 2.3
def reduce_filtriranje_niza(niz, x):
    global vrednosti_geni
    if x[0] in vrednosti_geni:
        niz.append(x)

    return niz


def filtriranje_niza_23(data):
    d = functools.reduce(reduce_filtriranje_niza, data, [])
    return d


#  ZADATAK 2.4
def sortiranje_vrednosti_24(data):
    list1 = sorted(data, key=lambda x: (x[0], -x[2]))
    return list1


#  ZADATAK 2.5
def reduce_normalizacija(niz, x):
    celija, gen, original = x
    vrednost = ((niz[-1])[3])-1
    tuptup = celija, gen, original, vrednost
    niz.append(tuptup)
    return niz


def rank_normalizacija_25(data):
    tupleti = []

    b = groupby(data, key=lambda x: x[0])
    for k, v in b:
        temp = list(v)

        d = functools.reduce(reduce_normalizacija, temp, [
                             ("G", "C", 0, len(temp)+1)])
        if d is None:
            continue
        d.pop(0)
        tupleti += d

    return tupleti


#  ZADATAK 2.6
def map_izbaci_original(data):
    q, b, _, d = data
    return q, b, d


def izbaci_original_26(data):
    rezultat = list(map(map_izbaci_original, data))
    return rezultat


#  ZADATAK 3.1

def reduce_grupisi_celije(niz, x):
    _, _, vrednost = x
    niz.append(vrednost)
    return niz


def grupisi_celije_31(data):
    tupleti = []

    data = sorted(data, key=lambda x: (x[1], x[0]))
    data = groupby(data, key=lambda x: x[1])
    for k, v in data:
        temp = list(v)
        d = functools.reduce(reduce_grupisi_celije, temp, [])
        tupl = k, d
        tupleti.append(tupl)
    return tupleti


#  ZADATAK 3.2
df = pd.read_table('ekspresije.tsv', index_col=0)
data = [(celija, gen, vrednost) for celija in df.columns
        for gen, vrednost in df[celija].items()]


def pozivanje20(data):
    tuples1 = srednja_vrednost_11(data)
    global vrednosti
    vrednosti = {k: v for k, v in tuples1}
    data = centriranje_ekspresija_12(data)
    tuples2 = standardna_devijacija_14(varijansa_13(data))
    global vrednosti_dev
    vrednosti_dev = {k: v for k, v in tuples2}
    data = standardna_vrednost_15(data)
    a_sort = sorted(data, key=lambda x: x[1])
    data = list(map(zameni_gen_celija, a_sort))
    return data


global vrednosti
global vrednosti_dev
global vrednosti_geni

data = pozivanje20(data)
vrednosti_geni = standardna_devijacija_gena_22(varijansa_gena_21(data))

data = filtriranje_niza_23(data)
data = sortiranje_vrednosti_24(data)
data = rank_normalizacija_25(data)
data = izbaci_original_26(data)
data = grupisi_celije_31(data)


#  ZADATAK 3.2
prvacelija, prvevrednosti = data[0]
dimenzije = len(prvevrednosti)
klasteri = 10


def generisi_centroide(centroidi):
    centroidi = [random.randint(5, 100) for _ in range(dimenzije)]
    return centroidi


def nadji_najblizi_centroid(data):
    celija, vrednosti = data
    rezultat = (celija, 0, 1000000)
    for x in range(klasteri):
        sum = 0
        for vrednost, centroid in zip(vrednosti, centroidi[x]):
            sum = sum + (centroid - vrednost)*(centroid - vrednost)
        if(math.sqrt(sum) < rezultat[2]):
            rezultat = celija, x, math.sqrt(sum)
    return rezultat[0], rezultat[1], vrednosti


def pomeri_centroid(niz, vrednost):
    if(niz[-1] == vrednost[1]):
        niz[-2] += 1
        for i in range(len(niz[niz[-1]])):
            niz[niz[-1]][i] += vrednost[2][i]
    else:
        niz[niz[-1]] = list(map(lambda x: x/niz[-2], niz[niz[-1]]))
        niz[-1] += 1
        niz[-2] = 1
        for i in range(len(niz[niz[-1]])):
            niz[niz[-1]][i] += vrednost[2][i]
    return niz


centroidi = []
centroidi.extend([] for _ in range(klasteri))
najblizi_centroidi = centroidi

centroidi = list(map(generisi_centroide, centroidi))

for _ in range(10):
    najblizi_centroidi = list(map(nadji_najblizi_centroid, data))
    najblizi_centroidi.sort(key=lambda x: x[1])

    centroidi.append(1)  # type: ignore
    centroidi.append(0)  # type: ignore
    centroidi = functools.reduce(
        pomeri_centroid, najblizi_centroidi, centroidi)  # type: ignore
    centroidi[centroidi[-1]
              ] = list(map(lambda x: x/centroidi[-2], centroidi[centroidi[-1]]))  # type: ignore
    centroidi.pop(-1)
    centroidi.pop(-1)

boje = ["red", "blue", "green", "purple", "brown",
        "black", "yellow", "orange", "pink", "grey"]

flag = True
embedding = []
with open('umap.tsv') as file:
    tsv_file = csv.reader(file, delimiter="\t")
    for line in tsv_file:
        if(line[0] == "cell"):
            continue
        embedding.append([line[0], float(line[1]), float(line[2])])
embedding.pop(0)

mapa_centroida = dict((x[0], x[1]) for x in najblizi_centroidi)

c = ["red", "blue", "green", "purple", "brown",
     "black", "yellow", "orange", "pink", "grey"]

for x in range(len(embedding)):
    plt.scatter(
        embedding[x][1],
        embedding[x][2],
        c=c[mapa_centroida[embedding[x][0]]])
