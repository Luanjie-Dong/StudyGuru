from rag import SGRagModel 
import os
from dotenv import load_dotenv
from google import genai
import random
import json
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np




load_dotenv()



class StudyGuru(SGRagModel):
    def __init__(self, model_name: str ="gemini-2.0-flash" , num : int = 0,embedding_model: str = None, collection: str = "",title_model: str=""):

        super().__init__(embedding_model, collection , title_model)

        self.api_key = os.getenv("GEMINI_API_KEY")  
        self.client = genai.Client(api_key=self.api_key)
        self.model = model_name
        self.num = num
        self.topic_generation = TopicSelector()
        
    
    def get_context(self,selected_topics,modules):
        
        content = ""
        for topic in selected_topics:
            query = f"What are the contents of {topic}"
            context = super().retrieve(query,modules)

            for i, c in enumerate(context):
                content += c['text'] +f" extracted from page: {c['page']}"+ "\n\n"
                print(f"Context {i+1}:",flush=True)
                print(c['text'],flush=True)
                print("\n",flush=True)

        return content

    def generate(self, topics , modules):
        selected_topics = self.topic_generation.diversity_based_selection(topics)
        print("Selected topics are: ",selected_topics,flush=True)

        selected_content = self.get_context(selected_topics,modules)

        generation_prompt = (
            f"Generate {self.num} questions based on the following context: {selected_content}\n\n"
            f"Create a mix of MCQ, Multi-select, and short open-ended questions, each with their answers. "
            f"Return the output as a JSON array where each question is an object with the following structure:\n"
            f"```json\n"
            f"{{\n"
            f"  \"question_no\": <integer>,\n"
            f"  \"question_type\": \"<MCQ|Multi-select|Short open-ended>\",\n"
            f"  \"question\": \"<text of the question>\",\n"
            f"  \"options\": [\"<option1>\", \"<option2>\", ...] (omit or empty array if not applicable),\n"
            f"  \"answer\": \"<correct answer(s) as a string or array if multi-select>\"\n"
            f"  \"hint\": \"<hint for the answer>\"\n"
            f"}}\n"
            f"```\n"
            f"Ensure the response is valid JSON and contains exactly {self.num} questions."
        )


        response = self.client.models.generate_content(
            model=self.model, contents=generation_prompt
        )


        if not response or not response.text:
            return "No response from Gemini."

        try:
            json_text = response.text.strip()
            if json_text.startswith("```json") and json_text.endswith("```"):
                json_text = json_text[7:-3].strip()  
            questions = json.loads(json_text)
            return questions 
        except json.JSONDecodeError as e:
            return f"Error parsing JSON response: {str(e)}\nRaw response: {response.text}"

        
    
# For local testing
def save_topics(topics,file):
    topics_path = data_path.split("/")[1]  

    save_dir = "test_data"
    os.makedirs(save_dir, exist_ok=True)

    file_path = os.path.join(save_dir, f"{topics_path}.txt")

    with open(file_path, "w") as file:
        for topic in topics:
            file.write(f"{topic}\n")

    print(f"Topics saved to {file_path}")

# For local testing
def load_topic(path):
    topics = []

    with open(path, 'r') as file:
        for topic in file:
            topic = topic.strip()  
            if topic:  
                topics.append(topic)

    return topics  

class TopicSelector:
    def __init__(self,num_topics: int = 5, embedder: str ="sentence-transformers/all-MiniLM-L6-v2"):
        self.num_topics = num_topics  
        self.embedder = SentenceTransformer(embedder) 

    def diversity_based_selection(self, topics, target=None, threshold=0.5):
        if not topics:
            return []

        topic_embeddings = self.embedder.encode(topics, convert_to_tensor=False)

        if target:
            target_embedding = self.embedder.encode([target], convert_to_tensor=False)[0]
            similarities = cosine_similarity([target_embedding], topic_embeddings).flatten()
            filtered_indices = [i for i, sim in enumerate(similarities) if sim >= threshold]
            filtered_topics = [topics[i] for i in filtered_indices]
            filtered_embeddings = topic_embeddings[filtered_indices]
        else:
            filtered_topics = topics
            filtered_embeddings = topic_embeddings

        if not filtered_topics:
            return []
        
        selected_indices = []
        remaining_indices = list(range(len(filtered_topics)))

        while len(selected_indices) < self.num_topics and remaining_indices:
            if not selected_indices:
                next_index = remaining_indices[0]
            else:
                selected_vectors = filtered_embeddings[selected_indices]
                similarities = cosine_similarity(selected_vectors, filtered_embeddings).mean(axis=0)
                next_index = remaining_indices[np.argmin(similarities[remaining_indices])]

            selected_indices.append(next_index)
            remaining_indices.remove(next_index)

        return [filtered_topics[i] for i in selected_indices]
    

if __name__ == "__main__":
    data_path = "test_data/test.pdf"
    hugging_llm  = "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B"
    hugging_embedding = "sentence-transformers/all-MiniLM-L6-v2"
    gemini_model = "gemini-2.0-flash"
    collection = "test-module"


    model = StudyGuru(num=5,embedding_model=hugging_embedding,collection=collection)

    topic_path = "test_data/test.pdf.txt"

    if os.path.exists(topic_path):
        print(f"Loading topics from: {topic_path}")
        topics = load_topic(topic_path)  
    else:
        print("File not found. Ingesting documents...")
        topics = model.ingest_documents()  
        save_topics(topics, topic_path) 
        print(f"Topics saved to: {topic_path}")

    questions = model.generate(topics)


    for question in questions:
        print(f"Question {question['question_number']} ({question['type']}): {question['question']}")

        for idx, option in enumerate(question['options']):
            print("{:>4}: {}".format(idx, option))
        
        print(f"Answer: {question['answer']}")
        print(f"Extracted content from: page {question['page']} \n")
        print(f"Context: {question['context']} \n")



    


    

    




