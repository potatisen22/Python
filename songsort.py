from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
gauth.LocalWebserverAuth()

drive = GoogleDrive(gauth)
import timeit
class song():
    def __init__(self,trackid,latid,artist,song):
        self.song = song
        self.tid = latid
        self.id = trackid
        self.artist = artist
    def __lt__(self, other):
        if self < other:
            return True
        return False

def upload(fil):
    file2 = drive.CreateFile()
    file2.SetContentFile(fil)
    file2.Upload()
    print('Created file %s with mimeType %s' % (file2['title'],
    file2['mimeType']))

def writefile(quicksort,linjtid,bintid,dictid,antal_element):
    with open("utskrift.txt","a",encoding = "utf-8") as utskrift:
        utskrift.write("antal element är: " + str(antal_element) + "\n")
        utskrift.write("Linjärsökning tog: " + str(linjtid) + " sekunder\n")
        utskrift.write("sorteringen tog: " + str(quicksort) +  " sekunder\n")
        utskrift.write("Binärsökning tog: " + str(bintid) + " sekunder\n")
        utskrift.write("Element sökning i dictionary tog: " + str(dictid) + " sekunder\n")
        utskrift.write("\n-----------------------\n")


def fillasning(filnamn,antalrader):
    objlista=[]
    objdict={}
    radnr = 0
    with open(filnamn, "r", encoding = "utf-8") as songfile: #inläsning
        for line in songfile:
            if antalrader <= radnr:
                return objdict,objlista
            lista = line.strip().split("<SEP>")
            objekt = song(lista[0],lista[1],lista[2],lista[3])
            objlista.append(objekt) # sparas i en lista
            objdict[objekt.artist] = objekt
            radnr=radnr+1
    return objdict,objlista


def binsearch(inlist,searched):
    low = 0
    high = len(inlist)-1
    found = False

    while low <= high and not found:
        middle = (low + high)//2
        if inlist[middle].artist == searched:
            found = True
        else:
            if searched < inlist[middle].artist:
                high = middle - 1
            else:
                low = middle + 1
    return found


def linesearch(inlist,searched):
    for object in inlist:
        if object.artist == searched:
            return True
    return False


def quicksort(data): #taget från föreläsningsanteckningar
    sista = len(data) - 1
    return qsort(data, 0, sista)


def qsort(data, low, high):#taget från föreläsningsanteckningar
    pivotindex = (low+high)//2
    # flytta pivot till kanten
    data[pivotindex], data[high] = data[high], data[pivotindex]

    # damerna först med avseende på pivotdata
    pivotmid = partitionera(data, low-1, high, data[high].artist)

    # flytta tillbaka pivot
    data[pivotmid], data[high] = data[high], data[pivotmid]

    if pivotmid-low > 1:
        qsort(data, low, pivotmid-1)
    if high-pivotmid > 1:
        qsort(data, pivotmid+1, high)
    return data


def partitionera(data, v, h, pivot):#taget från föreläsningsanteckningar
    while True:
        v = v + 1
        while data[v].artist < pivot:
            v = v + 1
        h = h - 1
        while h != 0 and data[h].artist > pivot:
            h = h - 1
        data[v], data[h] = data[h], data[v]
        if v >= h:
            break
    data[v], data[h] = data[h], data[v]
    return v


def main():
    open('utskrift.txt', 'w').close()
    filnamn="unique_tracks.txt"
    for antal in range(0,4):
        antal = 10**(antal)
        objdict,objlista=fillasning(filnamn,antal)
        antal_element = len(objlista)
        print("Antal element =", antal_element)
        sista = objlista[antal_element-1]
        testartist = sista.artist
        qsortering=timeit.timeit(stmt=lambda:quicksort(objlista),number = 1000)
        qsortering = round(qsortering,4)
        sortlista = quicksort(objlista) #problematiskt här då vi ska sortera efter artist och sorterar efter objekt atm, blir jobbigt
        linjtid = timeit.timeit(stmt = lambda: linesearch(objlista, testartist), number = 1000)
        linjtid = round(linjtid,4)
        bintid = timeit.timeit(stmt=lambda:binsearch(sortlista,testartist), number = 1000)
        bintid=round(bintid,4)
        dictid = timeit.timeit(stmt=lambda:objdict[testartist])
        dictid=round(dictid,4)
        writefile(qsortering,linjtid,bintid,dictid,antal_element)
    upload("utskrift.txt")
if __name__ == '__main__':
    main()
