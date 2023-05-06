from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import openai
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
allowed_origins = ["http://localhost:5173", "https://writelikenative.com"]
cors = CORS(app, resources={r"/api/*": {"origins": allowed_origins}})
# CORS(app)

app.config['CORS_HEADERS'] = 'Content-Type'

# Load the OpenAI API key from an environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/api/improve_text", methods=["POST"])
def improve_text():
    data = request.get_json()
    selected_prompt = data.get('selectedPrompt')
    input_text = data.get('inputText')

    prompts = {
        "correct": "I want you to act as a spelling corrector and grammar improver. I will send you a word, sentence, or paragraph, and you’ll send me the result. Reply only with the improved text and nothing else, do not write explanations.",
        "teammate": "I want you to act as an editor, spelling corrector, and grammar improver. I’m writing a message to my teammate in a messaging app or email. I want to sound like a native speaker but keep it simple, natural, and conversational. I will send you a sentence or paragraph, and you’ll send me the result. Reply only with the improved text and nothing else, do not write explanations.",
        "blog": "I want you to act as an editor, spelling corrector, and grammar improver. I’m writing a blog post for Substack or an article for Medium. I want to sound more like a native speaker but keep it simple and avoid words and phrases that may sound too pretentious. I will send you a sentence or paragraph, and you’ll send me the result. Reply only with the improved text and nothing else, do not write explanations.",
    }

    messages = [
        {"role": "system", "content": prompts[selected_prompt]},
        {"role": "user", "content": input_text},
    ]

    payload = {
        "model": "gpt-3.5-turbo",
        "messages": messages,
    }

    try:
        response = openai.ChatCompletion.create(**payload)
        return jsonify(response)
    except Exception as e:
        print(e)
        return jsonify({"error": "Unable to fetch results"}), 500

if __name__ == '__main__':
    if os.getenv("FLASK_ENV") == "development":
        app.run(debug=True)
    else:
        app.run(debug=False)
