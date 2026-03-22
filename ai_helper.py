import streamlit as st
from groq import Groq
 

 

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

def get_ai_suggestion(log_message):
    try:
        prompt = f"""
        You are a system log analysis expert.

        Analyze this log and provide:
        1. Issue
        2. Fix

        Keep answer short (2-3 lines).

        Log:
        {log_message}
        """

        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": "You analyze logs and suggest fixes."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
        )

        return response.choices[0].message.content.strip()

    except Exception:
        return "AI suggestion unavailable"