# edu-prompt-engine

# 📂 Estrutura do Projeto

```text
edu_prompt_engine/
│
├── data/                       # Arquivos de dados de entrada e persistência local
│   ├── profiles.json           # Os 3-5 perfis de alunos (mock data)
│   └── cache.json              # Sistema de cache para evitar chamadas repetidas
│
├── samples/                    # Diretório exigido pelo desafio para os outputs
│   └── (arquivos gerados pelo sistema ficarão aqui)
│
├── src/                        # Código-fonte principal (Core da aplicação)
│   ├── __init__.py
│   ├── config.py               # Carrega as variáveis do .env e configurações globais
│   ├── models.py               # Estruturas de dados (ex: classes para Aluno, Resposta)
│   ├── prompt_manager.py       # Gerencia as versões dos prompts e os templates (Engenharia)
│   ├── llm_service.py          # Gerencia a comunicação direta com a API (Gemini/OpenAI/Claude)
│   ├── cache_service.py        # Lógica de salvar/ler do cache (geração de hashes)
│   ├── generator.py            # Orquestra os prompts e a API para gerar os 4 tipos de conteúdo
│   └── cli.py                  # Lógica do menu interativo no terminal
│
├── tests/                      # (Opcional) Testes básicos para garantir ponto extra
│   └── test_generator.py
│
├── .env                        # Suas chaves de API (NUNCA commitar no Git)
├── .env.example                # Exemplo das chaves necessárias (exigido no desafio)
├── .gitignore                  # Impede que .env e cache sejam enviados ao Git
├── main.py                     # Ponto de entrada do programa (Chama o cli.py)
├── requirements.txt            # Dependências (requests, python-dotenv, etc.)
├── README.md                   # Documentação do projeto
└── PROMPT_ENGINEERING_NOTES.md # Explicação das estratégias de prompt (exigido)
```