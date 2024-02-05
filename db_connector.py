import mysql.connector
from mysql.connector import Error


#
# Klasse für die Connection zur Datenbank
#
class db_connect:
  
  def __init__(self):  
    # Verbindungsdaten der Datenbank
    self.host="localhost"
    self.user="root"
    self.password=""
    self.database="crm"
    self.mydb = ""
    self.cursor= ""
  # Funktion zum Verbindungs aufbau  
  def connect(self):
    try:
          self.mydb = mysql.connector.connect(
                                        host = self.host,
                                        user = self.user,
                                        password = self.password,
                                        database= self.database
                                      )   
          self.cursor = self.mydb.cursor()
    except mysql.connector.Error as error:
      print("Verbindung zur Datenbank nicht möglich{}".format(error))  
  # Funktion zu Verbindungs abbau
  def close(self):
    if self.mydb.is_connected():
          self.mydb.commit()
          self.cursor.close()
          print("MySQL Verbindung wurder geschlossen") 
    
  # Funktion zur überprüfung des Mitarbeiter Logins 
  def login(self, username, passwort):
    # Verbindunsaufbau
    self.connect()
    # SQL abfrage
    mySql_select_Query = "select  login_passwort, login_vorname, login_nachname, login_email from login where login_username = %s;"
    self.cursor.execute(mySql_select_Query, (username,))
    login = self.cursor.fetchone()
    print(login)
    # überprüfung des Passworts
    if passwort == login[0]:
      self.close()
    # übertragung der Mitarbeiter Daten
      return [login[0] , login[1] , login[2] , login[3] if len(login) == 4 else ""]
          
    else:
      self.close()
      return [False]
    
      
  def user_validierung(self, username):
    
    self.connect()
    mySql_select_Query = "select login_username from login where login_username = %s ;"
    self.cursor.execute(mySql_select_Query,(username,))
    row = self.cursor.fetchone()
    
    if row == None:
      self.close()
      return(True)
    else:
      self.close()
      return(False)
  
  def plz_validierung(self, plz, ort):
    
    self.connect()
    mySql_select_Query = "select plz from plz where plz = %s ;"
    self.cursor.execute(mySql_select_Query,(plz,))
    plz_check = self.cursor.fetchone()
    
    if plz_check == None:
      mySql_select_Query = "select ort_name from ort where ort_name = %s ;"
      self.cursor.execute(mySql_select_Query,(ort,))
      ort_check = self.cursor.fetchone()
      if ort_check == None:
        mySql_insert_query = "INSERT INTO ort VALUES (default, %s);"
        self.cursor.execute(mySql_insert_query, (ort,))
        self.close()
      self.add_plz(plz,ort)  
        
        
  def add_plz(self,plz,ort):    
    
      self.connect()
      mySql_insert_query = """INSERT INTO plz VALUES 
                              (default, %s,
                              (select ort_id from ort where ort_name = %s));"""
      self.cursor.execute(mySql_insert_query, (plz,ort))
      self.close()
      
  def registrierung(self, username, passwort, vorname,nachname,email): 
    
    self.connect() 
    mySql_insert_query = "INSERT INTO login VALUES (default, %s , %s, %s, %s, %s); "
    values = (username, passwort, vorname, nachname, email)
    self.cursor.execute(mySql_insert_query, values)
    self.close()
    

  def alle_kunden(self,var):
    
    self.connect()
    mySql_select_Query = "select * from alle_kundendaten order by %s"
    self.cursor.execute(mySql_select_Query, (var,))
    kundendaten = self.cursor
    self.close()
    return kundendaten
  
  def kunde_erstellen(self, kundendaten, plz , ort): 
    
    self.plz_validierung(plz,ort)
    self.connect() 
    values = kundendaten + (plz,)
    mySql_insert_query = """INSERT INTO kunde VALUES 
                          (default, %s , %s, %s, %s, %s, %s , %s, %s,
                          (select plz_id from plz where plz = %s) ); """
    self.cursor.execute(mySql_insert_query, values)
    self.close()
    
  def kunden_löschen(self , kunde_id):
  
    self.connect() 
    mySql_delete_query = """delete from kunde where kunde_id = %s;"""
    self.cursor.execute(mySql_delete_query, (kunde_id,))
    self.close()
    
  def kunden_bearbeiten(self , kundendaten, plz , ort, *var):
    
    self.plz_validierung(plz,ort)
    self.connect() 
    values = kundendaten + (plz,) + var
    print(values)
    mySql_insert_query = """update kunde
                            set
                            kunde_anrede = %s, 
                            kunde_vorname = %s, 
                            kunde_nachname = %s,
                            kunde_geburtsdatum = %s, 
                            kunde_straße = %s, 
                            kunde_hausnr = %s, 
                            kunde_telefon = %s, 
                            kunde_email = %s,
                            plz_id = (select plz_id from plz where plz = %s)
                            where
                            kunde_id =(select kunde_id from kunde
                            where kunde_vorname = %s and kunde_nachname = %s and kunde_geburtsdatum = %s) ; """
    self.cursor.execute(mySql_insert_query, values)
    self.close()
    
  def dokumente_löschen(self , kunde_id, kunde_löschen = False):
      self.connect() 
      mySql_delete_query = """delete from dokumente where kunde_id = %s;"""
      self.cursor.execute(mySql_delete_query, (int(kunde_id),))
      self.close()
      if kunde_löschen == True:
        self.kunden_löschen(kunde_id)