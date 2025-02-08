from llama_index.core import VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.faiss import FaissVectorStore
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.text_splitter import SentenceSplitter
from llama_index.core import Document
from extractor import SGExtractor
import faiss
from transformers import pipeline



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

class HuggingFaceQALLM():
    def __init__(self, model_name="distilbert-base-cased-distilled-squad"):
        self.qa_pipeline = pipeline("question-answering", model=model_name)

    def complete(self, prompt):
        """Generate a response based on context"""
        context, question = prompt.split("\n", 1)
        response = self.qa_pipeline(question=question, context=context)
        return response["answer"]


if __name__ == "__main__":
    data_path = "test_data/test.pdf"

    llm = HuggingFaceQALLM()

    embedding = HuggingFaceEmbedding(model_name="sentence-transformers/all-mpnet-base-v2")

    rag = SGRagModel(llm, embedding, data_path)

    test_query = "What are the financial functions?"
    context = rag.retrieve(test_query)

    rag.show_context(context)
