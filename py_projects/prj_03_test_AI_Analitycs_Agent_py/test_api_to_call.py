import os
import sqlite3
import requests
from fastapi import FastAPI, HTTPException
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
import uvicorn
import threading

DB_FILE = "prodotti.db"

# === CREAZIONE DB ===
def create_database():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS Prodotti (
            ID_Prodotto INTEGER PRIMARY KEY AUTOINCREMENT,
            Nome_Prodotto TEXT NOT NULL,
            Categoria TEXT NOT NULL,
            Prezzo REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def insert_products():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    products = [
        ("Samsung Galaxy S25 Ultra", "Smartphone", 1499.99),
        ("Apple iPhone 15 Pro Max", "Smartphone", 1599.99),
        ("Google Pixel 8 Pro", "Smartphone", 899.99),
        ("Sony WH-1000XM5", "Cuffie", 349.99),
        ("Dell XPS 13 (2024)", "Laptop", 1299.99),
        ("Apple Watch Series 9", "Smartwatch", 399.99),
        ("Sony A7 IV Camera", "Fotocamera", 2499.99),
        ("LG OLED C2 TV (55-inch)", "Televisore", 1499.99),
        ("NVIDIA GeForce RTX 4090", "Scheda Grafica", 1599.99)
    ]
    c.executemany('''
        INSERT INTO Prodotti (Nome_Prodotto, Categoria, Prezzo)
        VALUES (?, ?, ?)
    ''', products)
    conn.commit()
    conn.close()

# === FASTAPI APP ===
app = FastAPI()

@app.get("/prodotti")
def get_prodotti():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM Prodotti")
    prodotti = c.fetchall()
    conn.close()
    return {"prodotti": prodotti}

@app.get("/prodotti/categoria")
def get_categorie():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT DISTINCT Categoria FROM Prodotti")
    categorie = c.fetchall()
    conn.close()
    return {"categorie": [cat[0] for cat in categorie]}

@app.get("/prodotti/categoria/{categoria}")
def get_prodotti_by_categoria(categoria: str):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM Prodotti WHERE Categoria=?", (categoria,))
    prodotti = c.fetchall()
    conn.close()
    if not prodotti:
        raise HTTPException(status_code=404, detail="Nessun prodotto trovato")
    return {"prodotti": prodotti}

@app.get("/prodotti/categoria/{categoria}/prezzo/media")
def get_media_prodotti_by_categoria(categoria:str):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT AVG(Prezzo) FROM Prodotti WHERE Categoria=?", (categoria,))
    media = c.fetchone()[0]
    conn.close()
    if media is None:
        raise HTTPException(status_code=404, detail="Nessun prodotto trovato")
    return {"categoria": categoria, "prezzo_medio": media}

@app.get("/prodotti/categoria/prezzo/media")
def get_media_all_prodotti_for_categoria():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT Categoria, AVG(Prezzo) AS Media FROM Prodotti GROUP BY Categoria ORDER BY Media DESC")
    medie = c.fetchall()
    conn.close()
    if medie is None:
        raise HTTPException(status_code=404, detail="Nessun prodotto trovato")
    return {"medie_per_categoria": medie}

@app.get("/prodotti/categoria/{categoria}/prezzo/somma")
def get_somma_prodotti_by_categoria(categoria:str):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT SUM(Prezzo) FROM Prodotti WHERE Categoria=?", (categoria,))
    somma = c.fetchone()[0]
    conn.close()
    if somma is None:
        raise HTTPException(status_code=404, detail="Nessun prodotto trovato")
    return {"categoria": categoria, "prezzo_somma": somma}

# === LLM AGENT ===
model_name = "gpt-oss:120b-cloud"

def get_agent_router():
    """Modello che decide quale endpoint usare"""
    model = ChatOllama(model=model_name, streaming=False)
    prompt = ChatPromptTemplate.from_template(
        "Domanda utente: {input}\n"
        "Scegli uno tra i seguenti endpoint:\n"
        "- GET /prodotti\n"
        "- GET /prodotti/categoria\n"
        "- GET /prodotti/categoria/<categoria>\n"
        "- GET /prodotti/categoria/<categoria>/prezzo/media\n"
        "- GET /prodotti/categoria/<categoria>/prezzo/somma\n"
        "- GET /prodotti/categoria/prezzo/media\n\n"
        "Se serve una categoria, sostituisci <categoria> con il valore giusto.\n"
        "Rispondi SOLO con l'endpoint."
    )
    return prompt | model

def get_agent_response():
    """Modello che prende i dati e genera risposta naturale"""
    model = ChatOllama(model=model_name, streaming=False)
    prompt = ChatPromptTemplate.from_template(
        "Domanda: {question}\n"
        "Dati disponibili dal database:\n{data}\n\n"
        "Genera una risposta chiara e naturale per l'utente."
    )
    return prompt | model

def process_question(question: str):
    # Step 1: capire quale query eseguire
    chain_router = get_agent_router()
    llm_response = chain_router.invoke({"input": question})
    endpoint = llm_response.content.strip()
    
    base_url = "http://127.0.0.1:8000"
    resp = requests.get(base_url + endpoint.replace("GET", "").strip())
    data = resp.json()

    # Step 3: passare i dati al modello per la risposta finale
    chain_response = get_agent_response()
    final_response = chain_response.invoke({
        "question": question,
        "data": str(data)
    })

    return final_response.content

def start_server():
    uvicorn.run(app, host="127.0.0.1", port=8000)

# === MAIN ===
if __name__ == "__main__":
    os.system("cls")
    if not os.path.exists(DB_FILE):
        create_database()
        insert_products()

    # Avvio server FastAPI in background
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()

    os.system("pause")  # Attendo che il server sia attivo
    
    # Interfaccia CLI
    while True:
        print("""Esempio di domande:
                - Mostrami tutti i prodotti disponibili.
                - Quali prodotti ci sono nella categoria Smartphone?
                - Qual è la somma dei prezzi nella categoria Smartphone?
        """)
        domanda = input("Fai una domanda: ")
        if domanda == "":
            break
        print("💡", process_question(domanda))

    
    