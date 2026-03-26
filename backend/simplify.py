import json
import os
import google.generativeai as genai
import streamlit as st
from transformers import T5ForConditionalGeneration, T5Tokenizer

# ── Model setup ───────────────────────────────────────────────────────────────
model_name = "google/flan-t5-base"

print("Loading model...")
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
gemini = genai.GenerativeModel("gemini-1.5-flash")

# ── File structure setup (matches diagram) ────────────────────────────────────
os.makedirs("project/inputs", exist_ok=True)
os.makedirs("project/simplified", exist_ok=True)
os.makedirs("project/responses", exist_ok=True)


# ── Core generation helper (Flan-T5) ─────────────────────────────────────────
def generate(prompt: str, max_length=250) -> str:
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True)
    outputs = model.generate(**inputs, max_length=max_length, temperature=0.6, num_beams=4)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)


# ── Simplify Agent (Flan-T5) ──────────────────────────────────────────────────
GRADE_RULES = {
    "3rd grade": (
        "Use ONLY simple everyday words. No sentence may be longer than 8–10 words. "
        "Explain ideas slowly and clearly. Remove advanced vocabulary. "
        "If a word is hard, replace it with an easy word a child would know. "
        "Pretend you are teaching a 9-year-old who is still learning English."
    ),
    "5th grade": (
        "Use simple language. Sentences must be 10–12 words. "
        "Use examples to explain ideas. Avoid complex or academic vocabulary."
    ),
    "8th grade": (
        "Use clear middle-school language. Keep sentences under 14 words. "
        "Explain concepts with simple logic but include some detail."
    ),
    "high school": (
        "Use clear, academic English appropriate for high school. "
        "You may use mild technical terms but explain them. Sentences should be 14–18 words."
    ),
    "college": (
        "Use formal, academic English. You may use technical terms but define them clearly. "
        "Focus on accuracy and clarity."
    ),
    "Explain like I'm 5": (
        "Explain this idea to a 5-year-old child. Use extremely simple words. "
        "Use short sentences (6–8 words). Use friendly, gentle examples."
    ),
}

def simplify_agent(text: str, level: str) -> str:
    """Flan-T5 agent — simplifies text to the target reading level."""
    constraints = GRADE_RULES.get(level, "")
    prompt = (
        f"Simplify the text using these rules:\n{constraints}\n\n"
        f"Text:\n{text}\n\n"
        f"Simplified ({level} version):"
    )
    return generate(prompt)


# ── Manager Agent (Gemini) ────────────────────────────────────────────────────
def manager_evaluate(original: str, simplified: str, level: str) -> dict:
    """
    Manager is Gemini — reviews the Flan-T5 output and decides to approve or retry.
    Returns {"decision": "approve"} or {"decision": "retry", "feedback": "reason"}
    """
    prompt = (
        f"You are a quality-control manager for a text simplification tool.\n"
        f"Target reading level: {level}\n\n"
        f"Original text:\n{original}\n\n"
        f"Simplified version:\n{simplified}\n\n"
        f"Is this simplified version appropriate for a {level} reader?\n"
        f"Reply with ONLY a valid JSON object, no markdown, no explanation.\n"
        f'Either {{"decision": "approve"}} or {{"decision": "retry", "feedback": "specific reason"}}'
    )

    response = gemini.generate_content(prompt)
    raw = response.text.strip().replace("```json", "").replace("```", "").strip()

    try:
        result = json.loads(raw)
        if result.get("decision") in ("approve", "retry"):
            return result
    except (json.JSONDecodeError, KeyError):
        pass

    if "approve" in raw.lower():
        return {"decision": "approve"}
    return {"decision": "retry", "feedback": raw}


# ── Main pipeline: Manager loop ───────────────────────────────────────────────
def run_pipeline(text: str, level: str = "6th grade", input_id: str = "1", max_attempts: int = 3) -> str:
    """Full manager + agent loop. Saves each attempt to project/responses/."""

    with open(f"project/inputs/input{input_id}.txt", "w") as f:
        f.write(text)

    current_text = text
    attempt = 0

    while attempt < max_attempts:
        attempt += 1
        print(f"\n[Attempt {attempt}] Simplify agent running...")

        # 1. Flan-T5 simplifies
        simplified = simplify_agent(current_text, level)
        print(f"  Output: {simplified[:80]}...")

        with open(f"project/responses/simpl{input_id}-{attempt}.txt", "w") as f:
            f.write(simplified)

        # 2. Gemini manager evaluates
        print("[Manager] Evaluating output...")
        decision = manager_evaluate(text, simplified, level)
        print(f"  Decision: {decision}")

        if decision["decision"] == "approve":
            print("[Manager] Approved! Saving final output.")
            with open(f"project/responses/approved{input_id}.txt", "w") as f:
                f.write(simplified)
            with open(f"project/simplified/simpl{input_id}.txt", "w") as f:
                f.write(simplified)
            return simplified

        else:
            feedback = decision.get("feedback", "Please improve the simplification.")
            print(f"[Manager] Retrying with feedback: {feedback}")
            current_text = (
                f"Previous attempt was not good enough. Feedback: {feedback}\n\n"
                f"Original text:\n{text}"
            )

    print(f"[Manager] Max attempts ({max_attempts}) reached. Returning last output.")
    return simplified


# ── Other modes (summarize, explain, etc.) ────────────────────────────────────
def run_instruction(text: str, mode: str, level: str = "6th grade", input_id: str = "1") -> str:
    if mode == "simplify":
        return run_pipeline(text, level, input_id)
    elif mode == "summarize":
        return generate(f"Write a short, clear summary for a beginner:\n\n{text}")
    elif mode == "explain10":
        return generate(f"Explain the following in simple terms as if teaching a 10-year-old:\n\n{text}")
    elif mode == "example":
        return generate(f"Give a simple real-life example that helps explain this topic:\n\n{text}")
    elif mode == "steps":
        return generate(
            f"Break the following idea into 5–7 simple steps that a middle school student can follow:\n\n{text}"
        )
    else:
        return generate(text)


# ── Example usage ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    sample = (
        "Photosynthesis is the biochemical process by which chlorophyll-containing organisms "
        "convert light energy into chemical energy stored as glucose."
    )
    result = run_instruction(sample, mode="simplify", level="5th grade", input_id="1")
    print("\n=== Final Output ===")
    print(result)