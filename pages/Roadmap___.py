import os
import json
import streamlit as st
from fpdf import FPDF

st.set_page_config(layout="wide", page_title="Learning Roadmap Viewer")

ROADMAPS_FOLDER = "pages\Roadmaps"

# Load available roadmap files
roadmap_files = [f for f in os.listdir(ROADMAPS_FOLDER) if f.endswith(".txt")]

st.sidebar.title("📘 Select Roadmap")
selected_file = st.sidebar.selectbox("Choose a roadmap", roadmap_files)

# Load the selected roadmap JSON
def load_roadmap(file_path):
    with open(file_path, "r") as f:
        print(f)
        return json.load(f)

roadmap = load_roadmap(os.path.join(ROADMAPS_FOLDER, selected_file))
total_topics = sum(len(section["topics"]) for section in roadmap)

# PDF Generator
def generate_pdf(topics, title):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"{title} Roadmap", ln=True, align="C")

    for section in topics:
        pdf.set_font("Arial", "B", 12)
        pdf.cell(200, 10, txt=section["title"], ln=True)
        pdf.set_font("Arial", size=11)
        for topic in section["topics"]:
            pdf.multi_cell(0, 10, txt=f'- {topic["name"]}: {topic["url"]}')
        pdf.ln()

    return pdf

# Track selected topics
selected = []
st.title(f"🚀 {selected_file.replace('.txt', '').title()} Learning Roadmap")

for section in roadmap:
    with st.expander(section["title"]):
        for topic in section["topics"]:
            is_checked = st.checkbox(topic["name"], key=f'{section["title"]}_{topic["name"]}')
            if is_checked:
                selected.append(topic)

# Progress
completed_topics = len(selected)
progress_percent = int((completed_topics / total_topics) * 100)
st.sidebar.markdown("### 📊 Progress")
st.sidebar.progress(progress_percent / 100)
st.sidebar.markdown(f"✅ {completed_topics} / {total_topics} topics completed")
st.sidebar.markdown(f"📈 {progress_percent}% completed")

# Download PDF
if st.sidebar.button("📥 Download as PDF"):
    pdf = generate_pdf(roadmap, selected_file.replace(".txt", "").title())
    pdf.output("learning_roadmap.pdf")
    with open("learning_roadmap.pdf", "rb") as f:
        st.sidebar.download_button("Download PDF", f, file_name="learning_roadmap.pdf")
