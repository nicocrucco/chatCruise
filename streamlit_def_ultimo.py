import os
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import streamlit as st
import pyodbc
from datetime import datetime
import speech_recognition as sr
from fpdf import FPDF
import cv2 
import numpy as np
import math




# Leggi il file CSV e carica i dati in un DataFrame
script_dir = os.path.dirname(os.path.abspath(__file__))
# Ora puoi lavorare con il DataFrame 'df'

import requests
from bs4 import BeautifulSoup

note_file = os.path.join(script_dir,"data")
note_file = os.path.join(note_file,'notes.txt')

# segna_data_file = os.path.join(script_dir,'Segna_Data')
# pdf_file = os.path.join(script_dir, "output.pdf")


#scrivo la funiona per aggiungere una nota
def save_note(date_time, note):
    
    #se il file non esiste viene creato
    if not os.path.exists(note_file):
        open(note_file,'w')

    with open(note_file,'a', encoding='utf-8') as f: #modalità append
        f.writelines([date_time + note + "\n"]) #aggiungo la singola nota che voglio aggiungere

def read_note():

        # Leggi il contenuto del file
        with open(note_file, 'r', encoding='utf-8') as file:
            file_content = file.read()
        
        if len(file_content) > 0:
            # Restituisci il contenuto del file come stringa
            return file_content
        else:
            return 'Il file note è vuoto!'
        
def delete_note():

        with open(note_file, 'w', encoding='utf-8') as file:
            file.write('')

 
def delete_row(riga_da_eliminare):
 
        riga_da_eliminare = int(riga_da_eliminare)
 
        if riga_da_eliminare < 0:
            pass
        else:
            riga_da_eliminare -= 1
       
 
        # Leggi tutte le righe del file
        with open(note_file, 'r', encoding='utf-8') as file:
            righe = file.readlines()
       
        if len(righe) == 0:
            return 'Il file note è vuoto!'
 
        if riga_da_eliminare >= 0:
            # Elimina la riga specificata
            if 0 <= riga_da_eliminare < len(righe):
                del righe[riga_da_eliminare]
        else:
            del righe[riga_da_eliminare]
       
        # Riscrivi il file senza la riga eliminata
        with open(note_file, 'w', encoding='utf-8') as file:
            file.writelines(righe)
   
        return 'La nota è stata cancellata'


def mail(oggetto,body, indirizzo ):
    
    # Configurazione dei dettagli dell'email

    from_email = 'test1675@outlook.it'
    to_email = indirizzo
    subject = oggetto
    body = body
    
    # Credenziali dell'account email
    username = 'test1675@outlook.it'
    password = 'schiavo95'
    
    # Creazione del messaggio email
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    
    msg.attach(MIMEText(body, 'plain'))
    
    # Configurazione del server SMTP e invio dell'email
    try:
        server = smtplib.SMTP('smtp.office365.com', 587)
        server.starttls()
        server.login(username, password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        string= ('Email inviata con successo!')
    except Exception as e:
        string= (f'Errore durante l\'invio dell\'email: {e}')
    finally:
        server.quit()
    return string

    
def controllo_mail(mail):
    lista_mail_valida= [
    '@gmail.com', '@outlook.com', '@yahoo.com', '@aol.com','@icloud.com','@protonmail.com','@zoho.com','@libero.it', '@yahoo.it','@outlook.it','@hotmail.com','@hotmail.it',
    '@live.com','@live.com','@msn.com','@icloude.com','@me.com','@mac.com', '@protonmail.ch', '@zoho.eu', '@tiscali.it','@virgilio.it','@tim.it','@alice.it','@tin.it',
    '@fastwebnet.it','@vodafone.it','@yandex.com','@yadex.ru','@aol.com','@rediffmail.com','@alten.it'
    ]
    for suffix in lista_mail_valida:
        if suffix in mail:
            return True
        else:
            continue

    return False
    

def riassunto(oggetto, body, indirizzo):
    dict_riassunto = {"oggetto": oggetto, "contenuto":body, "mail": indirizzo}
    stringa_riassunto = "Questo è il riepilogo della tua mail: \n\n"
    for key in dict_riassunto.keys():
        stringa_riassunto += key + ": " + "\n" + dict_riassunto[key] + "\n\n"
    stringa_riassunto += "Sei sicuro di volerla inviare? Rispondi con Si o No"
    return stringa_riassunto 

def riassunto_segnalazione(body):
    dict_riassunto = {"contenuto":body}
    stringa_riassunto = "Questo è il riepilogo della tua segnalazione: \n\n"
    for key in dict_riassunto.keys():
        stringa_riassunto += dict_riassunto[key] + "\n\n"
    stringa_riassunto += "Sei sicuro di volerla inviare? Rispondi con Si o No"
    return stringa_riassunto 

def inserimento_acquisto(buy_btp,buy_quantità,lista_dati):
    #buy_btp = denominazione del btp che sto comprando
    try:
        con= pyodbc.connect('DRIVER={SQL Server};SERVER=bubidb.database.windows.net;DATABASE=mlacademy-sqldb;UID=MLacademy;PWD=alten-ML-academy2023')
        cursor= con.cursor()
        prezzo_query = """
                        SELECT TOP 1 Prezzo_ufficiale
                        FROM Gruppo1_btp_Az_finale
                        WHERE Denominazione = ? ORDER BY Data_Pr_Ufficiale DESC;
                        """
        insert_query = """
                        INSERT INTO ALTEN_CONTO (SOCIETA, ID_CONTO, DATA_TRANSAZIONE, IMPORTO_MOVIMENTO_EUR, IMPORTO_MOVIMENTO_VALUTA,
                        MONETA_MOVIMENTO, CODICE_MOVIMENTO, CAUSALE_MOVIMENTO, DARE_AVERE)
                        VALUES (?,?,?,?,?,?,?,?,?)
                        """
        
        cursor.execute(prezzo_query, (buy_btp,))
        prezzo = round(cursor.fetchall()[0][0],2)
        Societa= lista_dati[0]
        Id_conto= lista_dati[1]
        Data_transazione= lista_dati[2]
        Importo_movimento= -int(buy_quantità)*10*prezzo #perchè sarebbe (prezzo/100)*1000*quantità
        Moneta_Movimento= lista_dati[3]
        Codice_Movimento= lista_dati[4]
        Causale= lista_dati[5]
        Dare_avere=lista_dati[6]
        select_query = "select * from ALTEN_CONTO"
        cursor.execute(select_query)
        ultima_riga= cursor.fetchall()[len(cursor.fetchall())-1]
        saldo= ultima_riga[-2]
        if saldo < -Importo_movimento:
            return f"Saldo insufficiente, impossibile effettuare l'operazione. Il tuo saldo è {saldo:.2f} "
        lista=(Societa,Id_conto,Data_transazione,Importo_movimento,Importo_movimento,Moneta_Movimento,Codice_Movimento,Causale,Dare_avere)
        cursor.execute(insert_query, lista)
        
        #controllo sulla presenza dei btp in ALTEN_INVESTIMENTI
        select_btp = "select * from ALTEN_INVESTIMENTI"
        cursor.execute(select_btp)
        existing = False
        for row in cursor.fetchall():
            if buy_btp == row[1]:  
                id = row[0]
                update_btp = """
                        UPDATE ALTEN_INVESTIMENTI
                        SET Lotto = ?,
                            Data_investimento = ?
                        WHERE ID_Investimento = ?
                        """
                lotto_aggiornato = row[2] + int(buy_quantità)
                data_aggiornata = datetime.now()
                cursor.execute(update_btp, (lotto_aggiornato, data_aggiornata, id))
                con.commit()
                existing = True

                        
        if existing == False:
            insert_btp = """
                            INSERT INTO ALTEN_INVESTIMENTI (Denominazione, Lotto, Data_investimento)
                            VALUES (?,?,?)
                            """
            data = (buy_btp, buy_quantità, Data_transazione)
            cursor.execute(insert_btp, data)
            con.commit()
        con.close()
    except Exception as e:
         return e
    stringa="Acquisto effettuato correttamente!"
    return stringa


def is_convertible_to_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
    
def denominazione():
    try:
        con= pyodbc.connect('DRIVER={SQL Server};SERVER=bubidb.database.windows.net;DATABASE=mlacademy-sqldb;UID=MLacademy;PWD=alten-ML-academy2023')
        cursor= con.cursor()
        query = """
                            SELECT DISTINCT Denominazione
                            FROM Gruppo1_btp_Az_finale
                                                """
        cursor.execute(query)
        lista= []
        for row in cursor.fetchall():
            lista.append(row[0])
        con.close()
    except Exception as e:
        return e
    return lista

def inserimento_vendita(sell_btp,sell_quantità,lista_dati):
    try:
        con= pyodbc.connect('DRIVER={SQL Server};SERVER=bubidb.database.windows.net;DATABASE=mlacademy-sqldb;UID=MLacademy;PWD=alten-ML-academy2023')
        cursor= con.cursor()
        #controllo sulla presenza dei btp in ALTEN_INVESTIMENTI
        select_btp = "select * from ALTEN_INVESTIMENTI"
        cursor.execute(select_btp)
        existing = False
        for row in cursor.fetchall():
            if sell_btp == row[1]:
                if int(sell_quantità) <= row[2]:  
                    id = row[0]
                    update_btp = """
                            UPDATE ALTEN_INVESTIMENTI
                            SET Lotto = ?,
                                Data_investimento = ?
                            WHERE ID_Investimento = ?
                            """
                    lotto_aggiornato = row[2] - int(sell_quantità)
                    data_aggiornata = datetime.now()
                    cursor.execute(update_btp, (lotto_aggiornato, data_aggiornata, id))
                    con.commit()
                    existing = True
                else:
                    response = "La quantità di lotti che vuoi vendere è superiore a quella posseduta."
                    return response
        if existing == False:
            response = "Il Btp che vuoi vendere non è presente nei tuoi investimenti."
            return response
        prezzo_query = """
                        SELECT TOP 1 Prezzo_ufficiale
                        FROM Gruppo1_btp_Az_finale
                        WHERE Denominazione = ? ORDER BY Data_Pr_Ufficiale DESC;
                        """
        insert_query = """
                        INSERT INTO ALTEN_CONTO (SOCIETA, ID_CONTO, DATA_TRANSAZIONE, IMPORTO_MOVIMENTO_EUR, IMPORTO_MOVIMENTO_VALUTA,
                        MONETA_MOVIMENTO, CODICE_MOVIMENTO, CAUSALE_MOVIMENTO, DARE_AVERE)
                        VALUES (?,?,?,?,?,?,?,?,?)
                        """
        
        cursor.execute(prezzo_query, (sell_btp,))
        prezzo = round(cursor.fetchall()[0][0],2)
        Societa= lista_dati[0]
        Id_conto= lista_dati[1]
        Data_transazione= lista_dati[2]
        Importo_movimento= int(sell_quantità)*10*prezzo #perchè sarebbe (prezzo/100)*1000*quantità
        Moneta_Movimento= lista_dati[3]
        Codice_Movimento= lista_dati[4]
        Causale= 'Vendita investimento'
        Dare_avere= 'C'
        lista=(Societa,Id_conto,Data_transazione,Importo_movimento,Importo_movimento,Moneta_Movimento,Codice_Movimento,Causale,Dare_avere)
        cursor.execute(insert_query, lista)
        con.commit()
        con.close()
    except Exception as e:
        return e
    stringa="Vendita effettuata correttamente!"
    return stringa

def riconosci_discorso_da_mic():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
 
    with microphone as source:
    
        recognizer.adjust_for_ambient_noise(source, duration=1)
        st.write("Parla!.")
        audio = recognizer.listen(source)
 
    try:
        transcript = recognizer.recognize_google(audio, language="it-IT")
    except sr.RequestError:
        st.error("API non disponibile o errore di rete.")
        return None
    except sr.UnknownValueError:
        st.warning("Non è stato possibile riconoscere il discorso.")
        return None
 
    return transcript

#-------------------------------------------------------------------
#Funzioni per RAG

def leggi_valore_da_file():
    # Leggi il valore dal file
    try:
        with open(segna_data_file, 'r') as file:
            valore = file.readline().strip()
            return valore
    except FileNotFoundError:
        return None

def salva_valore_in_file(valore):
    # Apri il file in modalità di scrittura (write) e scrivi il valore
    with open(segna_data_file, 'w') as file:
        file.write(str(valore) + '\n')

def elimina_file_pdf():
   
    # Controlla se il file esiste e ha estensione .pdf
    if os.path.isfile(pdf_file) and pdf_file.endswith('.pdf'):
        os.remove(pdf_file)
    else:
        pass

class PDF(FPDF):
    def header(self):
        pass
   
    def footer(self):
        pass
 
    def chapter_title(self, title, date):
        self.set_font('Arial', 'B', 2)
        # Ensure UTF-8 encoding for titles
        title = title.encode('latin-1', 'replace').decode('latin-1')
        self.cell(0, 10, title, 0, 1, 'L')
        # Ensure UTF-8 encoding for dates
        date = date.encode('latin-1', 'replace').decode('latin-1')
        self.cell(0, 10, date, 0, 1, 'L')
        self.ln(10)
 
    def chapter_body(self, body):
        self.set_font('Arial', '', 1)
        # Ensure UTF-8 encoding for body text
        body = body.encode('latin-1', 'replace').decode('latin-1')
        self.multi_cell(0, 10, body)
        self.ln()
 
    def add_page_break(self):
        self.add_page()

def create_combined_pdf(dataframe, filename):
    pdf = PDF()
    pdf.add_page()
    for index, row in dataframe.iterrows():
        title = row['Titolo']
        date = row['Data_di_Pubblicazione']
        # Assuming date is already a string but might need formatting
        # You can format it like this if it's not already in a suitable string format
        date = date.strftime('%Y-%m-%d %H:%M')  # Adjust format as needed
        formatted_date = datetime.strptime(date, '%Y-%m-%d %H:%M').strftime('%Y-%m-%d %H:%M')
        article = row['Articolo']
        pdf.chapter_title(title, formatted_date)  # Pass the formatted date
        pdf.chapter_body(article)
        pdf.add_page_break()  # Add a page break after each article

    pdf.output(filename)

#-------------------------------------------------------------------
#Funzioni Tool Mappa
def immagine(jpg_bn = None, jpg_c = None):
    dim = (320,1024)
    if jpg_bn is not None:
        #ridimensione
        jpg_bn = cv2.resize(jpg_bn,dim)
        jpg_grey = cv2.cvtColor(jpg_bn,cv2.COLOR_BGR2GRAY)
        return jpg_grey
    else:
        jpg_c = cv2.resize(jpg_c,dim)
        return jpg_c
    
def distanza_euclidea(pos, dizionario, p):
    punto = dizionario[p]
    
    return np.sqrt((punto[0]-pos[0])**2 + (punto[1]-pos[1])**2)

def calcola_direzione1(coord1, coord2):
    """Calcola la direzione del movimento tra due coordinate."""
    dx = coord2[0] - coord1[0]
    dy = coord2[1] - coord1[1]
    angle = math.degrees(math.atan2(dy, dx))
    if angle < 0:
        angle += 360
    if 45 <= angle < 135:
        return "sud"
    elif 135 <= angle < 225:
        return "ovest"
    elif 225 <= angle < 315:
        return "nord"
    else:
        return "est"
 
def determina_svolta1(direzione_corrente, nuova_direzione):
    """Determina se la svolta è a destra, a sinistra o dritto."""
    # svolte = {
    #     "nord": {"nord": "dritto", "est": "destra", "ovest": "sinistra", "sud": "indietro"},
    #     "sud": {"nord": "indietro", "est": "sinistra", "ovest": "destra", "sud": "dritto"},
    #     "est": {"nord": "sinistra", "est": "dritto", "ovest": "indietro", "sud": "destra"},
    #     "ovest": {"nord": "destra", "est": "indietro", "ovest": "dritto", "sud": "sinistra"},
    # }
    svolte = {
        "nord": {"nord": "dritto", "est": "destra", "ovest": "sinistra", "sud": "indietro"},
        "sud": {"nord": "indietro", "est": "sinistra", "ovest": "destra", "sud": "dritto"},
        "est": {"nord": "sinistra", "est": "dritto", "ovest": "indietro", "sud": "destra"},
        "ovest": {"nord": "destra", "est": "indietro", "ovest": "dritto", "sud": "sinistra"},
    }
    return svolte[direzione_corrente][nuova_direzione]
 
def analizza_percorsi1(percorsi):
    chiavi = list(percorsi.keys())
    svolte = []
 
    for i in range(len(chiavi) - 1):
        coord1 = percorsi[chiavi[i]]
        coord2 = percorsi[chiavi[i + 1]]
        if i == 0:
            svolte.append("dritto")
            #direzione_corrente = 'est' 
            direzione_corrente = calcola_direzione1(coord1, coord2)
        
        else:
            nuova_direzione = calcola_direzione1(coord1, coord2)
            svolta = determina_svolta1(direzione_corrente, nuova_direzione)
            svolte.append(svolta)
            direzione_corrente = nuova_direzione  # Aggiorna la direzione corrente
            
    svolte.append("fine")  # Aggiungi "fine" per l'ultima coordinata
    return svolte

def verifica_partenza_arrivo(dizionario1, dizionario2, dizionario3, partenza, arrivo):
    dizionario = dizionario1 | dizionario2 | dizionario3
    dizionario['ascensore'] = None
    dizionario['ascensori'] = None 
    if arrivo == "ristorante":
        return 0.1
    if arrivo == "bar":
        return 0.2
    if partenza not in dizionario.keys() and arrivo not in dizionario.keys():
        return 1
    elif partenza not in dizionario.keys():
        return 2
    elif arrivo not in dizionario.keys():
        return 3
    else:
        return 9

def replace_occurrence(text, old_word, new_word):
    # Trova la prima occorrenza della parola
    first_occurrence_index = text.find(old_word)
    
    # Trova la seconda occorrenza della parola
    second_occurrence_index = text.find(old_word, first_occurrence_index + len(old_word))

    text_split = text.split()
    if "ristorante" in new_word or "bar" in new_word:
        
        if "ristorante" == text_split[len(text_split)-1] or "bar" == text_split[len(text_split)-1]: #caso in cui è specificata prima la partenza e poi l'arrivo
            if second_occurrence_index != -1:
                # Se la seconda occorrenza esiste, sostituiscila
                before_second = text[:second_occurrence_index]
                after_second = text[second_occurrence_index:].replace(old_word, new_word, 1)
                return before_second + after_second
            else:
                text = text.replace(old_word, new_word)
                return text
        else:
            if second_occurrence_index != -1:
                # Se la seconda occorrenza esiste, sostituiscila
                before_second = text[:second_occurrence_index].replace(old_word, new_word, 1)
                after_second = text[second_occurrence_index:]
                return before_second + after_second
            else:
                text = text.replace(old_word, new_word)
                return text
            
    else:
        if "ristorante" == text_split[len(text_split)-1] or "bar" == text_split[len(text_split)-1]: #caso in cui è specificata prima la partenza e poi l'arrivo
            if second_occurrence_index != -1:

                before_second = text[:second_occurrence_index]
                after_second = text[second_occurrence_index:].replace(old_word, old_word + ' ' + new_word, 1)
                return before_second + after_second
            else:
                text = text.replace(old_word, old_word + ' ' + new_word)
                return text
        else:
            if second_occurrence_index != -1:
                # Se la seconda occorrenza esiste, sostituiscila
                before_second = text[:second_occurrence_index].replace(old_word, old_word + ' ' + new_word, 1)
                after_second = text[second_occurrence_index:]
                return before_second + after_second
            else:
                text = text.replace(old_word, old_word + ' ' + new_word)
                return text
            
def Prenotazione_Ristoranti(Id_cliente,Luogo,FasciaOraria,Numero_persone):

    lista=FasciaOraria.split(" ")
    Giorno =lista[1]
    Orario = lista[-1]

    con= pyodbc.connect('DRIVER={SQL Server};SERVER=bubidb.database.windows.net;DATABASE=mlacademy-sqldb;UID=MLacademy;PWD=alten-ML-academy2023')
    cursor= con.cursor()
    insert_query = """ INSERT INTO Prenotazioni 
                        VALUES (?,?,?,?,?)"""
    cursor.execute(insert_query,(Id_cliente,Luogo,Orario,Giorno,Numero_persone))
    update_query= """UPDATE Ristoranti
                    SET CapienzaTotale = CapienzaTotale - ?
                    WHERE NomeRistorante =? AND FasciaOraria =? AND Giorno = ?;"""
    cursor.execute(update_query,(Numero_persone,Luogo,Orario,Giorno))
    cursor.close()
    con.commit()
    con.close()


    #----------------------------------------------------------QUERY PER PRENOTAZIONI ----------------------------------------------
def mostra_prenotazioni(numero,id_cliente):
    con= pyodbc.connect('DRIVER={SQL Server};SERVER=bubidb.database.windows.net;DATABASE=mlacademy-sqldb;UID=MLacademy;PWD=alten-ML-academy2023')
    cursor= con.cursor()

    if numero==1: #oggi
        insert_query = """ SELECT luogo, orario, giorno, numero_persone
                        FROM Prenotazioni
                        WHERE id_Cliente=? AND Giorno = CONVERT(date, GETDATE());"""
    elif numero==2: #domani
        insert_query="""SELECT luogo, orario, giorno, numero_persone
                        FROM Prenotazioni
                        WHERE id_Cliente=? AND Giorno = CONVERT(date, GETDATE()+1);"""
    
    else:
        insert_query="""SELECT luogo, orario, giorno, numero_persone
                        FROM Prenotazioni
                        WHERE id_Cliente=? AND Giorno >= CONVERT(date, GETDATE());"""
    cursor.execute(insert_query,(id_cliente))
    
    lista_prenotazioni=[]
    for row in cursor.fetchall():
        lista_prenotazioni.append(tuple(row))
        
    df_prenotazioni = pd.DataFrame(lista_prenotazioni, columns=['luogo', 'orario', 'giorno', 'numero_persone'])

    cursor.close()
    con.commit()
    con.close()

    return df_prenotazioni

def elimina_prenotazione(prenotazione_da_eliminare,id_cliente):
    lista=prenotazione_da_eliminare.split(" ")
    lista_2=[]
    for indice in range(len(lista)):
        if indice%2==1:
            lista_2.append(lista[indice])
    luogo=lista_2[0]
    orario=lista_2[1]
    giorno=lista_2[2]
    numero_persone=lista_2[3]
    con= pyodbc.connect('DRIVER={SQL Server};SERVER=bubidb.database.windows.net;DATABASE=mlacademy-sqldb;UID=MLacademy;PWD=alten-ML-academy2023')
    cursor= con.cursor()
    delete_query = """ DELETE FROM Prenotazioni WHERE luogo=? AND orario=? AND giorno=? AND numero_persone=?;"""
    cursor.execute(delete_query,(luogo,orario,giorno,numero_persone))
    update_query =  """UPDATE Ristoranti
                    SET CapienzaTotale = CapienzaTotale + ?
                    WHERE NomeRistorante =? AND FasciaOraria =? AND Giorno = ?;"""
    cursor.execute(update_query,(numero_persone,luogo,orario,giorno))
    cursor.close()
    con.commit()
    con.close()
