import os, zipfile, json
from langchain_classic.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_classic.chains.retrieval_qa.base import RetrievalQA
from langchain_openai import ChatOpenAI
from pinecone import Pinecone
from dotenv import load_dotenv


load_dotenv()


class SemanticSearch:
    def __init__(self, mode):
        self.mode = mode

        self.pinecone_client = Pinecone(
            api_key=os.environ["PINECONE_API_KEY"]
        )

        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small"
        )

        self.llm = ChatOpenAI(
            model_name="gpt-3.5-turbo",
            temperature=0.2,
            
        )

        self.index_name = "llm"
        self.zip_file_path = "documentos.zip"
        self.indexed_files_path = 'indexed_files.json'
        self.extracted_folder_path = "docs"

        self.documents = []
        self.chunks = []


    def run(self):
        if self.mode == "ingest":
            self.ingest()

        if self.mode == "query":
            self.query()


    def ingest(self):
        print("Inserindo novos documentos...")

        self.extract_documents()
        self.insert_documents()
        
        if not self.documents:
            print('Nenhum documento novo para indexar.')
            return

        self.chunking()
        self.create_vector_store()

        print("Indexação concluída")


    def extract_documents(self):
        with zipfile.ZipFile(self.zip_file_path, "r") as zip_ref:
            zip_ref.extractall(self.extracted_folder_path)


    def insert_documents(self) -> None:
        indexed_files = self.load_indexed_files()
        new_indexed_files = set(indexed_files)

        for filename in os.listdir(self.extracted_folder_path):
            if not filename.endswith(".pdf"):
                continue

            if filename in indexed_files:
                print(f'{filename} já indexado')
                continue

            print(f'Indexando: {filename}')
            file_path = os.path.join(self.extracted_folder_path, filename)
            loader = PyMuPDFLoader(file_path)
            self.documents.extend(loader.load())
            new_indexed_files.add(filename)


        self.save_indexed_files(new_indexed_files)
        print(new_indexed_files)


    def chunking(self):
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100,
            length_function=len
        )

        self.chunks = splitter.create_documents(
            [doc.page_content for doc in self.documents]
        )


    def create_vector_store(self):
        PineconeVectorStore.from_documents(
            documents=self.chunks,
            embedding=self.embeddings,
            index_name=self.index_name
        )


    def query(self):
        index = self.pinecone_client.Index(self.index_name)

        vector_store = PineconeVectorStore(
            index=index,
            embedding=self.embeddings
        )

        retriever = vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 3}
        )

        chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=retriever
        )

        for q in self.get_queries():
            response = chain.invoke(q)
            print(f"\nPrompt: {q}")
            print(f"Resposta: {response['result']}")


    def get_queries(self):
        return [
            "Qual o número do processo que trata de Violação de normas ambientais pela Empresa de Construção?",
            "Qual foi a decisão no caso de fraude financeira?",
            "Quais foram as alegações no caso de negligência médica?",
            "Quais foram as alegações no caso de Número do Processo: 822162?"
        ]
        
    
        
    def load_indexed_files(self):
        if not os.path.exists(self.indexed_files_path):
            return set()
        with open(self.indexed_files_path, 'r') as f:
            return set(json.load(f))


    def save_indexed_files(self, indexed_files):
        with open(self.indexed_files_path, 'w') as f:
            json.dump(list(indexed_files), f, indent=2)



# semantic = SemanticSearch(mode="ingest")
# semantic.run()


semantic = SemanticSearch(mode="query")
semantic.run()
