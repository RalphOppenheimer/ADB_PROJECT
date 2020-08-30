from tkinter import *
#import Backend
from Backend import Database # Import obiektu (klasy) Database z pliku database

#Funkcja przechwytująca zaznaczenie myszką w liście oraz zwracająca jego indeks.

database=Database("Books.db") # Utworzenie obiektu.
#Następnie zamieniam wszystko co było nazwane 'Backend' nazwą 'database'
#W backendzie jest opisane, po co wywołanie odbywa się z nazwą bazy danych
def get_selected_row(event):
    try:
        global selected_tuple
        index=listbox1.curselection()
        #Ponieważ metoda zwraca krotkę z indeksem zaznaczonego wiersza, stosuję zapis z indeksem [0] aby wyciągnąć liczbę
        selected_tuple=listbox1.get(index)
        #Poniższy kod wpisuje zawartość zaznaczenia w pola tekstowe
        e1.delete(0,END)
        e1.insert(END,selected_tuple[1])
        e2.delete(0,END)
        e2.insert(END,selected_tuple[2])
        e3.delete(0,END)
        e3.insert(END,selected_tuple[3])
        e4.delete(0,END)
        e4.insert(END,selected_tuple[4])
        #print(selected_tuple)
    except IndexError:
        pass
    #obsługa klikniecia w listę bez danych

def view_command():
    listbox1.delete(0, END) #Napierw jest kasowana obecna zawartość, a dopiero potem wpisywana wartość wyszukiwana
    #usuwane jest wszystko od 0 do końca
    for row in database.view():
        listbox1.insert(END,row) # każdy wiersz jest dodawnay na końcu

def search_command():
    listbox1.delete(0, END)#Napierw jest kasowana obecna zawartość, a dopiero potem wpisywana wartość wyszukiwana
    #usuwane jest wszystko od 0 do końca
    for row in database.search(title_text.get(),author_text.get(),year_text.get(),id_text.get()):
        listbox1.insert(END,row)
#database.search otrzymuje zmienne poprzez Dane wejścia w polach tekstowych (niżej są definicje)
#Ponieważ 'title_text', 'author_text'...etc. są typu StringVar, trzeba zastosować metodę '.get()', aby się dostać do surowego tekstu

def entry_command():
    database.insert(title_text.get(),author_text.get(),year_text.get(),id_text.get())
    #poniższa część kodu jest opcjonalna (wyświetla wprowadznie jako potwerdzenie dodania wpisu do bazy)
    listbox1.delete(0, END)
    listbox1.insert(END,(title_text.get(),author_text.get(),year_text.get(),id_text.get()))
    view_command()

#funkcja musi usuwać wpis z bazy na podstawie zaznaczonej pozycji
def delete_command():
    database.delete(selected_tuple[0])
    view_command()

def update_command():
    database.update(selected_tuple[0],title_text.get(),author_text.get(),year_text.get(),id_text.get())
    view_command()


window = Tk()
window.wm_title("Baza Danych")
#window.iconbitmap(default='iconfile.ico')

Grid.rowconfigure(window, 0, weight=1)
Grid.columnconfigure(window, 0, weight=1)

l1 = Label(window, text="Tytuł:")
l1.grid(row=0, column=0, sticky=N+S+E+W)
l2 = Label(window, text="Autor:")
l2.grid(row=0, column=2, sticky=N+S+E+W)
l3 = Label(window, text="Rok:", width=20)
l3.grid(row=1, column=0, sticky=N+S+E+W)
l4 = Label(window, text="ID:", width=20)
l4.grid(row=1, column=2, sticky=N+S+E+W)

#Dane wejścia w polach tekstowych
title_text = StringVar()
e1 = Entry(window, textvariable=title_text, width=20)
e1.grid(row=0, column=1, sticky=N+S+E+W)

author_text = StringVar()
e2 = Entry(window, textvariable=author_text, width=20)
e2.grid(row=0, column=3, sticky=N+S+E+W)

year_text = StringVar()
e3 = Entry(window, textvariable=year_text, width=20)
e3.grid(row=1, column=1, sticky=N+S+E+W)

id_text = StringVar()
e4 = Entry(window, textvariable=id_text, width=20)
e4.grid(row=1, column=3, sticky=N+S+E+W)


#Paraemtry okna wyświetlania oraz paska przeciągania (zachowanie w programie, rozmiar domyślny)
listbox1 = Listbox(window, height=25, width=44)
listbox1.grid(row=2, column=1, rowspan=9, columnspan=3, sticky=N+S+E+W)
scrollbar1 = Scrollbar(window)
scrollbar1.grid(row=2, rowspan=9, column=4, sticky=N+S+E+W)
#za pomocą rowspan regulujemy długośc paska przewijania okna
listbox1.configure(yscrollcommand=scrollbar1.set)
#za pomocą metody '.bind()' można wczytać id pozycji, która została wybrana myszką na liście 'listbox'
listbox1.bind('<<ListboxSelect>>', get_selected_row)
scrollbar1.configure(command=listbox1.yview)
#Ustawienia rozmiaru poszczególnych poszczególnych elementów za pomocą width
#sticky - oczywiste
b1 = Button(window, text="Pokaz wszystkie", width=20, command=view_command)
b1.grid(row=2, column=0, sticky=N+S+E+W)
b2 = Button(window, text="Szukaj", width=20, command=search_command)
b2.grid(row=3, column=0, sticky=N+S+E+W)
b3 = Button(window, text="Dodaj", width=20, command=entry_command)
b3.grid(row=4, column=0, sticky=N+S+E+W)
b4 = Button(window, text="Edytuj", width=20, command=update_command)
b4.grid(row=5, column=0, sticky=N+S+E+W)
b5 = Button(window, text="Usuń", width=20, command=delete_command)
b5.grid(row=6, column=0, sticky=N+S+E+W)
b6 = Button(window, text="Zamknij", width=20, command=window.destroy)
b6.grid(row=10, column=0, sticky=N+S+E+W)
#konfiguracja "rozciągalności kolumn i wierszy ze względu na wagę, czyli równomiernosci rozciągania"
window.grid_columnconfigure(0,weight=0)
window.grid_columnconfigure(1,weight=1)
window.grid_columnconfigure(2,weight=0)
window.grid_columnconfigure(3,weight=1)
window.grid_rowconfigure(0,weight=0)
window.grid_rowconfigure(1,weight=0)
window.grid_rowconfigure(2,weight=0)
window.grid_rowconfigure(3,weight=0)
window.grid_rowconfigure(9,weight=1)

window.mainloop()
