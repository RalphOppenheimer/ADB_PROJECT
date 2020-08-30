import sqlite3


class Database:

    def __init__(self, db): #zmiast 'def connect()''
        #meotdy w klasie, również konstruktor, muszą mieć przekazany do siebie obiekt. W tym wypadku przekazujemy metodzie 'siebie samego', stąd uzycie 'self'
        #każda metoda musi być wywoływana z parametrem 'self', ponieważ metody muszą przyjmowac parametr wywołania metody.
        #można przekazywać różne parametry przy tworzeniu obiektu, lecz 'self' musi być argumentem
        #powyzej po przecinku przekazanie nazwy bazy danych co umożliwia wykonywanie operacje na różnych plikach (w jednym pliku moga byc inne ksiazki niz w drugiej)
        #stąd poniżej zamiana '"Books.db"' na 'db'
        conn=sqlite3.connect(db)
        cur=conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS book(index_ INTEGER PRIMARY KEY, title text, author text, year integer, ID integer)")
        conn.commit()
        conn.close()

    def insert(self, title,author, year, ID):
        conn=sqlite3.connect("books.db")
        cur=conn.cursor()
        cur.execute("INSERT INTO book VALUES(NULL,?,?,?,?)",(title, author, year, ID))
        conn.commit()
        conn.close()

    def view(self):
        conn=sqlite3.connect("books.db")
        cur=conn.cursor()
        cur.execute("SELECT * FROM book")
        rows=cur.fetchall()
        conn.close()
        return rows

    def search(self,title="",author="", year="", ID=""): #domyslne wartości argumentów w wypadku ich olania
        #czyli uwzglednienie przypadku w którym użytkownik przy wyszukaniu nie poda wszystkich danych
        conn=sqlite3.connect("books.db")
        cur=conn.cursor()
        cur.execute("SELECT * FROM book WHERE title=? OR author=? OR year=? OR ID=?", (title,author,year,ID))
        rows=cur.fetchall()
        conn.close()
        return rows

    def delete(self, index_):
        conn=sqlite3.connect("books.db")
        cur=conn.cursor()
        cur.execute("DELETE FROM book WHERE index_=?",(index_,))
        conn.commit()
        conn.close()

    def update(self, index_, title, author, year,ID): #W tej funkcji nie trzeba się martwić tym, że uzytkownik nie zdefiniuje innych parametrów
        #Jezlei jakies argumenty nie zostaną podane, wtedy po prostu te pozycje nie ulegną modyfikacji
        conn=sqlite3.connect("books.db")
        cur=conn.cursor()
        cur.execute("UPDATE book SET title=?,author=?,year=?,ID=? WHERE index_=?",(title, author, year, ID, index_))
        conn.commit()
        conn.close()

#######Poniższe funkcje nie są potrzebne przy klasie Database
#connect()
#insert("The sea","John Lemon", 1920, 2132342)
#print(view()) #'view()' zwraca tablicę krotek w których są zapisane dane.
#print(search(author="John Lemon"))
