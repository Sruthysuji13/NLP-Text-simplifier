import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:5000/analyze"

st.title("🧠 Cognitive Load–Aware Text Rewriter")

text = st.text_area("Enter your text:", height=200)

if st.button("Analyze & Rewrite"):

    if text.strip() == "":
        st.warning("Please enter some text.")
    else:
        response = requests.post(BACKEND_URL, json={"text": text})

        if response.status_code == 200:
            data = response.json()

            st.subheader("📊 Results")

            st.write("### Original Text")
            st.write(data["original_text"])
            st.write(f"**Original Load Score:** {data['original_score']}")

            st.write("### Rewritten Text")
            st.write(data["rewritten_text"])
            st.write(f"**New Load Score:** {data['new_score']}")

            st.success(f"✅ Improvement: {data['improvement']}% reduction in cognitive load")
        else:
            st.error("Error connecting to backend.")