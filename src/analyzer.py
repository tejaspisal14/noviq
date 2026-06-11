import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def analyze_novelty(user_idea, patents):

    patent_text = ""

    for patent in patents[:5]:

        patent_text += f"""
Title: {patent['title']}
Abstract: {patent['abstract']}

"""

    prompt = f"""
You are a senior patent examiner.

Analyze the invention against the retrieved patents.

User Idea:
{user_idea}

Retrieved Patents:
{patent_text}

Return ONLY valid JSON in this format:

{{
    "novelty_score": 0,
    "risk_level": "",
    "overlaps": [],
    "novel_aspects": [],
    "analysis": ""
}}

Instructions:

1. novelty_score must be between 0 and 100
2. High novelty = 80-100
3. Medium novelty = 50-79
4. Low novelty = 0-49
5. Evaluate the uniqueness of the COMBINATION of features
6. Do not return markdown
7. Do not return explanations outside JSON
"""

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        text = response.text.strip()

        if text.startswith("```json"):

            text = text.replace(
                "```json",
                ""
            )

            text = text.replace(
                "```",
                ""
            )

            text = text.strip()

        return json.loads(text)

    except Exception as e:

        return {
            "novelty_score": 50,
            "risk_level": "Unknown",
            "overlaps": [],
            "novel_aspects": [],
            "analysis": f"Analysis unavailable: {str(e)}"
        }