import streamlit as st
from fpdf import FPDF
from urllib.parse import unquote
import json
import os
import streamlit.components.v1 as components
from utils import database
import re
# --- Load roadmap from JSON file ---
def load_roadmap_from_file(filepath):
    try:
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")
        
        with open(filepath, "r", encoding="utf-8") as file:
            content = file.read().strip()
            if not content:
                raise ValueError("The file is empty.")
            return json.loads(content)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON format in file: {filepath}") from e

# --- Get query parameters ---
query_params = st.query_params
filepath = unquote(query_params.get("path", ""))
title = query_params.get("title", "Learning Roadmap")
user_email_from_url = query_params.get("user", "")



# --- Restore session state if opened in new tab ---
if "user_email" not in st.session_state and user_email_from_url:
    st.session_state["user_email"] = user_email_from_url




####################   roadmap add to profile   ####################
if "user_email" in st.session_state:
    if st.button("⭐ Add to My List"):
        
        database.add_roadmap_to_user(st.session_state["user_email"], title, filepath)
        st.success("Added to your list!")
else:
    st.warning("🔒 Please login to add this roadmap to your list.")
####################

# --- Load roadmap ---
if filepath:
    try:
        data = load_roadmap_from_file(filepath)
        roadmap = data["sections"]
        title = data.get("title", title)

        # --- Load completed topics from user's saved roadmaps ---
        completed_topics_from_db = []
        if "user_email" in st.session_state:
            saved_roadmaps = database.get_user_roadmaps(st.session_state["user_email"])
            for saved in saved_roadmaps:
                if saved["roadmap_title"] == title:
                    completed_topics_from_db = saved.get("completed_topics", [])
                    break




    except Exception as e:
        st.error(f"❌ Failed to load roadmap from `{filepath}`")
        st.exception(e)
        st.stop()
else:
    st.error("❌ No roadmap path provided in the URL.")
    st.stop()

# --- Calculate total topics ---
total_topics = sum(len(section["topics"]) for section in roadmap)

# --- PDF Generator ---
def sanitize(text):
    return re.sub(r'[^\x00-\x7F]+', '', text)  # Remove non-ASCII characters (e.g., emojis)

def generate_pdf(topics, title):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=sanitize(title), ln=True, align="C")

    for section in topics:
        pdf.set_font("Arial", "B", 12)
        pdf.cell(200, 10, txt=sanitize(section["title"]), ln=True)
        pdf.set_font("Arial", size=11)
        for topic in section["topics"]:
            line = f'- {sanitize(topic["name"])}: {sanitize(topic["url"])}'
            pdf.multi_cell(0, 10, txt=line)
        pdf.ln()

    return pdf

# --- UI ---
selected = []
st.title(title)

for section in roadmap:
    with st.expander(section["title"]):
        for topic in section["topics"]:
            col1, col2 = st.columns([0.05, 0.95])
            with col1:
                is_checked = st.checkbox("", key=topic["name"], value=topic["name"] in completed_topics_from_db)

            with col2:
                st.markdown(f"<a href='{topic['url']}' target='_blank' style='text-decoration: none;'>{topic['name']}</a>", unsafe_allow_html=True)

            if is_checked:
                selected.append(topic)

# --- Sidebar Progress ---
completed_topics = len(selected)
progress_percent = int((completed_topics / total_topics) * 100) if total_topics > 0 else 0
st.sidebar.title("📊 Progress")
st.sidebar.progress(progress_percent / 100)
st.sidebar.markdown(f"### ✅ {completed_topics} / {total_topics} topics completed")
st.sidebar.markdown(f"### 📈 Progress: {progress_percent}%")

if st.sidebar.button("Save Progress"):
    completed_topic_names = [t["name"] for t in selected]
    email = st.session_state["user_email"]

    # ✅ Auto-add roadmap to user if not already added
    saved_roadmaps = database.get_user_roadmaps(email)
    already_added = any(r["roadmap_title"] == title for r in saved_roadmaps)

    if not already_added:
        database.add_roadmap_to_user(email, title, filepath)

    # ✅ Now update progress safely
    database.update_roadmap_progress(email, title, progress_percent, completed_topic_names)
    database.update_user_progress(email, title, progress_percent)

    st.sidebar.success("Progress saved to both tables!")


# --- Download Button ---
if st.sidebar.button("📥 Generate PDF"):
    pdf = generate_pdf(roadmap, title)
    pdf.output("roadmap.pdf")
    with open("roadmap.pdf", "rb") as f:
        st.sidebar.download_button(
            label="📄 Download Roadmap as PDF",
            data=f,
            file_name="roadmap.pdf",
            mime="application/pdf"
        )
