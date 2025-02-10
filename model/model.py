from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import VectorStoreIndex, Document , StorageContext
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.text_splitter import SentenceSplitter
from llama_index.vector_stores.chroma.base import ChromaVectorStore

import chromadb
from extractor import SGExtractor
import os
from dotenv import load_dotenv
import hashlib
from transformers import pipeline
from google import genai
import time

load_dotenv()



# StudyGuru Rag Model = SGRagModel
class SGRagModel:
    def __init__(self, llm, embedding , data , collection):
        
        self.data = data
        self.llm = llm 
        self.embedding = embedding
        self.dimension = 512
        self.chunk_size = 200
        self.chunk_overlap = 50
        self.db = chromadb.PersistentClient(path="./chroma_db")
        self.collection_name = collection

        self.chroma_collection = self.db.get_or_create_collection(name=self.collection_name)
        self.vector_store = ChromaVectorStore(self.chroma_collection)
        self.index = None 
        self.storage_context = StorageContext.from_defaults(vector_store=self.vector_store)
        
    def process_documents(self,file_path):
        print(f"Processing Documents from {file_path}")
        extractor = SGExtractor(file_path)
        content = extractor.extract_content()

        page_documents = [
            Document(
                text=content[chunk][0] + content[chunk][1],
                metadata={"file_name": file_path, "page": chunk},
            )
            for chunk in content
        ]
        return page_documents
    
    def contextual_chunking(self, chunk, chunk_info):
        print(f"Extracting title for: {chunk_info}")

        prompt = (
            f"INSTRUCTIONS: Identify the title of the following document. If you are not able to find the title then use a appriopriate summary title "
            f"Respond with ONLY the title and nothing else. "
            f"\n\nDOCUMENT:\n{chunk}"
        )

        chunk_title = self.llm.complete(prompt)
        time.sleep(5)

        return chunk_title


    def ingest_documents(self):
        print(f"Checking if this {self.data} has already been processed...")

        existing_data = self.chroma_collection.get(where={"file_name": self.data})  

        if existing_data["ids"]:  
            print(f"File '{self.data}' already exists in ChromaDB. Skipping processing.")
            return

        print("No existing records for this file. Processing and storing documents...")

        documents = self.process_documents(self.data)
        text_splitter = SentenceSplitter(chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)

        pipeline = IngestionPipeline(transformations=[text_splitter])
        nodes = pipeline.run(documents=documents)

        document_nodes = [
            Document(text="Chunk title: "+self.contextual_chunking(node.text,node.metadata)+"\n"+ "Chunk Information: "+node.text,
                     metadata=node.metadata,
                     id_=hashlib.sha256(node.text.encode()).hexdigest()) 
            for node in nodes
        ]

        self.index = VectorStoreIndex.from_documents(document_nodes, storage_context=self.storage_context, embed_model=self.embedding)
    

        
        print(f"File '{self.data}' successfully ingested into ChromaDB.")
        return nodes

    def generate_id(self, text, file_name, page):
        base_id = f"{file_name}_page_{page}"
        text_hash = hashlib.md5(text.encode()).hexdigest()
        return f"{base_id}_{text_hash}"
        

    def retrieve(self, query):
        if not self.index:
            self.index = VectorStoreIndex.from_vector_store(self.vector_store, embed_model=self.embedding)

        retriever = self.index.as_retriever(similarity_top_k=5) 
        results = retriever.retrieve(query)

        return results

    def show_context(self,context):
        for i, c in enumerate(context):
            print(f"Context {i+1}:")
            print(c.text)
            print(c.metadata)
            print("\n")

    def answer(self,context,query):
        context_text = "\n".join(node.text for node in context)
        prompt = f"Context: {context_text}\n\n Query: {query}"
        return self.llm.complete(prompt)


class HuggingFaceQALLM():
    def __init__(self, model_name="distilbert/distilbert-base-cased-distilled-squad"):
        self.qa_pipeline = pipeline("question-answering", model=model_name)

    def complete(self, prompt):
        context, question = prompt.split("\n\n", 1)
        response = self.qa_pipeline(question=question, context=context)
        return response["answer"]

class GeminiLLM:
    def __init__(self, model_name="gemini-2.0-flash"):

        self.api_key = os.getenv("GEMINI_API_KEY")  
        self.client = genai.Client(api_key=self.api_key)
        self.model = model_name
        

    def complete(self,prompt):

        response = self.client.models.generate_content(
        model=self.model ,contents=prompt
        )

        return response.text if response else "No response from Gemini."

if __name__ == "__main__":
    data_path = "test_data/test.pdf"
    hugging_llm  = "microsoft/phi-2"
    hugging_embedding = "sentence-transformers/all-MiniLM-L6-v2"
    gemini_model = "gemini-2.0-flash"
    collection = "document_store"

    # llm_model = HuggingFaceQALLM(hugging_llm)
    llm_model = GeminiLLM(gemini_model)
    embedding_model = HuggingFaceEmbedding(model_name=hugging_embedding)

    rag = SGRagModel(llm_model, embedding_model, data_path, collection)
    rag.ingest_documents()

    test_query = "What are the content?"
    context = rag.retrieve(test_query)

    context_display = rag.show_context(context)
    response = rag.answer(context,test_query)
    print(response)

    del rag