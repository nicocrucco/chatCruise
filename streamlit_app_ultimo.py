######################################################
 
#########      latest update: Kevin  ###############
 
######################################################


import streamlit as st
from sqlalchemy import create_engine
from langchain.chains import create_sql_query_chain
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from operator import itemgetter
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from langchain.schema import HumanMessage
import warnings
from langchain.memory import ConversationBufferMemory
from langchain_community.utilities import SQLDatabase
from pyprojroot import here
from llama_index.core.tools import FunctionTool
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationalRetrievalChain
from datetime import datetime, date, timedelta
import streamlit_def_ultimo as sfun
from PIL import Image
import streamlit.components.v1 as components
import pyodbc
import pymssql
import speech_recognition as sr
import pandas as pd
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import time
import cv2
import os
import numpy as np
from pathfinding.core.grid import Grid
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.finder.dijkstra import DijkstraFinder
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from PIL import Image
import io
from dotenv import load_dotenv
import itertools
from contextlib import suppress



st.set_page_config(page_title="chatCruise",page_icon="🤖",layout="wide")
# Reducing whitespace on the top of the page
st.markdown("""
<style>
 
.block-container
{
    padding-top: 0rem;
    padding-bottom: -15rem;
    margin-top: -1.6rem;
}
 
</style>
""", unsafe_allow_html=True)

# Custom HTML/CSS for the banner
custom_html = """
<div class="banner">
<img src="https://leyton.com/it/wp-content/uploads/sites/11/2023/10/Alten-logo.png" alt="Banner Image">
<span class="banner-text" style="font-family: sans-serif;"><b>chatCruise</b></span>
</div>
<style>
    .banner {
        width: 100%;
        height: 165px;
        overflow: hidden;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .banner img {
        width: 15%;
        object-fit: cover;
    }
    .banner-text{
        margin-left: 170px;
        font-size: 2em;
}
</style>
"""
# Display the custom HTML
components.html(custom_html)

st.markdown( 
"""
<style>
    .st-emotion-cache-vdokb0 {
        font-family: "font-family", sans-serif;
        margin-bottom: -1rem;
    }
<style>
""",unsafe_allow_html=True
)



# Applica lo stile CSS personalizzato

st.markdown( 
"""
<style>
    .st-emotion-cache-bho8sy {
        display: flex;
        width: 2rem;
        height: 2rem;
        flex-shrink: 0;
        border-radius: 0.5rem;
        -webkit-box-align: center;
        align-items: center;
        -webkit-box-pack: center;
        justify-content: center;
        color: rgb(255, 255, 255);
    }
<style>
""",unsafe_allow_html=True
)


#Allineamento omino utente sulla destra
st.markdown(
"""
<style>
    .st-emotion-cache-1c7y2kd { 
        flex-direction: row-reverse;
        text-align: right;
    }
</style>
""",unsafe_allow_html=True
)

# st.sidebar.title("**Scegli la mia creatività**")
# st.session_state.temperatura = st.sidebar.slider(    
#     "",
#     min_value=0.0,    
#     max_value=1.0,    
#     value=0.0,
#     step = 0.5,
#     help="La temperatura è un indicatore di creatività del chatbot.",
# )
# st.sidebar.write("""\n
#                 """)
# st.sidebar.write("""
#                 • **Preciso 0**\n
#                 • **Equilibrato 0.5**\n
#                 • **Creativo 1** 
#                 """)

#----------------------------------------------------------Dati Conto[Societa, Id conto,Data transazione, Moneta-Movimento,Codice Movimento,Causale,Dare/Avere]------------------------------------------------------------------------------------
Data_transazione= datetime.now()
if "lista_dati" not in st.session_state.keys():
    Societa= "ABC"
    Id_conto= "123456789012345678901234567"
    Moneta_Movimento= "EUR"
    Codice_Movimento= "BTP"
    Causale="Investimento"
    Dare_Avere="D"
    st.session_state.lista_dati = [Societa,Id_conto,Data_transazione,Moneta_Movimento,Codice_Movimento,Causale,Dare_Avere]

#----------------------------------------------------------Lista BTP--------------------------------------------------------------------------------------
if "lista_denominazione" not in st.session_state.keys():
    st.session_state.lista_denominazione = sfun.denominazione()

# ---------------------------------------------------------Begin Checker mail------------------------------------------------------------------------------------
if "mail_checker" not in st.session_state.keys():
    st.session_state.mail_checker = 0
    
if "mail_oggetto" not in st.session_state.keys():
    st.session_state.mail_oggetto = "Segnalazione"

if "mail_body" not in st.session_state.keys():
    st.session_state.mail_body = "stringa-segreta"

if "sicuro" not in st.session_state.keys():
    st.session_state.sicuro = "No"

if "mail_indirizzo" not in st.session_state.keys():
    st.session_state.mail_indirizzo = "andreapastore326@gmail.com"
# ---------------------------------------------------------End Checker mail------------------------------------------------------------------------------------


# ---------------------------------------------------------Begin Checker Buy----------------------------------------------------------------------------------
if "buy_checker" not in st.session_state.keys():
    st.session_state.buy_checker = 0
if "buy_btp" not in st.session_state.keys():
    st.session_state.buy_btp = "stringa-segreta"
if "buy_quantità" not in st.session_state.keys():
    st.session_state.buy_quantità = "stringa-segreta"
if "buy_sicuro" not in st.session_state.keys():
    st.session_state.buy_sicuro = "n"
# ---------------------------------------------------------End Checker Buy------------------------------------------------------------------------------------   

# ---------------------------------------------------------Begin Checker Sell----------------------------------------------------------------------------------
if "sell_checker" not in st.session_state.keys():
    st.session_state.sell_checker = 0
if "sell_btp" not in st.session_state.keys():
    st.session_state.sell_btp = "stringa-segreta"
if "sell_quantità" not in st.session_state.keys():
    st.session_state.sell_quantità = "stringa-segreta"
if "sell_sicuro" not in st.session_state.keys():
    st.session_state.sell_sicuro = "n"
# ---------------------------------------------------------End Checker Sell------------------------------------------------------------------------------------   
# ---------------------------------------------------------Begin Checker RAG------------------------------------------------------------------------------------   
if "RAG_checker" not in st.session_state.keys():
    st.session_state.RAG_checker = 0
# ---------------------------------------------------------End Checker RAG------------------------------------------------------------------------------------   
# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "avatar": 'https://www.shutterstock.com/image-vector/call-center-customer-support-vector-600nw-2285364015.jpg', "content": "Benvenuto a bordo!👋🏻\n\n Sono il tuo assistant navigator, come posso aiutarti?","contatore" : 0}]
if 'cont' not in st.session_state:
    cont = 0
    st.session_state['cont'] = 0
else:
    cont = st.session_state['cont']
# ---------------------------------------------------------Begin Checker Mappa------------------------------------------------------------------------------------   
if 'cont_mappa' not in st.session_state:
    cont_mappa = 0
    st.session_state['cont_mappa'] = 0
else:
    cont_mappa = st.session_state['cont_mappa']

if 'cont_mappa_display' not in st.session_state:
    cont_mappa_display = 0
    st.session_state['cont_mappa_display'] = 0
else:
    cont_mappa_display = st.session_state['cont_mappa_display']
# ---------------------------------------------------------End Checker Mappa-------------------------------------------------------------------------------------- 
# ---------------------------------------------------------Begin Checker Recensioni------------------------------------------------------------------------------------  
if 'recensioni' not in st.session_state:
    recensioni = list()
    st.session_state['recensioni'] = recensioni
else:
    recensioni = st.session_state['recensioni']
# ---------------------------------------------------------End Checker Recensioni------------------------------------------------------------------------------------   

# ---------------------------------------------------------Begin Checker Nota------------------------------------------------------------------------------------  
if 'checker_try_catch' not in st.session_state:
    checker_try_catch = 0
    st.session_state['checker_try_catch'] = 0
else:
    checker_try_catch = st.session_state['checker_try_catch']
# ---------------------------------------------------------End Checker Nota------------------------------------------------------------------------------------ 
# ---------------------------------------------------------Begin Save prompt------------------------------------------------------------------------------------   
if 'prompt_mappa' not in st.session_state:
    prompt_mappa = ''
    st.session_state['prompt_mappa'] = prompt_mappa
else:
    prompt_mappa = st.session_state['prompt_mappa']
if 'specificazione_bar_o_ristorante' not in st.session_state:
    specificazione_bar_o_ristorante = ''
    st.session_state['specificazione_bar_o_ristorante'] = specificazione_bar_o_ristorante
else:
    specificazione_bar_o_ristorante = st.session_state['specificazione_bar_o_ristorante']
if 'arrivo' not in st.session_state:
    arrivo = ''
    st.session_state['arrivo'] = arrivo
else:
    arrivo = st.session_state['arrivo']
# ---------------------------------------------------------End Save prompt------------------------------------------------------------------------------------   
risp_nota = ""

#-----------------------------------------------------------------Begin Checker Ristoranti-------------------------------------------------------------------------
if "checker_ristoranti" not in st.session_state:
    checker_ristoranti = []
    st.session_state["checker_ristoranti"] = checker_ristoranti
    st.session_state["checker_data"]=[]
    st.session_state["checker_persone"] = []
    st.session_state['checker_cucina']=[]
    st.session_state['checker_prenotazione_ristoranti']=[]
else:
    checker_ristoranti = st.session_state["checker_ristoranti"]
#-----------------------------------------------------------------End Checker Ristoranti------------------------------------------------------------------------------
#-------------------------------------------------------------Dizionari cucine---------------------------------------------------------------------------------------
ristoranti = ["Michelangelo", "Raffaello", "ying-yang", "Haveli", "Bella Italia", "Pizza360", "Wen", "Ritual", "Pegaso", "Greek Taverna", "My kimchi", "Istanbul", "Fusion", "Nippo", "Sushi Club", "Tao", "Gustoo", "Da Mario","Piedra del Sol","Burrito"]
dizionario_cucine = {"cinese": ["ying-yang", "Wen"], "giapponese": ["Nippo", "Fusion", "Sushi Club"], "italiana": ["Bella Italia", "Pizza360", "Gustoo", "Da Mario", "Michelangelo", "Raffaello"], "turca": ["Istanbul"], "malesiano": ["Pegaso"], "indiano": ["Haveli"], "greco": ["Greek Taverna"], "messicano": ["Ritual","Tao","Burrito","Piedra del Sol"], "coreano": ["My kimchi"]}
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------Begin data_prenotazione------------------------------------------------------------------------------------
if "data_prenotazione" not in st.session_state:
    data_prenotazione = []
    st.session_state.persone_prenotate = []
    st.session_state["data_prenotazione"] = data_prenotazione
else:
    data_prenotazione = st.session_state["data_prenotazione"]
#-----------------------------------------------------------------End data_prenotazione------------------------------------------------------------------------------
#-----------------------------------------------------------------Begin risposta_ristorante------------------------------------------------------------------------------------
if "risposta_ristorante" not in st.session_state:
    risposta_ristorante = []
    st.session_state["risposta_ristorante"] = risposta_ristorante
    st.session_state["risposta_cucina"] = []
else:
    risposta_state = st.session_state["risposta_ristorante"]
    
#-----------------------------------------------------------------End risposta_ristorante------------------------------------------------------------------------------
#-----------------------------------------------------------------Begin Mostra prenotazioni------------------------------------------------------------------------------------
if "checker_mostra_prenotazioni" not in st.session_state:
    st.session_state["df_prenotazioni"] = []
    st.session_state["checker_mostra_prenotazioni"] = []
    st.session_state.df_eliminazione=[]
    st.session_state["checker_elimina_prenotazioni"]=[]
    st.session_state.checker_prenotazioni=[]
    st.session_state.prenotazione_eliminata=[]


#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Display chat messages
Like_buttons = []
Dislike_buttons =[]
Data_buttons =[]
script_dir = os.path.dirname(os.path.abspath(__file__))
# Display chat messages
container = st.container(height=560)
j = 0
contatore_data=0
contatore_mostra=0
contatore_eliminazione=0
for i,message in enumerate(st.session_state.messages):
    with container:
        with st.chat_message(name = message["role"], avatar=message["avatar"]):
            if message["role"] == "user":
                st.markdown(message["content"])
                j += 1
            elif i == 0:
                st.markdown(message["content"])
            else:
                if st.session_state['cont'] == 1 or st.session_state['cont_mappa_display'] == 1:
                    if st.session_state['cont'] == 1:
                        st.text(message['content']) 
                        j += 1
                    else: 
                        try:
                            message['content'].seek(0)
                            st.image(message['content'], caption='Mappa', width = 320)
                        except AttributeError:
                            st.markdown(message["content"])
                            j += 1

                else:
                    st.markdown(message['content'])
                    j += 1
                            
            if message["role"]=="assistant" and i != 0 and st.session_state.mail_checker == 0 and st.session_state.buy_checker==0 and type(st.session_state.messages[i]["content"]) == str:

                col1, col2, col3 = st.columns([18,1,1])
                    
                with col2:
                    exec(f"Like_{j}=st.button('✅',key=f'btn_like{j}')")
                    exec(f"Like_buttons.append(Like_{j})")
                    if Like_buttons[-1]==True:
                        domanda = st.session_state.recensioni[j-2]["content"]
                        risposta = st.session_state.recensioni[j-1]["content"]
                        con= pyodbc.connect('DRIVER={SQL Server};SERVER=bubidb.database.windows.net;DATABASE=mlacademy-sqldb;UID=MLacademy;PWD=alten-ML-academy2023')
                        cursor= con.cursor()
                        select_query = "select * from ALTEN_RECENSIONE"
                        cursor.execute(select_query)
                        existing = False
                        for row in cursor.fetchall():
                            if domanda == row[2] and risposta == row[3]:
                                if 0 == row[1]:
                                    id = row[4]
                                    update_query = """
                                            UPDATE ALTEN_RECENSIONE
                                            SET ESITO = 1 
                                            WHERE ID = ?
                                            """
                                    cursor.execute(update_query, (id,))
                                    con.commit()
                                existing = True

                        
                        st.success(body="😄")
                        if existing == False:
                            insert_query = """
                                            INSERT INTO ALTEN_RECENSIONE
                                            VALUES (?,?,?,?)
                                            """
                            data = (str(datetime.now().date()), 1, domanda, risposta)
                            cursor.execute(insert_query, data)
                            con.commit()

                        con.close()

                
                #stampa 0 nella tabella quando l'esito è negativo
                with col3:
                    exec(f"Dislike_{j}=st.button('❌',key=f'btn_dislike{j}')")
                    exec(f"Dislike_buttons.append(Dislike_{j})")
                    if Dislike_buttons[-1]==True:
                        domanda = st.session_state.recensioni[j-1]["content"]
                        risposta = st.session_state.recensioni[j]["content"]
                        con= pyodbc.connect('DRIVER={SQL Server};SERVER=bubidb.database.windows.net;DATABASE=mlacademy-sqldb;UID=MLacademy;PWD=alten-ML-academy2023')
                        cursor= con.cursor()
                        select_query = "select * from ALTEN_RECENSIONE"
                        cursor.execute(select_query)
                        existing = False
                        for row in cursor.fetchall():
                            if domanda == row[2] and risposta == row[3]:
                                if 1 == row[1]:
                                    id = row[4]
                                    update_query = """
                                            UPDATE ALTEN_RECENSIONE
                                            SET ESITO = 0 
                                            WHERE ID = ?
                                            """
                                    cursor.execute(update_query, (id,))
                                    con.commit()
                                existing = True

                        
                        st.error(body="😞")
                        if existing == False:
                            insert_query = """
                                            INSERT INTO ALTEN_RECENSIONE
                                            VALUES (?,?,?,?)
                                            """
                            data = (str(datetime.now().date()), 0, domanda, risposta)

                            cursor.execute(insert_query, data)
                            con.commit()
                            
                        cursor.close()
                        con.close()
            elif message["role"]=="elimina_prenotazioni":
                lista_prenotazioni=[]
                num_rows = st.session_state.df_eliminazione[contatore_eliminazione].shape[0]
                nomi_colonne = list(st.session_state.df_eliminazione[contatore_eliminazione].columns)
                for indice in range(num_rows):
                    temporaneo=""
                    for column,indice_c in zip(list(st.session_state.df_eliminazione[contatore_eliminazione].loc[indice]),range(len(nomi_colonne))):
                        temporaneo= temporaneo+" "+nomi_colonne[indice_c]+": "+str(column)
                    lista_prenotazioni.append(temporaneo.strip())
                exec(f'd_{j}=st.selectbox(" ",{lista_prenotazioni}, key={j},label_visibility = "collapsed")')
                exec(f"st.session_state.prenotazione_eliminata[contatore_data] =d_{j}")
                exec(f"Data_{j}=st.button('Conferma',key=f'btn_dislike{j}')")
                exec(f"Data_buttons.append(Data_{j})")
                if Data_buttons[-1]==True and st.session_state.checker_prenotazioni[contatore_eliminazione]==1:
                    msg=f"La prenotazione {st.session_state.prenotazione_eliminata[contatore_eliminazione]} è stata cancellata con successo."
                    message = {"role": "assistant", "avatar": 'https://www.shutterstock.com/image-vector/call-center-customer-support-vector-600nw-2285364015.jpg' ,"content":msg,"contatore": 0}
                    st.session_state.messages.append(message)            
                    st.session_state.checker_prenotazioni[contatore_eliminazione]=0
                    sfun.elimina_prenotazione(st.session_state.prenotazione_eliminata[contatore_eliminazione],1984)
                contatore_eliminazione+=1
            elif message["role"]=="mostra_prenotazioni":
                st.table(st.session_state.df_prenotazioni[contatore_mostra])
                contatore_mostra+=1
            elif message["role"]=="data" and message["contatore"] == 4:
                 
                exec(f'd_{j}=st.selectbox(" ",{list(dizionario_cucine.keys())}, key={j},label_visibility = "collapsed")')
                exec(f"st.session_state['risposta_cucina'][contatore_data] =d_{j}")
                exec(f"Data_{j}=st.button('Conferma',key=f'btn_dislike{j}')")
                exec(f"Data_buttons.append(Data_{j})")

                if Data_buttons[-1]==True and st.session_state['checker_prenotazione_ristoranti'][contatore_data]==1:
                    if len(dizionario_cucine[st.session_state['risposta_cucina'][contatore_data]])==1:
                        st.session_state['risposta_ristorante'][contatore_data]=dizionario_cucine[st.session_state['risposta_cucina'][contatore_data]][0]
                        st.session_state.checker_ristoranti[contatore_data] -= 2
                        msg=f"L'unico ristorante di questa cucina è {st.session_state['risposta_ristorante'][contatore_data]}"
                        message = {"role": "data", "avatar": 'https://www.shutterstock.com/image-vector/call-center-customer-support-vector-600nw-2285364015.jpg' ,"content":msg+ ". Scegli il numero di persone.","contatore": st.session_state.checker_ristoranti[contatore_data]}
                        st.session_state.messages.append(message)            
                        st.session_state['checker_prenotazione_ristoranti'][contatore_data]=0

                    else:
                        st.session_state.checker_ristoranti[contatore_data] -= 1
                        msg=f"Il tipo di cucina che hai scelto è: {st.session_state['risposta_cucina'][contatore_data]}"
                        message = {"role": "data", "avatar": 'https://www.shutterstock.com/image-vector/call-center-customer-support-vector-600nw-2285364015.jpg' ,"content":msg+ ". Scegli il ristorante.","contatore": st.session_state.checker_ristoranti[contatore_data]}
                        st.session_state.messages.append(message)            
                        st.session_state['checker_prenotazione_ristoranti'][contatore_data]=0


            elif message["role"]=="data" and message["contatore"] == 3:
                lista_cucine=[]
                for i in dizionario_cucine[st.session_state["risposta_cucina"][contatore_data]]:
                    lista_cucine.append(i)

                if len(lista_cucine)==2:
                    col1,col2, col3, col4, col5= st.columns([2,5,3,5,2])
 
                    with col2:
                        if st.button(lista_cucine[0],key=f'button_uno_{j}') and st.session_state.checker_cucina[contatore_data]==1:
                            st.session_state.checker_ristoranti[contatore_data] -= 1 
                            st.session_state.checker_cucina[contatore_data]=0
                            st.session_state['risposta_ristorante'][contatore_data]=lista_cucine[0]
                            msg=f"Il ristorante che hai scelto è: {st.session_state['risposta_ristorante'][contatore_data]}"
                            message = {"role": "data", "avatar": 'https://www.shutterstock.com/image-vector/call-center-customer-support-vector-600nw-2285364015.jpg' ,"content":msg + ". Scegli il numero di persone.", "contatore": st.session_state.checker_ristoranti[contatore_data]}
                            st.session_state.messages.append(message)
 
                    with col4:
                        if st.button(lista_cucine[1],key=f'button_due_{j}') and st.session_state.checker_cucina[contatore_data]==1:
                            st.session_state.checker_ristoranti[contatore_data] -= 1 
                            st.session_state.checker_cucina[contatore_data]=0
                            st.session_state['risposta_ristorante'][contatore_data]=lista_cucine[1]
                            msg=f"Il ristorante che hai scelto è: {st.session_state['risposta_ristorante'][contatore_data]}"
                            message = {"role": "data", "avatar": 'https://www.shutterstock.com/image-vector/call-center-customer-support-vector-600nw-2285364015.jpg' ,"content":msg + ". Scegli il numero di persone.", "contatore": st.session_state.checker_ristoranti[contatore_data]}
                            st.session_state.messages.append(message)
                            

                elif len(lista_cucine)==3:
                    col1,col2, col3, col4, col5, col6, col7= st.columns([1,2,1,2,1,2,1])
 
                    with col2:
                        if st.button(lista_cucine[0],key=f'button_uno_{j}') and st.session_state.checker_cucina[contatore_data]==1:
                            st.session_state.checker_ristoranti[contatore_data] -= 1 
                            st.session_state.checker_cucina[contatore_data]=0
                            st.session_state['risposta_ristorante'][contatore_data]=lista_cucine[0]
                            msg=f"Il ristorante che hai scelto è: {st.session_state['risposta_ristorante'][contatore_data]}"
                            message = {"role": "data", "avatar": 'https://www.shutterstock.com/image-vector/call-center-customer-support-vector-600nw-2285364015.jpg' ,"content":msg + ". Scegli il numero di persone.", "contatore": st.session_state.checker_ristoranti[contatore_data]}
                            st.session_state.messages.append(message)

                    with col4:
                        if st.button(lista_cucine[1],key=f'button_due_{j}') and st.session_state.checker_cucina[contatore_data]==1:
                            st.session_state.checker_ristoranti[contatore_data] -= 1 
                            st.session_state.checker_cucina[contatore_data]=0
                            st.session_state['risposta_ristorante'][contatore_data]=lista_cucine[1]
                            msg=f"Il ristorante che hai scelto è: {st.session_state['risposta_ristorante'][contatore_data]}"
                            message = {"role": "data", "avatar": 'https://www.shutterstock.com/image-vector/call-center-customer-support-vector-600nw-2285364015.jpg' ,"content":msg + ". Scegli il numero di persone.", "contatore": st.session_state.checker_ristoranti[contatore_data]}
                            st.session_state.messages.append(message)
                    with col6:
                        if st.button(lista_cucine[2],key=f'button_tre_{j}') and st.session_state.checker_cucina[contatore_data]==1:
                            st.session_state.checker_ristoranti[contatore_data] -= 1 
                            st.session_state.checker_cucina[contatore_data]=0
                            st.session_state['risposta_ristorante'][contatore_data]=lista_cucine[2]
                            msg=f"Il ristorante che hai scelto è: {st.session_state['risposta_ristorante'][contatore_data]}"
                            message = {"role": "data", "avatar": 'https://www.shutterstock.com/image-vector/call-center-customer-support-vector-600nw-2285364015.jpg' ,"content":msg + ". Scegli il numero di persone.", "contatore": st.session_state.checker_ristoranti[contatore_data]}
                            st.session_state.messages.append(message)
                elif len(lista_cucine)==4:
                    col1,col2, col3, col4, col5, col6, col7,col8,col9= st.columns([1,2,1,2,1,2,1,2,1])
 
                    with col2:
                        if st.button(lista_cucine[0],key=f'button_uno_{j}') and st.session_state.checker_cucina[contatore_data]==1:
                            st.session_state.checker_ristoranti[contatore_data] -= 1 
                            st.session_state.checker_cucina[contatore_data]=0
                            st.session_state['risposta_ristorante'][contatore_data]=lista_cucine[0]
                            msg=f"Il ristorante che hai scelto è: {st.session_state['risposta_ristorante'][contatore_data]}"
                            message = {"role": "data", "avatar": 'https://www.shutterstock.com/image-vector/call-center-customer-support-vector-600nw-2285364015.jpg' ,"content":msg + ". Scegli il numero di persone.", "contatore": st.session_state.checker_ristoranti[contatore_data]}
                            st.session_state.messages.append(message)

                    with col4:
                        if st.button(lista_cucine[1],key=f'button_due_{j}') and st.session_state.checker_cucina[contatore_data]==1:
                            st.session_state.checker_ristoranti[contatore_data] -= 1 
                            st.session_state.checker_cucina[contatore_data]=0
                            st.session_state['risposta_ristorante'][contatore_data]=lista_cucine[1]
                            msg=f"Il ristorante che hai scelto è: {st.session_state['risposta_ristorante'][contatore_data]}"
                            message = {"role": "data", "avatar": 'https://www.shutterstock.com/image-vector/call-center-customer-support-vector-600nw-2285364015.jpg' ,"content":msg + ". Scegli il numero di persone.", "contatore": st.session_state.checker_ristoranti[contatore_data]}
                            st.session_state.messages.append(message)
                    with col6:
                        if st.button(lista_cucine[2],key=f'button_tre_{j}') and st.session_state.checker_cucina[contatore_data]==1:
                            st.session_state.checker_ristoranti[contatore_data] -= 1 
                            st.session_state.checker_cucina[contatore_data]=0
                            st.session_state['risposta_ristorante'][contatore_data]=lista_cucine[2]
                            msg=f"Il ristorante che hai scelto è: {st.session_state['risposta_ristorante'][contatore_data]}"
                            message = {"role": "data", "avatar": 'https://www.shutterstock.com/image-vector/call-center-customer-support-vector-600nw-2285364015.jpg' ,"content":msg + ". Scegli il numero di persone.", "contatore": st.session_state.checker_ristoranti[contatore_data]}
                            st.session_state.messages.append(message)
                    
                    with col8:
                        if st.button(lista_cucine[3],key=f'button_quattro_{j}') and st.session_state.checker_cucina[contatore_data]==1:
                            st.session_state.checker_ristoranti[contatore_data] -= 1 
                            st.session_state.checker_cucina[contatore_data]=0
                            st.session_state['risposta_ristorante'][contatore_data]=lista_cucine[3]
                            msg=f"Il ristorante che hai scelto è: {st.session_state['risposta_ristorante'][contatore_data]}"
                            message = {"role": "data", "avatar": 'https://www.shutterstock.com/image-vector/call-center-customer-support-vector-600nw-2285364015.jpg' ,"content":msg + ". Scegli il numero di persone.", "contatore": st.session_state.checker_ristoranti[contatore_data]}
                            st.session_state.messages.append(message)
                else:#Mettiamo la tendina
                    exec(f'd_{j}=st.selectbox(" ",{lista_cucine}, key={j},label_visibility = "collapsed")')
                    exec(f"st.session_state['risposta_ristorante'][contatore_data] =d_{j}")
                    exec(f"Data_{j}=st.button('Conferma',key=f'btn_dislike{j}')")
                    exec(f"Data_buttons.append(Data_{j})")
                    if Data_buttons[-1]==True and st.session_state.checker_cucina[contatore_data]==1:
                        st.session_state.checker_ristoranti[contatore_data] -= 1
                        msg=f"Il ristorante che hai scelto è: {st.session_state['risposta_ristorante'][contatore_data]}"
                        message = {"role": "data", "avatar": 'https://www.shutterstock.com/image-vector/call-center-customer-support-vector-600nw-2285364015.jpg' ,"content":msg+ ". Scegli il numero di persone.","contatore": st.session_state.checker_ristoranti[contatore_data]}
                        st.session_state.messages.append(message)            
                        st.session_state.checker_cucina[contatore_data]=0

                
                
               
                


            elif message["role"]=="data" and message["contatore"] == 2:
                exec(f'p_{j}=st.number_input(" ",min_value = 1, max_value = 50, key={j},label_visibility = "collapsed")')
                exec(f"st.session_state.persone_prenotate[{contatore_data}] =p_{j}")
                exec(f"Data_{j}=st.button('Conferma',key=f'btn_dislike{j}')")
                exec(f"Data_buttons.append(Data_{j})")
                if Data_buttons[-1]==True and st.session_state.checker_persone[contatore_data]== 1:
                    st.session_state.checker_ristoranti[contatore_data] -= 1  
                    msg=f"Il numero di persone è: {st.session_state.persone_prenotate[contatore_data]}"
                    message = {"role": "data", "avatar": 'https://www.shutterstock.com/image-vector/call-center-customer-support-vector-600nw-2285364015.jpg' ,"content":msg + ". Scegli la data e la fascia oraria tra quelle disponibili.", "contatore": st.session_state.checker_ristoranti[contatore_data]}

                    st.session_state.messages.append(message)
                    st.session_state.checker_persone[contatore_data]=0
                    

            elif message["role"]=="data" and message["contatore"] == 1:
                con= pyodbc.connect('DRIVER={SQL Server};SERVER=bubidb.database.windows.net;DATABASE=mlacademy-sqldb;UID=MLacademy;PWD=alten-ML-academy2023')
                cursor= con.cursor()
                select_date_disponibili = """SELECT Giorno, FasciaOraria
                                        FROM Ristoranti
                                        WHERE NomeRistorante = ? AND CapienzaTotale >= ? AND Giorno >= CONVERT(date, GETDATE());"""
                cursor.execute(select_date_disponibili,(st.session_state.risposta_ristorante[contatore_data],st.session_state.persone_prenotate[contatore_data]))
                lista_date_disponibili = []
                for row in cursor.fetchall():
                    lista_date_disponibili.append(row)

                lista_box=[]
                for i in lista_date_disponibili:
                    lista_box.append("Data: " + i[0] + " Fascia Oraria: " + i[1])
                con.close()

                date_default= datetime.now().date()
                exec(f'd_{j}=st.selectbox(" ",{lista_box}, key={j},label_visibility = "collapsed")')
                exec(f"st.session_state.data_prenotazione[{contatore_data}] =d_{j}")
                exec(f"Data_{j}=st.button('Conferma',key=f'btn_dislike{j}')")
                exec(f"Data_buttons.append(Data_{j})")
                if Data_buttons[-1]==True and st.session_state.checker_data[contatore_data]==1:
                    st.session_state.checker_ristoranti[contatore_data] = 0
                    msg=f"Prenotazione effettuata: {st.session_state.data_prenotazione[contatore_data]}"
                    sfun.Prenotazione_Ristoranti(1984,st.session_state.risposta_ristorante[contatore_data],st.session_state.data_prenotazione[contatore_data],st.session_state.persone_prenotate[contatore_data])
                    message = {"role": "assistant", "avatar": 'https://www.shutterstock.com/image-vector/call-center-customer-support-vector-600nw-2285364015.jpg' ,"content":msg,"contatore": st.session_state.checker_ristoranti[contatore_data]}
                    st.session_state.messages.append(message)            
                    st.session_state.checker_data[contatore_data]=0
                contatore_data+=1
                    
                    
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)),"Ambiente.env"))
azure_openai_endpoint = os.getenv("openai_endpoint")
azure_openai_key = os.getenv("openai_key")

#len(memoria.chat_memory.messages)

if 'chain_risposta1' not in st.session_state:
    llm_risposta1 = AzureChatOpenAI(
        deployment_name ="init-test-gpt-35-turbo",
        model="gpt-35-turbo",
        azure_endpoint = azure_openai_endpoint,
        openai_api_type="azure",
        openai_api_version = '2023-05-15',
        openai_api_key = azure_openai_key,
        temperature=0)

    answer_prompt_risposta1 = PromptTemplate.from_template(
    """
    Data una frase in input {question} interpreta la frase in modo tale da identificare le seguenti possibilità:

    -Restituisci solo 1 se nella frase è presente la parola oggi
    -Restituisci solo 2 se nella domanda è presente la parola domani
    -Restituisci solo 3 in tutti gli altri casi.

    NELLA RISPOSTA DEVE ESSERCI SOLO IL NUMERO

    Question: {question}
    Risposta:
    """
)
    chain_risposta1 = answer_prompt_risposta1 | llm_risposta1 
    st.session_state["chain_risposta1"] = chain_risposta1

else:
    chain_risposta1 = st.session_state["chain_risposta1"]

#----------------------------------------GESTIONE TEMPERATURA-------------------------------------------------------------------------------------
# if "temperatura" not in st.session_state.keys():
#     st.session_state.temperatura = 0


if 'memoria' not in st.session_state:

    memoria = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True,
    output_key='answer'
    ) #configurazione memoria
    st.session_state["memoria"] = memoria

else:
    memoria = st.session_state["memoria"] 

if 'embedding' not in st.session_state:
    embedding = AzureOpenAIEmbeddings(
    deployment="init-test-embedding",
    model="text-embedding-ada-002",
    azure_endpoint = azure_openai_endpoint,
    openai_api_type="azure",
    openai_api_key = azure_openai_key
)
    st.session_state["embedding"] = embedding

else:
    embedding = st.session_state["embedding"] 

llm_risposta3 = AzureChatOpenAI(
    deployment_name ="init-test-gpt-35-turbo",
    model="gpt-35-turbo",
    azure_endpoint = azure_openai_endpoint,
    openai_api_type="azure",
    openai_api_version = '2023-05-15',
    openai_api_key = azure_openai_key,
    temperature = 0)

# Build prompt
template = """
            Utilizza i seguenti elementi di contesto, le domande precedenti e le relative risposte per rispondere alle domande relative agli eventi giornalieri 
            di una crociera. Rispondi solo a queste domande. Se non conosci la risposta, di' semplicemente che non la sai, senza cercare di inventare una 
            risposta (fatta eccezione per i saluti dell'utente). 
            Se non comprendi la domanda perché è mal posta o contiene errori di battitura, chiedi gentilmente all'utente di riscriverla in maniera più 
            comprensibile. Mantieni la risposta concisa e informativa.

            Rispondi esclusivamente alla domanda dell'utente senza aggiungere ulteriori informazioni.
            Ciò che genererai è una risposta ad una domanda fatta dall'utente. Dovrai quindi riprendere le parole presenti nella domanda dell'utente.

            Esempio 1:
            Domanda: quali sono gli eventi di questa sera?
            Risposta: questa sera è prevista la cena al ristorante Red Velvet e successivamente lo spettacolo di benvenuto al teatro L'Avanguardia.
             

            NOTA BENE: 
            L'informazione temporale all'interno del contesto può essere rappresentata mediante fasce orarie, ad esempio: 14:00 - 17:00, 21:00 - 23:00, 
            8:30 - 9:30.
           
            Quando ti viene posta una domanda su un orario (ad esempio 15:30) che rientra in una fascia oraria (ad esempio 14:00 - 17:00) presente negli eventi 
            previsti, hai informazioni necessarie per poter rispondere e dire che quell'orario rientra nella fascia oraria in cui sono previsti determinati eventi. 

            Esempio 2:
            Domanda: Quale evento ci sarà alle 15:30?
            Risposta: Alle 15:30 avrai del tempo libero per esplorare Marsiglia, fare shopping o rilassarti in uno dei caffè locali. Questo potrai farlo dalle 14:00
            alle 17:00.

            Nella risposta puoi dirmi che non ci sono eventi specifici previsti se e solo se l'orario indicato dall'utente non rientra in nessuna fascia oraria.

            NB: se ti venisse posta una domanda per un orario al quale corrispondono più eventi, rispondi riportando ognuno di essi con i rispettivi orari di inizio e fine.
            
            Esempio 3:
            Domanda: Quali sono gli eventi previsti alle ore 9:30?
            Risposta: Alle ore 9:30 termina la colazione al Buffet Il Cerchio d'Oro. Inoltre, a partire dalle 9:00 sarà possibile partecipare ad una delle escursioni organizzate dalla nostra compagnia a Marsiglia.

            {context}
            Domanda: {question}
            Risposta:
            """
QA_CHAIN_PROMPT = PromptTemplate(input_variables=["context", "question"],template=template)


if "vectordb" not in st.session_state:
    text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,  # Size of each chunk in characters
    chunk_overlap=0,  # Overlap between consecutive chunks
    length_function=len,  # Function to compute the length of the text
    separators= ['---'] # Flag to add start index to each chunk
    )

 
    path_data = os.path.join(script_dir, "data")

    input_pdf_path = os.path.join(path_data, "programma_giornaliero_msc_giorno2.pdf")
    output_pdf_path = os.path.join(path_data, "programma_giornaliero_msc_giorno2_modificato.pdf")
    second_line = sfun.process_pdf(input_pdf_path, output_pdf_path)

    loader = PyPDFLoader(output_pdf_path)
    pages = loader.load()


    chunks = text_splitter.split_documents(pages)

    for chunk in chunks:
        chunk.metadata['giorno_di_riferimento'] = second_line  

    vectordb = Chroma.from_documents(
         documents=chunks,
         embedding=embedding
     )
    


    st.session_state["vectordb"] = vectordb
else:
    vectordb = st.session_state['vectordb']


qa_chain = ConversationalRetrievalChain.from_llm(
    llm_risposta3,
    retriever=vectordb.as_retriever(),
    combine_docs_chain_kwargs = {'prompt': QA_CHAIN_PROMPT},
    memory = memoria
)

#-------------------------------------------------Navigazione nave-------------------------------------------------------------------#

path_piantina = os.path.join(script_dir, "piantine")

#piano 1 nero e colorato
file1 = os.path.join(path_piantina, "piano1_nera.jpg")
file2 = os.path.join(path_piantina,"piano1_colorata.jpg")

#piano 2 nero e colorato
file3 = os.path.join(path_piantina, "piano2_nera.jpg")
file4 = os.path.join(path_piantina, "piano2_colorato.jpg")

#piano 3 nero e colorato
file5 = os.path.join(path_piantina, "piano3_nero.jpg")
file6 = os.path.join(path_piantina, "piano3_colorata.jpg")

#primo piano
image1 = cv2.imread(file1,cv2.IMREAD_UNCHANGED)
image_colori1 = cv2.imread(file2,cv2.IMREAD_COLOR)
image_colori1 = cv2.cvtColor(image_colori1, cv2.COLOR_BGR2RGB)

#secondo piano
image2 = cv2.imread(file3,cv2.IMREAD_UNCHANGED)
image_colori2 = cv2.imread(file4,cv2.IMREAD_COLOR)
image_colori2 = cv2.cvtColor(image_colori2, cv2.COLOR_BGR2RGB)

#terzo piano
image3 = cv2.imread(file5,cv2.IMREAD_UNCHANGED)
image3_colore = cv2.imread(file6,cv2.IMREAD_UNCHANGED)

dim_colori1 = (160,1024)
image_colori1 = cv2.resize(image_colori1,dim_colori1)

dim_colori2 = (320, 1024)
image_colori2 =  cv2.resize(image_colori2,dim_colori2)

image_colori3= cv2.resize(image3_colore, dim_colori2)

piano1_bn = sfun.immagine(jpg_bn=image1)
piano1_c = sfun.immagine(jpg_c=image_colori1)
piano2_bn = sfun.immagine(jpg_bn=image2)
piano2_c = sfun.immagine(jpg_c=image_colori2)
piano3_bn = sfun.immagine(jpg_bn=image3)
piano3_c = sfun.immagine(jpg_c=image3_colore)

if "dizionario1" not in st.session_state:
    prima_fila = {}
    seconda_fila = {}
    terza_fila = {}
    quarta_fila = {}

    #prima fila
    for i in range(1202,1258,4):
        prima_fila[i] = None

    for i in range(1256,1272,2):
        prima_fila[i] = None
        
    for i in range(1274,1350,4):
        prima_fila[i] = None
        
    for i in range(1348,1392,2):
        prima_fila[i] = None
        
    for i in range(1396,1420,4):
        prima_fila[i] = None

    #quarta fila
    for i in range(1201,1213,4):
        quarta_fila[i] = None
        
    for i in range(1215,1259,4):
        quarta_fila[i] = None

    for i in range(1257,1273,2):
        quarta_fila[i] = None

    for i in range(1275,1315,4):
        quarta_fila[i] = None

    for i in range(1317,1353,4):
        quarta_fila[i] = None
        
    for i in range(1351,1391,2):
        quarta_fila[i] = None

    for i in range(1393,1413,4):
        quarta_fila[i] = None

    for i in range(1415,1427,4):
        quarta_fila[i] = None
        
    #seconda fila 
    for i in range(1204,1256,4):
        seconda_fila[i] = None

    for i in range(1272,1348,4):
        seconda_fila[i] = None
    seconda_fila[1392] = None

    for i in range(1394,1422,4):
        seconda_fila[i] = None

    seconda_fila[1420] = None

    #terza fila
    for i in range(1203,1215,4):
        terza_fila[i] = None
        
    for i in range(1217,1257,4):
        terza_fila[i] = None

    for i in range(1273,1313,4):
        terza_fila[i] = None

    for i in range(1315,1351,4):
        terza_fila[i] = None

    #terza_fila[1391] = None
    for i in range(1391,1415,4):
        terza_fila[i] = None

    for i in range(1417,1429,4):
        terza_fila[i] = None

    ascensori = {
        'ascensore 1':[161,348],
        'ascensore 2':[161,843]
    }

    vettore = np.linspace(153, 315, 15)
    vettore2 = np.linspace(337,946,69-15)    
    indice = range(15,len(prima_fila))


    vettore_seconda_fila = np.linspace(153,293,13)
    vettore_seconda_fila_2 = np.linspace(405,612,19)
    vettore_seconda_fila_3 = np.linspace(876,957,8)
    indice_fila_due = range(13,13+19)
    indice_file_due_3 = range(13+19+1,13+19+9)


    #prima fila
    for index,coordinata in enumerate(vettore):
        chiave = list(prima_fila.keys())[index]
        prima_fila[chiave] = [83,round(coordinata)]
        
    for index,coordinata in zip(indice,vettore2):
        chiave = list(prima_fila.keys())[index]
        prima_fila[chiave] = [83,round(coordinata)]
        
    #quarta fila
    for index,coordinata in enumerate(vettore):
        chiave = list(quarta_fila.keys())[index]
        quarta_fila[chiave] = [236,round(coordinata)]

    for index,coordinata in zip(indice,vettore2):
        chiave = list(quarta_fila.keys())[index]
        quarta_fila[chiave] = [236,round(coordinata)]
        
    #seconda fila
    for index,coordinata in enumerate(vettore_seconda_fila):
        chiave = list(seconda_fila.keys())[index]
        seconda_fila[chiave] = [88,round(coordinata)]

    for index,coordinata in zip(indice_fila_due,vettore_seconda_fila_2):
        chiave = list(seconda_fila.keys())[index]
        seconda_fila[chiave] = [88,round(coordinata)]
        
    for index,coordinata in zip(indice_file_due_3,vettore_seconda_fila_3):
        chiave = list(seconda_fila.keys())[index]
        seconda_fila[chiave] = [88,round(coordinata)]
        
    seconda_fila[1392] = [88,858]

    #terza fila
    for index,coordinata in enumerate(vettore_seconda_fila):
        chiave = list(terza_fila.keys())[index]
        terza_fila[chiave] = [231,round(coordinata)]
    for index,coordinata in zip(indice_fila_due,vettore_seconda_fila_2):
        chiave = list(terza_fila.keys())[index]
        terza_fila[chiave] = [231,round(coordinata)]
    for index,coordinata in zip(indice_file_due_3,vettore_seconda_fila_3):
        chiave = list(terza_fila.keys())[index]
        terza_fila[chiave] = [231,round(coordinata)]
    terza_fila[1391] = [231,858]

    # unire dizionari
    dizionario_piano1 = [prima_fila, seconda_fila, terza_fila, quarta_fila,ascensori]
    dizionario1 ={}
    for dict in dizionario_piano1:
        for i in dict.keys():
            dizionario1[i]=dict[i]
    
    st.session_state["dizionario1"] = dizionario1
else:
    dizionario1 = st.session_state["dizionario1"]

if "dizionario2" not in st.session_state:
    vettore1_piano2 = np.linspace(73, 225, 13) 

    fila1_piano2 = {}
    fila2_piano2 = {}
    ambienti_piano2 = {}

    #prima fila
    for i in range(70101,70127,2):
        fila1_piano2[i] = None

    #seconda fila
    for i in range(70102,70128,2):
        fila2_piano2[i] = None

    #prima fila
    for index,coordinata in enumerate(vettore1_piano2):
        #cv2.line(piano2_bn,[85,round(coordinata)],[85,round(coordinata)],color=(0,0,255),thickness=2)
        chiave = list(fila1_piano2.keys())[index]
        fila1_piano2[chiave] = [85,round(coordinata)]

    #seconda fila
    for index,coordinata in enumerate(vettore1_piano2):
        #cv2.line(piano2_bn,[230,round(coordinata)],[230,round(coordinata)],color=(0,0,255),thickness=2)
        chiave = list(fila2_piano2.keys())[index]
        fila2_piano2[chiave] = [230,round(coordinata)]
    

    ambienti_piano2 = {
        'profumeria':[99,328],
        'duty free shop':[215,328],
        'card room':[69,368],
        'market place':[245,368],
        'portobello':[227,368],
        'panoramic elevator':[184,368],
        'area lounge':[159, 516],
        'casino':[159,546],
        'montecarlo casino':[158, 629],
        'conference center':[88,794],
        'conference room':[88,818],
        'cappella':[231,823],
        'teatro': [160, 855],
        'bar bellavista':[175,992],
        'corridoio tra ascensore panoramico e card room':[101, 363],
        'galleria monmatre sinistra': [118,230],
        'galleria monmatre destra': [195,230],
        'corridoio destra montecarlo casino': [196,711],
        'ala dx teatro': [273, 941], 
        'corridoio tra conference room e teatro': [110,866],
        'corridoio tra conference room e conference center': [95, 807],
        # 'corridoio sotto montecarlo casino': [115,711],
        'corridoio sopra montecarlo casino': [126, 611],
        'ascensore 1':[159,275],
        'ascensore 2':[159,807],
        #'corridoio tra teatro e cappella': [231,873],
        'corridoio tra ascensore e cappella': [206,800]
    }

    # unire dizionari
    dizionario_piano2 = [fila1_piano2, fila2_piano2, ambienti_piano2]
    dizionario2 ={}
    for dict in dizionario_piano2:
        for i in dict.keys():
            dizionario2[i]=dict[i]
        
    st.session_state["dizionario2"] = dizionario2
else:
    dizionario2 = st.session_state["dizionario2"]

if "dizionario3" not in st.session_state:
    dizionario3 = {
        'teatro rex':[156,317],
        'ufficio turistico':[95,385],
        'servizio clienti':[256,396],
        'atrio costa':[100,434],
        'bar costa':[256,452],
        'ristorante raffaello':[160,494],
        'atrio michelangelo':[159,880],
        'ristorante michelangelo':[161,946],
        'ascensore 1':[159,353],
        'ascensore 2':[159,838],
        'corridoio tra teatro rex e ufficio turistico':[98,360],
        'corridoio tra teatro rex e servizio clienti':[221,360]
    }
    st.session_state["dizionario3"] = dizionario3
else:
    dizionario3 = st.session_state["dizionario3"]


#-----------------------------------------------------------------------Ristoranti-----------------------------------------------------------------------------------------    



if "chain_interpreta_ristoranti" not in st.session_state:
    llm_partenza = AzureChatOpenAI(
    deployment_name ="init-test-gpt-35-turbo",
    model="gpt-35-turbo",
    azure_endpoint = azure_openai_endpoint,
    openai_api_type="azure",
    openai_api_version = '2023-05-15',
    openai_api_key = azure_openai_key,
    temperature=0)

    answer_prompt_nota = PromptTemplate.from_template(
        """Data una lista di luoghi: {ristoranti} e una parola in entrata: {question}, trova nella lista la parola più simile o quella uguale, se c'è. La risposta deve contenere solo la parola selezionata dalla lista, scritta esattamente com'era scritta nella lista.
            Esempio: Lista di luoghi: ["Roma", "Milano", "Firenze", "Napoli"] Parola in entrata: "Milano"
            Risposta: Milano
            Lista di luoghi: ["Roma", "Milano", "Firenze", "Napoli"] Parola in entrata: "Napl"
            Risposta: Napoli
        
            Rispondi solo con la risposta

        """
    )

    answer_nota = answer_prompt_nota | llm_partenza  
    chain_interpreta_ristoranti = answer_nota
    st.session_state["chain_interpreta_ristoranti"] = chain_interpreta_ristoranti
else:
    chain_interpreta_ristoranti = st.session_state["chain_interpreta_ristoranti"]

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------


if "chain_jpg" not in st.session_state:
    llm = AzureChatOpenAI(
    deployment_name ="init-test-gpt-35-turbo",
    model="gpt-35-turbo",
    azure_endpoint = azure_openai_endpoint,
    openai_api_type="azure",
    openai_api_version = '2023-05-15',
    openai_api_key = azure_openai_key,
    temperature=0)

    template_prova = """
    Devi descrivere lo spostamento che un utente deve seguire su una nave per arrivare da un punto A a un punto B.
    In input riceverai un dizionario: {dizionario_template}, nel quale le chiavi rappresentano le cabine, gli ascensori e le altre aree della nave e il valore associato 
    indica la direzione da seguire per raggiungere il punto successivo, rappresentato dalla chiave successiva nel dizionario. 
    Tutte le chiavi che non hanno numeri non sono cabine. 
    Esempio:
    - 1202 è una cabina.
    - Bar costa, Ristorante Raffaello, Profumeria, cappella non sono cabine. 

    Nota importante: la prima chiave del dizionario rappresenta sempre la {partenza}, l'ultima chiave del dizionario rappresenta sempre l'{arrivo}.
    Devi descrivere il percorso da seguire usando come riferimento per gli spostamenti le diverse aree contenute nelle chiavi del dizionario {dizionario_template}.
    
    Istruzioni per descrivere il percorso:
        - Sii sintetico e conciso;
        - Stacca le parole.
         
           
    Come descrivere il percorso:
        - Specifica il punto di partenza;
        - Usa e nomina solo le cabine che compaiono nelle chiavi di  {dizionario_template};
        - per ogni chiave, il valore associato rappresenta lo spostamente che devi seguire per arrivare all'area rappresentata dalla chiave successiva. NON devi inserire tu stesso degli spostamenti;
        - descrivi il percorso seguendo l'ordine di {dizionario_template};
        - non specificare mai che il percorso è finito.

    NB1: per descrivere il percorso devi obbligatoriamente utilizzare tutti ed esclusivamente gli elementi contenuti in {dizionario_template} e rispettarne l'ordine.
    NB2: se per descrivere un percorso dovessi passare per "Panoramic Elevator", questo non significherà che l'utente deve prendere quest'ascensore.
    
    Input:
    `dizionario_finale`: {dizionario_template};
    `partenza`: {partenza};
    `arrivo`: {arrivo};
    Output richiesto:
    Descrizione sintetica del percorso.
    """

    prompt3 = PromptTemplate(input_variables=['dizionario_template','partenza','arrivo'],template=template_prova)
    chain_jpg = prompt3 | llm

    st.session_state["chain_jpg"] = chain_jpg
else:
    chain_jpg = st.session_state["chain_jpg"]

#----------------------------------------------------- Ramo decisionale ---------------------------------

if "chain" not in st.session_state:

    llm_partenza = AzureChatOpenAI(
    deployment_name ="init-test-gpt-35-turbo",
    model="gpt-35-turbo",
    azure_endpoint = azure_openai_endpoint,
    openai_api_type="azure",
    openai_api_version = '2023-05-15',
    openai_api_key = azure_openai_key,
    temperature=0)

    answer_prompt = PromptTemplate.from_template(
    """Data la seguente richiesta dell'utente:

    - Restituisci 1 se la domanda dell'utente include richieste sul mostrare/vedere/elencare delle prenotazioni effettuate.
     Rispondi con "1#rischiesta dell'utente" 

    - Restituisci 2 se la domanda dell'utente include richieste di informazioni sulle attività quotidiane oppure sugli eventi che si terranno.
      Rispondi con "2#domanda" senza modificare in alcun modo la domanda dell'utente.

    - Restituisci 3 se la domanda dell'utente include richieste come eliminare/cancellare/disdire/annullare una prenotazione.
      Rispondi con "3#rischiesta dell'utente" 

    - Restituiscimi 4 se l'utente richiede di annotare qualcosa. All'interno del content, oltre al numero 4, scrivi la richiesta dell'utente. 
      La struttura del content deve essere: 4#richiesta completa dell'utente. Ad esempio, un tipo di richiesta può essere la
      seguente: "Annotami che domani c'ho una riunione". In questo caso, il content sarà il seguente: 4#Annotami che domani c'ho una riunione;
    
    - Restituiscimi soltanto 5# se l'utente richiede di leggere il contenuto del file note. Ad esempio, un tipo di richiesta può essere: "Fammi visualizzare le note scritte all'interno del file note";

    - Restituiscimi soltanto 6 se l'utente richiede di cancellare il contenuto del file note. Ad esempio, un tipo di richiesta può essere: "Elimina le note scritte all'interno del file note";
    
    - Restituiscimi 7 se l'utente richiede di cancellare una riga specifica dal file note. All'interno della richiesta dell'utente sarà specificato un valore numerico 
    (ad esempio: prima, uno, 1, seconda, due, 2, etc.). All'interno del content, oltre al numero 7, scrivi questo numero. Quindi, ad esempio, 
    la struttura del content deve essere: 7#numero specificato dall'utente. Ad esempio, ad un tipo di richiesta: "Elimina la prima nota all'interno
    del file note" corrisponde un content: "7#1".
      Se l'utente specifica di cancellare l'ultima nota la struttura del content deve essere: 7#-1; Se l'utente specifica di cancellare la penultima
     nota la struttura del content deve essere: 7#-2;
    
    -Restituiscimi "9" se l'utente chiede di inviare una segnalazione oppure se l'utente dice di avere un problema. 
    Esempi di domande che possono essere poste e che ti aiuteranno ad interpretare la domanda da parte dell'utente sono: "Voglio fare una segnalazione", "Ho un problema" e "Voglio fare una segnalazione per un problema"

    -Restituiscimi "10" se l'utente chiede di fare una prenotazione o vuole mangiare in un determinato posto, indipendentemente dal tipo di cucina. 
    Analizza la richiesta e individua il luogo della prenotazione oppure l'oggetto della domanda. 
    La struttura della risposta deve essere: 10#luogo della prenotazione. Se non viene specificato il luogo, utilizza "stringa-segreta".
    Esempi: 
    Domanda: Voglio prenotare al ristorante michelangelo
    Risposta: 10#ristorante michelangelo
    Domanda : Voglio fare una prenotazione
    Risposta: 10#stringa-segreta

    -Restituiscimi "11" se l'utente vuole prenotare o vuole mangiare una particolare tipologia di cucina. 
    Esempi di tipologie di cucine: italiana, cinese, giapponese, coreana, indiana, messicana, greca, turca, malesiana...
    Esempi:
    Domanda: Voglio mangiare cinese
    Risposta: 11#cinese
    Domanda: Voglio prenotare ad un ristorante giapponese
    Risposta: 11#giapponese

    -Restituiscimi "12" se l'utente chiede di dargli delle indicazioni sul percorso migliore per arrivare da un punto di partenza ad un punto di arrivo. 
     I punti di arrivo e partenza possono essere o numeri di cabine, ascensori o ambienti ad esempio: market place, bar, capriccio lounge, ecc.. 
     Gli ascensori sono due: ascensore 1 e ascensore 2. L'utente specificherà il punto di partenza e il punto di arrivo. 
     La struttura della risposta dovrà essere del tipo: 12#punto di partenza#punto di arrivo
     Ad esempio: 
     Domanda: dimmi come arrivare alla cabina 1202 partendo dalla cabina 1307 
     Risposta: 12#1307#1202
     Domanda: come arrivo dal cinema al teatro?
     Risposta: 12#cinema#teatro
     Domanda: sono alla 70121 e devo arrivare al market place
     Risposta: 12#70121#market place
     NB: nella risposta non devi aggiungere altro.

    
    Domanda: {question}
    Risposta: """
    )


    answer = answer_prompt | llm_partenza  
    chain = answer
    
    st.session_state["chain"] = chain
else:
    chain = st.session_state["chain"]

if 'chain_nota' not in st.session_state:
    llm_partenza = AzureChatOpenAI(
    deployment_name ="init-test-gpt-35-turbo",
    model="gpt-35-turbo",
    azure_endpoint = azure_openai_endpoint,
    openai_api_type="azure",
    openai_api_version = '2023-05-15',
    openai_api_key = azure_openai_key,
    temperature=0)

    answer_prompt_nota = PromptTemplate.from_template(
        """Data la seguente richiesta dell'utente:

        - Restituiscimi soltanto 1 se l'utente richiede di annotare una risposta da te fornita precedentemente. 
          Ad esempio, un tipo di richiesta può essere la seguente: "Scrivimi questo risultato in una nota" o "Salvamelo".

        - Restituisci 2 qualora l'utente richieda espressamente di annotare qualcosa all'interno di una nota. 
          All'interno del content, oltre al numero 2, scrivi la nota. Quindi, ad esempio, la struttura del content deve essere: "2 - [nota da scrivere]".

        Ad Esempio:

        Richiesta dell'utente: "Per favore, annota che la riunione è stata spostata a domani."
        Risposta: "2 - la riunione è stata spostata a domani."

    Domanda: {question}
    Risposta: """
    )

    answer_nota = answer_prompt_nota | llm_partenza  
    chain_nota = answer_nota

    st.session_state["chain_nota"] = chain_nota
else:
    chain_nota = st.session_state["chain_nota"]



from datetime import datetime

def generate_response(prompt_input):
    cont = 0
    cont_mappa = 0
    checker_try_catch = 0
    st.session_state['cont'] = cont
    st.session_state['cont_mappa'] = cont_mappa
    st.session_state['checker_try_catch'] = checker_try_catch
    global risp_nota 
    risposta = chain.invoke({"question": prompt_input}).content #Stampami un Codice Isin casuale
    lista_risposta=risposta.split('#')



    if lista_risposta[0].strip() == '1': 
        risultato = chain_risposta1.invoke({"question": lista_risposta[1]}).content
        st.session_state.df_prenotazioni.append(sfun.mostra_prenotazioni(int(risultato[0]),1984))
        #st.table(df_prenotazioni)
        st.session_state["checker_mostra_prenotazioni"].append(1)
        risp_nota="Queste sono le tue prenotazioni:"
        return "Queste sono le tue prenotazioni:"


    elif lista_risposta[0].strip() == '2': #RAG: Prende informazione da pdf
        question = lista_risposta[1]
       
        result = qa_chain({"question": question})
        risultato = result['answer']
        return risultato

    
    elif lista_risposta[0].strip() == '3':
        st.session_state.df_eliminazione.append(sfun.mostra_prenotazioni(3,1984))
        #st.table(df_prenotazioni)
        st.session_state["checker_elimina_prenotazioni"].append(1)
        st.session_state.checker_prenotazioni.append(1)
        st.session_state.prenotazione_eliminata.append(1)
        risp_nota="Quale prenotazione vuoi eliminare?"
        return "Quale prenotazione vuoi eliminare?:"
             

    elif lista_risposta[0].strip() == '4': #Salvataggio in nota

        st.session_state['checker_try_catch'] = 1
        risposta_nota = chain_nota.invoke({"question": lista_risposta[1]}).content
        # Ottieni la data e l'ora corrente
        now = datetime.now()

        # Formatta la data come stringa
        date_string = now.strftime("%Y-%m-%d %H:%M:%S")

        date_string = 'Nota del ' + date_string +": "
        if risposta_nota == '1':
            try:
                sfun.save_note(date_string, st.session_state['risultato'])
                risp_nota = "La nota è stata salvata correttamente :)"
                # return "La nota è stata salvata correttamente :)"
            except NameError:
                risp_nota = "Non è stato possibile elaborare la richiesta"
                #return 'Non è stato possibile elaborare la richiesta'
        else:
            lista_risposta_nota = risposta_nota.split('-')
            sfun.save_note(date_string, lista_risposta_nota[1].strip())
            #return "La nota è stata salvata correttamente :)"
            risp_nota = "La nota è stata salvata correttamente :)"
    
    elif lista_risposta[0].strip() == "5":
        cont += 1
        st.session_state["cont"] = cont

        risultato = sfun.read_note()
        st.session_state["risultato"] = risultato
        return risultato
    
    elif lista_risposta[0].strip() == "6": #cancellazione note

        st.session_state['checker_try_catch'] = 1
        risultato = sfun.delete_note()
        risp_nota = "Il contenuto delle note è stato cancellato con successo."
        #return 'Il contenuto delle note è stato cancellato con successo.'

    elif lista_risposta[0].strip()== "7":
        st.session_state['checker_try_catch'] = 1
        risultato = sfun.delete_row(lista_risposta[1].strip())
        risp_nota = "La nota è stata cancellata"
        #return 'La nota è stata cancellata'
    
    elif risposta[0].strip() == "8": 
        return "Non sono autorizzato ad eseguire queste operazioni"
    

    elif lista_risposta[0].strip() == "9":
        
        

        if "stringa-segreta" not in st.session_state.mail_body:
            st.session_state.sicuro = 's'
            return sfun.riassunto_segnalazione(st.session_state.mail_body)
        else:
            st.session_state.mail_checker= 2
            return "Inserisci il testo della segnalazione (se non vuoi mandare la segnalazione scrivi esci)"
        
    #PRENOTAZIONI
    elif lista_risposta[0].strip() == "10" or lista_risposta[0].strip() == "11":
        st.session_state['checker_try_catch'] = 1
        risposta_ristoranti = lista_risposta[1].split(" ")
        if len(risposta_ristoranti) == 1:
            if risposta_ristoranti[0] == "stringa-segreta":
                st.session_state["checker_ristoranti"].append(4)
                st.session_state["risposta_cucina"].append(risposta)
                st.session_state["checker_data"].append(1)
                st.session_state["checker_persone"].append(1)
                st.session_state.persone_prenotate.append(1)
                st.session_state.data_prenotazione.append(1)
                st.session_state.checker_cucina.append(1)
                st.session_state.risposta_ristorante.append(1)
                st.session_state['checker_prenotazione_ristoranti'].append(1)
                risp_nota ="Scegli la cucina che desideri mangiare"
                return "Scegli la cucina che desideri mangiare"
            else:
                risposta = chain_interpreta_ristoranti.invoke({"question": risposta_ristoranti[0], "ristoranti": dizionario_cucine.keys()}).content
                st.session_state["risposta_cucina"].append(risposta)
                st.session_state["checker_data"].append(1)
                st.session_state["checker_persone"].append(1)
                st.session_state.persone_prenotate.append(1)
                st.session_state.data_prenotazione.append(1)
                st.session_state.checker_cucina.append(1)
                st.session_state['checker_prenotazione_ristoranti'].append(1)
                if len(dizionario_cucine[risposta]) > 1:
                    risp_nota ="Scegli il ristorante di questa cucina"
                    st.session_state["checker_ristoranti"].append(3)
                    st.session_state["risposta_ristorante"].append(1)
                    return "Scegli il ristorante di questa cucina"
                else:
                    risp_nota = f"L'unico ristorante di questa cucina è {dizionario_cucine[risposta][0]}"
                    st.session_state["risposta_ristorante"].append(dizionario_cucine[risposta][0])
                    st.session_state["checker_ristoranti"].append(2)
                    return  f"L'unico ristorante di questa cucina è {dizionario_cucine[risposta][0]}"
        else:
            risposta1 = chain_interpreta_ristoranti.invoke({"question": risposta_ristoranti[1], "ristoranti": dizionario_cucine.keys()}).content
            risposta2 = chain_interpreta_ristoranti.invoke({"question": risposta_ristoranti[1], "ristoranti": ristoranti}).content
            if risposta1 in dizionario_cucine.keys():
                st.session_state["risposta_cucina"].append(risposta1)
                st.session_state["checker_data"].append(1)
                st.session_state["checker_persone"].append(1)
                st.session_state.persone_prenotate.append(1)
                st.session_state.data_prenotazione.append(1)
                st.session_state.checker_cucina.append(1)
                st.session_state['checker_prenotazione_ristoranti'].append(1)
                if len(dizionario_cucine[risposta1]) > 1:
                    risp_nota ="Scegli il ristorante di questa cucina"
                    st.session_state["checker_ristoranti"].append(3)
                    st.session_state["risposta_ristorante"].append(1)
                    return "Scegli il ristorante di questa cucina"
                else:
                    risp_nota = f"L'unico ristorante di questa cucina è {dizionario_cucine[risposta1][0]}"
                    st.session_state["checker_ristoranti"].append(2)
                    st.session_state["risposta_ristorante"].append(dizionario_cucine[risposta1][0])
                    return  f"L'unico ristorante di questa cucina è {dizionario_cucine[risposta1][0]}"
            elif risposta2 in ristoranti:
                st.session_state["risposta_ristorante"].append(risposta2)
                st.session_state["risposta_cucina"].append(1)
                st.session_state["checker_ristoranti"].append(2)
                st.session_state["checker_data"].append(1)
                st.session_state["checker_persone"].append(1)
                st.session_state.persone_prenotate.append(1)
                st.session_state.data_prenotazione.append(1)
                st.session_state.checker_cucina.append(1)
                st.session_state['checker_prenotazione_ristoranti'].append(1)
                risp_nota="Selezione il numero di persone per la prenotazione."
                return "Selezione il numero di persone per la prenotazione."
            else:
                return "Il ristorante non esiste"
            

    #Tool Mappa
    elif lista_risposta[0].strip() == "12":
        st.session_state['prompt_mappa'] = prompt_input
        cont_mappa_display = 1
        st.session_state["cont_mappa_display"] = cont_mappa_display

        lista_partenza_arrivo = lista_risposta[1:len(lista_risposta)]

        if lista_partenza_arrivo[0][0].isdigit():
            partenza = int(lista_partenza_arrivo[0])
        else:
            partenza = lista_partenza_arrivo[0].lower()

        if lista_partenza_arrivo[1][0].isdigit():
            arrivo = int(lista_partenza_arrivo[1])
        else:
            arrivo = lista_partenza_arrivo[1].lower()

        tmp = sfun.verifica_partenza_arrivo(st.session_state["dizionario1"], st.session_state["dizionario2"], st.session_state["dizionario3"], partenza, arrivo)

        if tmp == 0.1:
            st.session_state["arrivo"] = arrivo
            return "A quale ristorante vuoi andare? Ristorante Michelangelo o Ristorante Raffaello."
        elif tmp == 0.2:
            st.session_state["arrivo"] = arrivo
            return "A quale bar vuoi andare? Bar Bellavista o Bar Costa."
        elif tmp == 1:
            return "Il punto di partenza e il punto di arrivo indicati non sono presenti a bordo. Rielabora la richiesta."
        elif tmp == 2:
            return "Il punto di partenza indicato non è presente a bordo. Rielabora la richiesta."
        elif tmp == 3:
            return "Il punto di arrivo indicato non è presente a bordo. Rielabora la richiesta."
        else:
            cont_piano = 0
            cont_mappa += 1
            st.session_state["cont_mappa"] = cont_mappa
        
        ascensori1 = {
            'ascensore 1':[161,348],
            'ascensore 2':[161,843]
        }

        ascensori2 = {
            'ascensore 1':[159,275],
            'ascensore 2':[159,807]
        }

        ascensori3 = {
            'ascensore 1':[159,353],
            'ascensore 2':[159,838]
        }

        lista_dizionari = [dizionario1,dizionario2,dizionario3]
        lista_ascensori = [ascensori1,ascensori2,ascensori3]

        #andare all'ascensore
        def verso_ascensore(dizionario_piano,index):
            #if partenza in dizionario_piano.keys():
                minimo = float('inf')
                for i,j in lista_ascensori[index].items():
                    if sfun.distanza_euclidea(j,dizionario_piano, partenza) < minimo:
                        arrivo = i
                        minimo = sfun.distanza_euclidea(j,dizionario_piano, partenza)
                return arrivo
            
            
        #passare da un piano a un altro
        def cambiare_piano(indice_partenza,indice_arrivo):
            partenza1 = partenza
            minimo = float('inf')
            for i,j in lista_ascensori[indice_partenza].items():
                    if sfun.distanza_euclidea(j,lista_dizionari[indice_partenza], partenza1) < minimo:
                        arrivo1 = i
                        minimo = sfun.distanza_euclidea(j,lista_dizionari[indice_partenza], partenza1)
            piano_partenza = indice_partenza +1       
            partenza2 = arrivo1
            arrivo2 = arrivo
            piano_arrivo = indice_arrivo +1
            cont_piano = 1
            
            return piano_partenza,piano_arrivo,partenza1,arrivo1,partenza2,arrivo2,cont_piano
        
        #voglio andare all'ascensore più vicino
        if type(arrivo) != int and 'ascensore' in arrivo:
            if arrivo == 'ascensore':
                for i in range(len(lista_dizionari)):
                    if partenza in lista_dizionari[i].keys():
                        arrivo = verso_ascensore(lista_dizionari[i],i)
            else: 
                pass
            
        #parto da un ascensore
        elif type(partenza) != int and 'ascensore' in partenza:
            for index in range(len(lista_dizionari)):
                if arrivo in lista_dizionari[index].keys():
                    str_partenza_ascensore = f"Portati al piano {index+1}. "
                    for i,j in lista_ascensori[index].items():
                        if i == partenza:        
                            pass

        #passo da un piano a un altro
        else:
            perm = itertools.permutations(range(len(lista_dizionari)),2)
            for p in perm:
                if partenza in lista_dizionari[p[0]] and arrivo in lista_dizionari[p[1]]:
                    piano_partenza,piano_arrivo,partenza1,arrivo1,partenza2,arrivo2,cont_piano = cambiare_piano(p[0],p[1])

        def percorso(partenza, arrivo, piano):
    
            immagine = None
            dizionario = None
            finder = None 
            
            if piano == 1:
                immagine = piano1_bn
                dizionario = dizionario1
                #finder = DijkstraFinder(diagonal_movement=DiagonalMovement.never) 

            elif piano == 2:
                immagine = piano2_bn
                dizionario = dizionario2
                #finder = DijkstraFinder(diagonal_movement=DiagonalMovement.never)
             
            else:
                immagine = piano3_bn
                dizionario = dizionario3
                #finder = DijkstraFinder(diagonal_movement=DiagonalMovement.never)            

            finder = DijkstraFinder(diagonal_movement=DiagonalMovement.never)
            _,image_binary = cv2.threshold(immagine,150,255,cv2.THRESH_BINARY)
            image_binary = image_binary // 255

            punto_partenza = dizionario[partenza]
            punto_arrivo = dizionario[arrivo]
            grid = Grid(matrix=image_binary)
            part = grid.node(punto_partenza[0],punto_partenza[1])
            arr = grid.node(punto_arrivo[0],punto_arrivo[1])
            path, _ = finder.find_path(part,arr,grid)
            path_coordinate = [(node.x,node.y) for node in path]

            nuovo_path = [path_coordinate[0]]
        
            for i in range(1, len(path_coordinate) - 1):
                # Controlla se la prima o la seconda componente cambiano rispetto alle coordinate precedente e successiva
                if (path_coordinate[i][0] != path_coordinate[i-1][0] or path_coordinate[i][0] != path_coordinate[i+1][0]) and \
                    (path_coordinate[i][1] != path_coordinate[i-1][1] or path_coordinate[i][1] != path_coordinate[i+1][1]):
                    nuovo_path.append(path_coordinate[i])
            
            # Aggiungi l'ultima coordinata
            nuovo_path.append(path_coordinate[-1])

            minimo = 1e8
            prova = list()
            cabina = None

            for cor in nuovo_path:
                minimo = 1e8
                for i,j in dizionario.items():
                    #current = abs((cor[0]-j[0])) + abs((cor[1]-j[1]))
                    current = np.sqrt((cor[0]-j[0])**2 + (cor[1]-j[1])**2)
                    if current < minimo:
                        minimo = current
                        cabina = i
                if cabina not in prova:
                    prova.append(cabina)
                else:
                    continue

            dizionario_finale = {}
            for i in prova:
                dizionario_finale[i] = dizionario[i]

            return path_coordinate, dizionario_finale
    
        canale_blu = (0,0,255)
        canale_rosso = (255,0,0)
        canale_verde = (0,255,0)

        green = plt.Line2D([0],[0],marker='o',color='w',markerfacecolor='green',markersize=10)
        red = plt.Line2D([0],[0],marker='o',color='w',markerfacecolor='red',markersize=10)
        blue = plt.Line2D([0],[0],marker='o',color='w',markerfacecolor='blue',markersize=10)

        def plot_percorso(partenza,arrivo,piano,path):
            if piano == 1:
                immagine_colore = piano1_c
                dizionario = dizionario1
            elif piano == 2:
                immagine_colore = piano2_c
                dizionario = dizionario2
            elif piano == 3:
                immagine_colore = piano3_c
                dizionario = dizionario3 
                
            punto_partenza = dizionario[partenza]
            punto_arrivo = dizionario[arrivo]
            rosso = cv2.circle(immagine_colore,center=punto_partenza,radius=3,color=canale_rosso,thickness=4)
            verde = cv2.circle(immagine_colore,center=punto_arrivo,radius=3,color=canale_verde,thickness=4)
            
            for i in range(len(path)-1):
                cv2.line(immagine_colore,path[i],path[i+1],color=canale_blu,thickness=2)

            return immagine_colore

        if cont_piano == 1:
            itinerario = [(partenza1,arrivo1,piano_partenza),(partenza2,arrivo2,piano_arrivo)]
            indicazione1, dizionario_finale1= percorso(itinerario[0][0], itinerario[0][1],itinerario[0][2])
            indicazione2, dizionario_finale2= percorso(itinerario[1][0], itinerario[1][1],itinerario[1][2])
            
            im1 = plot_percorso(partenza1,arrivo1,piano_partenza,indicazione1)
            im2 = plot_percorso(partenza2,arrivo2,piano_arrivo,indicazione2) 

        else:
            if partenza in dizionario1.keys() and arrivo in dizionario1.keys():
                indicazione, dizionario_finale = percorso(partenza,arrivo,1)
                im = plot_percorso(partenza,arrivo,1,indicazione)
            
            elif partenza in dizionario2.keys() and arrivo in dizionario2.keys(): 
                indicazione, dizionario_finale = percorso(partenza,arrivo,2)
                im = plot_percorso(partenza,arrivo,2,indicazione)

            elif partenza in dizionario3.keys() and arrivo in dizionario3.keys():
                indicazione, dizionario_finale = percorso(partenza,arrivo,3)
                im = plot_percorso(partenza,arrivo,3,indicazione) 

        if cont_piano  == 0:
            svolte = sfun.analizza_percorsi1(dizionario_finale)
        elif cont_piano  == 1:
            svolte_1 = sfun.analizza_percorsi1(dizionario_finale1)
            svolte_2 = sfun.analizza_percorsi1(dizionario_finale2)
        
        dizionario1_template = {}
        if cont_piano  == 0:
            for i,j in zip(dizionario_finale,svolte):
                dizionario1_template[i] = j
            p = list(dizionario_finale.keys())[0]
            a = list(dizionario_finale.keys())[-1]
        else:
            dizionario2_template = {}
            for i,j in zip(dizionario_finale1, svolte_1):
                dizionario1_template[i] = j
            p1 = list(dizionario_finale1.keys())[0]
            a1 = list(dizionario_finale1.keys())[-1]
            for i,j in zip(dizionario_finale2, svolte_2):
                dizionario2_template[i] = j
            p2 = list(dizionario_finale2.keys())[0]
            a2 = list(dizionario_finale2.keys())[-1]
        if cont_piano  == 0:
            risposta = chain_jpg.invoke({'dizionario_template':dizionario1_template,'partenza':p,'arrivo':a}).content
            if 'ascensore' in partenza:
                risposta = str_partenza_ascensore + risposta
            st.session_state["prompt_mappa"] = ''
            return im, None, risposta
        elif cont_piano == 1:
            risposta_1 = chain_jpg.invoke({'dizionario_template':dizionario1_template,'partenza':p1,'arrivo':a1}).content
            risposta_2 = chain_jpg.invoke({'dizionario_template':dizionario2_template,'partenza':p2,'arrivo':a2}).content
            
            if piano_partenza < piano_arrivo:
                if piano_arrivo - piano_partenza == 1:
                    stringa = " Arrivato alla zona ascensore, sali di un piano. "
                else:
                    stringa = " Arrivato alla zona ascensore, sali di {} piani. ".format(piano_arrivo-piano_partenza)
            else:
                if piano_partenza - piano_arrivo == 1:
                    stringa = " Arrivato alla zona ascensore, scendi di un piano. "
                else:
                    stringa = " Arrivato alla zona ascensore, scendi di {} piani. ".format(piano_partenza-piano_arrivo)
            risposta = risposta_1 + stringa + risposta_2
            st.session_state["prompt_mappa"] = ''
            return im1, im2, risposta
    else:
        return risposta



# Funzione per il riconoscimento vocale
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

c1,c2 = st.columns([30,1])
# User-provided prompt
with c1:
    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user",  "avatar": 'https://www.clipartmax.com/png/middle/434-4349876_profile-icon-vector-png.png', "content": prompt,"contatore": 0})
        st.session_state.recensioni.append({"role": "user",  "avatar": 'https://www.clipartmax.com/png/middle/434-4349876_profile-icon-vector-png.png', "content": prompt,"contatore": 0})

        with container:
            with st.chat_message(name="user", avatar='https://www.clipartmax.com/png/middle/434-4349876_profile-icon-vector-png.png'):
                st.write(prompt)


with c2:
    if st.button("🎙️"):
        prompt = riconosci_discorso_da_mic()
        if prompt:
            # Aggiungi la trascrizione vocale alla chat come un messaggio dell'utente
            st.session_state.messages.append({"role": "user", "avatar": 'https://www.clipartmax.com/png/middle/434-4349876_profile-icon-vector-png.png', "content": prompt})
            st.session_state.recensioni.append({"role": "user", "avatar": 'https://www.clipartmax.com/png/middle/434-4349876_profile-icon-vector-png.png', "content": prompt})

            with container:
                with st.chat_message(name="user", avatar='https://www.clipartmax.com/png/middle/434-4349876_profile-icon-vector-png.png'):
                    st.write(prompt)
        else:
            st.warning("Non è stato possibile riconoscere il tuo discorso. Riprova.")


# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant" and st.session_state.messages[-1]["role"] != "mail" and st.session_state.messages[-1]["role"] != "data" and st.session_state.messages[-1]["role"] != "mostra_prenotazioni" and st.session_state.messages[-1]["role"] != "elimina_prenotazioni":
    with container:
        with st.chat_message(name = "assistant", avatar='https://www.shutterstock.com/image-vector/call-center-customer-support-vector-600nw-2285364015.jpg'):
            with st.spinner("Sto pensando...🤔"):
                if 's' in st.session_state.sicuro:
                        st.session_state.sicuro= prompt
                        if st.session_state.sicuro.lower()[0] == "s":
                                st.write(sfun.mail(st.session_state.mail_oggetto,st.session_state.mail_body, st.session_state.mail_indirizzo))
                                response ="Segnalazione inviata correttamente. Riceverai presto assistenza."
                        else:    
                                response = "Ok, segnalazione non inviata"
                                st.write(response)
                        st.session_state.mail_checker=0
                        st.session_state.sicuro ="n"
                        st.session_state.mail_body = "stringa-segreta"
                        st.session_state.mail_oggetto = "Segnalazione"
                        st.session_state.mail_indirizzo = "andreapastore326@gmail.com"

                # elif st.session_state.mail_checker == 1:
                #     if "stringa-segreta" in st.session_state.mail_body:
                #         st.write("inserisci il testo della segnalazione (se non vuoi mandare la segnalazione scrivi esci)")
                #         st.session_state.mail_checker+=1
                #         response="inserisci il testo della segnalazione (se non vuoi mandare la segnalazione scrivi esci)"
                #     else:
                #         response= sfun.riassunto_segnalazione(st.session_state.mail_body)
                #         st.write(response)
                #         st.session_state.sicuro = "s"
                    
                elif st.session_state.mail_checker==2:
                    if prompt.replace(" ","") == "":
                        st.write("inserisci il testo della segnalazione (se non vuoi mandare la segnalazione scrivi esci)")
                        response=""
                    elif prompt.lower() == "esci":
                        st.write("Segnalazione non mandata")
                        st.session_state.mail_checker=0
                        response="Segnalazione non mandata"
                    else:
                        st.session_state.mail_body= prompt
                        response= sfun.riassunto_segnalazione(st.session_state.mail_body)
                        st.write(response)
                        st.session_state.sicuro = 's'

                elif st.session_state.buy_sicuro=="s":
                    st.session_state.buy_sicuro= prompt
                    if st.session_state.buy_sicuro.lower()[0] == "s":
                            
                            if st.session_state.buy_btp in st.session_state.lista_denominazione:
                                if sfun.is_convertible_to_int(st.session_state.buy_quantità):
                                    if int(st.session_state.buy_quantità) >0:
                                        response =sfun.inserimento_acquisto(st.session_state.buy_btp,st.session_state.buy_quantità,st.session_state.lista_dati)
                                    else:
                                        response ="La quantità inserita deve essere positiva"
                                else:
                                    response ="La quantità inserita deve essere un intero positivo"
                            else:
                                 response ="Il btp inserito non è corretto"

                    else:    
                            response = "Ok procedura interrotta"
                    st.session_state.buy_checker=0
                    st.session_state.buy_sicuro ="n"
                elif st.session_state.buy_checker == 1:
                    if "stringa-segreta" in st.session_state.buy_btp:
                        st.session_state.buy_btp=prompt
                        response="Sei sicuro del tuo acquisto?"
                        st.session_state.buy_checker-=1
                        st.session_state.buy_sicuro = "s"
                    else:
                        st.session_state.buy_quantità=prompt
                        response="Sei sicuro del tuo acquisto?"
                        st.session_state.buy_checker-=1
                        st.session_state.buy_sicuro = "s"
                elif st.session_state.buy_checker == 2:
                        st.session_state.buy_btp=prompt
                        response="Inserisci quanti lotti da 1000 Euro vuoi acquistare"
                        st.session_state.buy_checker-=1
                #VENDITA:
                elif st.session_state.sell_sicuro=="s":
                    st.session_state.sell_sicuro= prompt
                    if st.session_state.sell_sicuro.lower()[0] == "s":
                            
                            if st.session_state.sell_btp in st.session_state.lista_denominazione:
                                if sfun.is_convertible_to_int(st.session_state.sell_quantità):
                                    if int(st.session_state.sell_quantità) >0:
                                        response =sfun.inserimento_vendita(st.session_state.sell_btp,st.session_state.sell_quantità,st.session_state.lista_dati)
                                    else:
                                        response ="La quantità inserita deve essere positiva"
                                else:
                                    response ="La quantità inserita deve essere un intero positivo"
                            else:
                                 response ="Il btp inserito non è corretto"                

                    else:    
                            response = "Ok procedura interrotta"
                    st.session_state.sell_checker=0
                    st.session_state.sell_sicuro ="n"
                elif st.session_state.sell_checker == 1:
                    if "stringa-segreta" in st.session_state.sell_btp:
                        st.session_state.sell_btp=prompt
                        response="Sei sicuro della tua vendita?"
                        st.session_state.sell_checker-=1
                        st.session_state.sell_sicuro = "s"
                    else:
                        st.session_state.sell_quantità=prompt
                        response="Sei sicuro della tua vendita?"
                        st.session_state.sell_checker-=1
                        st.session_state.sell_sicuro = "s"
                elif st.session_state.sell_checker == 2:
                        st.session_state.sell_btp=prompt
                        response="Inserisci quanti lotti da 1000 Euro vuoi vendere"
                        st.session_state.sell_checker-=1

                elif st.session_state["specificazione_bar_o_ristorante"] == "sì":
                    nuovo_prompt = sfun.replace_occurrence(st.session_state["prompt_mappa"], arrivo, prompt.lower())
                    img1, img2, response = generate_response(nuovo_prompt)
                    st.session_state["specificazione_bar_o_ristorante"] = ""
                    if 'img1' in globals():
                            if img2 is None: 
                                st.image(img1, caption='Mappa', width = 320)
                                st.markdown(response)
                                # Creare un oggetto PIL.Image dall'immagine matrice
                                image_buffer = Image.fromarray(img1)
                                # Converti l'immagine PIL in un buffer di memoria
                                buffer = io.BytesIO()
                                image_buffer.save(buffer, format="PNG")
                                buffer.seek(0)
                            else:
                                st.image(img1, caption='Mappa', width = 320)
                                st.image(img2, caption='Mappa', width = 320)

                                st.markdown(response)
                                # Creare un oggetto PIL.Image dall'immagine matrice
                                image1_buffer = Image.fromarray(img1)
                                image2_buffer = Image.fromarray(img2)
                                # Converti l'immagine PIL in un buffer di memoria
                                buffer1 = io.BytesIO()
                                buffer2 = io.BytesIO()
                                image1_buffer.save(buffer1, format="PNG")
                                image2_buffer.save(buffer2, format = 'PNG')
                                buffer1.seek(0)
                                buffer2.seek(0)
                else:
                    try:
                        img1, img2, response = generate_response(prompt)                              
                    except Exception as e:
                        if st.session_state.checker_try_catch == 1:
                            response = risp_nota
                        else:
                            if st.session_state["prompt_mappa"] == "":
                                response = generate_response(prompt)
                            else:
                                response = generate_response(prompt)
                                st.markdown(response)
                                if response == "A quale ristorante vuoi andare? Ristorante Michelangelo o Ristorante Raffaello." or response == "A quale bar vuoi andare? Bar Bellavista o Bar Costa.":
                                    st.session_state["specificazione_bar_o_ristorante"] = "sì"
                                # Chiedi all'utente di inserire un prompt
                                # while True:                              
                                #     user_input = st.text_input('Per favore inserisci il tuo prompt:')
                                #     if user_input:
                                #         prompt = sfun.replace_occurrence(st.session_state["prompt_mappa"], arrivo, user_input.lower())
                                #         img1, img2, response = generate_response(prompt)
                                #         break
                                #     else:
                                #         pass
                                
                                # while user_input is None:
                                #     with suppress(Exception):
                                #         user_input = st.text_input('Per favore inserisci il tuo prompt:', value = "")
                                #         user_input = None if user_input == "" else user_input

                                #         if user_input is not None:
                                #             prompt = sfun.replace_occurrence(st.session_state["prompt_mappa"], arrivo, user_input.lower())
                                #             img1, img2, response = generate_response(prompt)
                                #             break
                                #         else:
                                #             pass

                    if st.session_state['cont_mappa'] == 1:
                        if 'img1' in globals():
                            if img2 is None: 
                                st.image(img1, caption='Mappa', width = 320)
                                st.markdown(response)
                                # Creare un oggetto PIL.Image dall'immagine matrice
                                image_buffer = Image.fromarray(img1)
                                # Converti l'immagine PIL in un buffer di memoria
                                buffer = io.BytesIO()
                                image_buffer.save(buffer, format="PNG")
                                buffer.seek(0)
                            else:
                                st.image(img1, caption='Mappa', width = 320)
                                st.image(img2, caption='Mappa', width = 320)

                                st.markdown(response)
                                # Creare un oggetto PIL.Image dall'immagine matrice
                                image1_buffer = Image.fromarray(img1)
                                image2_buffer = Image.fromarray(img2)
                                # Converti l'immagine PIL in un buffer di memoria
                                buffer1 = io.BytesIO()
                                buffer2 = io.BytesIO()
                                image1_buffer.save(buffer1, format="PNG")
                                image2_buffer.save(buffer2, format = 'PNG')
                                buffer1.seek(0)
                                buffer2.seek(0)
                        else:
                            st.markdown(response)
                    else:
                        st.markdown(response)


    if len(st.session_state.checker_ristoranti)==0:
        tmp=0
    else:
        if  st.session_state.checker_ristoranti[-1]==0:
            tmp=0
        else:
            tmp=1  
    if len(st.session_state.checker_mostra_prenotazioni)==0:
        tmp1=0
    else:
        if  st.session_state.checker_mostra_prenotazioni[-1]==0:
            tmp1=0
        else:
            tmp1=1     
    if len(st.session_state.checker_elimina_prenotazioni)==0:
        tmp2=0
    else:
        if  st.session_state.checker_elimina_prenotazioni[-1]==0:
            tmp2=0
        else:
            tmp2=1                
    if st.session_state.mail_checker == 0  and tmp==0 and tmp1==0 and tmp2==0:
        if st.session_state.cont_mappa == 1:
            if 'img1' in globals():
                if img2 is None:
                    message = {"role": "assistant", "avatar": 'https://www.shutterstock.com/image-vector/call-center-customer-support-vector-600nw-2285364015.jpg' ,"content": buffer,"contatore": 0}
                    st.session_state.messages.append(message)
                    message = {"role": "assistant", "avatar": 'https://www.shutterstock.com/image-vector/call-center-customer-support-vector-600nw-2285364015.jpg' ,"content": response,"contatore": 0}
                    st.session_state.messages.append(message)
                    st.session_state.recensioni.append(message)
                else:
                    message = {"role": "assistant", "avatar": 'https://www.shutterstock.com/image-vector/call-center-customer-support-vector-600nw-2285364015.jpg' ,"content": buffer1,"contatore": 0}
                    st.session_state.messages.append(message)
                    message = {"role": "assistant", "avatar": 'https://www.shutterstock.com/image-vector/call-center-customer-support-vector-600nw-2285364015.jpg' ,"content": buffer2,"contatore": 0}
                    st.session_state.messages.append(message)
                    message = {"role": "assistant", "avatar": 'https://www.shutterstock.com/image-vector/call-center-customer-support-vector-600nw-2285364015.jpg' ,"content": response,"contatore": 0}
                    st.session_state.messages.append(message)
                    st.session_state.recensioni.append(message)
            else: 
                message = {"role": "assistant", "avatar": 'https://www.shutterstock.com/image-vector/call-center-customer-support-vector-600nw-2285364015.jpg' ,"content": response,"contatore": 0}
                st.session_state.messages.append(message)
                st.session_state.recensioni.append(message)
        else:
            message = {"role": "assistant", "avatar": 'https://www.shutterstock.com/image-vector/call-center-customer-support-vector-600nw-2285364015.jpg' ,"content": response,"contatore": 0}
            st.session_state.messages.append(message)
            st.session_state.recensioni.append(message)
    elif tmp>0:
        message = {"role": "data", "avatar": 'https://www.shutterstock.com/image-vector/call-center-customer-support-vector-600nw-2285364015.jpg' ,"content": response,"contatore": st.session_state.checker_ristoranti[-1]}
        st.session_state.messages.append(message)
        st.session_state.recensioni.append(message)
    elif tmp1>0:
        message = {"role": "mostra_prenotazioni", "avatar": 'https://www.shutterstock.com/image-vector/call-center-customer-support-vector-600nw-2285364015.jpg' ,"content": response,"contatore": 0}
        st.session_state.messages.append(message)
        st.session_state.recensioni.append(message)
        st.session_state.checker_mostra_prenotazioni[-1]=0
    elif tmp2>0:
        message = {"role": "elimina_prenotazioni", "avatar": 'https://www.shutterstock.com/image-vector/call-center-customer-support-vector-600nw-2285364015.jpg' ,"content": response,"contatore": 0}
        st.session_state.messages.append(message)
        st.session_state.recensioni.append(message)
        st.session_state.checker_elimina_prenotazioni[-1]=0
    else:
        message = {"role": "mail", "avatar": 'https://www.shutterstock.com/image-vector/call-center-customer-support-vector-600nw-2285364015.jpg' ,"content": response,"contatore": 0}
        st.session_state.messages.append(message)
        st.session_state.recensioni.append(message)
    st.rerun()




#----------------------------------------------------------------------------------------------------------------------------------------------------

 

# Fine dell'applicazione