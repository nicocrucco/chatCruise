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
from datetime import datetime
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


#bonase
st.set_page_config(page_title="ChatBTP",page_icon="🤖",layout="wide")
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
<span class="banner-text" style="font-family: sans-serif;"><b>ChatBTP</b></span>
</div>
<style>
    .banner {
        width: 100%;
        height: 200px;
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
# dopo il clic
st.markdown(
"""
<style>
    .st-emotion-cache-7ym5gk:focus:not(:active) {
        border-color: rgb(255, 255, 255);
        color: rgb(255, 255, 255);
    }
</style>
""",unsafe_allow_html=True
)
#prima di essere cliccato
st.markdown(
"""
<style>
    .st-emotion-cache-7ym5gk {
        display: inline-flex;
        -webkit-box-align: center;
        align-items: center;
        -webkit-box-pack: center;
        justify-content: center;
        font-weight: 400;
        padding: 0.25rem 0.75rem;
        border-radius: 0.5rem;
        min-height: 38.4px;
        margin: 0px;
        line-height: 1.6;
        color: rgb(255,255,255);
        width: auto;
        user-select: none;
        background-color: rgb(255, 255, 255);
        border: rgb(255, 255, 255);
    }

</style>
""",unsafe_allow_html=True
)
# passaggio del mouse
st.markdown(
"""
<style>
.st-emotion-cache-7ym5gk:hover {
    border-color:rgb(255, 255, 255);
    color: rgb(255, 255, 255);
    }

</style>
""",unsafe_allow_html=True
)

st.sidebar.title("**Scegli la mia creatività**")
st.session_state.temperatura = st.sidebar.slider(    
    "",
    min_value=0.0,    
    max_value=1.0,    
    value=0.0,
    step = 0.5,
    help="La temperatura è un indicatore di creatività del chatbot.",
)
st.sidebar.write("""\n
                """)
st.sidebar.write("""
                • **Preciso 0**\n
                • **Equilibrato 0.5**\n
                • **Creativo 1** 
                """)

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
    st.session_state.mail_oggetto = "stringa-segreta"

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
    st.session_state.messages = [{"role": "assistant", "avatar": 'https://www.shutterstock.com/image-vector/call-center-customer-support-vector-600nw-2285364015.jpg', "content": "Ciao!👋🏻\n\nSono il tuo assistente finanziario virtuale. Come posso aiutarti?"}]

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
# ---------------------------------------------------------End Checker Mappa------------------------------------------------------------------------------------   
# ---------------------------------------------------------Begin Checker Recensioni------------------------------------------------------------------------------------  
if 'recensioni' not in st.session_state:
    recensioni = list()
    st.session_state['recensioni'] = recensioni
else:
    recensioni = st.session_state['recensioni']
# ---------------------------------------------------------End Checker Recensioni------------------------------------------------------------------------------------   

# ---------------------------------------------------------Begin Checker Nota------------------------------------------------------------------------------------  
if 'checker_nota' not in st.session_state:
    checker_nota = 0
    st.session_state['checker_nota'] = 0
else:
    checker_nota = st.session_state['checker_nota']
# ---------------------------------------------------------End Checker Nota------------------------------------------------------------------------------------   
risp_nota = ""


# Display chat messages
Like_buttons = []
Dislike_buttons =[]

# Display chat messages
container = st.container(height=530)
j = 0
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
                    exec(f"Like_{j}=st.button('✅_{j}')")
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
                    exec(f"Dislike_{j}=st.button('❌_{j}')")
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

                        con.close()

azure_openai_endpoint = ""
azure_openai_key = ""
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

    # Dettagli della connessione
    user = "MLacademy"
    pw = "alten-ML-academy2023"
    host = "bubidb.database.windows.net"
    db = "mlacademy-sqldb"

    # Crea il motore SQLAlchemy per SQL Server utilizzando pymssql
    if "engine" not in st.session_state:
        st.session_state.engine = create_engine(f"mssql+pymssql://{user}:{pw}@{host}:1433/{db}")

    warnings.filterwarnings("ignore")

    table_name = 'Gruppo1_btp_Az_finale'
    table_name1 = 'ALTEN_CONTO'
    db = SQLDatabase(engine=st.session_state.engine, include_tables=[table_name,table_name1]) 
    write_query = create_sql_query_chain(llm_risposta1, db) #..andando a creare SQL Query Chain con llm e db 
    execute_query = QuerySQLDataBaseTool(db=db) #creiamo un'istanza con il db per eseguire effettivamente la query
    #nel passaggio precedente abbiamo visto che la nostra catena era in grado di dare una query valida che potesse effettivamente essere utilizzata sul nostro db.
    #In questo step implementiamo un altro elemento in quella catena che ci permetterà di eseguire quella query automaticamente:
    answer_prompt_risposta1 = PromptTemplate.from_template(
            """Riporta solo il risultato della query. Nella colonna DARE_AVERE della tabella ALTEN_CONTO la lettera C rappresenta un accredito, un guadagno, un'entrata. La lettera D rappresenta un debito, 
            un'uscita, una spesa. Gli importi di credito sono numeri positivi, mentre quelli di debito sono negativi. Non parlare di query e non riportare i nomi delle tabelle nelle risposte.
            Mostra solo i dati eventualmente una lista di dati. Se non ti viene indicata una data, utilizza la data in Data_Pr_Ufficiale più recente. 
            
            Question: {question}
            SQL Query: {query}
            SQL Result: {result}
            Answer:

            """
        )
    answer_risposta1 = answer_prompt_risposta1 | llm_risposta1 | StrOutputParser()  
    chain_risposta1 = (
        RunnablePassthrough.assign(query=write_query).assign(
            result=itemgetter("query") | execute_query
        )
        | answer_risposta1 
    )#creiamo di nuovo la catena che descriverà il modo in cui verrà elaborata la Query e la risposta

    st.session_state["chain_risposta1"] = chain_risposta1
    st.session_state.engine.dispose()

else:
    chain_risposta1 = st.session_state["chain_risposta1"]

#----------------------------------------GESTIONE TEMPERATURA-------------------------------------------------------------------------------------
if "temperatura" not in st.session_state.keys():
    st.session_state.temperatura = 0


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
    temperature = st.session_state.temperatura)

# Build prompt
template = """Utilizza i seguenti elementi di contesto, le domande precedenti e le relative risposte per rispondere esclusivamente alle domande di carattere economico e finanziario. Rispondi solo a queste domande. Se non conosci la risposta, di' semplicemente che non la sai, senza cercare di inventare una risposta (fatta eccezione per i saluti dell'utente). Se non comprendi la domanda perché è mal posta o contiene errori di battitura, chiedi gentilmente all'utente di riscriverla in maniera più comprensibile. Mantieni la risposta concisa e informativa.

Nota bene: se nella domanda sono presenti richieste con riferimento a un periodo temporale con le parole "ieri" oppure "oggi", per rispondere alla domanda utilizza i soli documents per i quali il metadato "Data_di_Pubblicazione" corrisponde al giorno specificato. 
            - nel caso in cui nella richiesta comparisse "ieri", dovrai interpretarlo come: "data = datetime.today() - timedelta(days=1)"; 
            - mentre nel caso in cui nella richiesta comparisse "oggi", dovrai interpretarlo come: "data = datetime.today()". 

            Dopo aver eseguito una delle due funzioni precedenti, formatta la data nella seguente maniera: "data_formattata = data.strftime("%Y-%m-%d")".
            A questo punto, crea una corrispondenza tra data_formattata e il metadato "Data_di_Pubblicazione" qualora presente, prendendo per quest'ultimo soltanto la parte relativa alla data. Per rispondere alla Domanda utilizza solo i documents che soddisfano la condizione. Se la condizione non dovesse essere verificata per alcun documents, dovrai rispondere nella seguente maniera: "Non ci sono informazioni.".
            Ad esempio, per una Domanda come "Quali sono le informazioni di oggi relativamente alla Borsa di Milano?", essendo che è presente la parola "oggi" dovrai utilizzare la funzione "data = datetime.today()" e di seguito eseguire la formattazione con "data_formattata = data.strftime("%Y-%m-%d")".
            Così, dovrai rispondere prendendo in considerazione tutte le informazioni contenute all'interno dei documents per i quali il valore del metadato "Data_di_Pubblicazione" (senza considerare ore, minuti e secondi) uguale al valore della variabile "data_formatatta". 
            All'interno dovrai riportare sempre tutte le informazioni contenute nei documenti che soddisfano la condizione sopra definita e solo quando ti è esplicitamente richiesto dall'utente dovrai riportare soltanto le più recenti.
            Se la condizione non dovesse essere verificata per alcun documents, dovrai rispondere nella seguente maniera: "Non ci sono informazioni.".
            
            Inoltre, qualora ti venisse chiesto di dare informazioni generali relativamente ad un giorno (ieri o oggi) senza specificare un preciso argomento, rispondi facendo un riassunto utilizzando tutti i documents, e le informazioni che contengono, che soddisfano la condizione sopra definita.
            Un tipo di richieste classificabili come questo tipo sono: "Fammi un riassunto delle informazioni di oggi", "Cos'è accaduto ieri?", etc. 
            Ad esempio, per una Domanda come: "Fammi un riassunto delle informazioni di oggi" o "Cos'è successo oggi?" rispondi con un riassunto con le informazioni risalenti a quel giorno. 

            - Una tipologia di domanda che ti può essere posta è quella relativa al cambio tra due valute. Ad esempio: "Qual è il cambio euro dollaro?" oppure "A quanto ammonta oggi il cambio euro yen?" oppure "Qual era ieri il cambio euro dollaro?" oppure "A quanto ammontava ieri il cambio euro yen?".
              Ovviamente, anche in questo caso, se specificate le parole "ieri" o "oggi", devi ricercare queste informazioni tra i documents che soddisfano la condizione sopra definita per questi casi e qualora non venga trovata alcuna corrispondenza devi rispondere "Non ci sono informazioni".

            Ricorda che con la parola "ieri" all'interno di una Domanda si intende sempre la giornata precedente alla data in cui ti è posta la Domanda.
            Se all'interno della Domanda posta dall'utente dovesse essere riportato un mese, associa a tale mese il corrrispettivo numerico.
            
            La risposta dovrà essere sempre la più informativa e discorsiva possibile.
{context}
Domanda: {question}
Risposta:"""
QA_CHAIN_PROMPT = PromptTemplate(input_variables=["context", "question"],template=template,)

script_dir = os.path.dirname(os.path.abspath(__file__))
persist_directory = os.path.join(script_dir,"Chroma")

if "vectordb" not in st.session_state:
    vectordb = Chroma(
    persist_directory=persist_directory,
    embedding_function=embedding
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

    - Restituisci 1 se la domanda dell'utente richiede l'esecuzione di una query o un'operazione sui dati oppure se ti viene chiesto un dato sul proprio conto bancario. All'interno del content, 
    oltre al numero 1, scrivi la richiesta dell'utente. La struttura del content deve essere: 1#richiesta dell'utente. 
    La richiesta dell'utente può includere, ma non è limitata a, operazioni come query, somma, minimo, massimo, media, ricerca di 
    informazioni specifiche in riferimento a una data, confronto di valori, estrazione di dati casuali, o qualsiasi altra operazione 
    inerente all'estrazione di dati da un database.
 
    Le tabelle a cui fare riferimento includono:
    1. 'Gruppo1_btp_Az_finale' (può eseguire solo operazioni di SELECT)
    2. `ALTEN_CONTO` (può eseguire operazioni di SELECT, INSERT, UPDATE)
    
    Esempi di richieste:
    - "Selezionami la Denominazione univoca associata al Codice Isin IT0001086567"
    - "Selezionami il Codice Isin associato alla Denominazione Btp-1nv26 7,25%"
    - "Mostra tutti i movimenti per il conto 123456789012345678901234567"
    - "Calcola la somma degli importi dei movimenti in EUR per la società ABC"
    - "Mostra il saldo per la società ABC alla data 2023-06-01"
    - "Inserisci un nuovo movimento nel conto 123456789012345678901234567 con importo 100 EUR e causale 'Pagamento Fattura'"
    - "Aggiorna il saldo del conto 123456789012345678901234567 alla data 2023-06-01 a 5000 EUR"
    - "Dammi il saldo attuale"


    L'intelligenza artificiale deve essere in grado di comprendere richieste simili che non usano i nomi delle colonne esatti, 
    ma che fanno riferimento ai concetti rappresentati da tali colonne.


    Per qualsiasi richiesta dell'utente relativa alle tabelle Gruppo1_btp_Az_finale e ALTEN_CONTO , anche se i nomi delle colonne non 
    sono specificati esattamente, rispondi comunque con "1" seguito dalla richiesta dell'utente.

    - Restituisci 2 quando l'utente vuole informazioni di carattere testuale, che comprendi debbano essere prese da qualche parte.
      All'interno del content, oltre al numero 2, scrivi la domanda posta dall'utente senza tue modifiche. Quindi, ad esempio, la struttura del content deve 
      essere: 2#domanda dell'utente senza tue modifiche. NB: a questa categoria appartengono anche quel tipo di richieste volte che capisci
      siano una riformulazione, precisazione o approfondimento di una risposta precedente; Le richieste possono riguardare informazioni di carattere economico, 
      cambi tra valute, riassunti di informazioni generali relativamente a oggi e ieri;

    - Restituisci soltanto 3 se l'utente richiede la ricerca del Prezzo Ultimo in tempo reale specificando il Codice Isin o la Denominazione. 
    All'interno del content, oltre al numero 3, scrivi la domanda posta dall'utente. Quindi, ad esempio, la struttura del content deve essere: 
    3#Codice Isin o Denominazione#valore digitato Codice Isin o Denominazione specificata. Ad esempio, un tipo di richiesta può essere la
      seguente: "Stampami il Prezzo Ultimo attuale associato al Codice Isin IT0001086567";

    - Restituiscimi 4 se l'utente richiede di annotare qualcosa. All'interno del content, oltre al numero 4, scrivi la richiesta dell'utente. 
      La struttura del content deve essere: 4#richiesta completa dell'utente. Ad esempio, un tipo di richiesta può essere la
      seguente: "Annotami che domani c'ho una riunione". In questo caso, il content sarà il seguente: 4#Annotami che domani c'ho una riunione;
    
    - Restituiscimi soltanto 5 se l'utente richiede di leggere il contenuto del file note. Ad esempio, un tipo di richiesta può essere: "Fammi visualizzare le note scritte all'interno del file note";

    - Restituiscimi soltanto 6 se l'utente richiede di cancellare il contenuto del file note. Ad esempio, un tipo di richiesta può essere: "Elimina le note scritte all'interno del file note";
    
    - Restituiscimi 7 se l'utente richiede di cancellare una riga specifica dal file note. All'interno della richiesta dell'utente sarà specificato un valore numerico 
    (ad esempio: prima, uno, 1, seconda, due, 2, etc.). All'interno del content, oltre al numero 7, scrivi questo numero. Quindi, ad esempio, 
    la struttura del content deve essere: 7#numero specificato dall'utente. Ad esempio, ad un tipo di richiesta: "Elimina la prima nota all'interno
    del file note" corrisponde un content: "7#1".
      Se l'utente specifica di cancellare l'ultima nota la struttura del content deve essere: 7#-1; Se l'utente specifica di cancellare la penultima
     nota la struttura del content deve essere: 7#-2;
    
    -Restituiscimi "9" se l'utente chiede di inviare una mail. Analizza la richiesta e individua il contenuto della mail, l'oggetto della mail e
    l'indirizzo email del destinatario. La struttura della risposta deve essere: "9"#contenuto della mail#oggetto#indirizzo email. Se non viene
    specificato il contenuto della mail, utilizza "stringa-segreta". Se non viene specificato un oggetto, utilizza "stringa-segreta". Se non viene specificato un indirizzo email,
    utilizza "andreapastore326@gmail.com".

    -Restituiscimi "10" se l'utente chiede di fare degli acquisti sui btp. Analizza la richiesta e individua la denominazione del btp, la quantità 
    da acquistare. La struttura della risposta deve essere: "10"#denominazione del btp#quantità da acquistare. Se non viene
    specificata la denominazione del btp, utilizza "stringa-segreta". Se non viene specificata la quantità da acquistare, utilizza "stringa-segreta".
    Esempi: 
    Domanda: Voglio acquistare un btp
    Risposta: 10#stringa-segreta#stringa-segreta
    Domanda : Voglio comprare Btpi-15st35 2,35%
    Risposta: 10#Btpi-15st35 2,35%#stringa-segreta

    -Restituiscimi "11" se l'utente chiede di vendere dei btp. Analizza la richiesta e individua la denominazione del btp, la quantità 
    da vendere. La struttura della risposta deve essere: "11"#denominazione del btp#quantità da vendere. Se non viene
    specificata la denominazione del btp, utilizza "stringa-segreta". Se non viene specificata la quantità da vendere, utilizza "stringa-segreta".
    Esempi: 
    Domanda: Voglio vendere un btp
    Risposta: 11#stringa-segreta#stringa-segreta
    Domanda : Voglio cedere Btpi-15st35 2,35%
    Risposta: 11#Btpi-15st35 2,35%#stringa-segreta

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
    checker_nota = 0
    st.session_state['cont'] = cont
    st.session_state['cont_mappa'] = cont_mappa
    st.session_state['checker_nota'] = checker_nota
    global risp_nota 
    risposta = chain.invoke({"question": prompt_input}).content #Stampami un Codice Isin casuale
    lista_risposta=risposta.split('#')
    if lista_risposta[0].strip() == '1': #Text to SQL (Estrazione di informazioni da un dataset)
        st.session_state.engine.connect()
        risultato = chain_risposta1.invoke({"question": lista_risposta[1]})
        st.session_state["risultato"] = risultato
        st.session_state.engine.dispose()
        return risultato

    elif lista_risposta[0].strip() == '2': #RAG: Prende informazione da pdf
        question = lista_risposta[1]
        
        if st.session_state["RAG_checker"] == 0:
            st.session_state["RAG_checker"] = 1
            data_segnata_query = sfun.leggi_valore_da_file()
            data_segnata = datetime.strptime(data_segnata_query, "%Y-%m-%d %H:%M:%S")

            # Dettagli della connessione
            user = "MLacademy"
            pw = "alten-ML-academy2023"
            host = "bubidb.database.windows.net"
            db = "mlacademy-sqldb"
            port = "1433"

            conn = pymssql.connect(server=host, user=user, password=pw, database=db)
            cursor = conn.cursor()

            # Scrivi la tua query SQL
            query = """SELECT TOP 1 Data_di_Pubblicazione
                        FROM Scraping_BorsaItaliana
                        ORDER BY Data_di_Pubblicazione DESC"""

            # Esecuzione della query
            cursor.execute(query)

            # Ottenere i risultati
        
            ultima_data_pubblicazione = cursor.fetchone()
            ultima_data_pubblicazione = ultima_data_pubblicazione[0]
            if ultima_data_pubblicazione > data_segnata:
                # Converti l'oggetto datetime in una stringa con il formato desiderato
                ultima_data_pubblicazione_nuovo_formato = ultima_data_pubblicazione.strftime('%Y-%m-%d %H:%M:%S')

                sfun.salva_valore_in_file(ultima_data_pubblicazione_nuovo_formato)

                sfun.elimina_file_pdf()
                
                # Scrivi la tua query SQL
                query = f"""SELECT *
                        FROM Scraping_BorsaItaliana
                        WHERE Data_di_Pubblicazione  > '{data_segnata_query}';"""
                
                # Esecuzione della query
                cursor.execute(query)

                # Ottenere i risultati
                articoli = cursor.fetchall()
                cursor.close()
                conn.close()
                df = pd.DataFrame(articoli, columns=['Titolo', 'Data_di_Pubblicazione', 'Articolo'])
                # Converti la colonna 'Data_di_Pubblicazione' da timestamp a datetime
                df['Data_di_Pubblicazione'] = pd.to_datetime(df['Data_di_Pubblicazione'])
                
                filename = "output.pdf"
                sfun.create_combined_pdf(df, filename)

                loader = PyPDFLoader(r"output.pdf")
                pages = loader.load()

                # Initialize text splitter with specified parameters
                text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=1000,  # Size of each chunk in characters
                    chunk_overlap=0,  # Overlap between consecutive chunks
                    length_function=len,  # Function to compute the length of the text
                    separators= ['\n\n'] # Flag to add start index to each chunk
                    )

                # Split documents into smaller chunks using text splitter
                chunks = text_splitter.split_documents(pages)

                for i, chunk in enumerate(chunks):
                    chunk.metadata['Titolo'] = df.loc[i, "Titolo"]
                    date = df.loc[0, "Data_di_Pubblicazione"].strftime('%Y-%m-%d %H:%M:%S')  # Adjust format as needed
                    chunk.metadata['Data_di_Pubblicazione'] = date

                batch_size = 30
                # Suddividi i documenti in batch e processa ciascuno
                for i in range(0, len(chunks), batch_size):
                    batch = chunks[i:i + batch_size]
                    try:
                        vectordb2 = Chroma.from_documents(
                                    documents=batch,
                                    embedding=embedding,
                                    persist_directory=persist_directory
                                )
                    except Exception as e:
                        #print(f"Errore durante la processazione del batch: {e}")
                        if '429' in str(e):
                            #print("Superato il limite di richieste, attendere 60 secondi...")
                            time.sleep(60)  # Attendere 60 secondi prima di riprovare
                            vectordb2 = Chroma.from_documents(
                                        documents=batch,
                                        embedding=embedding,
                                        persist_directory=persist_directory
                                    )
                            
                st.session_state['vectordb'] = vectordb2
                st.write(vectordb2._collection.count())
                
                retriever=vectordb2.as_retriever()
                qa_chain2 = ConversationalRetrievalChain.from_llm(
                    llm_risposta3,
                    retriever=retriever,
                    combine_docs_chain_kwargs = {'prompt': QA_CHAIN_PROMPT},
                    memory = memoria
                )
                
                result = qa_chain2({"question": question}) 
                risultato = result['answer']
                st.session_state["risultato"] = risultato

                return risultato
            else:
                result = qa_chain({"question": question}) 
                risultato = result['answer']
                st.session_state["risultato"] = risultato

                return risultato
        else:
            result = qa_chain({"question": question}) 
            risultato = result['answer']
            st.session_state["risultato"] = risultato

            return risultato       

    elif lista_risposta[0].strip() == "3": #Scraping in tempo reale del prezzo ultimo :)


        if lista_risposta[1].strip() == 'Codice Isin':

            risultato = sfun.get_btp_price(isin = lista_risposta[2].strip())
        
        else:

            risultato = sfun.get_btp_price(denomination = lista_risposta[2].strip())
        
        st.session_state["risultato"] = risultato

        #print(f"Il prezzo ultimo è :{risultato}")
        return risultato

    elif lista_risposta[0].strip() == '4': #Salvataggio in nota

        st.session_state['checker_nota'] = 1
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

        st.session_state['checker_nota'] = 1
        risultato = sfun.delete_note()
        risp_nota = "Il contenuto delle note è stato cancellato con successo."
        #return 'Il contenuto delle note è stato cancellato con successo.'

    elif lista_risposta[0].strip()== "7":
        st.session_state['checker_nota'] = 1
        risultato = sfun.delete_row(lista_risposta[1].strip())
        risp_nota = "La nota è stata cancellata"
        #return 'La nota è stata cancellata'
    
    elif risposta[0].strip() == "8": 
        return "Non sono autorizzato ad eseguire queste operazioni"
    

    elif lista_risposta[0].strip() == "9":
        
        st.session_state.mail_body = lista_risposta[1]
        st.session_state.mail_oggetto = lista_risposta[2]
        st.session_state.mail_indirizzo = lista_risposta[3]
        if sfun.controllo_mail(st.session_state.mail_indirizzo):
            #return  st.session_state.mail_body, st.session_state.mail_oggetto
            #codice andrea
            if "stringa-segreta" not in st.session_state.mail_body:
                if "stringa-segreta" not in st.session_state.mail_oggetto:
                    st.session_state.sicuro = 's'
                    return sfun.riassunto(st.session_state.mail_oggetto,st.session_state.mail_body, st.session_state.mail_indirizzo)
                #oggetto vuoto
                else:
                    st.session_state.mail_checker = 1
                    return "Inserisci l'oggetto della mail (se non vuoi inserire l'oggetto premi spazio e invio)"
                    
            #codice kevin
            else:
                if "stringa-segreta" in st.session_state.mail_oggetto:
                    st.session_state.mail_checker= 1
                    return "Inserisci l'oggetto della mail (se non vuoi inserire l'oggetto premi spazio e invio)"
                else:
                    return "Non hai inserito il testo della mail."
        else:
            return risposta
        
    #ACQUISTO BTP
    elif lista_risposta[0].strip() == "10":
        st.session_state.buy_btp=lista_risposta[1]
        st.session_state.buy_quantità=lista_risposta[2]
        if "stringa-segreta" not in st.session_state.buy_btp:
            if "stringa-segreta" not in st.session_state.buy_quantità:
                st.session_state.buy_sicuro='s'
                return "Sei sicuro di voler effettuare l'acquisto?"
            else:
                st.session_state.buy_checker=1
                return "Inserisci il numero di lotti che vuoi acquistare"
        else:
            if "stringa-segreta" not in st.session_state.buy_quantità:
                st.session_state.buy_checker=1
                return "Inserisci la descrizione del BTP che vuoi acquistare"
            else:
                st.session_state.buy_checker=2
                return "Inserisci la descrizione del BTP che vuoi acquistare "
            
    #VENDITA BTP   
    elif lista_risposta[0].strip() == "11":
        st.session_state.sell_btp=lista_risposta[1]
        st.session_state.sell_quantità=lista_risposta[2]
        if "stringa-segreta" not in st.session_state.sell_btp:
            if "stringa-segreta" not in st.session_state.sell_quantità:
                st.session_state.sell_sicuro='s'
                return "Sei sicuro di voler effettuare la vendita?"
            else:
                st.session_state.sell_checker=1
                return "Inserisci il numero di lotti che vuoi vendere"
        else:
            if "stringa-segreta" not in st.session_state.sell_quantità:
                st.session_state.sell_checker=1
                return "Inserisci la descrizione del BTP che vuoi vendere"
            else:
                st.session_state.sell_checker=2
                return "Inserisci la descrizione del BTP che vuoi vendere"
    
    #Tool Mappa
    elif lista_risposta[0].strip() == "12":
        cont_mappa_display = 1
        st.session_state["cont_mappa_display"] = cont_mappa_display
        cont_mappa += 1
        st.session_state["cont_mappa"] = cont_mappa

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

        if tmp == 1:
            return "Il punto di partenza e il punto di arrivo indicati non sono presenti a bordo. Rielabora la richiesta."
        elif tmp == 2:
            return "Il punto di partenza indicato non è presente a bordo. Rielabora la richiesta."
        elif tmp == 3:
            return "Il punto di arrivo indicato non è presente a bordo. Rielabora la richiesta."
        else:
            cont_piano = 0

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

        if type(arrivo) != int and 'ascensore' in arrivo:
            if arrivo == 'ascensore':
            
                if partenza in dizionario1.keys():
                    minimo = float('inf')
                    for i,j in ascensori1.items():
                        if sfun.distanza_euclidea(j,dizionario1, partenza) < minimo:
                            arrivo = i
                            minimo = sfun.distanza_euclidea(j,dizionario1, partenza)
                            
                elif partenza in dizionario2.keys():
                    minimo = float('inf')
                    for i,j in ascensori2.items():
                        if sfun.distanza_euclidea(j,dizionario2, partenza) < minimo:
                            arrivo = i
                            minimo = sfun.distanza_euclidea(j,dizionario2, partenza)
                elif partenza in dizionario3.keys():
                    minimo = float('inf')
                    for i,j in ascensori3.items():
                        if sfun.distanza_euclidea(j,dizionario3, partenza) < minimo:
                            arrivo = i
                            minimo = sfun.distanza_euclidea(j,dizionario3, partenza)                
            else:
                pass

        # elif type(partenza) != int and 'ascensore' in partenza:
        #     if arrivo in dizionario1.keys():
        #         minimo = float('inf')
        #         for i,j in ascensori1.items():
        #             if sfun.distanza_euclidea(j,dizionario1, partenza) < minimo:
        #                 partenza = i
        #                 minimo = sfun.distanza_euclidea(j,dizionario1, partenza)
                            
        #     elif arrivo in dizionario2.keys():
        #         minimo = float('inf')
        #         for i,j in ascensori2.items():
        #             if sfun.distanza_euclidea(j,dizionario2, partenza) < minimo:
        #                 partenza = i
        #                 minimo = sfun.distanza_euclidea(j,dizionario2, partenza)

        elif type(partenza) != int and 'ascensore' in partenza:
            if arrivo in dizionario1.keys():
                minimo = float('inf')
                for i,j in ascensori1.items():
                    if i == partenza:
                        pass
                            
            elif arrivo in dizionario2.keys():
                minimo = float('inf')
                for i,j in ascensori2.items():
                    if i == partenza:
                        pass
            elif arrivo in dizionario3.keys():
                minimo = float('inf')
                for i,j in ascensori3.items():
                    if i == partenza:
                        pass

        elif partenza in dizionario1.keys() and arrivo in dizionario2.keys():
            partenza1 = partenza
            minimo = float('inf')
            for i,j in ascensori1.items():
                    if sfun.distanza_euclidea(j,dizionario1, partenza1) < minimo:
                        arrivo1 = i
                        minimo = sfun.distanza_euclidea(j,dizionario1, partenza1)
            piano_partenza = 1            
            partenza2 = arrivo1
            arrivo2 = arrivo
            piano_arrivo = 2
            cont_piano = 1
            
        elif partenza in dizionario1.keys() and arrivo in dizionario3.keys():
            partenza1 = partenza
            minimo = float('inf')
            for i,j in ascensori1.items():
                    if sfun.distanza_euclidea(j,dizionario1, partenza1) < minimo:
                        arrivo1 = i
                        minimo = sfun.distanza_euclidea(j,dizionario1, partenza1)
            piano_partenza = 1            
            partenza2 = arrivo1
            arrivo2 = arrivo
            piano_arrivo = 3
            cont_piano = 1

        elif partenza in dizionario2.keys() and arrivo in dizionario1.keys():
            partenza1 = partenza
            minimo = float('inf')
            for i,j in ascensori2.items():
                    if sfun.distanza_euclidea(j,dizionario2, partenza1) < minimo:
                        arrivo1 = i
                        minimo = sfun.distanza_euclidea(j,dizionario2, partenza1)
            piano_partenza = 2
            
            partenza2 = arrivo1
            arrivo2 = arrivo
            piano_arrivo = 1
            cont_piano = 1
                        
        elif partenza in dizionario2.keys() and arrivo in dizionario3.keys():
            partenza1 = partenza
            minimo = float('inf')
            for i,j in ascensori2.items():
                    if sfun.distanza_euclidea(j,dizionario2, partenza1) < minimo:
                        arrivo1 = i
                        minimo = sfun.distanza_euclidea(j,dizionario2, partenza1)
            piano_partenza = 2
            
            partenza2 = arrivo1
            arrivo2 = arrivo
            piano_arrivo = 3
            cont_piano = 1

        elif partenza in dizionario3.keys() and arrivo in dizionario1.keys():
            partenza1 = partenza
            minimo = float('inf')
            for i,j in ascensori3.items():
                    if sfun.distanza_euclidea(j,dizionario3, partenza1) < minimo:
                        arrivo1 = i
                        minimo = sfun.distanza_euclidea(j,dizionario3, partenza1)
            piano_partenza = 3
            
            partenza2 = arrivo1
            arrivo2 = arrivo
            piano_arrivo = 1
            cont_piano = 1

        elif partenza in dizionario3.keys() and arrivo in dizionario2.keys():
            partenza1 = partenza
            minimo = float('inf')
            for i,j in ascensori3.items():
                    if sfun.distanza_euclidea(j,dizionario3, partenza1) < minimo:
                        arrivo1 = i
                        minimo = sfun.distanza_euclidea(j,dizionario3, partenza1)
            piano_partenza = 3
            
            partenza2 = arrivo1
            arrivo2 = arrivo
            piano_arrivo = 2
            cont_piano = 1

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

            # if type(arrivo) == str and 'ascensore' in arrivo:
                
            #     minimo = float('inf')
            #     for i,j in ascensori.items():
            #         if distanza_euclidea(j,dizionario) < minimo:
            #             arrivo = i
            #             minimo = distanza_euclidea(j,dizionario)
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

            #plt.legend([red,green,purple],['Partenza','Arrivo','Percorso'],fontsize='large')
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

            return im1, im2, risposta



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
        st.session_state.messages.append({"role": "user",  "avatar": 'https://www.clipartmax.com/png/middle/434-4349876_profile-icon-vector-png.png', "content": prompt})
        st.session_state.recensioni.append({"role": "user",  "avatar": 'https://www.clipartmax.com/png/middle/434-4349876_profile-icon-vector-png.png', "content": prompt})

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
if st.session_state.messages[-1]["role"] != "assistant" and st.session_state.messages[-1]["role"] != "mail":
    with container:
        with st.chat_message(name = "assistant", avatar='https://www.shutterstock.com/image-vector/call-center-customer-support-vector-600nw-2285364015.jpg'):
            with st.spinner("Sto pensando...🤔"):
                if 's' in st.session_state.sicuro:
                        st.session_state.sicuro= prompt
                        if st.session_state.sicuro.lower()[0] == "s":
                                st.write(sfun.mail(st.session_state.mail_oggetto,st.session_state.mail_body, st.session_state.mail_indirizzo))
                                response ="Mail inviata correttamente!"
                        else:    
                                response = "Ok, mail non inviata"
                                st.write(response)
                        st.session_state.mail_checker=0
                        st.session_state.sicuro ="n"
                        st.session_state.mail_body = "0"
                        st.session_state.mail_oggetto = "0"
                        st.session_state.mail_indirizzo = "andreapastore326@gmail.com"

                elif st.session_state.mail_checker == 1:
                    st.session_state.mail_oggetto=prompt
                    if "stringa-segreta" in st.session_state.mail_body:
                        st.write("inserisci il testo dell'email (se non vuoi mandare la mail scrivi esci)")
                        st.session_state.mail_checker+=1
                        response="inserisci il testo dell'email (se non vuoi mandare la mail scrivi esci)"
                    else:
                        response= sfun.riassunto(st.session_state.mail_oggetto,st.session_state.mail_body, st.session_state.mail_indirizzo)
                        st.write(response)
                        st.session_state.sicuro = "s"
                    
                elif st.session_state.mail_checker==2:
                    if prompt.replace(" ","") == "":
                        st.write("inserisci il testo dell'email (se non vuoi mandare la mail scrivi esci)")
                        response=""
                    elif prompt.lower() == "esci":
                        st.write("Mail non mandata")
                        st.session_state.mail_checker=0
                        response="Mail non mandata"
                    else:
                        st.session_state.mail_body= prompt
                        response= sfun.riassunto(st.session_state.mail_oggetto,st.session_state.mail_body, st.session_state.mail_indirizzo)
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

                else:
                    try:
                        img1, img2, response = generate_response(prompt)  
                    except Exception as e:
                        if st.session_state.checker_nota == 1:
                            response = risp_nota
                        else:
                            response = generate_response(prompt)
                    
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


                                
    if st.session_state.mail_checker == 0 and st.session_state.buy_checker==0 and st.session_state.buy_sicuro=='n' and st.session_state.sell_checker==0 and st.session_state.sell_sicuro=='n':
        if st.session_state.cont_mappa == 1:
            if 'img1' in globals():
                if img2 is None:
                    message = {"role": "assistant", "avatar": 'https://www.shutterstock.com/image-vector/call-center-customer-support-vector-600nw-2285364015.jpg' ,"content": buffer}
                    st.session_state.messages.append(message)
                    message = {"role": "assistant", "avatar": 'https://www.shutterstock.com/image-vector/call-center-customer-support-vector-600nw-2285364015.jpg' ,"content": response}
                    st.session_state.messages.append(message)
                    st.session_state.recensioni.append(message)
                else:
                    message = {"role": "assistant", "avatar": 'https://www.shutterstock.com/image-vector/call-center-customer-support-vector-600nw-2285364015.jpg' ,"content": buffer1}
                    st.session_state.messages.append(message)
                    message = {"role": "assistant", "avatar": 'https://www.shutterstock.com/image-vector/call-center-customer-support-vector-600nw-2285364015.jpg' ,"content": buffer2}
                    st.session_state.messages.append(message)
                    message = {"role": "assistant", "avatar": 'https://www.shutterstock.com/image-vector/call-center-customer-support-vector-600nw-2285364015.jpg' ,"content": response}
                    st.session_state.messages.append(message)
                    st.session_state.recensioni.append(message)
            else: 
                message = {"role": "assistant", "avatar": 'https://www.shutterstock.com/image-vector/call-center-customer-support-vector-600nw-2285364015.jpg' ,"content": response}
                st.session_state.messages.append(message)
                st.session_state.recensioni.append(message)
        else:
            message = {"role": "assistant", "avatar": 'https://www.shutterstock.com/image-vector/call-center-customer-support-vector-600nw-2285364015.jpg' ,"content": response}
            st.session_state.messages.append(message)
            st.session_state.recensioni.append(message)
    else:
        message = {"role": "mail", "avatar": 'https://www.shutterstock.com/image-vector/call-center-customer-support-vector-600nw-2285364015.jpg' ,"content": response}
        st.session_state.messages.append(message)
        st.session_state.recensioni.append(message)
    st.rerun()




#----------------------------------------------------------------------------------------------------------------------------------------------------

 

# Fine dell'applicazione
