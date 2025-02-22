from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import VectorStoreIndex, Document , StorageContext
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.text_splitter import SentenceSplitter
from llama_index.vector_stores.chroma.base import ChromaVectorStore

import chromadb
from Extractor import SGExtractor
import os
from dotenv import load_dotenv
import hashlib
from transformers import pipeline , AutoTokenizer
from google import genai
import time
from transformers import pipeline

load_dotenv()



# StudyGuru Rag Model = SGRagModel
class SGRagModel:
    def __init__(self, embedding , data , collection):
        
        self.data = data
        self.embedding = HuggingFaceEmbedding(model_name=embedding)
        self.chunk_size = 512
        self.chunk_overlap = 100
        self.db = chromadb.PersistentClient(path="./chroma_db")
        self.collection_name = collection

        self.chroma_collection = self.db.get_or_create_collection(name=self.collection_name)
        self.vector_store = ChromaVectorStore(self.chroma_collection)
        self.index = None 
        self.storage_context = StorageContext.from_defaults(vector_store=self.vector_store)
        self.title_extractor = pipeline("summarization", model="Falconsai/text_summarization")
        
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


        summary = self.title_extractor(
            chunk,
            max_length=20,
            min_length=5,
            do_sample=True,      
            top_k=50,            
            top_p=0.95,          
            temperature=0.1
        )

        context = summary[0]['summary_text']


        print(f'Context found: {context} \n')

        return context


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

        chunk_titles = []
        document_nodes = []

        for node in nodes:
            chunk_title = self.contextual_chunking(node.text, node.metadata)
            
            chunk_titles.append(chunk_title)
            
            document = Document(
                text="Chunk title: " + chunk_title + "\n" + "Chunk Information: " + node.text,
                metadata=node.metadata,
                id_=hashlib.sha256(node.text.encode()).hexdigest()
            )
            
            document_nodes.append(document)

        self.index = VectorStoreIndex.from_documents(document_nodes, storage_context=self.storage_context, embed_model=self.embedding)
    

        
        print(f"File '{self.data}' successfully ingested into ChromaDB.")
        return chunk_titles

    def generate_id(self, text, file_name, page):
        base_id = f"{file_name}_page_{page}"
        text_hash = hashlib.md5(text.encode()).hexdigest()
        return f"{base_id}_{text_hash}"
        

    def retrieve(self, query):
        if not self.index:
            self.index = VectorStoreIndex.from_vector_store(self.vector_store, embed_model=self.embedding)

        retriever = self.index.as_retriever(similarity_top_k=2) 
        results = retriever.retrieve(query)

        return results

    def show_context(self,context):
        for i, c in enumerate(context):
            print(f"Context {i+1}:")
            print(c.text)
            print(c.metadata)
            print("\n")


def save_topics(topics,file):
    topics_path = data_path.split("/")[1]  

    save_dir = "test_data"
    os.makedirs(save_dir, exist_ok=True)

    file_path = os.path.join(save_dir, f"{topics_path}.txt")

    with open(file_path, "w") as file:
        for topic in topics:
            file.write(f"{topic}\n")

    print(f"Topics saved to {file_path}")

    


# class HuggingFaceQALLM():
#     def __init__(self, model_name="distilbert/distilbert-base-cased-distilled-squad", max_length=512):
#         self.qa_pipeline = pipeline("question-answering", model=model_name)

#     def complete(self, prompt):
#         context, question = prompt.split("\n\n", 1)
#         response = self.qa_pipeline(question=question, context=context)
#         return response["answer"]

# class GeminiLLM:
#     def __init__(self, model_name="gemini-2.0-flash"):

#         self.api_key = os.getenv("GEMINI_API_KEY")  
#         self.client = genai.Client(api_key=self.api_key)
#         self.model = model_name
        

#     def complete(self,prompt):

#         response = self.client.models.generate_content(
#         model=self.model ,contents=prompt
#         )

#         return response.text if response else "No response from Gemini."
    

if __name__ == "__main__":
    data_path = "test_data/test.pdf"
    hugging_llm  = "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B"
    hugging_embedding = "sentence-transformers/all-MiniLM-L6-v2"
    gemini_model = "gemini-2.0-flash"
    collection = "document_store"

    # llm_model = HuggingFaceQALLM()
    # llm_model = GeminiLLM(gemini_model)

    embedding_model = HuggingFaceEmbedding(model_name=hugging_embedding)

    rag = SGRagModel(embedding_model, data_path, collection)
    topics = rag.ingest_documents()

    if topics:
        save_topics(topics,data_path)



    test_query = "What are the regression measurements?"
    context = rag.retrieve(test_query)

    context_display = rag.show_context(context)
    print(context_display)
    # print(topics)

    del rag

    