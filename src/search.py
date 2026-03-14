import os
import sys
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_postgres import PGVector
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# Initialize environment variables
load_dotenv()

# Global Constants from .env
DB_URL = os.getenv("DATABASE_URL")
COLLECTION = os.getenv("PG_VECTOR_COLLECTION_NAME")
EMB_MODEL = os.getenv("GOOGLE_EMBEDDING_MODEL")
CHAT_MODEL = os.getenv("GOOGLE_CHAT_MODEL")


# The specific template provided by the exercise
PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""

def search_prompt():
    """
    Constructs the RAG chain with robust error handling and parameterized models.
    """
    try:
        # Validate environment configuration
        if not all([DB_URL, COLLECTION, EMB_MODEL, CHAT_MODEL]):
            raise ValueError("Missing required environment variables in .env file.")

        # Initialize Google Embeddings
        embeddings = GoogleGenerativeAIEmbeddings(model=EMB_MODEL)
        
        # Initialize Vector Store connection (PostgreSQL)
        vectorstore = PGVector(
            embeddings=embeddings,
            collection_name=COLLECTION,
            connection=DB_URL,
            use_jsonb=True,
        )

        # Configure Retriever (Requirement: exactly k=10 results)
        retriever = vectorstore.as_retriever(search_kwargs={"k": 10})

        # Initialize LLM with dynamic model selection
        llm = ChatGoogleGenerativeAI(model=CHAT_MODEL, temperature=0)

        # Build the Chain using LCEL (LangChain Expression Language)
        prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        
        chain = (
            {
                "contexto": retriever, 
                "pergunta": RunnablePassthrough()
            }
            | prompt
            | llm
            | StrOutputParser()
        )
        
        return chain

    except Exception as e:
        print(f"[!] Critical error initializing search chain: {e}", file=sys.stderr)
        return None