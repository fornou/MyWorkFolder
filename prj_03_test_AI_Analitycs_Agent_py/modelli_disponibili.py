from openai import OpenAI
from dotenv import load_dotenv
import os

# 🔑 Carica API key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("❌ Chiave API non trovata!")
    exit()

client = OpenAI(api_key=api_key)

models = client.models.list()
for m in models.data:
    print(m.id)
