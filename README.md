# IA-RAG

Busca Semântica com IA

Este projeto implementa um sistema de busca semântica utilizando Inteligência Artificial, combinando embeddings, banco vetorial e LLM para recuperação de informações relevantes a partir de documentos PDF.

A solução permite indexar documentos e realizar consultas inteligentes baseadas em similaridade semântica, em vez de busca por palavras-chave.

Visão Geral da Arquitetura

O fluxo do sistema é dividido em duas etapas principais:

Ingestão (Indexação)
Extração de PDFs a partir de um arquivo ZIP
Leitura e carregamento dos documentos
Divisão em chunks
Geração de embeddings
Armazenamento em banco vetorial (Pinecone)
Consulta (Query)
Recebimento de perguntas
Recuperação de chunks mais relevantes
Geração de resposta utilizando LLM
Tecnologias Utilizadas
Python
LangChain
OpenAI (Embeddings e LLM)
Pinecone (Vector Database)
PyMuPDF (Leitura de PDFs)
dotenv
Estrutura do Projeto
.
├── semantic_search.py
├── documentos.zip
├── docs/                  # Pasta gerada com PDFs extraídos
├── indexed_files.json     # Controle de arquivos já indexados
├── requirements.txt
└── .env
Configuração do Ambiente
1. Clonar o repositório
git clone https://github.com/seu-usuario/seu-repo.git
cd seu-repo
2. Criar ambiente virtual

Linux / Mac:

python3 -m venv venv
source venv/bin/activate

Windows:

python -m venv venv
venv\Scripts\activate
3. Instalar dependências
pip install -r requirements.txt
4. Configurar variáveis de ambiente

Crie um arquivo .env na raiz do projeto:

OPENAI_API_KEY=your_openai_key
PINECONE_API_KEY=your_pinecone_key
Como Usar
1. Preparar os documentos

Coloque os PDFs dentro de um arquivo chamado:

documentos.zip
2. Rodar ingestão (indexação)

No código, altere:

semantic = SemanticSearch(mode="ingest")
semantic.run()

Execute:

python semantic_search.py

Isso irá:

Extrair os PDFs
Processar os documentos
Gerar embeddings
Armazenar no Pinecone
3. Rodar consultas

Altere o modo para:

semantic = SemanticSearch(mode="query")
semantic.run()

Execute:

python semantic_search.py

O sistema irá responder automaticamente às queries definidas no método:

def get_queries(self):
Funcionamento Interno
1. Extração de documentos
Arquivos são extraídos de documentos.zip
Apenas PDFs são considerados
2. Controle de indexação
Arquivos já indexados são armazenados em indexed_files.json
Evita reprocessamento desnecessário
3. Chunking

Os documentos são divididos em partes menores:

chunk_size: 1000 caracteres
overlap: 100 caracteres

Isso melhora a qualidade da busca semântica.

4. Embeddings
Modelo: text-embedding-3-small
Cada chunk é convertido em vetor numérico
5. Armazenamento vetorial
Banco: Pinecone
Índice: llm
6. Recuperação
Tipo: Similaridade
Top K: 3 resultados mais relevantes
7. Geração de resposta
Modelo: gpt-3.5-turbo
Chain: RetrievalQA
Exemplo de Queries

O sistema responde perguntas como:

Número de processos
Decisões judiciais
Alegações em casos legais

Exemplo:

Qual foi a decisão no caso de fraude financeira?
