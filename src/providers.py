from abc import ABC, abstractmethod

import tiktoken
from langchain_core.embeddings import Embeddings
from langchain_core.language_models import BaseChatModel
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

import settings
from logger import logger


class BaseProvider(ABC):
    """Abstract base class for AI providers."""

    @abstractmethod
    def get_embeddings(self) -> Embeddings:
        """Get the embeddings model instance."""
        pass

    @abstractmethod
    def get_llm(self) -> BaseChatModel:
        """Get the language model instance."""
        pass

    @abstractmethod
    def get_info(self) -> str:
        """Get a human-readable string of the provider's models."""
        pass

    @abstractmethod
    def count_tokens(self, text: str) -> int:
        """Count tokens in a given text according to the provider's model."""
        pass


class OpenAIProvider(BaseProvider):
    """Provider for OpenAI models."""

    def get_embeddings(self) -> OpenAIEmbeddings:
        logger.info(f"Using OpenAI Embeddings: {settings.OPENAI_EMBEDDING_MODEL}")
        return OpenAIEmbeddings(model=settings.OPENAI_EMBEDDING_MODEL)

    def get_llm(self) -> ChatOpenAI:
        logger.info(f"Using OpenAI LLM: {settings.OPENAI_LLM_MODEL}")
        return ChatOpenAI(model=settings.OPENAI_LLM_MODEL, temperature=0)

    def get_info(self) -> str:
        return (
            f"OpenAI ({settings.OPENAI_EMBEDDING_MODEL} + {settings.OPENAI_LLM_MODEL})"
        )

    def count_tokens(self, text: str) -> int:
        try:
            encoding = tiktoken.encoding_for_model(settings.OPENAI_EMBEDDING_MODEL)
            return len(encoding.encode(text))
        except Exception:
            logger.warning("Tiktoken model not found, falling back to character count.")
            return len(text) // 4


class GeminiProvider(BaseProvider):
    """Provider for Google Gemini models."""

    def get_embeddings(self) -> GoogleGenerativeAIEmbeddings:
        logger.info(f"Using Gemini Embeddings: {settings.GOOGLE_EMBEDDING_MODEL}")
        return GoogleGenerativeAIEmbeddings(model=settings.GOOGLE_EMBEDDING_MODEL)

    def get_llm(self) -> ChatGoogleGenerativeAI:
        logger.info(f"Using Gemini LLM: {settings.GOOGLE_LLM_MODEL}")
        return ChatGoogleGenerativeAI(model=settings.GOOGLE_LLM_MODEL, temperature=0)

    def get_info(self) -> str:
        return (
            f"Gemini ({settings.GOOGLE_EMBEDDING_MODEL} + {settings.GOOGLE_LLM_MODEL})"
        )

    def count_tokens(self, text: str) -> int:
        # Gemini does not have a standard local tokenizer library like tiktoken.
        # We fall back to a rough character-based estimation.
        return len(text) // 4


def get_provider_choice() -> BaseProvider:
    """Get user's provider choice via CLI and return an instance."""

    print("\n🤖 Escolha o provedor de IA:")
    print("1. OpenAI")
    print("2. Gemini")

    while True:
        try:
            choice = int(input("\nDigite sua opção (1 ou 2): ").strip())
            if choice == 1:
                return OpenAIProvider()
            elif choice == 2:
                return GeminiProvider()
            else:
                print("❌ Opção inválida. Digite 1 ou 2.")
        except (ValueError, IndexError):
            print("❌ Opção inválida. Digite 1 ou 2.")
