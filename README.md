# 🎓 Edu Prompt Engine

O **Edu Prompt Engine** é um sistema avançado de geração de conteúdo educacional adaptativo baseado em Inteligência Artificial. Ele utiliza técnicas modernas de Engenharia de Prompt para criar explicações, exemplos práticos, perguntas socráticas e resumos visuais (ASCII) perfeitamente ajustados à idade, nível de conhecimento e estilo de aprendizagem (VARC) de cada aluno.

Este projeto foi desenvolvido com foco em resiliência, otimização de custos (Cache) e estruturação rigorosa de dados (JSON) em interações com LLMs.

---

## 🚀 Principais Funcionalidades

* **Adaptação de Persona (VARC):** O sistema molda o tom da IA e o tipo de analogia com base no estilo de aprendizagem do aluno (Visual, Auditivo, Leitura/Escrita, Cinestésico) e na sua idade.
* **Zero-Shot Chain-of-Thought (CoT):** Obriga a IA a estruturar um planejamento pedagógico invisível (`raciocinio`) antes de gerar o conteúdo final, evitando alucinações e garantindo a adequação do tom.
* **Restrição Estrita de Saída (JSON):** Tratamento de erros e limpeza de strings para garantir que o LLM retorne apenas *schemas* JSON válidos, permitindo a integração segura com o software.
* **Sistema de Cache Local (MD5):** Evita chamadas redundantes à API para prompts idênticos, economizando tempo e cota de uso.
* **Rate Limiting Handling:** Sistema de pausas estratégicas (`time.sleep`) para evitar o bloqueio por excesso de requisições na camada gratuita da API.
* **Testes A/B de Prompts:** Ferramenta integrada para comparar a qualidade das respostas entre um prompt básico (`v1`) e um prompt avançado (`v2`).

---

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3.10+
* **LLM API:** Google Gemini (`gemini-2.5-flash`)
* **Bibliotecas Principais:** * `google-generativeai` (Comunicação com o modelo)
    * `python-dotenv` (Gerenciamento de variáveis de ambiente)
    * `hashlib` e `json` (Nativas do Python para Cache e Parsing)

---

## 📂 Estrutura do Projeto

```text
edu-prompt-engine/
│
├── data/                       # Arquivos de dados de entrada e persistência local
│   ├── profiles.json           # Banco de dados de perfis de alunos (Mock data)
│   └── cache.json              # Sistema de cache para evitar chamadas repetidas à API
│
├── samples/                    # Diretório de outputs gerados pelo sistema
│   └── (Arquivos JSON com os materiais finais ficam salvos aqui)
│
├── src/                        # Código-fonte principal
│   ├── config.py               # Carrega as variáveis do .env e configurações globais
│   ├── prompt_manager.py       # Gerencia as versões dos prompts e templates
│   ├── llm_service.py          # Comunicação direta e tratamento de erros com a API Gemini
│   ├── cache_service.py        # Lógica de salvar/ler do cache via geração de hashes MD5
│   └── generator.py            # Orquestra os prompts e a API para gerar os conteúdos
│
├── .env                        # Chave de API local
├── .env.example                # Exemplo das chaves necessárias para rodar o projeto
├── .gitignore                  # Regras de segurança para não expor a chave de API
├── main.py                     # Ponto de entrada e lógica do menu interativo no terminal
├── requirements.txt            # Dependências do projeto
├── README.md                   # Documentação do projeto
└── PROMPT_ENGINEERING_NOTES.md # Análise técnica das estratégias de prompt utilizadas
```

## ⚙️ Como Executar o Projeto Localmente
### **1. Pré-requisitos**
Certifique-se de ter o `Python` instalado na sua máquina (versão 3.8 ou superior) e uma chave de API válida do [Google AI Studio](https://aistudio.google.com/).

### **2. Clonar o Repositório**
```bash
git clone https://github.com/luismiguuel/edu-prompt-engine.git
cd edu-prompt-engine
```

### **3. Configurar o Ambiente Virtual (Recomendado)**
```bash
# Criar o ambiente virtual
python -m venv venv
# Ativar o ambiente (Windows)
venv\Scripts\activate
# Ativar o ambiente (Linux/macOS)
source venv/bin/activate
```

### **4. Instalar Dependências**
```bash
pip install -r requirements.txt
```

### **5. Configurar as Variáveis de Ambiente**
Crie um arquivo chamado .env na raiz do projeto, baseado no .env.example, e adicione a sua chave da API:
```
GEMINI_API_KEY=sua_chave_secreta_aqui
```
*(Nota: O arquivo .env já está no .gitignore para garantir que a sua chave não seja exposta).*

### **6. Executar a Aplicação**
Inicie o menu interativo através do terminal:
```bash
python main.py
```

### 📖 Documentação Adicional
Para entender a fundo as decisões arquiteturais e as técnicas avançadas aplicadas na comunicação com o LLM (como System Persona, Chain-of-Thought e Context Ingestion), consulte o arquivo `PROMPT_ENGINEERING_NOTES.md` incluído neste repositório.