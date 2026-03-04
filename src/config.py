import os
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

# Pega a chave do Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Validação de segurança
if not GEMINI_API_KEY:
    raise ValueError("ERRO: A variável GEMINI_API_KEY não foi encontrada. Verifique seu arquivo .env!")