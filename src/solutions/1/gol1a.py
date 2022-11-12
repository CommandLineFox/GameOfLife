from threading import Lock, Thread


class Celija:
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value
        self.susedi = 0
        self.procitani = 0
        self.iteracija = 0

    def __str__(self):
        return f"{self.value}"


class Cekaonica:
    def __init__(self, n, m):
        self.brojnitiusle = 0
        self.brojnitiizasle = n*m
        self.trajeproces = True


def upis_matrice(n, m):
    mat = []
    for i in range(n):
        cur = []
        for j in range(m):
            c = Celija(i, j, int(input()))
            cur.append(c)
        mat.append(cur)
    return mat


def ispis_matrice(mat, m, n):
    for i in range(n):
        for j in range(m):
            print(mat[i][j], end=" ")
        print()


def proveri_polje(mat, i, j, n, m):
    if i < 0 or i >= n or j < 0 or j >= m:
        return 0
    c = mat[i][j]
    if c.value == 1:
        return 1
    return 0


def vrati_broj_suseda(mat, i, j, n, m):
    broj_suseda = 0
    for k in range(i - 1, i + 2):
        for l in range(j - 1, j + 2):
            if (k != i or l != j) and proveri_polje(mat, k, l, n, m) == 1:
                broj_suseda += 1
    return broj_suseda


def slucaj(mat, i, j, n, m, cekaonica, lock):

    c = mat[i][j]

    broj_suseda = vrati_broj_suseda(mat, i, j, n, m)

    cekaonica.brojnitiusle += 1
    if (cekaonica.trajeproces == True):
        cekaonica.trajeproces = False

    # Zakljucaj kada svi udju

    while True:
        if cekaonica.brojnitiusle == n*m and cekaonica.trajeproces == False:
            acquired = lock.acquire(blocking=False)
            if acquired:
                break

    # KADA POSLEDNJI UDJE RESETUJE TRAJANJE PROCESA I BROJ UNETIH
    global brojac
    brojac += 1
    if (brojac == n*m):
        cekaonica.brojnitiusle = 0
        cekaonica.trajeproces = True

    if (broj_suseda < 2 or broj_suseda > 3):
        c.value = 0
    elif (broj_suseda == 3):
        c.value = 1

    cekaonica.brojnitiizasle -= 1
    lock.release()


def IgraZivota(mat, n, m):

    threads = []
    lock = Lock()
    global brojac
    brojac = 0
    cekaonica = Cekaonica(n, m)
    for i in range(n):
        for j in range(m):
            t = Thread(target=slucaj, args=[mat, i, j, n, m, cekaonica, lock])
            t.start()
            threads.append(t)

    # Kada sve niti izadju iz prve iteracije krece sledeca
    while True:
        if cekaonica.brojnitiizasle == 0:
            for tr in threads:
                tr.join()
            break


def DodajSusede(mat, n, m):
    for i in range(n):
        for j in range(m):
            if (i == 0 and j == 0) or (i == n-1 and j == 0) or (i == 0 and j == m-1) or (i == n-1 and j == 0):
                mat[i][j].susedi = 3
            elif i == 0 or j == 0 or i == n-1 or j == m-1:
                mat[i][j].susedi = 5
            else:
                mat[i][j].susedi = 8


def main():
    n = int(input("Enter the number of rows: "))
    m = int(input("Enter the number of columns: "))
    mat = upis_matrice(n, m)
    DodajSusede(mat, n, m)

    ispis_matrice(mat, n, m)
    IgraZivota(mat, n, m)
    ispis_matrice(mat, n, m)


main()
