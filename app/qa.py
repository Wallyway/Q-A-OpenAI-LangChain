#======================================================================
 
# YOUTUBE SOURCE= https://www.youtube.com/watch?v=swwXhsl-PJ4&t=209s

#======================================================================



from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings

from langchain_community.llms import OpenAI
from langchain.chains import RetrievalQA
from langchain_core.documents import Document

import toml

PATH_SOURCES = "app/sources.txt"                # Path to the sources file
PATH_VECTORSTORE = "/app/store"             # Path to the vector store

#import dotenv

#dotenv.load_dotenv()

# Load the config.toml file
#config = toml.load("config.toml")

# Access the API key from the config
#api_key = config["general"]["OPENAI_API_KEY"]



class QAModel:
    def __init__(self):
        self.api_key = api_key
        self.load_sources()
        self.split_document()
        self.store_vectors()
        self.init_qa_retriever()
    

    def __call__(self,request: str):
        return self.retriever({                                                # Retrieve the answer
            "query": request                                                   # The question
        })

    # Load the sources from the sources file
    def load_sources(self):
        with open(PATH_SOURCES, "r") as ps:
            self.sources= ps.read()                                            # Read the sources from the file
        



    # Split the text into sentences (recursive)
    def split_document(self):
        splitter = RecursiveCharacterTextSplitter(      
            chunk_size=500,                                                     # Maximum number of characters in a chunk
            chunk_overlap=100,                                                  # Number of characters to overlap between chunks
            separators=["\n\n","(?<=\. )", " ", ""])                            # Sentence separators
        self.splits = [Document(page_content=chunk) for chunk in splitter.split_text(self.sources)]    # Split the document into sentences

    
    # Store the vectors of the sentences https://python.langchain.com/docs/integrations/vectorstores/
    def store_vectors(self):
        self.vectorstore = InMemoryVectorStore.from_documents(
            documents=self.splits,                                              # The sentences to store
            embedding=OpenAIEmbeddings(),                                       # The Embeddings where the vectors are stored
            persist_directory=PATH_VECTORSTORE)                                 # The directory to store the vectors
    

    # Initialize the QA retriever https://python.langchain.com/docs/integrations/llms/
    def init_qa_retriever(self):
        self.retriever = RetrievalQA.from_chain_type(
            llm=OpenAI(),                                                        # The LLM to use
            chain_type="map_reduce",                                             # The chain type
            retriever=self.vectorstore.as_retriever(search_type="mmr"))          # The retriever to use (More Similar or More Diverse)   

