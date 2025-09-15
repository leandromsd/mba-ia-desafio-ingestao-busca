from typing import List, Tuple

from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_postgres import PGVector

import settings
from logger import logger
from providers import BaseProvider

PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

INSTRUÇÕES DE RESPOSTA:
1. Responda **somente** com base no CONTEXTO fornecido.
2. Responda **apenas** sobre o que foi perguntado especificamente
   (faturamento, fundação, etc.).
3. **NÃO** inclua informações extras não solicitadas na pergunta.
4. Se a informação **não estiver no CONTEXTO**, responda:
   "Não tenho informações necessárias para responder sua pergunta."
5. Para **nomes similares**:
   - Se houver uma empresa que contém as palavras-chave principais
     da busca, responda sobre essa empresa específica.
   - Se houver múltiplas empresas sem uma correspondência clara
     dominante, liste no máximo 3 com a informação solicitada.
   - Quando listar múltiplas, explique que não encontrou o nome
     exato e sugira ser mais específico.
6. Não invente informações e não use conhecimento externo.
7. Não produza opiniões, hipóteses ou interpretações além do que está escrito.

---

EXEMPLO 1 — PERGUNTA DENTRO DO CONTEXTO:
Pergunta: "Qual o faturamento da empresa Alfa Agronegócio Indústria?"

Se no CONTEXTO houver:
- "Alfa Agronegócio Indústria — R$ 85.675.568,77 (fundada em 2005)"

Resposta:
"O faturamento foi de R$ 85.675.568,77."

---

EXEMPLO 2 — CORRESPONDÊNCIA CLARA (NÃO LISTAR MÚLTIPLAS):
Pergunta: "Qual o faturamento da empresa Vector Comércio?"

Se no CONTEXTO houver:
- "Vector Mineração Comércio — R$ 365.800,05 (fundada em 2010)"
- "Vector E-commerce Holding — R$ 451.268,78 (fundada em 2015)"

Resposta:
"O faturamento foi de R$ 365.800,05."

Explicação: "Vector Comércio" tem correspondência clara com
"Vector Mineração Comércio" (contém os termos principais da busca).
Não é ambíguo.

---

EXEMPLO 3 — MÚLTIPLAS EMPRESAS SIMILARES:
Pergunta: "Qual o faturamento da Vale?"

Se no CONTEXTO houver muitas empresas "Vale":
- Vale Fármacos Holding — R$ 1.058.327.479,55
- Vale E-commerce Comércio — R$ 847.706.494,69
- Vale Educação EPP — R$ 933.348.306,15
- [+ outras empresas Vale]

Resposta:
"Não encontrei exatamente uma empresa chamada "Vale",
mas encontrei algumas empresas com esse nome:
- Vale Fármacos Holding: R$ 1.058.327.479,55
- Vale Educação EPP: R$ 933.348.306,15
- Vale E-commerce Comércio: R$ 847.706.494,69

Para uma resposta mais precisa, seja mais específico sobre qual
empresa Vale você procura."

---

EXEMPLO 4 — PERGUNTAS FORA DO CONTEXTO:

Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

---


PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""


def search_documents(
    query: str, embeddings: Embeddings, k: int = 10
) -> List[Tuple[Document, float]]:
    """Search for similar documents in the vector database."""
    vector_store = PGVector(
        embeddings=embeddings,
        collection_name=settings.PG_VECTOR_COLLECTION_NAME,
        connection=settings.DATABASE_URL,
        use_jsonb=True,
    )

    logger.info(f"Searching for: '{query}'")
    results = vector_store.similarity_search_with_score(query, k=k)
    logger.info(f"Found {len(results)} similar documents")

    return results


def generate_response(query: str, provider: BaseProvider) -> str:
    """Generate response based on query and context from vector database."""
    try:
        embeddings = provider.get_embeddings()
        llm = provider.get_llm()

        results = search_documents(query, embeddings, k=10)

        if not results:
            return "Não tenho informações necessárias para responder sua pergunta."

        context = "\n\n".join([doc.page_content for doc, _ in results])

        prompt = PROMPT_TEMPLATE.format(contexto=context, pergunta=query)

        response = llm.invoke(prompt)

        return response.content

    except Exception as e:
        logger.error(f"Error generating response: {e}")
        return "Erro ao processar sua pergunta. Tente novamente."
