from llama_index.core import VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.faiss import FaissVectorStore
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.text_splitter import SentenceSplitter
from llama_index.core import Document
from extractor import SGExtractor
import faiss
from transformers import pipeline
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()


# StudyGuru Rag Model = SGRagModel
class SGRagModel:
    def __init__(self, llm, embedding , data):
        
        self.data = data
        self.llm = llm 
        self.embedding = embedding
        self.dimension = 512
        self.chunk_size = 200
        self.chunk_overlap = 50
        
    def process_documents(self,file_path):
        print(f"Processing Documents from {file_path}")
        extractor = SGExtractor(file_path)
        content = extractor.extract_content()
        return [Document(text=content)]

    def ingest_documents(self):
        print("Ingesting Documents!")

        documents = self.process_documents(self.data)
        faiss_index = faiss.IndexFlatL2(self.dimension)
        vector_store = FaissVectorStore(faiss_index=faiss_index)
        text_splitter = SentenceSplitter(chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)

        pipeline = IngestionPipeline(
            transformations =[
                text_splitter
            ],
        vector_store=vector_store, 
        )

        nodes = pipeline.run(documents=documents)

        return nodes
        

    def retrieve(self,query):
        nodes = self.ingest_documents()
        vector_store_index = VectorStoreIndex(nodes,embed_model = self.embedding)
        retriever = vector_store_index.as_retriever(similarity_top_k=2)
        output = retriever.retrieve(query)

        return output

    def show_context(self,context):
        for i, c in enumerate(context):
            print(f"Context {i+1}:")
            print(c.text)
            print("\n")

    def answer(self,context,query):
        context_text = "\n".join(node.text for node in context)
        prompt = f"{context_text}\n\n{query}"
        return self.llm.complete(prompt)


class HuggingFaceQALLM():
    def __init__(self, model_name="distilbert/distilbert-base-cased-distilled-squad"):
        self.qa_pipeline = pipeline("question-answering", model=model_name)

    def complete(self, prompt):
        """Generate a response based on context"""
        context, question = prompt.split("\n\n", 1)
        response = self.qa_pipeline(question=question, context=context)
        return response["answer"]

class GeminiLLM:
    def __init__(self, model_name="gemini-2.0-flash"):

        self.api_key = os.getenv("GEMINI_API_KEY")  
        self.client = genai.Client(api_key=self.api_key)
        self.model = model_name
        

    def complete(self,prompt):
        """Generate a response using Google Gemini API."""

        response = self.client.models.generate_content(
        model=self.model ,contents=prompt
        )

        return response.text if response else "No response from Gemini."

if __name__ == "__main__":
    data_path = "test_data/test.pdf"

    llm_model = GeminiLLM()
    embedding_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-mpnet-base-v2")

    rag = SGRagModel(llm_model, embedding_model, data_path)

    test_query = "What are the financial functions?"
    context = rag.retrieve(test_query)

    context_display = rag.show_context(context)
    response = rag.answer(context,test_query)
    print(response)