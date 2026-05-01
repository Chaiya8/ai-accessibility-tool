import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
gemini = genai.GenerativeModel("gemini-2.5-flash")



# This is a simple wrapper around Gemini that checks if the output from the generator matches the requested mode and reading level.
#  If it doesn't, it provides feedback and a corrected version.
def verify_output(original_text: str, output_text: str, level: str, mode: str) -> dict:
    """
    Returns a dict:
    {
      "pass": True/False,
      "feedback": "...",
      "fixed_version": "..."
    }
    """

    prompt = f"""
You are a strict AI quality control agent.

TASK:
A generator AI produced an output for a user request.

MODE: {mode}
TARGET LEVEL: {level}

RULES:
- The output must match the requested mode.
- The output must match the target reading level.
- No advanced vocabulary if the level is low.
- Keep sentences short and clear.
- If the output fails rules, rewrite it correctly.

ORIGINAL TEXT:
{original_text}

GENERATOR OUTPUT:
{output_text}

Respond ONLY in JSON format like this:
{{
  "pass": true/false,
  "feedback": "...",
  "fixed_version": "..."
}}
"""
    response = gemini.generate_content(prompt)
    text = response.text.strip()


    # If the output is wrapped in code blocks, extract the JSON inside
    if text.startswith("```"):
        text = text.split("```")[1].strip()
        if text.startswith("json"):
            text = text[4:].strip()

    import json
    return json.loads(text)