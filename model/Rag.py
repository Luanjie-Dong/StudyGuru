from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import  Document 
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.text_splitter import SentenceSplitter
from pinecone import Pinecone, ServerlessSpec
import pinecone


from extractor import SGExtractor
import os
from dotenv import load_dotenv
import hashlib
from transformers import pipeline , AutoTokenizer
from sentence_transformers import SentenceTransformer
import time
from transformers import pipeline

load_dotenv()

# StudyGuru Rag Model = SGRagModel
class SGRagModel:
    def __init__(self, embedding_model, module):
        self.module = module
        
        self.embedding_model = SentenceTransformer(embedding_model)
        self.dimension = self.embedding_model.get_sentence_embedding_dimension()
        
        self.chunk_size = 512
        self.chunk_overlap = 100
        self.pinecone_api_key = os.getenv("PINECONE_API_KEY") 
        self.pinecone_env = os.getenv("PINECONE_ENVIRONMENT")  
        self.pinecone_index_name = f"{module}-index" 
        self.pc = Pinecone(api_key=self.pinecone_api_key)

        if self.pinecone_index_name not in self.pc.list_indexes().names():
            self.pc.create_index(
                name=self.pinecone_index_name,
                dimension=self.dimension, 
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region="us-east-1")  
            )
        
        self.pinecone_index = self.pc.Index(self.pinecone_index_name)
        
        self.title_extractor = pipeline("summarization", model="Falconsai/text_summarization")

    
        
    def process_documents(self,file_path):
        print(f"Processing Documents from {file_path}")
        extractor = SGExtractor(file_path)
        content = extractor.extract_content()

        page_documents = [
            Document(
                text= " ".join(content[chunk]),
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


    def ingest_documents(self,data):
        
        print(f"Checking if this {data} has already been processed...")
        
        query_result = self.pinecone_index.query(
            vector=[0] * 384,  
            filter={"file_name": {"$eq": data}},
            top_k=1,
            include_metadata=True
        )
        if query_result['matches']:
            print(f"File '{data}' already exists in Pinecone. Skipping processing.")
            return

        print("No existing records for this file. Processing and storing documents...")

        documents = self.process_documents(data)
        text_splitter = SentenceSplitter(chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)

        pipeline = IngestionPipeline(transformations=[text_splitter])
        nodes = pipeline.run(documents=documents)

        chunk_titles = []

        for node in nodes:
            chunk_title = self.contextual_chunking(node.text, node.metadata)
            chunk_titles.append(chunk_title)

            embedding = self.embedding_model.encode(node.text).tolist()

            doc_id = self.generate_id(node.text, node.metadata["file_name"], node.metadata["page"])

            metadata = {
                "file_name": node.metadata["file_name"],
                "page": node.metadata["page"],
                "chunk_title": chunk_title,
                "text": node.text
            }

            self.pinecone_index.upsert([(doc_id, embedding, metadata)])
        
        print(f"File '{self.data}' successfully ingested into Pinecone.")
        return chunk_titles

    def generate_id(self, text, file_name, page):
        base_id = f"{file_name}_page_{page}"
        text_hash = hashlib.md5(text.encode()).hexdigest()
        return f"{base_id}_{text_hash}"
        

    def retrieve(self, query):
        query_embedding = self.embedding_model.encode(query).tolist()

        results = self.pinecone_index.query(
            vector=query_embedding,
            top_k=2,
            include_metadata=True
        )

        formatted_results = []
        for match in results['matches']:
            formatted_results.append({
                "id": match['id'],
                "score": match['score'],
                "metadata": match['metadata'],
                "text": "Title: "+match['metadata'].get("chunk_title", "") + "\n\n" + match['metadata'].get("text", ""),
                "page": match['metadata'].get("page","")
            })

        return formatted_results

    def show_context(self,context):
        for i, c in enumerate(context):
            print(f"Context {i+1}:")
            print(c['text'])
            print(c['page'])
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


    

if __name__ == "__main__":
    data_path = "test_data/test.pdf"
    hugging_llm  = "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B"
    embedding_model = "sentence-transformers/all-MiniLM-L6-v2"
    gemini_model = "gemini-2.0-flash"
    collection = "test-module"


    #embedding_model, data, module
    rag = SGRagModel(embedding_model, collection)
    topics = rag.ingest_documents()

    if topics:
        save_topics(topics,data_path)



    test_query = "What are the regression measurements?"
    context = rag.retrieve(test_query)

    context_display = rag.show_context(context)
    print(context_display)
    # print(topics)

    del rag

    