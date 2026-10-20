"""Page 3: ticket triage (Part G pipeline, src/triage.py)."""
import os
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))     # lets us import src/triage.py
MAX_CHARS = 1000
MAX_PER_SESSION = 20                                                      # protects the free API quota


@st.cache_resource
def load_triage():
    import triage
    triage.DELAY = 0                      # the pause between calls is only needed for bulk runs
    return triage


st.title("Ticket triage")
try:
    key = st.secrets["GROQ_API_KEY"]      # the key lives in st.secrets, never in the code
except Exception:
    key = None
if not key:
    st.error("GROQ_API_KEY is missing from st.secrets. Add it to .streamlit/secrets.toml "
             "(or to the app's Secrets on Streamlit Cloud).")
    st.stop()
os.environ["GROQ_API_KEY"] = key
triage = load_triage()

text = st.text_area("Paste a customer complaint", height=150)
if st.button("Triage ticket"):
    text = text.strip()
    if not text:
        st.error("Please paste a complaint first.")
    elif len(text) > MAX_CHARS:
        st.error(f"The complaint is {len(text)} characters. The limit is {MAX_CHARS}.")
    elif st.session_state.get("calls", 0) >= MAX_PER_SESSION:
        st.error("Limit of 20 tickets per session reached. Reload the page to continue.")
    else:
        st.session_state["calls"] = st.session_state.get("calls", 0) + 1
        with st.spinner("Classifying..."):
            try:
                result = triage.classify(text, triage.PROMPT_V2)
            except SystemExit as err:
                st.error(str(err))
                st.stop()
        if result["status"] == "failed":
            st.error("The model did not return a valid answer after several tries. Please try again.")
        else:
            a, b, c = st.columns(3)
            a.metric("Category", result["category"])
            b.metric("Sentiment", result["sentiment"])
            c.metric("Urgency", f"{result['urgency']} / 5")
            st.write(f"**Summary:** {result['summary']}")
