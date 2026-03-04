import json
import os
from datetime import datetime
from src.llm_service import GeminiService
from src.prompt_manager import PromptManager
from src.cache_service import CacheService

class GeradorConteudo:
    def __init__(self):
        self.llm = GeminiService()
        self.prompt_manager = PromptManager()
        self.cache = CacheService()
        
        # Carrega os perfis dos alunos
        with open("data/profiles.json", "r", encoding="utf-8") as f:
            self.perfis = json.load(f)
            
        # Garante que a pasta samples existe
        os.makedirs("samples", exist_ok=True)

    def _obter_perfil(self, aluno_id: str) -> dict:
        for perfil in self.perfis:
            if perfil["id"] == aluno_id:
                return perfil
        raise ValueError(f"Aluno com ID '{aluno_id}' não encontrado.")

    def _limpar_json_markdown(self, texto: str) -> dict:
        """
        Remove blocos de markdown e converte a string da IA para um dicionário Python.
        Tratamento robusto de erros (Edge case).
        """
        if not texto:
            return {"erro": "Nenhum texto retornado pela API."}
        try:
            # Tenta converter direto primeiro
            return json.loads(texto)
        except json.JSONDecodeError:
            # Se falhar, tenta limpar as crases de markdown
            texto_limpo = texto.strip()
            if texto_limpo.startswith("```json"):
                texto_limpo = texto_limpo[7:]
            elif texto_limpo.startswith("```"):
                texto_limpo = texto_limpo[3:]
                
            if texto_limpo.endswith("```"):
                texto_limpo = texto_limpo[:-3]
                
            try:
                return json.loads(texto_limpo.strip())
            except json.JSONDecodeError:
                # Se falhar miseravelmente, retorna como texto puro dentro de um dict
                return {"erro_parse": "A IA não retornou um JSON válido", "texto_bruto": texto}

    def _salvar_resultado(self, dados: dict, prefixo: str):
        """Salva o resultado na pasta samples com timestamp."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_arquivo = f"samples/{prefixo}_{timestamp}.json"
        
        with open(nome_arquivo, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=4)
            
        return nome_arquivo

    def gerar(self, aluno_id: str, topico: str, tipo_conteudo: str, versao_prompt: str = "v2_avancado"):
        """
        Orquestra todo o processo de geração para um tipo específico de conteúdo.
        """
        perfil = self._obter_perfil(aluno_id)
        
        # 1. Verifica o Cache
        chave_cache = self.cache.gerar_chave(topico, aluno_id, versao_prompt, tipo_conteudo)
        resultado = self.cache.obter(chave_cache)
        
        usou_cache = True
        if not resultado:
            usou_cache = False
            # 2. Constrói o Prompt
            prompt = self.prompt_manager.construir_prompt(
                versao=versao_prompt,
                tipo_conteudo=tipo_conteudo,
                perfil_aluno=perfil,
                topico=topico
            )
            
            # 3. Chama a IA
            resposta_bruta = self.llm.generate_text(prompt)

            if not resposta_bruta:
                return None, {"erro": "A IA não retornou nenhum conteúdo."}
            
            # 4. Processa a resposta (limpa o JSON se necessário)
            if versao_prompt == "v2_avancado":
                resultado = self._limpar_json_markdown(resposta_bruta)
            else:
                resultado = {"conteudo": resposta_bruta} # v1 não pede JSON
                
            # 5. Salva no Cache
            self.cache.salvar(chave_cache, resultado)

        # 6. Salva o arquivo de output final
        dados_finais = {
            "metadados": {
                "aluno": perfil["nome"],
                "topico": topico,
                "tipo_conteudo": tipo_conteudo,
                "versao_prompt": versao_prompt,
                "usou_cache": usou_cache
            },
            "resultado": resultado
        }
        
        arquivo_salvo = self._salvar_resultado(dados_finais, f"{aluno_id}_{tipo_conteudo}_{versao_prompt}")
        return arquivo_salvo, dados_finais
        
    def comparar_prompts(self, aluno_id: str, topico: str, tipo_conteudo: str):
        """
        Gera o mesmo conteúdo usando v1 e v2 para comparação (Requisito 4b e 4c).
        """
        _, res_v1 = self.gerar(aluno_id, topico, tipo_conteudo, "v1_basico")
        _, res_v2 = self.gerar(aluno_id, topico, tipo_conteudo, "v2_avancado")
        
        comparacao = {
            "topico": topico,
            "aluno": self._obter_perfil(aluno_id)["nome"],
            "comparacao": {
                "v1_basico": res_v1["resultado"],
                "v2_avancado_com_tecnicas": res_v2["resultado"]
            }
        }
        
        arquivo = self._salvar_resultado(comparacao, f"COMPARACAO_{aluno_id}_{tipo_conteudo}")
        return arquivo, comparacao