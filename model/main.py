from flask import Flask, request, jsonify
from StudyGuru import StudyGuru as sguru , StudyGuruReviewer as sgurureview
from flask_cors import CORS  
from rag import SGRagModel as ragmodel
from endpoints import get_topics , get_quizzes
import json

app = Flask(__name__)
CORS(app)

@app.route("/generate_question",methods=['POST'])
def generate_quiz():
    
    data = request.json
    if not data:
            return jsonify({"error": "No JSON data provided"}), 400
    
    challenge_type = data.get('type',"DAILY") #str
    modules = data.get('modules',[])          #list
    course = data.get('course_id',"")         #str
    challenge_id = data.get("challenge_id","")

    try:
        num_questions = challenge_questions(challenge_type)
        questions = generate_questions(num_questions,course,modules)
    except:
        return [], 400
    return format_questions(questions,challenge_id)


@app.route("/generate_topics",methods=['POST'])
def generate_topics():

    data = request.get_json()

    if not data:
        return jsonify({"error": "No JSON data provided"}), 400
    
    hugging_embedding = "sentence-transformers/all-MiniLM-L6-v2"
    title_model = "./title_model"

    
    note_url = data.get('note_URL',"")
    module = data.get('module_id',"")
    course = data.get('course_id',"")

    if note_url == "" or module == "":
        return jsonify({"error": "Missing notes or module data"}), 400
    
    print("Generating topics for document...",flush=True)
    rag = ragmodel(hugging_embedding,course,title_model)

    
    attempts = 3
    while attempts > 0:
        try:
            topics = rag.ingest_documents(note_url,module)

            if topics and topics != "Processed":
                return topics
            
            if topics == "Processed":
                return "Topics already extracted"
                    
        except:
            print("No topics generated",flush=True)

        if attempts > 0:
            print(f"Retrying... ({attempts-1} attempts left) \n")
        
        attempts -= 1
    
    return []
    
     
@app.route("/review",methods=['POST'])
def review_quiz():
    
    data = request.json
    if not data:
            return jsonify({"error": "No JSON data provided"}), 400
    
    challenge_id = data.get("challenge_id","")

    try:
        print(f"Extracting questions from challenge {challenge_id} to review",flush=True)
        # questions = get_quizzes(challenge_id)
        questions = data["questions"]

        # Used to test
        # with open("test_data/questions.json", 'r', encoding='utf-8') as file:
        #     test = json.load(file)
        # questions = test

        if questions:
            print(f"Reviewing questions of {challenge_id}",flush=True)
            try:
                model = sgurureview()
                reviewed = model.review(questions)
                return reviewed
            except Exception as e:
                print(e)
        else:
            return f"No questions extracted from {challenge_id}", 400

    except:
        return [], 400
    
    
# Helper functions  
def generate_questions(num,course,modules):

    hugging_embedding = "sentence-transformers/all-MiniLM-L6-v2"
    title_model = "./title_model"
    model = sguru(num=num,embedding_model=hugging_embedding,collection=course,title_model=title_model)

    print("Extraction topics for question generation",flush=True)

    topics = []
    for module in modules:
        sub_topic = get_topics(module)
        topics.extend(sub_topic)

    if topics == []:
        return "Error in retrieving topics :/ Try again later"

    print(f"Generating {num} questions from {len(topics)} topics...",flush=True)

    try:
        questions = model.generate(topics,modules)
        return questions
    except:
        return "Error in generating questions :/"


def challenge_questions(challenge_type):
    if challenge_type == "DAILY":
        return 5
    else:
        return 20
    

def format_questions(questions,challenge_id):

    output = []
    for question in questions:

        question_detail = {
            "type": question['question_type'],
            "options":question['options'],
            "question": question["question"]
        }

        if question['question_type'] in ["MCQ", "SHORT_ANSWER"]:
            answer = [question["answer"]]
        else:
            answer = question["answer"]

        detail = {
            "challenge_id": challenge_id,
            "question_no": question['question_no'],
            "question_detail":question_detail,
            "input": "",
            "answer": answer,
            "explanation":"",
            "hint": question["hint"],
            "correct": None,
            "question_score":0,
        }

        output.append(detail)

    return output


# def review_quizzes(questions):

#     reviewed = []

#     return reviewed


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)