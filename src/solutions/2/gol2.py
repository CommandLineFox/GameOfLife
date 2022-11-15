from multiprocessing import Process, Queue


class Celija:
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value
        self.susedi = 0
        self.procitani = 0
        self.iteracija = 0
        self.conn1 = []
        self.conn2 = []

    def __str__(self):
        return f"{self.value}"


class Red:
    def __init__(self, queue, x1, y1, x2, y2):
        self.queue = queue
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2


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


def izvuciredove(nizredova, i, j):

    brojac = 0
    for red in nizredova:
        if (red.x1 == i and red.y1 == j) or (red.x2 == i and red.y2 == j):
            brojac += 1


def slucaj(i, j, mat, vp, nizredova):

    c = mat[i][j]

    broj_suseda = 0

    for red in nizredova:
        if (red.x1 == i and red.y1 == j):
            red.queue.put(c.value)
           # print("Red je %s i %s =====  %s i %s  Upisuje %s" % (red.x1, red.y1,red.x2, red.y2,c.value))

    for red in nizredova:
        if (red.x2 == i and red.y2 == j):
            b = red.queue.get()
           # print("Red je %s i %s =====  %s i %s  Ispisuje %s" % (red.x1, red.y1,red.x2, red.y2,b))
            if b == 1:
                broj_suseda += 1

    if (broj_suseda < 2 or broj_suseda > 3):
        c.value = 0
    elif (broj_suseda == 3):
        c.value = 1
    vp.put(c.value)


def IgraZivota(mat, n, m, nizredova):

    multiprocessing = []
    vrednost_polja = []

    for i in range(n):
        for j in range(m):
            vp = Queue()
            vrednost_polja.append(vp)
            p = Process(target=slucaj, args=(i, j, mat, vp, nizredova,))
            p.start()
            multiprocessing.append(p)

    for tr in multiprocessing:
        tr.join()

    brojevi = []
    for vp in vrednost_polja:
        brojopet = vp.get()
        brojevi.append(brojopet)

    br = 0
    for i in range(n):
        for j in range(m):
            mat[i][j].value = brojevi[br]
            br += 1

    ispis_matrice(mat, n, m)


def DodajSusede(mat, n, m):
    for i in range(n):
        for j in range(m):
            if (i == 0 and j == 0) or (i == n-1 and j == 0) or (i == 0 and j == m-1) or (i == n-1 and j == 0):
                mat[i][j].susedi = 3
            elif i == 0 or j == 0 or i == n-1 or j == m-1:
                mat[i][j].susedi = 5
            else:
                mat[i][j].susedi = 8


def PopuniQueueMultiProcessing(mat, n, m):

    nizredova = []
    for i in range(n):
        for j in range(m):

            if j < m-1 and i < n-1:
                queue = Queue(maxsize=1)
                nizredova.append(Red(queue, i+1, j+1, i, j))
                queue = Queue(maxsize=1)
                nizredova.append(Red(queue, i, j, i+1, j+1))

            if j < m-1:
                queue = Queue(maxsize=1)
                nizredova.append(Red(queue, i, j+1, i, j))
                queue = Queue(maxsize=1)
                nizredova.append(Red(queue, i, j, i, j+1))

            if i < n-1:
                queue = Queue(maxsize=1)
                nizredova.append(Red(queue, i+1, j, i, j))
                queue = Queue(maxsize=1)
                nizredova.append(Red(queue, i, j, i+1, j))

            if j > 0 and i < n-1:
                queue = Queue(maxsize=2)
                nizredova.append(Red(queue, i+1, j-1, i, j))
                queue = Queue(maxsize=1)
                nizredova.append(Red(queue, i, j, i+1, j-1))

    return nizredova


if __name__ == '__main__':
    n = int(input("Enter the number of rows: "))
    m = int(input("Enter the number of columns: "))
    mat = upis_matrice(n, m)
    DodajSusede(mat, n, m)
    nizredova = PopuniQueueMultiProcessing(mat, n, m)

    ispis_matrice(mat, n, m)
    IgraZivota(mat, n, m, nizredova)
