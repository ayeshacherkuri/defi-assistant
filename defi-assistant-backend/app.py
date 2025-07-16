from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message', '')

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [
            {"role": "system", "content": "You are a DeFi advisor AI. Suggest decentralized finance strategies, staking options, and portfolio ideas."},
            {"role": "user", "content": user_input}
        ]
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        result = response.json()
        reply = result['choices'][0]['message']['content']
        return jsonify({'reply': reply})

    except Exception as e:
        print("Error talking to AI:", e)
        return jsonify({'reply': "Sorry, failed to connect to AI."}), 500

if __name__ == '__main__':
    app.run(debug=True)
