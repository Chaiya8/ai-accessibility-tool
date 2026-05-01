import streamlit as st
import requests

st.set_page_config(page_title="LearnEasy – AI Accessibility Tool", layout="wide")

st.title("LearnEasy – AI Accessibility Tool")
st.write("Paste any text below and choose how you want it transformed.")

text = st.text_area("Text to transform", height=200)

mode = st.selectbox(
    "Choose transformation mode:",
    [
        "simplify",
        "summarize",
        "explain10",
        "example",
        "steps"
    ]
)

level = st.selectbox(
    "Reading level (used for simplify mode):",
    ["3rd grade", "5th grade", "6th grade", "8th grade", "High school"],
    index=2
)

if st.button("Transform"):
    if not text.strip():
        st.warning("Please paste some text first.")
    else:
        try:
            response = requests.post(
                "http://127.0.0.1:8000/transform",
                json={"text": text, "mode": mode, "level": level},
                timeout=60
            )
            response.raise_for_status()
            result = response.json().get("result", "")
            st.subheader("Output:")
            st.write(result)
        except Exception as e:
            st.error(f"Error contacting backend: {e}")