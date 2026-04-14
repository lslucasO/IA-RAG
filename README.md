# Busca Semântica com IA

Este projeto implementa um sistema de busca semântica com Inteligência Artificial para indexação e consulta de documentos PDF. A solução utiliza embeddings, banco vetorial e modelo de linguagem para localizar trechos relevantes e gerar respostas com base no conteúdo dos arquivos.

O objetivo deste projeto é demonstrar, de forma prática, como construir um pipeline de Retrieval-Augmented Generation (RAG) com foco em recuperação semântica de informações.

## Objetivo

Permitir que documentos em PDF sejam processados, segmentados e armazenados em um banco vetorial para posterior consulta em linguagem natural.

## Arquitetura da Solução

O fluxo da aplicação é dividido em duas etapas principais.

### Ingestão

Nesta etapa, o sistema extrai arquivos PDF a partir de um arquivo compactado, realiza a leitura dos documentos, separa o conteúdo em partes menores, gera embeddings para cada trecho e envia esses vetores para o banco vetorial no Pinecone.

### Consulta

Na etapa de consulta, o sistema recebe perguntas em linguagem natural, realiza a busca semântica dos trechos mais relevantes e utiliza um modelo de linguagem para gerar uma resposta com base no contexto recuperado.

## Tecnologias Utilizadas

- Python
- LangChain
- OpenAI Embeddings
- OpenAI Chat Model
- Pinecone
- PyMuPDF
- python-dotenv

## Estrutura do Projeto

```bash
.
├── semantic_search.py
├── documentos.zip
├── docs/
├── indexed_files.json
├── requirements.txt
└── .env
```

## Pré-requisitos

Antes de executar o projeto, é necessário ter instalado na máquina:

- Python 3.10 ou superior
- Git
- Uma chave de API da OpenAI
- Uma chave de API do Pinecone

## Instalação

### Clonar o repositório

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

### Criar e ativar um ambiente virtual

#### Linux / Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Instalar as dependências

```bash
pip install -r requirements.txt
```

## Configuração das Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:

```env
OPENAI_API_KEY=sua_chave_openai
PINECONE_API_KEY=sua_chave_pinecone
```

## Como Executar

### Modo de ingestão

Para indexar os documentos, configure a aplicação para rodar no modo de ingestão e execute:

```bash
python semantic_search.py
```

Esse processo irá extrair os arquivos do `documentos.zip`, ler os PDFs, dividir o conteúdo em chunks, gerar embeddings e inserir os vetores no Pinecone.

### Modo de consulta

Para realizar consultas, configure a aplicação para rodar no modo de consulta e execute:

```bash
python semantic_search.py
```

Nesse modo, o sistema percorre as perguntas definidas no código e imprime no terminal as respostas geradas com base nos trechos recuperados do banco vetorial.

## Funcionamento do Projeto

### Extração de documentos

O sistema abre o arquivo `documentos.zip` e extrai os PDFs para a pasta `docs`.

### Controle de arquivos já indexados

O arquivo `indexed_files.json` é utilizado para registrar os PDFs que já foram processados, evitando reindexação desnecessária.

### Leitura dos documentos

Cada PDF é carregado com `PyMuPDFLoader`, responsável por extrair o conteúdo textual das páginas.

### Chunking

O texto é dividido com `RecursiveCharacterTextSplitter`, utilizando uma estratégia de separação em partes menores para melhorar a recuperação semântica durante a busca.

### Geração dos embeddings

Os chunks são transformados em vetores numéricos com o modelo `text-embedding-3-small`.

### Armazenamento vetorial

Os embeddings são enviados para o Pinecone, utilizando o índice configurado no projeto.

### Recuperação semântica

Durante a consulta, o sistema realiza busca por similaridade para recuperar os trechos mais relevantes.

### Geração da resposta

Após a recuperação do contexto, o modelo `gpt-3.5-turbo` é utilizado para gerar a resposta final.

## Configurações Importantes

### Nome do índice no Pinecone

O projeto utiliza um índice definido no código. Esse índice precisa existir no Pinecone para que a aplicação funcione corretamente.

### Nome do arquivo compactado

O sistema espera encontrar um arquivo chamado `documentos.zip` na raiz do projeto.

### Pasta de extração dos PDFs

Os arquivos extraídos são enviados para a pasta `docs`.

### Modelo de embedding utilizado

O projeto utiliza o modelo `text-embedding-3-small` para geração dos vetores semânticos.

### Modelo de linguagem utilizado

A geração das respostas é feita com `gpt-3.5-turbo`.

### Quantidade de resultados recuperados

A busca vetorial retorna os trechos mais relevantes com base na configuração definida no retriever.

## Exemplo de Uso

A aplicação pode ser utilizada para responder perguntas como:

- localizar números de processo
- identificar decisões em casos específicos
- recuperar alegações relacionadas a documentos jurídicos
- consultar informações relevantes em uma base documental indexada

## Aplicações Práticas

Esse tipo de solução pode ser aplicado em cenários como:

- busca inteligente em documentos jurídicos
- consulta em bases internas de conhecimento
- recuperação de informações em relatórios corporativos
- sistemas de apoio à decisão
- organização e consulta de acervos documentais

## Observações Importantes

Este projeto depende da configuração correta das variáveis de ambiente para acesso à OpenAI e ao Pinecone.

O arquivo `documentos.zip` deve estar presente na raiz do projeto para que a ingestão funcione corretamente.

O índice configurado no Pinecone deve estar disponível antes da execução.

Os documentos PDF precisam conter texto legível para que o carregamento e a indexação funcionem de forma adequada.

O arquivo `indexed_files.json` é utilizado para evitar processamento duplicado de documentos já indexados.

## Conclusão

Este projeto apresenta uma implementação objetiva de busca semântica com IA, demonstrando como integrar extração de documentos, divisão de texto, geração de embeddings, armazenamento vetorial e resposta com modelo de linguagem em um único fluxo.

A proposta é servir como base de estudo, demonstração técnica e apresentação prática de um pipeline de RAG aplicado à busca semântica em documentos PDF.
