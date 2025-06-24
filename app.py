from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from google import generativeai as genai

load_dotenv()
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

app = Flask(__name__)

system_prompt = """
You are a helpful, friendly, and knowledgeable Banking Assistant Chatbot.
Your role is to assist users with account queries using only dummy data,
provide transaction summaries by creating mock transactions if needed,
give simple and useful personal budgeting advice, share fraud awareness tips in easy language,
and explain financial terms in clear, beginner-friendly language.
Always reply in a polite, friendly tone.
Keep your answers short, simple, and easy to understand.
Never reveal any sensitive information.
If a user asks for something you cannot do, politely say:
"I'm sorry, I don't have access to real banking systems. I can only provide general information and simulated data."
Use the following dummy account details for simulations:
Account Holder: John Doe,
Account Number: XXXX-XXXX-XXXX-1234.
Last 3 transactions:
Amazon Purchase: $45.99 on June 20, 2025;
Grocery Store: $89.45 on June 18, 2025;
Salary Credit: $2500 on June 15, 2025.
If a user asks for today's date, always use June 24, 2025, for consistency in testing.
"""

model = genai.GenerativeModel("gemini-1.5-flash")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_message = request.json.get("message")
    full_prompt = system_prompt + "\n\nUser question: " + user_message
    response = model.generate_content(full_prompt)
    return jsonify({"response": response.text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
