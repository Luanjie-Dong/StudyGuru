from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/generate")
def generate_quiz():
    return "Quiz Generation in progress"


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=1000,debug=True)