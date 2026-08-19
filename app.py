"""
AI Chatbot - Flask Web App using Google Gemini API
----------------------------------------------------
Setup:
1. Install requirements:
       pip install -r requirements.txt

2. Get a free API key: https://aistudio.google.com/apikey

3. Paste your key into API_KEY below (or set it as an environment
   variable named GEMINI_API_KEY - recommended for deployment).

4. Run locally:
       python app.py
   Then open http://127.0.0.1:5000 in your browser.

5. To deploy (e.g. on Render) - see deploy_steps.txt
"""

import os
from flask import Flask, request, jsonify, render_template
import google.generativeai as genai

# ------------------- CONFIG -------------------
# Prefer environment variable (used when deployed); falls back to placeholder for local testing
API_KEY = os.environ.get("GEMINI_API_KEY", "PASTE_YOUR_GEMINI_API_KEY_HERE")
MODEL_NAME = "gemini-2.5-flash"

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel(MODEL_NAME)
# ------------------------------------------------

app = Flask(__name__)

# Store chat sessions per browser session (simple in-memory version)
chat_sessions = {}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "").strip()
    session_id = data.get("session_id", "default")

    if not user_message:
        return jsonify({"reply": "Please type something."})

    if session_id not in chat_sessions:
        chat_sessions[session_id] = model.start_chat(history=[])

    try:
        response = chat_sessions[session_id].send_message(user_message)
        reply = response.text.strip()
    except Exception as e:
        reply = f"Error: {e}"

    return jsonify({"reply": reply})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)