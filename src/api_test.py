import os
from google import genai
from dotenv import load_dotenv

# Carregar chave de API do Gemini em .environment
load_dotenv('.environment')
api_key = os.getenv("GEMINI_API_KEY")

# Configurar o cliente da API do Gemini
client = genai.Client(api_key=api_key)

print("Modelos disponíveis:")
print("-" * 40)
try:
    # Lista os modelos
    for model in client.models.list():
        print(model.name)
except Exception as e:
    print(f"Erro ao acessar a API: {e}")