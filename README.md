# Desafio MBA Engenharia de Software com IA - Full Cycle

# 🤖 PDF RAG Assistant (LangChain + Gemini + pgvector)

[Português](#br-versao-em-portugues) | [English](#en-english-version)

---

### <a name="br-versao-em-portugues"></a>🇧🇷 Versão em Português

# 🤖 Assistente de PDF (RAG) - MBA IA

Este projeto implementa uma solução de **RAG (Retrieval-Augmented Generation)** utilizando LangChain, Google Gemini e PostgreSQL (pgvector). O sistema permite ingerir documentos PDF e realizar perguntas interativas com base no conteúdo extraído.

---

## 🚀 Como Executar a Solução

### 1. Pré-requisitos
* **Python 3.12**
* **Docker** e **Docker Compose**
* **Google Gemini API Key** (Obtida no Google AI Studio)

### 2. Configuração do Ambiente
1. Clone o repositório e acesse a pasta do projeto.
2. Crie e ative seu ambiente virtual:
   - `python -m venv venv`
   - `source venv/Scripts/activate` (No Windows: `venv\Scripts\activate`)
3. Instale as dependências:
   - `pip install -r requirements.txt`
4. Crie um arquivo **.env** na raiz do projeto com as seguintes chaves:
   - `GOOGLE_API_KEY=sua_chave_aqui`
   - `PDF_PATH=document.pdf`
   - `DATABASE_URL=postgresql+psycopg2://ai:ai@localhost:5432/ai`
   - `PG_VECTOR_COLLECTION_NAME=documents_pdf`
   - `GOOGLE_EMBEDDING_MODEL=gemini-embedding-001`
   - `GOOGLE_CHAT_MODEL=gemini-1.5-flash`

---

## 🛠️ Fluxo de Execução

### Passo 1: Iniciar Banco de Dados
Certifique-se de que o Docker está rodando e inicie o container:
`docker compose up -d`

### Passo 2: Ingestão de Dados
Execute o script para processar o PDF e salvar os vetores no banco:
`python src/ingest.py`

### Passo 3: Chat Interativo
Execute o assistente para iniciar as perguntas:
`python src/chat.py`

---

## 🏛️ Detalhes Técnicos
* **Recuperação:** Busca pelos 10 documentos mais relevantes ($k=10$).
* **Prompt:** Configurado com regras estritas para evitar alucinações (Few-shot prompting).
* **Arquitetura:** Separação entre ingestão (`ingest.py`), lógica de busca (`search.py`) e interface de chat (`chat.py`).

---
## <a name="en-english-version"></a>EN English Version

# 🤖 PDF RAG Assistant - MBA AI

This project implements a robust **RAG (Retrieval-Augmented Generation)** solution using LangChain, Google Gemini, and PostgreSQL (pgvector). The system allows for PDF document ingestion and interactive Q&A based on the extracted content.

---

## 🚀 How to Run the Solution

### 1. Prerequisites
* **Python 3.12**
* **Docker** and **Docker Compose**
* **Google Gemini API Key** (Obtained from Google AI Studio)

### 2. Environment Setup
1. Clone the repository and navigate to the project folder.
2. Create and activate your virtual environment:
   - `python -m venv venv`
   - `source venv/Scripts/activate` (On Windows: `venv\Scripts\activate`)
3. Install the dependencies:
   - `pip install -r requirements.txt`
4. Create a **.env** file in the project root with the following keys:
   - `GOOGLE_API_KEY=your_key_here`
   - `PDF_PATH=document.pdf`
   - `DATABASE_URL=postgresql+psycopg2://ai:ai@localhost:5432/ai`
   - `PG_VECTOR_COLLECTION_NAME=documents_pdf`
   - `GOOGLE_EMBEDDING_MODEL=gemini-embedding-001`
   - `GOOGLE_CHAT_MODEL=gemini-1.5-flash`

---

## 🛠️ Execution Workflow

### Step 1: Start Database
Ensure Docker is running and start the container:
`docker compose up -d`

### Step 2: Data Ingestion
Run the script to process the PDF and store the vectors in the database:
`python src/ingest.py`

### Step 3: Interactive Chat
Run the assistant to start the Q&A session:
`python src/chat.py`

---

## 🏛️ Technical Details
* **Retrieval:** Fetches the top 10 most relevant documents ($k=10$).
* **Prompting:** Configured with strict rules to prevent hallucinations (Few-shot prompting).
* **Architecture:** Clean separation between ingestion (`ingest.py`), search logic (`search.py`), and chat interface (`chat.py`).