LangSmith AI Observability Demo - Code Review Assistant

Prerequisites

1. Python Environment
Python 3.8 or higher
pip package manager

2. API Keys Required
Google AI API Key: Access to Gemini AI model
LangSmith API Key: For observability features

3. LangSmith Account
Create account at https://smith.langchain.com/
Generate API key from account settings

Installation

Step 1: Install Dependencies

    pip install langchain
    pip install langchain-google-genai
    pip install langsmith
    pip install python-dotenv

Step 2: Set Up Environment Variables

Create a .env file in the same directory as your script:

    GOOGLE_API_KEY=your_google_api_key_here
    LANGSMITH_API_KEY=your_langsmith_api_key_here


Getting API Keys

Google AI API Key

Visit Google AI Studio
Sign in with your Google account
Click "Create API Key"
Copy the generated key

LangSmith API Key

Sign up at LangSmith
Go to Settings → API Keys
Click "Create API Key"
Copy the generated key

Running the Demo

Basic Execution
    python code_review_demo.py


The demo includes 5 comprehensive test cases:
1. Python Security Vulnerability

Code: SQL injection vulnerable login function
Focus: Security analysis capabilities
Expected: Detection of SQL injection vulnerability

2. JavaScript Performance Issue

Code: O(n²) nested loop algorithm
Focus: Performance optimization detection
Expected: Identification of algorithmic inefficiency

3. Well-Written Go Code

Code: Proper context handling with timeout
Focus: Recognition of best practices
Expected: Positive review with minor suggestions

4. Validation Error - Empty Code

Code: Empty string
Focus: Input validation handling
Expected: Validation error with clear message

5. Validation Error - Unsupported Language

Code: SQL query with unsupported language
Focus: Language validation
Expected: Unsupported language error

LangSmith Dashboard Access

After running the demo:
Visit https://smith.langchain.com/
Navigate to your project: code_review_demo
View traces, performance metrics, and analytics

---

UK Weather Predictor Streamlit App

This repository now includes a Streamlit app that predicts hourly London temperatures using historical Open-Meteo data.

Files for the Streamlit app:
- `app.py` — Streamlit application
- `requirements.txt` — App dependency list

Run locally:

    pip install -r requirements.txt
    streamlit run app.py

Deploy to Streamlit Cloud:
1. Push the repo to GitHub.
2. Go to https://share.streamlit.io/.
3. Select the repo, branch `main`, and the path `app.py`.
4. Deploy and use the public URL.
