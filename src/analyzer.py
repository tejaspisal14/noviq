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

    for patent in patents[:10]:

        patent_text += f"""
Patent Title: {patent.get('title', '')}

Patent ID: {patent.get('patent_id', '')}

Similarity Score: {patent.get('similarity', 0)}%

Patent Abstract:
{patent.get('abstract', '')}

Patent URL:
{patent.get('url', '')}

----------------------------------------
"""

    prompt = f"""
You are a senior patent examiner and IP analyst.

Evaluate the invention against the retrieved patents.

USER INVENTION:
{user_idea}

RETRIEVED PATENTS:
{patent_text}

Your task:

1. Assess novelty against prior art.
2. Identify major overlaps.
3. Identify novel contributions.
4. Identify the 3 closest prior-art patents.
5. Extract the key technical contribution of each.
6. Explain how the user invention differs.
7. Estimate confidence in your assessment.
8. Estimate patentability risk.

Return ONLY valid JSON.

{{
    "novelty_score": 0,
    "confidence": 0,
    "risk_level": "",
    "overlaps": [],
    "novel_aspects": [],
    "closest_patents": [
        {{
            "title": "",
            "patent_id": "",
            "similarity": "",
            "key_claim": "",
            "difference": "",
            "url": ""
        }}
    ],
    "analysis": ""
}}

SCORING GUIDELINES:

90-100:
Breakthrough concept with little overlap.

75-89:
Strong novelty with limited overlap.

50-74:
Moderate novelty with several related patents.

25-49:
Heavy overlap with prior art.

0-24:
Very little novelty.

IMPORTANT:

- Consider the COMBINATION of features.
- Do not penalize merely because patents exist in the same domain.
- Focus on technical differentiation.
- Return JSON ONLY.
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

        result = json.loads(text)

        if "confidence" not in result:
            result["confidence"] = 70

        if "closest_patents" not in result:
            result["closest_patents"] = []

        return result

    except Exception as e:

        return {
            "novelty_score": 50,
            "confidence": 50,
            "risk_level": "Unknown",
            "overlaps": [],
            "novel_aspects": [],
            "closest_patents": [],
            "analysis": f"Analysis unavailable: {str(e)}"
        }