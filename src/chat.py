import settings
from logger import logger
from providers import get_provider_choice
from search import generate_response


def main():
    """Main CLI function for interactive chat."""

    print("🤖 Chat com Documentos PDF")
    print("=" * 50)

    try:
        settings.validate_environment()
        provider = get_provider_choice()
        provider_info = provider.get_info()

        print(f"\n✅ Provedor selecionado: {provider_info}")
        print("=" * 50)
        print("Digite suas perguntas sobre o documento PDF.")
        print("Digite 'sair' para encerrar.")
        print("=" * 50)

        while True:
            question = input("\nPERGUNTA: ").strip()

            if question.lower() == "sair":
                print("\n👋 Até logo!")
                break

            if not question:
                print("❌ Por favor, digite uma pergunta.")
                continue

            print("\n🔍 Buscando informações...")
            response = generate_response(question, provider)
            print(f"\nRESPOSTA: {response}")
    except Exception as e:
        logger.error(f"Erro no chat: {e}")
        print(f"\n❌ Erro: {e}")


if __name__ == "__main__":
    main()
