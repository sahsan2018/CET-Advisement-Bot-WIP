import os
import pickle
import tempfile
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

class Embedder:

    def __init__(self):
        self.PATH = "embeddings"
        self.createEmbeddingsDir()
    
    def createEmbeddingsDir(self):
        """
        Creates directory to store embeddings vectors
        """
        if not os.path.exists(self.PATH):
            os.mkdir(self.PATH)

    def storeDocEmbeds(self, file, original_filename):
        """
        Stores document embeddings using Langchain and FAISS
        """
        with tempfile.NamedTemporaryFile(mode="wb", delete=False) as tmp_file:
            tmp_file.write(file)
            tmp_file_path = tmp_file.name
            
        def get_file_extension(uploaded_file):
            file_extension =  os.path.splitext(uploaded_file)[1].lower()
            
            return file_extension
        
        #splits document with recursive character method
        text_splitter = RecursiveCharacterTextSplitter(
                chunk_size = 1500,
                chunk_overlap  = 150,
                length_function = len,
            )
        
        #setup for future iterations with support for multiple file types
        file_extension = get_file_extension(original_filename)

        if file_extension == ".pdf":
            loader = PyPDFLoader(file_path=tmp_file_path)  
            data = loader.load_and_split(text_splitter)
        
        #utilize OpenAI embeddings
        embeddings = OpenAIEmbeddings()

        #vectorstore with FAISS
        vectors = FAISS.from_documents(data, embeddings)
        os.remove(tmp_file_path)

        # Save the vectors to a pickle file
        with open(f"{self.PATH}/{original_filename}.pkl", "wb") as f:
            pickle.dump(vectors, f)

    def getDocEmbeds(self, file, original_filename):
        """
        Retrieves document embeddings
        """
        if not os.path.isfile(f"{self.PATH}/{original_filename}.pkl"):
            self.storeDocEmbeds(file, original_filename)

        # Load the vectors from the pickle file
        with open(f"{self.PATH}/{original_filename}.pkl", "rb") as f:
            vectors = pickle.load(f)
        
        return vectors
