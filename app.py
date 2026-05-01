import os
import streamlit as st
from core.pipeline import run_instruction
from core.tts import text_to_audio_bytes

# PAGE CONFIG

st.set_page_config(page_title="LearnEasy", layout="wide")


api_key = st.secrets["GEMINI_API_KEY"]


# CUSTOM CSS
st.markdown("""
<style>
.stApp {
    background-color: #0b0f14;
    color: white;
}
header, footer {visibility: hidden;}

.banner {
    background: linear-gradient(90deg, #0ea5a4, #0f766e);
    padding: 40px 20px;
    border-radius: 14px;
    text-align: center;
    margin-bottom: 30px;
}

.banner h1 {
    font-size: 48px;
    margin: 0;
    font-weight: 800;
    color: white;
}

.banner p {
    font-size: 15px;
    margin-top: 10px;
    color: #e5e7eb;
}

.section-title {
    font-size: 15px;
    font-weight: 600;
    margin-top: 20px;
    margin-bottom: 10px;
    color: #e5e7eb;
}

.process-btn button {
    background-color: #0ea5a4 !important;
    color: white !important;
    font-weight: 700 !important;
    border-radius: 10px !important;
    height: 50px !important;
    width: 100% !important;
    font-size: 16px !important;
}

.output-box {
    background: #111827;
    border: 1px solid #1f2937;
    border-radius: 14px;
    padding: 20px;
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)



st.markdown("""
<div class="banner">
    <h1>📖 LearnEasy ✨</h1>
    <p>
        AI-powered accessibility tool that transforms complex content into clear, digestible formats
        bridging the reading comprehension gap for learners everywhere.
    </p>
</div>
""", unsafe_allow_html=True)



st.markdown('<div class="section-title">Paste your text below</div>', unsafe_allow_html=True)

text = st.text_area(
    "",
    height=180,
    placeholder="Paste complex text here an article, textbook passage, or research paper..."
)



#tools
st.markdown('<div class="section-title">Choose a tool</div>', unsafe_allow_html=True)

tools = {
    "Simplify": "simplify",
    "Summarize": "summarize",
    "Explain": "explain10",
    "Example": "example",
    "Steps": "steps"
}

tool_list = list(tools.keys())

if "tool" not in st.session_state:
    st.session_state.tool = "Simplify"

cols = st.columns(len(tool_list))

for i, tool_name in enumerate(tool_list):
    with cols[i]:
        if st.button(tool_name, use_container_width=True):
            st.session_state.tool = tool_name

st.caption(f"Selected Tool: **{st.session_state.tool}**")




#reading level
st.markdown('<div class="section-title">Target reading level</div>', unsafe_allow_html=True)

levels = {
    "3rd grade": "Elementary",
    "5th grade": "Middle School",
    "8th grade": "High School",
    "college": "College",
    "high school": "Professional"
}

if "level" not in st.session_state:
    st.session_state.level = "5th grade"

level_cols = st.columns(5)

for i, (level_value, label) in enumerate(levels.items()):
    with level_cols[i]:
        if st.button(label, key=f"level_{i}", use_container_width=True):
            st.session_state.level = level_value

st.caption(f"Selected Level: **{st.session_state.level}**")



#button
st.markdown("<br>", unsafe_allow_html=True)

process_col = st.columns([2, 1, 2])[1]
with process_col:
    st.markdown('<div class="process-btn">', unsafe_allow_html=True)
    run = st.button("✨ Process Text")
    st.markdown("</div>", unsafe_allow_html=True)





# OUTPUT
if "output" not in st.session_state:
    st.session_state.output = ""

if run:
    if not text.strip():
        st.warning("Please paste some text first.")
    else:
        with st.spinner("Processing..."):
            mode = tools[st.session_state.tool]
            level = st.session_state.level
            st.session_state.output = run_instruction(text=text, mode=mode, level=level)

if st.session_state.output:
    st.markdown("---")
    st.subheader("Output")

    st.markdown(
        f"<div class='output-box'>{st.session_state.output}</div>",
        unsafe_allow_html=True
    )

    st.download_button(
        "⬇️ Download Output",
        data=st.session_state.output,
        file_name="learneasy_output.txt",
        mime="text/plain"
    )

    #TTS BUTTON
    st.markdown("### 🔊 Listen")
    if st.button("Generate Audio"):
        with st.spinner("Generating audio..."):
            audio_bytes = text_to_audio_bytes(st.session_state.output)
        st.audio(audio_bytes, format="audio/mp3")

st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center;color:#9ca3af;'>LearnEasy: Bridging the reading comprehension gap with AI accessibility</p>",
    unsafe_allow_html=True
)