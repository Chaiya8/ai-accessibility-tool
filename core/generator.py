from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

MODEL_NAME = "google/flan-t5-small"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

# Flan-T5 wrapper that generates text based on a prompt.
def flan_generate(prompt: str, max_length: int = 256) -> str:
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, padding=True)

    outputs = model.generate(
        **inputs,
        max_length=max_length,
        num_beams=4
    )

    return tokenizer.decode(outputs[0], skip_special_tokens=True).strip()