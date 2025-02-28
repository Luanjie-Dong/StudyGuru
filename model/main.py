from flask import Flask, request, jsonify
from StudyGuru import StudyGuru
from flask_cors import CORS  

app = Flask(__name__)
CORS(app)

@app.route("/generate",methods=['POST'])
def generate_quiz():
    
    data = request.json
    if not data:
            return jsonify({"error": "No JSON data provided"}), 400
    
    challenge_type = data.get('type',"DAILY") # str
    files = data.get('modules',[]) # list
    course = data.get('course_id',"") #str

    num_questions = challenge_questions(challenge_type)
    questions = generate_questions(num_questions,course,files)


    return questions


    
def generate_questions(num,module,files):

    hugging_embedding = "sentence-transformers/all-MiniLM-L6-v2"
    title_model = "./title_model"
    model = StudyGuru(num=num,embedding_model=hugging_embedding,collection=module,title_model=title_model)

    all_topics = []
    for file in files:
        topics = model.ingest_documents(file)

        if topics:
            print("Adding topics")
            all_topics.extend(topics)

    if not all_topics:
        print("No topics found in the provided files. Cannot generate questions.")
        return None

    # all_topics = [' • Contributions / MonthMonthly Loan Installment', '(n.d.) The role of the store: Merging digital and physical for seamless', 'ESSENCIA could capitalize on their “Pivot to Tech” initiative', 'Singapore & MalaysiaTARGETS Proposal for ESSEN', '(McKinsey & Company, 2023)Appare']

    print(f"Generating {num} questions from {len(all_topics)} topics...")
    questions = model.generate(all_topics)

    return questions



def challenge_questions(challenge_type):
    if challenge_type == "DAILY":
        return 5
    else:
        return 20

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)