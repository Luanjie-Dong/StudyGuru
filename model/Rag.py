from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import  Document 
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.text_splitter import SentenceSplitter
from pinecone import Pinecone, ServerlessSpec


from extractor import SGExtractor
import os
from dotenv import load_dotenv
import hashlib
from sentence_transformers import SentenceTransformer
from transformers import  AutoTokenizer, AutoModelForSeq2SeqLM
import torch

load_dotenv()

# StudyGuru Rag Model = SGRagModel
class StudyGuruRag:
    def __init__(self, embedding_model: str = "", course = "", title_model_name: str = ""):
        self.course = course
        
        
        self.embedding_model = SentenceTransformer(embedding_model)
        self.dimension = self.embedding_model.get_sentence_embedding_dimension()
        
        self.chunk_size = 512
        self.chunk_overlap = 100
        self.pinecone_api_key = os.getenv("PINECONE_API_KEY") 
        self.pinecone_env = os.getenv("PINECONE_ENVIRONMENT")  
        self.pinecone_index_name = f"course-{self.course}" 
        self.pc = Pinecone(api_key=self.pinecone_api_key)

        if self.pinecone_index_name not in self.pc.list_indexes().names():
            self.pc.create_index(
                name=self.pinecone_index_name,
                dimension=self.dimension, 
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region="us-east-1")  
            )
        
        self.pinecone_index = self.pc.Index(self.pinecone_index_name)
        
        self.title_model_name = title_model_name
        self.title_model = AutoModelForSeq2SeqLM.from_pretrained(title_model_name)
        self.title_model_tokenizer= AutoTokenizer.from_pretrained(title_model_name)

    
    
    def process_documents(self,note,module):
        print(f"Processing Documents from {note}")
        extractor = SGExtractor(note)
        content = extractor.extract_content()

        page_documents = [
            Document(
                text= " ".join(content[chunk]),
                metadata={"note_name": note, "page": chunk,"module_name":module},
            )
            for chunk in content
        ]
        return page_documents
    
    def extract_title(self,text):

        inputs = self.title_model_tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
        device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
        self.title_model.to(device)
        inputs = {key: val.to(device) for key, val in inputs.items()}  

        with torch.no_grad():
            outputs = self.title_model.generate(**inputs,
            max_length=20,
            num_beams=4,
            no_repeat_ngram_size=3,
            early_stopping=True,
            )

        decoded_output = self.title_model_tokenizer.decode(outputs[0], skip_special_tokens=True)

        return decoded_output
    
    def contextual_chunking(self, chunk, chunk_info):

        print(f"Extracting title for: {chunk_info}")
        context = self.extract_title(chunk)

        print(f'Context found: {context} \n')

        return context


    def ingest_documents(self,note,module):
        
        print(f"Checking if this {note} has already been processed...")
        
        query_result = self.pinecone_index.query(
            vector=[0] * 384,  
            filter={"file_name": {"$eq": note}},
            top_k=1,
            include_metadata=True
        )
        if query_result['matches']:
            print(f"File '{note}' already exists in Pinecone. Skipping processing.")
            return "Processed"

        print("No existing records for this file. Processing and storing documents...")

        documents = self.process_documents(note,module)
        text_splitter = SentenceSplitter(chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)

        pipeline = IngestionPipeline(transformations=[text_splitter])
        nodes = pipeline.run(documents=documents)

        chunk_titles = []

        for node in nodes:
            chunk_title = self.contextual_chunking(node.text, node.metadata)
            chunk_titles.append(chunk_title)

            embedding = self.embedding_model.encode(node.text).tolist()

            doc_id = self.generate_id(node.text, node.metadata["note_name"], node.metadata["page"])

            metadata = {
                "file_name": node.metadata["note_name"],
                "page": node.metadata["page"],
                "module": node.metadata["module_name"],
                "chunk_title": chunk_title,
                "text": node.text
            }

            self.pinecone_index.upsert([(doc_id, embedding, metadata)])
        
        print(f"Files successfully ingested into Pinecone.")
        return chunk_titles

    def generate_id(self, text, file_name, page):
        base_id = f"{file_name}_page_{page}"
        text_hash = hashlib.md5(text.encode()).hexdigest()
        return f"{base_id}_{text_hash}"
        

    def retrieve(self, query , modules):
        query_embedding = self.embedding_model.encode(query).tolist()

        if modules:
            filter_condition = {
            "module": {"$in": modules}  
            }

        results = self.pinecone_index.query(
            vector=query_embedding,
            top_k=2,
            include_metadata=True,
            filter_condition = filter_condition
        )

        formatted_results = []
        for match in results['matches']:
            formatted_results.append({
                "id": match['id'],
                "score": match['score'],
                "metadata": match['metadata'],
                "text": "Title: "+match['metadata'].get("chunk_title", "") + "\n\n" + match['metadata'].get("text", "") ,
                "page": match['metadata'].get("page",""),
                "note_url": match['metadata'].get("file_name", "")
            })

        if not formatted_results:
            print(f"No results found for '{query}' in modules {modules}")
            print(f"Raw Pinecone results: {results}")

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

    