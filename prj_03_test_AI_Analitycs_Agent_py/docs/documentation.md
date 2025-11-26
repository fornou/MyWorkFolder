# Modelli AI disponibili per questo piano
- gpt-3.5-turbo  
- gpt-audio  
- gpt-5-mini  
- gpt-5-nano-2025-08-07  
- gpt-5-nano  
- gpt-audio-2025-08-28  
- davinci-002  
- babbage-002  
- gpt-3.5-turbo-instruct  
- gpt-3.5-turbo-instruct-0914  
- dall-e-3  
- dall-e-2  
- gpt-3.5-turbo-1106  
- tts-1-hd  
- tts-1-1106  
- tts-1-hd-1106  
- text-embedding-3-small  
- text-embedding-3-large  
- gpt-3.5-turbo-0125  
- gpt-4o  
- gpt-4o-2024-05-13  
- gpt-4o-mini-2024-07-18  
- gpt-4o-mini  
- gpt-4o-2024-08-06  
- o1-mini-2024-09-12  
- o1-mini  
- gpt-4o-audio-preview-2024-10-01  
- gpt-4o-audio-preview  
- omni-moderation-latest  
- omni-moderation-2024-09-26  
- gpt-4o-audio-preview-2024-12-17  
- gpt-4o-mini-audio-preview-2024-12-17  
- o1-2024-12-17  
- o1  
- gpt-4o-mini-audio-preview  
- o3-mini  
- o3-mini-2025-01-31  
- gpt-4o-2024-11-20  
- gpt-4o-search-preview-2025-03-11  
- gpt-4o-search-preview  
- gpt-4o-mini-search-preview-2025-03-11  
- gpt-4o-mini-search-preview  
- gpt-4o-transcribe  
- gpt-4o-mini-transcribe  
- gpt-4o-mini-tts  
- o3-2025-04-16  
- o4-mini-2025-04-16  
- o3  
- o4-mini  
- gpt-4.1-2025-04-14  
- gpt-4.1  
- gpt-4.1-mini-2025-04-14  
- gpt-4.1-mini  
- gpt-4.1-nano-2025-04-14  
- gpt-4.1-nano  
- gpt-image-1  
- gpt-4o-audio-preview-2025-06-03  
- gpt-5-chat-latest  
- gpt-5-2025-08-07  
- gpt-5  
- whisper-1  
- tts-1  
- gpt-3.5-turbo-16k  
- text-embedding-ada-002


# Funzione per creare una risposta con OpenAI

Questo esempio mostra come generare una risposta utilizzando il metodo `client.chat.completions.create()`.

```python
resp = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": get_model_prompt("interpretazione_domanda.txt")},
        {"role": "user", "content": user_question}
    ],
    max_tokens=20,
    temperature=0
)
``` 
# Descrizione dei parametri

## model
Indica il modello da utilizzare (es. `gpt-4o-mini`, `gpt-4`, `gpt-3.5-turbo`).  
La scelta del modello influenza capacità, costo e velocità della risposta.

## messages
È una lista di messaggi che definiscono il contesto e la conversazione.  
Ogni messaggio è un dizionario con due chiavi:

- **role**: può essere `system`, `user`, o `assistant`  
- **content**: il testo effettivo del messaggio  

Nell’esempio:
- **system** → imposta il comportamento del modello, caricando un prompt da file.  
- **user** → rappresenta la domanda effettiva posta dall’utente.  

## max_tokens
Limita la lunghezza massima della risposta (numero di token generati).

## temperature
Controlla la creatività del modello:
- `0` → risposta deterministica, più precisa.  
- `1` → risposta più varia e creativa.  
- valori >1 → aumentano la casualità.  

# Output
La variabile `resp` contiene l’oggetto risposta generato dal modello.  
Puoi accedere al contenuto della risposta con:

```python
print(resp.choices[0].message["content"])