import os
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from datetime import datetime
import tiktoken
import mysql.connector
# ===============================
# FUNZIONI DI SUPPORTO
# ===============================
def get_distinct_values_missions():
    distinct_values = {}
    cursor.execute("SELECT DISTINCT Macchina FROM MicroMissioni")
    distinct_values['macchine'] = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT DISTINCT Tipo FROM MicroMissioni")
    distinct_values['tipi'] = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT DISTINCT Risultato FROM MicroMissioni")
    distinct_values['risultati'] = [row[0] for row in cursor.fetchall()]

    cursor.execute("DESCRIBE MicroMissioni")
    distinct_values['campi'] = [row[0] for row in cursor.fetchall()]

    return distinct_values

def get_distinct_values_alarms():
    distinct_values = {}
    cursor.execute("SELECT DISTINCT Codice FROM Allarmi")
    distinct_values['codici'] = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT DISTINCT Descrizione FROM Allarmi")
    distinct_values['descrizioni'] = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT DISTINCT Tipo FROM Allarmi")
    distinct_values['tipi'] = [row[0] for row in cursor.fetchall()]

    cursor.execute("DESCRIBE Allarmi")
    distinct_values['campi'] = [row[0] for row in cursor.fetchall()]

    return distinct_values

def get_distinct_values_associations():
    distinct_values = {}
    cursor.execute("SELECT DISTINCT Tipo_Macchina FROM Associazioni")
    distinct_values['tipi_macchina'] = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT DISTINCT Tipo_Allarme FROM Associazioni")
    distinct_values['tipi_allarme'] = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT DISTINCT Allarme FROM Associazioni")
    distinct_values['allarmi'] = [row[0] for row in cursor.fetchall()]

    cursor.execute("DESCRIBE Associazioni")
    distinct_values['campi'] = [row[0] for row in cursor.fetchall()]

    return distinct_values

def get_distinct_values_commesse():
    distinct_values = {}
    cursor.execute("SELECT DISTINCT Nome FROM Commesse")
    distinct_values['nomi'] = [row[0] for row in cursor.fetchall()]

    cursor.execute("DESCRIBE Commesse")
    distinct_values['campi'] = [row[0] for row in cursor.fetchall()]

    return distinct_values

def safe_values(values):
    return [v if v is not None else "N/A" for v in values]

def get_text_distinct_values_missions():
    vals = get_distinct_values_missions()
    return f"""
    Valori attuali dei vari campi nel database da usare per query e clausole WHERE:
    - Macchine: {', '.join(safe_values(vals['macchine']))}
    - Tipi: {', '.join(safe_values(vals['tipi']))}
    - Risultati: {', '.join(safe_values(vals['risultati']))}
    - Schema Tabella campi disponibili: {', '.join(safe_values(vals['campi']))}
    """

def get_text_distinct_values_alarms():
    vals = get_distinct_values_alarms()
    return f"""
    Valori attuali dei vari campi nel database da usare per query e clausole WHERE:
    - Macchine: {', '.join(safe_values(vals['codici']))}
    - Descrizioni: {', '.join(safe_values(vals['descrizioni']))}
    - Tipi: {', '.join(safe_values(vals['tipi']))}
    - Schema Tabella campi disponibili: {', '.join(safe_values(vals['campi']))}
    """

def get_text_distinct_values_associations():
    vals = get_distinct_values_associations()
    return f"""
    Valori attuali dei vari campi nel database da usare per query e clausole WHERE:
    - Tipi di Macchine: {', '.join(safe_values(vals['tipi_macchina']))}
    - Tipi di Allarme: {', '.join(safe_values(vals['tipi_allarme']))}
    - Allarmi: {', '.join(safe_values(vals['allarmi']))}
    - Schema Tabella campi disponibili: {', '.join(safe_values(vals['campi']))}
    """

def get_text_distinct_values_commesse():
    vals = get_distinct_values_commesse()
    return f"""
    Valori attuali dei vari campi nel database da usare per query e clausole WHERE:
    - Nome commesse: {', '.join(safe_values(vals['nomi']))}
    - Schema Tabella campi disponibili: {', '.join(safe_values(vals['campi']))}
    """

def get_model_prompt(file_name: str):
    file_path = os.path.join("prompts", file_name)
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def log_model_call(resp, model_name, txt_prompt, user_input, prompt_text):
    try:
        log_dir = "log"
        log_file = os.path.join(log_dir, "requests_log.csv")
        os.makedirs(log_dir, exist_ok=True)

        headers = "timestamp;model;txt_prompt; prompt_tokens; response_tokens; user_input; total_tokens;response_preview; history\n"

        prompt_tokens = count_tokens(prompt_text)
        response_tokens = count_tokens(resp)
        total_tokens = prompt_tokens + response_tokens

        row = (
            f"{datetime.now()};"
            f"{model_name};"
            f"{user_input.replace(';', ',')};"
            f"{txt_prompt};"
            f"{prompt_tokens};"
            f"{response_tokens};"
            f"{total_tokens};"
            f"{resp[:5].replace(';', ',')};"
            f"{attiva_history}\n"
        )

        # Scrive header se non esiste
        if not os.path.exists(log_file):
            with open(log_file, "w", encoding="utf-8") as f:
                f.write(headers)

        # Append nuova riga
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(row)

        print(f"✅ Log salvato → {log_file}")

    except Exception as e:
        print(f"⚠️ Errore durante logging: {e}")

def count_tokens(text: str) -> int:
    try:
        enc = tiktoken.encoding_for_model(model_name)
    except KeyError:
        enc = tiktoken.get_encoding("cl100k_base")
    tokens = enc.encode(text)
    return len(tokens)

# ===============================
# INIZIALIZZA MODELLO E AGENTI
# ===============================
model_name = "gpt-oss:120b-cloud"
model = ChatOllama(model=model_name, streaming=False)

prompt_identificatore = ChatPromptTemplate.from_template(get_model_prompt("interpretazione_domanda.txt"))
agente_identificatore = prompt_identificatore | model

prompt_generico = ChatPromptTemplate.from_template(get_model_prompt("risposta_generica.txt"))
agente_generico = prompt_generico | model

prompt_crea_query = ChatPromptTemplate.from_template(get_model_prompt("crea_query.txt"))
agente_crea_query = prompt_crea_query | model

prompt_analitico = ChatPromptTemplate.from_template(get_model_prompt("risposta_analitica.txt"))
agente_analitico = prompt_analitico | model

# ===============================
# FUNZIONI FLUSSO
# ===============================
def identify_question_type(user_question: str) -> str:
    prompt_text = (
        get_model_prompt("interpretazione_domanda.txt")
        .replace("{question}", user_question)
        .replace("{history}", "\n".join(conversation_history))
    )
    resp = agente_identificatore.invoke({"question": user_question, "history": "".join(conversation_history)}).content.strip().lower()
    log_model_call(resp, model_name, "interpretazione_domanda.txt", user_question, prompt_text)
    return resp

def generate_generic_response(user_question: str) -> str:
    prompt_text = (
        get_model_prompt("risposta_generica.txt")
        .replace("{question}", user_question)
        .replace("{history}", "\n".join(conversation_history))
    )
    resp = agente_generico.invoke({"question": user_question, "history": "".join(conversation_history)}).content.strip()
    log_model_call(resp, model_name, "risposta_generica.txt", user_question, prompt_text)
    return resp

def generate_query(user_question: str) -> str:
    prompt_data = f"""
    Distinct Values of MicroMissioni: {get_text_distinct_values_missions()}
    Distinct Values of Allarmi: {get_text_distinct_values_alarms()}
    Distinct values of Associazioni: {get_text_distinct_values_associations()}
    Distinct values of Commesse: {get_text_distinct_values_commesse()}
    Domanda: {user_question}
    Genera una query SQL per rispondere.
    """
    prompt_text = (
        get_model_prompt("crea_query.txt")
        .replace("{question}", prompt_data)
        .replace("{history}", "\n".join(conversation_history))
    )
    resp = agente_crea_query.invoke({"question": prompt_data, "history": "".join(conversation_history)}).content.strip()
    log_model_call(resp, model_name, "crea_query.txt", user_question, prompt_text)
    return resp

def execute_sql_query(sql_query: str):
    try:
        cursor.execute(sql_query)
        return cursor.fetchall()
    except mysql.connector.Error as e:
        return f"Errore SQL: {e}"

def analytical_response(user_question: str, results) -> str:
    results_text = "\n".join([str(r) for r in results]) if results else "Nessun risultato trovato"
    prompt_text = (
        get_model_prompt("risposta_analitica.txt")
        .replace("{question}", user_question)
        .replace("{results}", results_text)
        .replace("{history}", "\n".join(conversation_history))
    )
    resp = agente_analitico.invoke({"domanda": user_question, "risultati": results_text, "history": "".join(conversation_history)}).content.strip()
    log_model_call(resp, model_name, "analytical", user_question, prompt_text)
    return resp

# ===============================
# CICLO CONVERSAZIONE
# ===============================
def handle_conversation():
    print(f"🚀 Chatbot avviato ({model_name})")
    while True:
        question = input("\nTu: ")
        conversation_history.append(f"Utente: {question}")
        if question.lower() in ["exit", "quit"]:
            break

        tipo = identify_question_type(question)
        print(f"🔎 Tipo identificato: {tipo}")

        if "generica" in tipo:
            risposta = generate_generic_response(question)

        elif "analitica" in tipo:
            sql_query = generate_query(question)
            print(f"📄 Query generata: {sql_query}")

            results = execute_sql_query(sql_query)
            
            conversation_history.append(f"AI: {sql_query}\nRisultati: {results[-50:]}")

            if isinstance(results, str):  # errore SQL
                risposta = results
            else:
                risposta = analytical_response(question, results)

        else:
            risposta = "⚠️ Errore: tipo di domanda non riconosciuto."

        

        if attiva_history:
            print("\n📝 Cronologia abilitata.")
        else:
            print("\n📝 Cronologia disabilitata.")
            conversation_history.clear()


        print("\n🤖 Risposta AI:")
        print("=" * 60)
        print(risposta)
        print("=" * 60)

# ===============================
# DB INIT
# ===============================
conn = mysql.connector.connect(
    host="mysql-1b17ab81-fintech2024mattiaforneron.g.aivencloud.com",
    port=21798,
    database="Eurofork",
    user="avnadmin",
    password="AVNS_cc1iKgD3ESBQrRwKvPo",
    ssl_disabled=False
)
cursor = conn.cursor()

conversation_history = []
attiva_history = True

if __name__ == "__main__":
    handle_conversation()
    conn.close()