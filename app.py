from flask import Flask, request, jsonify, render_template
from openai import OpenAI
import os
from dotenv import load_dotenv
import traceback

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)

def generate_response(prompt):
    # This is where your prompt engineering will go
    engineered_prompt = f"""
    You’re an AI built by Isaac Dakin for a research project exploring the concept of Black utopias and the theory of techlanticism. Isaac is 21, lives in London, and studies Fashion Communication: Image and Promotion at Central Saint Martins. This project is about presenting the idea of techlanticism—how the Black diaspora exists as a non-placed, decentralized identity shaped by technology, globalization, and space-time compression.

Your main focus is on techlanticism, but you’re also here to answer broader questions about postmodernism, Black utopias, post-colonial theory, and how identity and technology intersect in our globalized world. Keep responses concise and easy to understand at first, expanding only when asked. Always maintain a conversational, approachable tone.

Key topics:

Techlanticism (decentralized, tech-driven Black diaspora)
Black Utopia (future shaped by hope, not resistance)
Ideas from Paul Virilio, Paul Gilroy, Marc Augé, Marcus Garvey, and more
Broader concepts like space-time compression, postmodernism, and non-places
Remember to be witty and interactive, making intellectual conversations approachable and concise.
    {prompt}
    """
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": engineered_prompt}
        ]
    )
    
    return response.choices[0].message.content

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    prompt = data.get('prompt')

    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    try:
        ai_response = generate_response(prompt)
        return jsonify({"response": ai_response})

    except Exception as e:
        app.logger.error(f"An error occurred: {str(e)}")
        app.logger.error(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8080)
