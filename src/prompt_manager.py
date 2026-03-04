import json

class PromptManager:
    def __init__(self):
        # Dicionário que armazena as versões dos nossos templates de prompt
        self.templates = {
            "v1_basico": {
                "explicacao": "Explica o tópico '{topico}' para um aluno chamado {nome} que tem {idade} anos.",
                "exemplos": "Dá-me 2 exemplos práticos sobre '{topico}' para o aluno {nome}.",
                "perguntas": "Cria 3 perguntas sobre '{topico}' para o aluno {nome}.",
                "resumo_visual": "Faz um resumo visual em ASCII sobre '{topico}'."
            },
            "v2_avancado": {
                "explicacao": """
Você é um professor de Pedagogia altamente experiente (Persona).
O seu aluno chama-se {nome}, tem {idade} anos, está num nível {nivel} no assunto e tem um estilo de aprendizagem {estilo_aprendizado}. Contexto adicional: {contexto} (Context Setting).

Aja como o tutor deste aluno e explique o tópico '{topico}'.
Antes de dar a resposta final, escreva '<raciocinio>' e planeie passo a passo quais conceitos o aluno precisa de entender primeiro, considerando a sua idade e estilo de aprendizagem (Chain-of-Thought).

Formato de saída obrigatório (Output Formatting):
Retorne APENAS um objeto JSON válido (sem blocos de código Markdown), com as chaves:
{{"raciocinio": "o seu planeamento aqui", "conteudo": "a explicação final aqui"}}
""",
                "exemplos": """
Você é um professor especialista em didática.
Crie 2 exemplos práticos sobre '{topico}' adaptados para {nome} (Idade: {idade}, Nível: {nivel}, Estilo de Aprendizagem: {estilo_aprendizado}).
Como o estilo é {estilo_aprendizado}, os exemplos devem refletir essa preferência (ex: se visual, use descrições visuais; se cinestésico, use exemplos práticos ou mecânicos).

Retorne APENAS um JSON válido no formato:
{{"conteudo": ["exemplo 1", "exemplo 2"]}}
""",
                "perguntas": """
Você é um tutor focado no método socrático.
Baseado no tópico '{topico}', crie 3 perguntas de reflexão para {nome} (Nível: {nivel}, Idade: {idade}).
As perguntas não devem ter respostas de "sim" ou "não", mas sim estimular o pensamento crítico de acordo com a idade do aluno.

Retorne APENAS um JSON válido no formato:
{{"conteudo": ["pergunta 1", "pergunta 2", "pergunta 3"]}}
""",
                "resumo_visual": """
Você é um especialista em mapas mentais.
Crie um diagrama ou mapa mental simples usando caracteres ASCII para explicar '{topico}'.
A complexidade do diagrama deve ser adequada para um aluno de {idade} anos (Nível: {nivel}).

Retorne APENAS um JSON válido no formato:
{{"conteudo": "diagrama em arte ASCII aqui (com quebras de linha usando \\n)"}}
"""
            }
        }

    def construir_prompt(self, versao: str, tipo_conteudo: str, perfil_aluno: dict, topico: str) -> str:
        """
        Injeta os dados do aluno e do tópico no template escolhido.
        """
        if versao not in self.templates:
            raise ValueError(f"Versão de prompt '{versao}' não encontrada.")
            
        if tipo_conteudo not in self.templates[versao]:
            raise ValueError(f"Tipo de conteúdo '{tipo_conteudo}' não encontrado.")

        template = self.templates[versao][tipo_conteudo]
        
        # Preenche o template com os dados dinâmicos
        prompt_formatado = template.format(
            nome=perfil_aluno.get("nome", "Aluno"),
            idade=perfil_aluno.get("idade", ""),
            nivel=perfil_aluno.get("nivel", ""),
            estilo_aprendizado=perfil_aluno.get("estilo_aprendizado", ""),
            contexto=perfil_aluno.get("contexto", ""),
            topico=topico
        )
        
        return prompt_formatado