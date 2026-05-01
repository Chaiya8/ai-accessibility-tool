from .generator import flan_generate
from .verifier import verify_output


def build_prompt(text: str, mode: str, level: str) -> str:
    if mode == "simplify":
        return f"Rewrite this text for a {level} reading level:\n\n{text}"

    elif mode == "summarize":
        return f"Summarize this text in a short clear way:\n\n{text}"

    elif mode == "explain10":
        return f"Explain this text like you are teaching a 10-year-old:\n\n{text}"

    elif mode == "example":
        return f"Give a real-world example to explain this text:\n\n{text}"

    elif mode == "steps":
        return f"Break this into 5-7 simple steps:\n\n{text}"

    else:
        return text


def run_instruction(text: str, mode: str, level: str = "6th grade") -> str:
    prompt = build_prompt(text, mode, level)

    # Agent 1: Flan generates
    generated = flan_generate(prompt)

    # Agent 2: Gemini verifies
    verdict = verify_output(text, generated, level, mode)

    # If pass, return generator output
    if verdict["pass"] is True:
        return generated

    # If fail, return Gemini fixed version (clean rewrite)
    return verdict["fixed_version"]