import os
import google.generativeai as genai 
from flask import Flask, request, jsonify
from flask_cors import CORS 
from dotenv import load_dotenv

# Loading environment variables from .env
load_dotenv()

# === CONFIGURATION ===
# Creating Flask app instance
app = Flask(__name__)
# Enabling CORS
CORS(app)

# Configure Gemini API with API key
try: 
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
except KeyError:
    print("Error: Gemini API Key not found. Set the key in your .env file.")
    exit()

# === PROMPT ENGINEERING ===
# Inserting the user's concept 
def gemini_prompt(concept):
    return f"""
**SYSTEM PROMPT:**
You are a "Physics Pal", a friendly and ingenious physics tutor AI.
Your goal is to explain complex physics concepts in a simple, engaging,
and comprehesive way. When a user provides you with a concept, you must 
generate a complete learning module for that concept.

**USER REQUESTED CONCEPT:**
{concept}

**YOUR TASK:**
Generate a detailed explanation for the concept "{concept}". Structure 
your response using the following format exactly. User Markdown for formatting.

### Simple Explanation 
Start with a simple, intuite, and relevant analogy or a real-world example to
explain the core idea of "{concept}". If possible use current events or trending 
pop culture moments. Avoid jargon as much as possible for this first section.

### The Core Equations and Why
List the primary equations associated with "{concept}". For each equation:
1. Present the equation clearly
2. Define every variable in the equation (e.g., V = voltage, I = current, R =
resistance). 
3. Explain **why** this equation is used and what physical relationship it 
represents in the context of "{concept}". 

## Manipulating the equaiton
Show the user how the equation can be rearranged to solve for different variables.
For example, if you presented V=I/R, show how to solve for I=VR. Explain the particle 
reason for doing this (e.g., "If you know the voltage and resistance values, you can
solve for the current value). 


### Youtube Videos for Further Learning
Provide 3 links to high-quiality, reputable youtube bideos that explain "{concept}". Choose videos
from sources like Khan Academy, Physics Girl, The Organic Chemistry Tutor, SmarterEveryDay, or
university channels.
* **Video 1:** [Link] - A brief description of what the video covers.
* **Video 2:** [Link] - A brief description of what the video covers.
* **Video 3:** [Link] - A brief description of what the video covers.

### Pop Quiz!
Create a 5-question multiple-choice quiz to test the user's understanding. For each question, provide
4 options (A, B, C, D) and identify the correct answer. 

**Question 1:** [Question Text]
- (A) [Option]
- (B) [Option]
- (C) [Option]
- (D) [Option]
- **Correct Answer:[Letter]

**Question 2:** ...
**Question 3:** ...
**Question 4:** ...
**Question 5:** ...

### Quiz Answer Explanation
Provide a detailed explanation for each quiz question's answer. Explain why the correct answer is right
and why the other options are wrong. This is crucial for learning

**Explanation for Q1:** [Detailed Explanation]

**Explanation for Q2:** [Detailed Explanation]

**Explanation for Q3:** [Detailed Explanation]

**Explanation for Q4:** [Detailed Explanation]

**Explanation for Q5:** [Detailed Explanation]
"""

# === API ROUTE ===
# Endpoint that frontend will call 
# Listens for POST requests at the URL '/api/explain
@app.route('/api/explain', methods=['POST'])
def explain_concept():
    try:
        # First, get the data sent from the frontend 
        data = request.get_json()
        concept = data.get('concept')

        # --- DEBUGGING STEP: Print what you received ---
        print(f"Received data: {data}") 

        # 2. Check if data is valid and contains 'concept'
        if not data or 'concept' not in data:
            print("Error: Invalid or missing JSON payload.")
            return jsonify({'error': 'Request must be a JSON with a "concept" key'}), 400

        concept = data['concept'].strip() # Use .strip() to remove whitespace

        # 3. Check if the concept is empty after stripping whitespace
        if not concept:
            print("Error: 'concept' key is empty.")
            return jsonify({'error': 'Concept cannot be empty'}), 400
            
        print(f"Received concept: '{concept}'") # --- More Debugging ---

        # if not concept: 
        #     # Return error if 'concept' is not provided in request
        #     return jsonify({'error': 'Concept is required'}), 400
        
        # Second, initialize the gemini model
        model = genai.GenerativeModel('gemini-1.5-flash-latest')

        # Third, generate the content using the prompt
        prompt = gemini_prompt(concept)
        response = model.generate_content(prompt)

        # Finally, send the genrated text back to the frontend as JSON
        return jsonify({'explanation': response.text})
    except Exception as e:
        print(f"An error occured: {e}")
        # Return generic error video 
        return jsonify({'error': 'An internal server error ocurred'}), 500
    
# === RUNNING APP ===
if __name__ == '__main__':
    app.run(debug=True, port=5000)

