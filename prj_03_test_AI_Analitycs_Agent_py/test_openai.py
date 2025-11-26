import os
import sqlite3
from dotenv import load_dotenv
from openai import OpenAI
from datetime import datetime

# 🔑 Carica API key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("❌ Chiave API non trovata!")
    exit()

client = OpenAI(api_key=api_key)

# 🗄️ Connessione SQLite
conn = sqlite3.connect("eurofork.db")  
cursor = conn.cursor()

# Creazione tabella se non esiste
cursor.execute("""
CREATE TABLE IF NOT EXISTS MicroMissioni (
    ID_Micromissione INTEGER PRIMARY KEY AUTOINCREMENT,
    Macchina varchar(100) DEFAULT NULL,
    Tipo varchar(50) DEFAULT NULL,
    Risultato varchar(50) DEFAULT NULL,
    Data_Ora datetime DEFAULT NULL
)
""")

# 📑 Log richieste in un file CSV
def log_request(model_name, user_input, txt_prompt, usage, response_text=""):
    try:
        log_dir = "log"
        log_file = os.path.join(log_dir, "requests_log.csv")
        os.makedirs(log_dir, exist_ok=True)

        headers = "timestamp;model;user_input;txt_prompt;prompt_tokens;completion_tokens;total_tokens;response_preview\n"

        # Se usage è None (può capitare in errori/timeout)
        prompt_tokens = getattr(usage, "prompt_tokens", 0) if usage else 0
        completion_tokens = getattr(usage, "completion_tokens", 0) if usage else 0
        total_tokens = getattr(usage, "total_tokens", prompt_tokens + completion_tokens)

        row = (
            f"{datetime.now()};"
            f"{model_name};"
            f"{user_input.replace(';', ',')};"
            f"{txt_prompt};"
            f"{prompt_tokens};"
            f"{completion_tokens};"
            f"{total_tokens};"
            f"{response_text[:50].replace(';', ',')}\n"
        )

        # Scrive header se non esiste
        if not os.path.exists(log_file):
            with open(log_file, "w", encoding="utf-8") as f:
                f.write(headers)

        # Append nuova riga
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(row)

        print(f"✅ Log salvato ({total_tokens} token) → {log_file}")

    except Exception as e:
        print(f"⚠️ Errore durante logging: {e}")

# Funzione wrapper per loggare e restituire testo
def extract_and_log(resp, model_name, txt_prompt, user_input):
    try:
        usage = getattr(resp, "usage", None)
        text = resp.choices[0].message.content.strip() if resp.choices else ""
        log_request(model_name, user_input, txt_prompt, usage, text)
        return text
    except Exception as e:
        print(f"⚠️ Errore in extract_and_log: {e}")
        return "⚠️ Errore durante l'elaborazione della risposta."

# Funzione: valori DISTINCT dal DB
def get_distinct_values():
    distinct_values = {}
    cursor.execute("SELECT DISTINCT Macchina FROM MicroMissioni")
    distinct_values['macchine'] = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT DISTINCT Tipo FROM MicroMissioni")
    distinct_values['tipi'] = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT DISTINCT Risultato FROM MicroMissioni")
    distinct_values['risultati'] = [row[0] for row in cursor.fetchall()]

    return distinct_values

# Utility: prompt valori DB
def get_text_distinct_values():
    distinct_vals = get_distinct_values()
    return f"""
    Valori attuali dei vari campi nel database da usare per query e clausole WHERE:
    - Macchine: {', '.join(distinct_vals['macchine'])}
    - Tipi: {', '.join(distinct_vals['tipi'])}
    - Risultati: {', '.join(distinct_vals['risultati'])}
    """

# Caricatore di un prompt da un file testo
def get_model_prompt(file_name: str):
    file_name = os.path.join("prompts", file_name)
    with open(file_name, "r", encoding="utf-8") as f:
        return f.read()

# Step 1: Identificazione domanda
def identify_question_type(user_question: str) -> str:
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": get_model_prompt("interpretazione_domanda.txt")},
            {"role": "user", "content": user_question}
        ],
        max_tokens=10,
        temperature=0
    )
    return extract_and_log(resp, "gpt-4o-mini", "interpretazione_domanda.txt", user_question).lower()

# Step 2A: Risposta generica
def generate_generic_response(user_question: str) -> str:
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": get_model_prompt("risposta_generica.txt")},
            {"role": "user", "content": user_question}
        ],
        max_tokens=300,
        temperature=0
    )
    return extract_and_log(resp, "gpt-4o-mini", "risposta_generica.txt", user_question)

# Step 2B.1: Query SQL
def generate_query(user_question: str) -> str:
    prompt = f"""
    Usa i seguenti valori distinti per formulare una query SQL:
    {get_text_distinct_values()}

    Genera una query SQL per rispondere alla seguente domanda:
    Domanda: "{user_question}"
    La query deve essere compatibile con SQLite e restituire i campi rilevanti.
    Rispondi solo con la query SQL, senza spiegazioni.
    """
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": get_model_prompt("crea_query.txt")},
            {"role": "user", "content": prompt}
        ],
        max_tokens=200,
        temperature=0
    )
    return extract_and_log(resp, "gpt-4o-mini", "crea_query.txt", user_question)

# Step 2B.2: Esecuzione query SQL
def generate_sql_and_execute(sql_query: str):
    try:
        cursor.execute(sql_query)
        results = cursor.fetchall()
        return results
    except sqlite3.Error as e:
        return f"Errore SQL: {e}"

# Step 2B.3: Risposta analitica
def analytical_response(user_question: str, results) -> str:
    formatted_results = "\n".join([str(r) for r in results]) if results else "Nessun risultato trovato"
    prompt_answer = f"""
    Domanda utente: "{user_question}".
    Risultati DB: {formatted_results}.
    Scrivi una risposta chiara e professionale basata sui dati.
    """
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Sei un assistente tecnico che analizza i valori restituiti da una query SQL e restituisce spiegazioni chiare."},
            {"role": "user", "content": prompt_answer}
        ],
        max_tokens=300,
        temperature=0.2
    )
    return extract_and_log(resp, "gpt-4o-mini", "no txt", user_question)

# Gestrore principale del flusso
def ask_chatbot(user_question: str):
    question_type = identify_question_type(user_question)
    print(f"🔍 Tipo di domanda identificata: {question_type}")

    if question_type == 'generica':
        print("🤖 Risposta generica in corso...")
        return generate_generic_response(user_question)

    elif question_type == 'analitica':
        print("🤖 Generazione query SQL...")
        sql_query = generate_query(user_question)
        print(f"📄 Query: {sql_query}")

        results = generate_sql_and_execute(sql_query)
        if isinstance(results, str) and results.startswith("Errore"):
            return results

        print("📊 Analisi risultati...")
        return analytical_response(user_question, results)

    else:
        return "⚠️ Errore: tipo di domanda non riconosciuto."

# 🚀 Avvio programma
if __name__ == "__main__":
    print("🚀 Sistema di Analisi Database ESS - Magazzino Automatizzato")
    print("="*60)

    distinct_vals = get_distinct_values()
    print("📊 Database inizializzato:")
    print(f"   Macchine attive: {len(distinct_vals['macchine'])}")
    print(f"   Tipi missione: {len(distinct_vals['tipi'])}")
    print(f"   Risultati unici: {len(distinct_vals['risultati'])}")
    print("-"*60)

    while True:
        domanda = input("\n🤔 Fai una domanda (vuoto per uscire): ").strip()
        if not domanda:
            break

        print("\n🔄 Elaborazione in corso...")
        risposta = ask_chatbot(domanda)
        print("\n🤖 Risposta AI:")
        print("="*60)
        print(risposta)
        print("="*60)

    conn.close()
    print("\n👋 Arrivederci!")
