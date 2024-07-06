from flask import Flask, render_template, request
import os
from groq import Groq
import yfinance as yf
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Groq API Key setup
os.environ["GROQ_API_KEY"] = "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"
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))


def get_code_comments(theCode, model):

 messages = [
        {
            "role": "system",
            "content": "You are coding assistant that help comment code to simplify its understanding. "
        },
        {
            "role": "user",
        "content": f"CodeInsert:\n{str(theCode)}\n\n----\n\nPrompt:Explain this code use one line comments. Analyze to give a simpler undersatdning of this code given {theCode}. Place the comment 1 line above\n"
        },
    ]

 response = client.chat.completions.create(model=model, messages=messages,temperature=0.7, max_tokens=1200)
 response_content = response.choices[0].message.content

 return response_content

# Print the Groq Comment Analysis



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    theCode = request.form['theCode']
    groq_code_analysis = get_code_comments(theCode, "llama3-70b-8192")

    return render_template('result.html', theCode=theCode, groq_code_analysis=groq_code_analysis)

if __name__ == '__main__':
    app.run(debug=True)