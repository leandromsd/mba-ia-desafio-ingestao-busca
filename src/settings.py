import os

from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL")
OPENAI_LLM_MODEL = os.getenv("OPENAI_LLM_MODEL")

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_EMBEDDING_MODEL = os.getenv("GOOGLE_EMBEDDING_MODEL")
GOOGLE_LLM_MODEL = os.getenv("GOOGLE_LLM_MODEL")

DATABASE_URL = os.getenv("DATABASE_URL")
PG_VECTOR_COLLECTION_NAME = os.getenv("PG_VECTOR_COLLECTION_NAME")
PDF_PATH = os.getenv("PDF_PATH")

DATABASE_VARS = {"DATABASE_URL", "PG_VECTOR_COLLECTION_NAME"}
GOOGLE_VARS = {"GOOGLE_API_KEY", "GOOGLE_EMBEDDING_MODEL", "GOOGLE_LLM_MODEL"}
OPENAI_VARS = {"OPENAI_API_KEY", "OPENAI_EMBEDDING_MODEL", "OPENAI_LLM_MODEL"}

ALL_VARS = DATABASE_VARS | GOOGLE_VARS | OPENAI_VARS | {"PDF_PATH"}


def validate_environment() -> None:
    """Validate that all environment variables are configured."""
    missing_vars = {var for var in ALL_VARS if not globals().get(var)}
    if missing_vars:
        raise RuntimeError(
            f"❌ Variáveis obrigatórias não configuradas: "
            f"{', '.join(sorted(missing_vars))}\n"
            f"Configure todas as variáveis no arquivo .env"
        )
