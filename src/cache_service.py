import json
import os
import hashlib

class CacheService:
    def __init__(self, cache_file_path: str = "data/cache.json"):
        self.cache_file = cache_file_path
        self._garantir_arquivo_cache()

    def _garantir_arquivo_cache(self):
        """Garante que a pasta data/ e o arquivo cache.json existam."""
        os.makedirs(os.path.dirname(self.cache_file), exist_ok=True)
        if not os.path.exists(self.cache_file):
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump({}, f)

    def gerar_chave(self, topico: str, aluno_id: str, versao_prompt: str, tipo_conteudo: str) -> str:
        """
        Gera um hash MD5 único para a combinação exata de parâmetros.
        """
        # Normaliza a string (tudo em minúsculas) para evitar que "Célula" e "célula" gerem caches diferentes
        string_base = f"{topico}_{aluno_id}_{versao_prompt}_{tipo_conteudo}".lower()
        
        # Cria o hash MD5
        return hashlib.md5(string_base.encode('utf-8')).hexdigest()

    def obter(self, chave: str):
        """
        Busca a resposta no cache. Retorna None se não encontrar.
        """
        try:
            with open(self.cache_file, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
                return cache_data.get(chave)
        except (json.JSONDecodeError, FileNotFoundError):
            # Se o arquivo estiver corrompido ou não existir, assumimos que não há cache
            return None

    def salvar(self, chave: str, resposta_ia: str):
        """
        Salva uma nova resposta da IA no arquivo de cache.
        """
        try:
            with open(self.cache_file, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            cache_data = {}

        # Adiciona a nova chave e salva no arquivo
        cache_data[chave] = resposta_ia

        with open(self.cache_file, 'w', encoding='utf-8') as f:
            json.dump(cache_data, f, ensure_ascii=False, indent=4)