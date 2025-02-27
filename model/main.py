from flask import Flask, request, jsonify
from StudyGuru import StudyGuru

app = Flask(__name__)

@app.route("/generate",methods='POST')
def generate_quiz():

    challenge_type = ""
    files = []
    course = ""

    num_questions = challenge_questions(challenge_type)
    questions = generate_questions(num_questions,course,files)

    

    

    return questions


def generate_questions(num,module,files):

    hugging_embedding = "sentence-transformers/all-MiniLM-L6-v2"
    model = StudyGuru(num=num,embedding_model=hugging_embedding,collection=module)

    all_topics = []
    for file in files:
        topics = model.ingest_documents(file)
        all_topics.extend(topics)

    questions = model.generate(all_topics)

    return questions



def challenge_questions(challenge_type):
    if challenge_type == "Daily":
        return 5
    else:
        return 20

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=1000,debug=True)