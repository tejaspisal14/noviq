import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
print("API KEY FOUND:", os.getenv("GEMINI_API_KEY"))


client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def analyze_novelty(user_idea, patents):

    patent_text = ""

    for patent in patents:
        patent_text += f"""
Title: {patent['title']}
Abstract: {patent['abstract']}

"""

    prompt = f"""
You are an expert patent analyst.

User Idea:
{user_idea}

Retrieved Similar Patents:
{patent_text}

Provide:

1. Major overlaps with existing patents
2. Potential novel aspects
3. Novelty risk (Low/Medium/High)

Keep the response concise and professional.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text