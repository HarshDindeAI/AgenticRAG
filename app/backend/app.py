from flask import Flask, jsonify, request,  send_from_directory
from flask_cors import CORS
from agent import RAGagent
import os
import dotenv
dotenv.load_dotenv()
app = Flask(__name__, static_folder="static")
CORS(app)  # Enable CORS for all routes

@app.route("/")
def serve_index():
    return send_from_directory("static", "index.html")

@app.route("/<path:path>")
def serve_static(path):
    return send_from_directory("static", path)

@app.route("/init")
async def init():
    app.config['agent'] = RAGagent()
    return jsonify({"status": "success"}), 200

@app.route("/ask", methods=["POST"])
async def ask():
    question = request.json["question"]
    history = request.json["history"]
    print(history)
    agent: RAGagent = RAGagent()
    answer = await agent.kickoff(question, history)
    print(answer)
    return {"answer": str(answer)}, 200

if __name__ == "__main__":
    app.run()