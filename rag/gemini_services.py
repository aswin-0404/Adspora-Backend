import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model=genai.GenerativeModel("gemini-2.5-flash-lite")
def generate_ai_replay(query,spaces):
    if not spaces:
        return "Iam sorry i cant find a space as per your request"
    
    context="\n".join([
        f"{s.title} in {s.location}, Rs{s.price}"
        for s in spaces
    ])

    prompt=f"""
User query:{query}

Available advertisement spaces:
{context}

Instructions:
- Give a short, clear answer.
- Do NOT write long explanations.
- Just summarize matching spaces in 2–3 sentences.
"""
    
    response=model.generate_content(prompt)

    return response.text