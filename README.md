# Chat com Documentos PDF

Sistema de ingestão e busca semântica usando LangChain, PostgreSQL e pgVector.

## 🚀 Como Executar

### 1. Configurar Ambiente

```bash
# Criar ambiente virtual
python -m venv venv
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

### 2. Configurar Variáveis

Copie o arquivo de exemplo e configure suas variáveis.

```bash
cp .env.example .env
```

### 3. Executar Sequência

```bash
# 1. Subir banco de dados
docker compose up -d

# 2. Ingerir PDF no banco
python src/ingest.py

# 3. Iniciar chat interativo
python src/chat.py
```

## 📁 Estrutura

```
├── src/
│   ├── chat.py      # CLI interativo
│   ├── ingest.py    # Ingestão do PDF
│   ├── logger.py    # Sistema de logging
│   ├── providers.py # Provedores de IA (OpenAI/Google)
│   ├── search.py    # Busca semântica
│   └── settings.py  # Configurações e variáveis
├── .env.example     # Exemplo de variáveis
├── document.pdf     # PDF para processar
├── requirements.txt # Dependências Python
└── docker-compose.yml # Banco PostgreSQL
```

## 💬 Como Usar o Chat

1. **Escolha o provedor de IA** (OpenAI ou Gemini)
2. Digite suas perguntas sobre o documento PDF
3. O sistema busca informações relevantes e responde baseado apenas no conteúdo do PDF
4. Digite `sair` para encerrar

**Exemplo:**
```
🤖 Escolha o provedor de IA:
1. OpenAI
2. Gemini

Digite sua opção (1 ou 2): 1
✅ Provedor selecionado: OpenAI (text-embedding-3-small + gpt-4o-mini)

PERGUNTA: Qual o faturamento da empresa Verde Biotech LTDA?
RESPOSTA: O faturamento foi de R$ 284.496.406,98.
```

## 🛠️ Desenvolvimento

### Formatação e Lint

O projeto usa ferramentas padrão para manter qualidade do código:

```bash
# Formatar código
black src/

# Organizar imports
isort src/

# Verificar lint
flake8 src/

# Executar tudo de uma vez
isort src/ && black src/ && flake8 src/
```

### Configurações

- **Black**: Line length 88, target Python 3.10+
- **isort**: Profile "black" para compatibilidade
- **flake8**: Max line length 88, ignora E203/W503

As configurações estão em `pyproject.toml` e `.flake8`.