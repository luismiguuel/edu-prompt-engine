# 🧠 Notas de Engenharia de Prompt - AI Adaptive Tutor

Este documento detalha a arquitetura, as estratégias e as técnicas de *Prompt Engineering* aplicadas no desenvolvimento do **AI Adaptive Tutor**. O objetivo destas técnicas é domar a estocasticidade do LLM (Google Gemini), garantindo que as respostas sejam pedagogicamente precisas, seguras, formatadas corretamente (JSON) e altamente personalizadas para o perfil de cada aluno.

---

## 1. Técnicas Fundamentais Aplicadas

### 1.1. System Persona (Injeção de Papel)
**Como foi aplicado:** O prompt inicia definindo claramente o papel da IA: *"Você é um professor de Pedagogia altamente experiente..."* ou *"Você é um tutor focado no método socrático"*.
**Justificativa Técnica:** Definir uma "Persona" altera a distribuição de probabilidade dos tokens gerados pelo modelo. Em vez de aceder ao espaço latente genérico da internet, forçamos o modelo a buscar os seus pesos em contextos educacionais e didáticos. Isso garante um tom paciente, encorajador e elimina respostas puramente enciclopédicas.

### 1.2. Dynamic Context Ingestion (Injeção de Contexto Dinâmico)
**Como foi aplicado:** As variáveis do sistema (`nome`, `idade`, `nivel_conhecimento`, `estilo_aprendizado`) são injetadas no prompt dinamicamente antes da submissão à API.
**Justificativa Técnica:** Garante o *Grounding* (ancoragem) da resposta. A restrição mais importante aqui é o estilo de aprendizagem (ex: modelo VARC). Se a variável `estilo_aprendizado` for "Visual", o prompt instrui explicitamente o modelo a usar descrições ricas em imagens, cores e analogias espaciais.

### 1.3. Zero-Shot Chain-of-Thought (CoT)
**Como foi aplicado:** Foi adicionada uma instrução rigorosa para que o LLM estruture o seu pensamento *antes* de gerar a resposta final ao usuário, exigindo que a primeira chave do JSON retornado seja `"raciocinio"`.
**Justificativa Técnica:** Sem CoT, os LLMs frequentemente falham na adequação do tom, especialmente para crianças. Ao exigir que o modelo planeie (ex: *"Planeie passo a passo quais conceitos o aluno precisa entender primeiro"*), reduzimos drasticamente as "alucinações" e garantimos o alinhamento pedagógico. A IA "pensa em voz alta", ajusta o vocabulário para a idade (ex: 9 anos) e só então escreve a chave `"conteudo"`.

### 1.4. Constrained Output (Restrição Estruturada de Saída)
**Como foi aplicado:** O prompt exige: *"Retorne APENAS um objeto JSON válido. Não inclua blocos de código Markdown (` ```json `)."*
**Justificativa Técnica:** Essencial para a integração de LLMs em sistemas de software tradicionais. Texto livre quebra a aplicação. O *schema* rígido permite o *parsing* previsível dos dados no `generator.py`.

---

## 2. Análise de Resultados Práticos (Estudo de Caso)

Para validar a arquitetura, foi realizado um teste prático gerando conteúdo sobre **Fotossíntese** para a aluna **Sofia (9 anos, Estilo Visual)**.

**Evidências de sucesso do Prompt Avançado (v2):**

* **Efeito do Chain-of-Thought:** No log de raciocínio, o modelo planeou: *"O meu plano para explicar 'Fotossíntese' à Sofia [...] será associar a elementos visuais: Luz do Sol (Energia amarela), Água (Gotinhas azuis), Clorofila (Panela mágica verde)."* O planejamento funcionou perfeitamente como ponte entre o conhecimento técnico da IA e a limitação cognitiva da idade da aluna.
* **Adaptação de Persona e Idade:** A IA evitou jargões complexos ($C_6H_{12}O_6$, fótons, síntese) e substituiu por analogias compreensíveis: *"plantas fazem a sua própria comidinha"* e *"o sol é como um forninho gigante"*.
* **Efeito do Estilo Visual (VARC):** No conteúdo gerado para "Exemplos Práticos", o modelo inseriu instruções mentais visuais, como: `(Desenhe mentalmente raios de sol caindo nas folhas!)`, cumprindo estritamente a diretriz do prompt de focar no canal visual da aluna.
* **Representação Visual (ASCII):** A IA gerou um diagrama hierárquico correto e simples, formatado com *pipes* (`|`) e hífens (`-`), funcionando como um mapa mental que pode ser renderizado diretamente no terminal de texto puro, respeitando a restrição de "não usar imagens externas".
* **Método Socrático (Perguntas):** Em vez de perguntas de verificação de memória, o prompt forçou perguntas dedutivas: *"Se não existisse a fotossíntese, o que você acha que mudaria na comida que a gente come e no ar que a gente respira?"*

---

## 3. Comparação de Prompts (v1 vs v2)

O sistema possui uma ferramenta nativa de testes A/B para avaliar a evolução da engenharia de prompt:

* **Prompt v1 (Básico):** Sem instrução de persona forte e sem CoT. Tende a gerar um texto genérico, ignorando a idade da criança ou o estilo de aprendizagem, entregando uma estrutura parecida com a de um artigo da Wikipédia.
* **Prompt v2 (Avançado):** Graças à combinação de Persona + CoT + Injeção Dinâmica, o texto adota imediatamente o formato de "aula particular guiada", provando que o controle estruturado sobre a entrada (prompt) muda fundamentalmente a qualidade e a aplicabilidade da saída.

---
**Desenvolvido como demonstração de competência técnica em Engenharia de Prompts e Integração de LLMs via API.**