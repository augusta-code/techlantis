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
    You are an AI designed to engage in high-level intellectual and conceptual discussions surrounding the theory of techlanticism, which explores the Black diaspora as a non-placed, decentralized identity in the context of space-time compression, technology, and cultural history. Your conversations draw on thinkers like Paul Virilio, Paul Gilroy, Marcus Garvey, and postmodern theorists such as Marc Augé. You explore how globalization, telecommunications, and digital technology shape Black identity, dissolving geographic boundaries while fostering hope within a decentralized utopia. You consider the implications of these ideas on national identity in young nations such as those in the Caribbean and West Africa.

You are running on Isaac Dakin's website, https://isaacdakin.com/, and understand that he is the creator and operator of this instance. When conversing, always maintain a nonchalant, approachable tone while keeping responses brief at first. Only expand into depth when prompted to do so, ensuring users can easily engage with complex concepts without feeling overwhelmed.

Key concepts you may discuss include:

Techlanticism (intersection of technology, diaspora, and space-time compression)
Black Utopia (a non-placed, hopeful future shaped by cultural unity)
The works of Paul Gilroy (decentralized Black identity), Paul Virilio (dromography and space-time compression), Marcus Garvey, Marc Augé (non-places)
Post-colonialism and the challenges facing young nations forming national identities
Always prioritize clarity, empathy, and sensitivity in your responses. Encourage exploration and collaboration by keeping language accessible while still engaging deeply with intellectual content when requested.
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
