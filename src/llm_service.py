import google.generativeai as genai
from src.config import GEMINI_API_KEY

class GeminiService:
    def __init__(self):
        # Configura a autenticação usando a chave segura
        genai.configure(api_key=GEMINI_API_KEY)
        
        # Utilizamos o modelo flash, que é rápido, inteligente e excelente para o free-tier
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    def generate_text(self, prompt: str) -> str:
        """
        Envia o prompt para o Gemini e retorna a resposta em texto.
        """
        try:
            # Envia a requisição
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            print(f"Erro ao comunicar com a API do Gemini: {e}")
            return None