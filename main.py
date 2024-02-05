import tkinter as tk
import hashlib
import style
import re
from db_connector import *
from tkinter import messagebox
from tkinter import ttk
#
#   Globale variablen
#
db = db_connect()
stylesheet = style.stylesheet()
#
#   Loggin der Mitarbeiter
#
class Login(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        # Login Fenster Erstellen
        tk.Tk.__init__(self, *args, **kwargs)
        main_frame = tk.Frame(self, bg = stylesheet.style["background"], height=431, width=626)
        main_frame.pack(fill="both", expand="true")

        # Login Fenster Style
        self.geometry("626x432") 
        self.resizable(0, 0) 
        title_styles = {"font": (stylesheet.style["font_type"], 16), 
                        "background": (stylesheet.style["background"])}
        
        # Login BOX Style 
        login_box = tk.Frame(main_frame, bg=stylesheet.style["background"], relief="sunken", bd=2)  
        login_box.place(rely=0.35, relx=0.175, height=130, width=400)

        # Login BOX Inhalt
        # lable Liste wird erstellt und positioniert
        lable_list = ["Nutzername:","Passwort:"]
        lable_list = create_lable(login_box,lable_list)

        for lable in range(len(lable_list)):
            lable_list[lable].grid(row=lable+1, column=0)
        
        #entry Liste wird erstellt und positioniert
        entry_list =["Nutzername:","Passwort:"]
        entry_list = create_entry(login_box,entry_list)
       
        for entry in range(len(entry_list)):
            entry_list[entry].grid(row=entry+1, column=1)
        
        # Überschrieft Label wird erstellt und positioniert
        titel_label = tk.Label(login_box, title_styles, text="Anmeldung")
        titel_label.grid(row=0, column=1, columnspan=1)

        # Buttons wird erstellt und positioniert
        login_button = ttk.Button(login_box, text="Anmelden", command=lambda: einloggen())
        login_button.place(rely=0.70, relx=0.50)

        regestrier_button = ttk.Button(login_box, text="Regestrieren", command=lambda: Registrierung())
        regestrier_button.place(rely=0.70, relx=0.75)
        
        #
        #Login Funtion
        #
        def einloggen():
            global mitarbeiter
            # Login Daten einlesen Passwort Hashen
            username = entry_list[0].get()
            password  = hexa_hash(entry_list[1].get().encode('utf-8'))
            #Login Daten Kontrolieren
            # Übergebene werte bei erfolgreihem Login 
            #   0 = Passwort
            #   1 = Vorname
            #   2 = Nachname
            #   3 = Email
            mitarbeiter= db.login(username, password)
            if mitarbeiter[0] != False:
                tk.messagebox.showinfo("Anmeldung erfolgreich", "Wilkommen {} {}".format(mitarbeiter[1], mitarbeiter[2]))
                root.deiconify()
                top.destroy()
            else:
                tk.messagebox.showerror("Information", "Falscher Nutzername oder Passwort")
#
#   Regestrierung von Mitarbeitern
#
class Registrierung(tk.Tk):

    def __init__(self, *args, **kwargs):
        # Regestrier Fenster erstellen
        global mitarbeiter
        tk.Tk.__init__(self, *args, **kwargs)
        side_frame = tk.Frame(self, bg = stylesheet.style["background"], height=400, width=600)
        side_frame.pack(fill="both", expand="true")
        
        # Regestrier Fenster Style
        side_frame.pack_propagate(0)
        side_frame.pack(fill="both", expand="true")
        self.geometry("600x400")
        self.resizable(0, 0)
        self.title("Registrierung")
        # Regestrierbox style
        regestrier_box = tk.Frame(side_frame, bg=stylesheet.style["background"], relief="sunken", bd=2)  
        regestrier_box.place(rely=0.075, relx=0.075, height=300, width=500)
        
        # Regestrier BOX Inhalt
        # lable Liste wird erstellt und positioniert
        lable_list = ["Neuer Nutzername:","Neues Passwort:","Vorname:","Nachname:","E-mail:"]
        lable_list = create_lable(regestrier_box,lable_list)
        
        for lable in range(len(lable_list)):
            lable_list[lable].grid(row=lable+1, column=0)
        
        # entry Liste wird erstellt und positioniert
        entry_list =["Neuer Nutzername:","Neues Passwort:","Vorname:","Nachname:","E-mail:"]
        entry_list = create_entry(regestrier_box,entry_list)
       
        for entry in range(len(entry_list)):
            entry_list[entry].grid(row=entry+1, column=1)
        
        # Button wird erstellt und positioniert
        button = ttk.Button(regestrier_box, text="Login erstellen", command=lambda: signup())
        button.grid(row=8, column=1)

        # signup funktion
        def signup():
            # Regestrierdaten Einlesen
            username = entry_list[0].get()
            passwort = entry_list[1].get()
            vorname = entry_list[2].get()
            nachname = entry_list[3].get()
            email = entry_list[4].get()
            # Testen Ob der Benutzername bereits vergeben ist
            validierung = db.user_validierung(username)
            if not validierung:
                tk.messagebox.showerror("Information", "Der Nutzer existiert bereits")
            else:
                # Mindestlänge vom Passwort Prüfen
                if len(passwort) > 5:
                    # Passwort Hashen und Daten in der Datenbank Speichern
                    passwort = hexa_hash(passwort.encode('utf-8'))
                    db.registrierung(username, passwort,vorname,nachname,email)
                    tk.messagebox.showinfo("Information", "Ihr Nutzername wurde angelegt")
                    Registrierung.destroy(self)

                else:
                    tk.messagebox.showerror("Information", "Das Passwort muss aus mindestens 6 Zeichen bestehen")
#
#   Erstellen und bearbeiten von Kunden
#
class Kunden_erstellen(tk.Tk):

    def __init__(self, kundendaten,*args, **kwargs):
        
        # übernahme der Kundendaten bei bearbeitung
        if len(kundendaten) > 0:
            global mitarbeiter
            values = kundendaten["values"]
            kunde_id = int(values[0])
            strasse , Hausnummer = values[5].split()
            plz , ort = values[6].split()
            self.kundendaten = [values[1],values[2],values[3],
                                values[4],strasse , Hausnummer 
                                ,plz,ort,values[7],
                                values[8],values[0]]
        # erstellen einer leeren Listen bei erstellung von Kunden    
        else:
            self.kundendaten = []
            
        # Regestrier Fenster erstellen
        tk.Tk.__init__(self, *args, **kwargs)
        add_frame = tk.Frame(self, bg = stylesheet.style["background"], height=400, width=600)
        add_frame.pack(fill="both", expand="true")
        
        # Regestrier Fenster Style
        add_frame.pack_propagate(0)
        add_frame.pack(fill="both", expand="true")
        self.geometry("600x400")
        self.resizable(0, 0)
        self.title("Kunden erstellen")
        
        # Regestrierbox style
        add_box = tk.Frame(add_frame, bg=stylesheet.style["background"], relief="sunken", bd=2)  
        add_box.place(rely=0.07, relx=0.08, height=350, width=500)
        
        # Regestrier BOX Inhalt
        # erstellen einer Dropdown Box für die anreder stadtart Value "keine Angaben"
        anrede_dropdown = ttk.Combobox(add_box,state="readonly",
        values=["Keine Angabe", "Herr", "Frau"])
        anrede_dropdown.grid(row="0", column="1")
        if self.kundendaten != []:
            anrede_dropdown.set(self.kundendaten[0])
        else:
            anrede_dropdown.set("Keine Angabe")    
        
        # label Liste wird erstellt und positioniert
        self.lable_list = ["Vorname:","Nachname:","Geburtsdatum:","Straße:","Hausnummer:","PLZ:","Ort:","Telefon:","E-mail:"]
        self.lable_list = create_lable(add_box,self.lable_list)

        for lable in range(len(self.lable_list)):
            self.lable_list[lable].grid(row=lable+1, column=0)
        
        self.entry_list =["Vorname:","Nachname:","Geburtsdatum:","Straße:","Hausnummer:","PLZ:","Ort:","Telefon:","E-mail:"]
        self.entry_list = create_entry(add_box,self.entry_list, self.kundendaten)
        
        # entry Liste wird erstellt und positioniert
        for entry in range(len(self.entry_list)):
            self.entry_list[entry].grid(row=entry+1, column=1)

        # löschen und ändern button erstellen wenn Kunden bearbeitet werden
        if self.kundendaten != []:
            button1 = ttk.Button(add_box, text="Kunden ändern", command=lambda: validation_check_kunde(True))
            button1.grid(row=11, column=1)
            button2 = ttk.Button(add_box, text="Kunden löschen", command=lambda: [Löschen(kunde_id), Kunden_erstellen.destroy(self)])
            button2.grid(row=11, column=0)
        # erstellen button wenn ein neuer kunde erstellt werden soll    
        else:
            button1 = ttk.Button(add_box, text="Kunden erstellen", command=lambda: validation_check_kunde())
            button1.grid(row=11, column=0)
        
        # funktion zur überprüfung der eingegebenen daten nach syntax fehler, und vollständigkeit
        def validation_check_kunde(chance = False):
            # algorytmen zur definition der syntaxen von datum, email und telefonnr
            regex_date = r'\b[0-9]{4,4}+-[0-9]{2,2}+-[0-9]{2,2}\b'
            regex_mail = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            regex_tel = r'\b[0-9./+]{6,}\b'
            
            # prüfung der entrys nach vollständigkeit und syntax
            if self.entry_list[0].get() == "":
                 tk.messagebox.showinfo("Information", "Bitte Vornamen eingeben")
            elif self.entry_list[1].get() == "": 
                tk.messagebox.showinfo("Information", "Bitte Nachnamen eingeben")
            elif self.entry_list[2].get() == "": 
                tk.messagebox.showinfo("Information", "Bitte Geburtsdatum eingeben")
            elif not (re.fullmatch(regex_date, self.entry_list[2].get())):  
                tk.messagebox.showinfo("Information", "Das eingegeben Geburtsdatum ist ungültig YYYY-MM-DD") 
            elif self.entry_list[3].get() == "": 
                tk.messagebox.showinfo("Information", "Bitte Straße eingeben")
            elif self.entry_list[4].get() == "": 
                tk.messagebox.showinfo("Information", "Bitte Hausnummer eingeben")
            elif self.entry_list[5].get() == "": 
                tk.messagebox.showinfo("Information", "Bitte PLZ eingeben")  
            elif self.entry_list[6].get() == "": 
                tk.messagebox.showinfo("Information", "Bitte Ort eingeben")
            elif not self.entry_list[7].get() == "" and not self.entry_list[7].get() == "None" and not (re.fullmatch(regex_tel, self.entry_list[7].get())):    
                    tk.messagebox.showinfo("Information", "Die eingegeben Telefonnummer ist ungültig")          
            elif not self.entry_list[8].get() == "" and not self.entry_list[8].get() == "None" and not  (re.fullmatch(regex_mail, self.entry_list[8].get())):
                    tk.messagebox.showinfo("Information", "Die eingegeben E-mail ist ungültig")     
            else:
                # aufruf der erstellklasse bei richtiger angabe
                erstellen(chance)
        
        
        # funktion zur erstellung von neuen Kunden oder änderung der daten
        def erstellen(chance = False):
            # Regestrierdaten Einlesen
            #  ändern des values der Anrede bei der auswahl "keine Angabe"
            if anrede_dropdown.get() == "Keine Angabe":
                anrede = ""
            else:
                anrede =  anrede_dropdown.get() 
            # speichern der eingegeben werte in einem tupel
            self.kundendaten =   (
                            anrede,
                            self.entry_list[0].get(),
                            self.entry_list[1].get(),
                            self.entry_list[2].get(),
                            self.entry_list[3].get(),
                            self.entry_list[4].get(),
                            self.entry_list[7].get(),
                            self.entry_list[8].get()
                            )
            # externe speicherung von plz und ort zur validierung 
            plz = self.entry_list[5].get()
            ort = self.entry_list[6].get()
    
            # erstellen einen neuen kunden wenn kunde ein kunde erstellt werden soll
            if chance == False:
                db.kunde_erstellen(self.kundendaten,plz,ort)
                tk.messagebox.showinfo("Information", "Der Kunde wurde angelegt")
            # änderung der kundendaten wenn kundendaten bearbeitet werden sollen    
            else:
                db.kunden_bearbeiten(self.kundendaten,plz,ort,values[2],values[3],values[4])
                tk.messagebox.showinfo("Information", "Kundendaten wurden geändert")
            Kunden_erstellen.destroy(self)
#
# Löschen von Kunden daten
#
class Löschen(tk.Tk):

    def __init__(self, kunde_id ,*args, **kwargs):
        # Regestrier Fenster erstellen
        global mitarbeiter
        tk.Tk.__init__(self, *args, **kwargs)
        del_frame = tk.Frame(self, bg = stylesheet.style["background"], height=400, width=600)
        del_frame.pack(fill="both", expand="true")
        
        # Regestrier Fenster Style
        del_frame.pack_propagate(0)
        del_frame.pack(fill="both", expand="true")
        self.geometry("600x400")
        self.resizable(0, 0)
        self.title("Löschen")
        
        # Regestrierbox style
        regestrier_box = tk.Frame(del_frame, bg=stylesheet.style["background"], relief="sunken", bd=2)  
        regestrier_box.place(rely=0.075, relx=0.075, height=300, width=500)
        
        # Regestrier BOX Inhalt
        
        # label Liste wird erstellt und positioniert
        lable_list = ["Sind sie sich sicher das Sie den Kunden löschen möchten?:","Bitte mit Ihrem Passwort bestätigen!",]
        lable_list = create_lable(regestrier_box,lable_list)
        
        for lable in range(len(lable_list)):
            lable_list[lable].grid(row=lable+1, column=1)
        
        # entry Liste wird erstellt und positioniert
        entry_list =["Passwort:"]
        entry_list = create_entry(regestrier_box,entry_list)
       
        for entry in range(len(entry_list)):
            entry_list[entry].grid(row=3, column=1)
        
        # Löschen button wird erstellt und positioniert
        button = ttk.Button(regestrier_box, text="Kunden Löschen", command=lambda: self.passwort_check(entry_list[0].get(),kunde_id))
        button.grid(row=8, column=1)
    
    # funktion zur überprüfung des Mitarbeiter Passworts bei löschung von kundendaten
    def passwort_check(self,passwort,kunde_id):
        # passwort wird gehasht
        passwort = hexa_hash(passwort.encode('utf-8'))
        # passwort wird mit passwort aus der Datenbank verglichen
        if passwort == mitarbeiter[0]:
            # erst werden alle dokumente dann der kunde gelöscht
            db.dokumente_löschen(kunde_id,True)
            tk.messagebox.showinfo("Information", "Der Kunde wurde gelöscht")
            Löschen.destroy(self)
        else:
            tk.messagebox.showinfo("Information", "Falsches Passwort")
                
#
#   Klasse zur erstellung eines Dropdown Menüs
#              
class MenuBar(tk.Menu):
    def __init__(self, parent):
        tk.Menu.__init__(self, parent)
        # Menü Bar einrichten
        crm_menu = tk.Menu(self, tearoff=0)
        self.add_cascade(label="CRM", menu=crm_menu)
        crm_menu.add_command(label="Aktualisieren", command=lambda: parent.show_frame())
        crm_menu.add_separator()
        crm_menu.add_command(label="Beenden", command=lambda: parent.Quit_application())
        crm_menu.add_separator()
        crm_menu.add_command(label="Beenden", command=lambda: parent.Quit_application())
#
#   erstellen des Hauptprogramm Fensters
#
class CRM(tk.Tk):

    def __init__(self, *args, **kwargs):   
        tk.Tk.__init__(self, *args, **kwargs)
        global mitarbeiter
        #Menübar aufrufen
        menubar = MenuBar(self)
        tk.Tk.config(self, menu=menubar)
        
        
        #Main Fenster erstellen
        self.main_frame = tk.Frame(self, bg= stylesheet.style["background"], height=800, width=1024)
        self.main_frame.pack(fill="both", expand="true")
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        #Frames erstellen
        # Daten ausgabe Frame
        frame1 = tk.LabelFrame(self, stylesheet.frame_styles, text="Kunden")
        frame1.place(rely=0.01, relx=0.01, height=600, width=1000)
        
        #Button Frame
        frame2 = tk.LabelFrame(self, stylesheet.frame_styles, text="")
        frame2.place(rely=0.775, relx=0.01, height=50, width=1000)

        # Dokumente Frame
        frame3 = tk.LabelFrame(self, stylesheet.frame_styles, text="")
        frame3.place(rely=0.85, relx=0.01, height=100, width=1000)


        # Spalten Erstellen Frame 1
        # Erstellen einer Tabele und einfügen alle vorhandenen kundendaten
        treeview_kundendaten = ttk.Treeview(frame1)
        column_list_account1 = ["Kundennr","Anrede","Vorname","Nachname","Geburtsdatum","Adresse","Ort","Telefon", "Email"]
        treeview_kundendaten['columns'] = column_list_account1
        treeview_kundendaten["show"] = "headings"  # removes empty column
        for column in column_list_account1:
            treeview_kundendaten.heading(column, text=column, command=lambda c=column: sort_treeview(treeview_kundendaten, c, False) )
            treeview_kundendaten.column(column, width=50)
        treeview_kundendaten.place(relheight=1, relwidth=0.995)
        
        # Scroll Balken erstellen Frame 1
        # scrollbars für Frame 1 werden erstellt und positioniert
        scrollbar_rechts= tk.Scrollbar(frame1)
        scrollbar_unten= tk.Scrollbar(frame1)
        scrollbar_rechts.configure(orient="vertical",command=treeview_kundendaten.yview)
        scrollbar_unten.configure(orient="horizontal",command=treeview_kundendaten.xview)
        treeview_kundendaten.configure(yscrollcommand=scrollbar_rechts.set)
        treeview_kundendaten.configure(xscrollcommand=scrollbar_unten.set)
        scrollbar_rechts.pack(side="right", fill="y")
        scrollbar_unten.pack(side="bottom", fill="x")

        # Button Frame 2
        # buttons für Frame2 werden erstellt und positioniert
        button_refrech= tk.Button(frame2, text="Aktualisieren", command=lambda: Refresh_data())
        button_refrech.place(rely=0.2, relx=0.1, height=30, width=150)
        button_add = tk.Button(frame2, text="Kunde Hinzufügen", command=lambda: Kunden_erstellen(""))
        button_add.place(rely=0.2, relx=0.3, height=30, width=150)
        button_upload = tk.Button(frame2, text="Dokument Hinzufügen", command=lambda: Kunden_erstellen(""))
        button_upload.place(rely=0.2, relx=0.5, height=30, width=150)
        button_edit = tk.Button(frame2, text="Kunden Bearbeiten", command=lambda: Kunden_erstellen(treeview_kundendaten.item(treeview_kundendaten.focus())))
        button_edit.place(rely=0.2, relx=0.7, height=30, width=150)


        #Spalten erstellen Frame 3
        # Erstellen einer Tabele und einfügen alle vorhandenen Dokumente
        treeview_dokumente = ttk.Treeview(frame3)
        column_list_account3 = ["Dokumentenname","Eingangsdatum", "Dokumentenpfad"]
        treeview_dokumente['columns'] = column_list_account3
        treeview_dokumente["show"] = "headings"  # removes empty column
        for column in column_list_account3:
            treeview_dokumente.heading(column, text=column)
            treeview_dokumente.column(column, width=50)
        treeview_dokumente.place(relheight=1, relwidth=0.995)
        
        # Scroll Balken erstellen Frame 1
        scrollbar_rechts2= tk.Scrollbar(frame3)
        scrollbar_unten2= tk.Scrollbar(frame3)
        scrollbar_rechts2.configure(orient="vertical",command=treeview_dokumente.yview)
        scrollbar_unten2.configure(orient="horizontal",command=treeview_dokumente.xview)
        treeview_dokumente.configure(yscrollcommand=scrollbar_rechts2.set)
        treeview_dokumente.configure(xscrollcommand=scrollbar_unten2.set)
        scrollbar_rechts2.pack(side="right", fill="y")
        scrollbar_unten2.pack(side="bottom", fill="x")
        
        # Funktion zum sortieren der Kundendaten
        def sort_treeview(tree, col, descending):
            data = [(tree.set(item, col), item) for item in tree.get_children('')]
            data.sort(reverse=descending)
            for index, (val, item) in enumerate(data):
                tree.move(item, '', index)
            tree.heading(col, command=lambda: sort_treeview(tree, col, not descending))
        
        # Funktion zum laden der Kundendaten
        def Load_data():
            Kunden_daten = db.alle_kunden("kunden_id")
            for row in Kunden_daten:
                treeview_kundendaten.insert("", "end", values=row)
        # Funktion zur aktualisieren von Kundendaten           
        def Refresh_data():
            for i in treeview_kundendaten.get_children():
                treeview_kundendaten.delete(i)
            Load_data()

        Refresh_data()

# Funktion zum Hashen von Passwörtern
def hexa_hash( password):
    password = hashlib.sha256(password)
    password = password.hexdigest()  
    return password
# erstellen von labeln in einer schleife
def create_lable(frame, list):
    lable_list = []
    for i in range(len(list)):
        label = tk.Label(frame, stylesheet.text_styles, text= list[i])
        lable_list.append(label)
    return lable_list
# erstellen von entry in einer schleife
def create_entry(frame, list, text_list = []): 
    entry_list = []
    
    for i in range(len(list)):
        
        if list[i] == "Passwort:" or list[i] == "Neues Passwort:":
            entry = ttk.Entry(frame, width=45, cursor="xterm", show="*" )
        else :
            entry = ttk.Entry(frame, width=45, cursor="xterm"  )
        entry_list.append(entry)
        if len(text_list) > 0:
            entry.insert(0, text_list[i+1])
    return entry_list     

# Mainloop  
top = Login()
top.title("Anmeldung")
root = CRM()
root.withdraw()
root.title("CRM")
root.mainloop()            