import streamlit as st
from fpdf import FPDF

st.set_page_config(layout="wide", page_title="Python Learning Roadmap")

# -------------------------------------
# Learning roadmap content (fully editable!)
# -------------------------------------
roadmap = [
    {
        "title": "1. Python Basics",
        "topics": [
            {"name": "Introduction to Python", "url": "https://www.w3schools.com/python/python_intro.asp"},
            {"name": "Variables and Data Types", "url": "https://www.journaldev.com/232/python-variables"},
            {"name": "Operators in Python", "url": "https://www.w3schools.com/python/python_operators.asp"},
            {"name": "Control Flow (if-else, switch-case, loops)", "url": "https://www.geeksforgeeks.org/python-conditional-statements/"},
            {"name": "Functions/Methods", "url": "https://www.javatpoint.com/functions-in-python"},
        ]
    },
    {
        "title": "2. Object-Oriented Programming (OOP)",
        "topics": [
            {"name": "Classes and Objects", "url": "https://www.w3schools.com/python/python_classes.asp"},
            {"name": "Constructors", "url": "https://www.geeksforgeeks.org/python-constructors/"},
            {"name": "Inheritance", "url": "https://www.journaldev.com/1780/python-inheritance"},
            {"name": "Polymorphism", "url": "https://www.geeksforgeeks.org/polymorphism-in-python/"},
            {"name": "Encapsulation", "url": "https://www.geeksforgeeks.org/encapsulation-in-python/"},
        ]
    },
    {
        "title": "3. Advanced Python Concepts",
        "topics": [
            {"name": "Exception Handling", "url": "https://www.javatpoint.com/exceptions-in-python"},
            {"name": "Collections in Python", "url": "https://www.journaldev.com/1543/python-collections"},
            {"name": "Generators", "url": "https://www.geeksforgeeks.org/python-generators/"},
            {"name": "Concurrency and Parallelism", "url": "https://realpython.com/python-concurrency/"},
        ]
    },
    {
        "title": "4. Python Libraries and Frameworks",
        "topics": [
            {"name": "Flask Framework", "url": "https://flask.palletsprojects.com/en/2.0.x/"},
            {"name": "Django Framework", "url": "https://docs.djangoproject.com/en/stable/"},
            {"name": "Pandas Library", "url": "https://pandas.pydata.org/"},
            {"name": "Matplotlib Library", "url": "https://matplotlib.org/"},
        ]
    },
]

# -------------------------------------
# Calculate total number of topics dynamically
# -------------------------------------
total_topics = sum(len(section["topics"]) for section in roadmap)

# -------------------------------------
# PDF Generator
# -------------------------------------
def generate_pdf(topics):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Python Learning Roadmap", ln=True, align="C")

    for section in topics:
        pdf.set_font("Arial", "B", 12)
        pdf.cell(200, 10, txt=section["title"], ln=True)
        pdf.set_font("Arial", size=11)
        for topic in section["topics"]:
            pdf.multi_cell(0, 10, txt=f'- {topic["name"]}: {topic["url"]}')
        pdf.ln()

    return pdf

# -------------------------------------
# Streamlit App UI
# -------------------------------------
selected = []
st.title("🐍 Python Learning Roadmap")

for section in roadmap:
    with st.expander(section["title"]):
        for topic in section["topics"]:
            is_checked = st.checkbox(topic["name"], key=topic["name"])
            if is_checked:
                selected.append(topic)

# -------------------------------------
# Sidebar Progress Tracker
# -------------------------------------
completed_topics = len(selected)
progress_percent = int((completed_topics / total_topics) * 100)
st.sidebar.title("📊 Progress")
st.sidebar.progress(progress_percent / 100)
st.sidebar.markdown(f"### ✅ {completed_topics} / {total_topics} topics completed")
st.sidebar.markdown(f"### 📈 Progress: {progress_percent}%")

# -------------------------------------
# Sidebar Download PDF Button
# -------------------------------------
if st.sidebar.button("📥 Generate PDF"):
    pdf = generate_pdf(roadmap)
    pdf.output("python_learning_roadmap.pdf")
    with open("python_learning_roadmap.pdf", "rb") as f:
        st.sidebar.download_button(
            label="📄 Download Roadmap as PDF",
            data=f,
            file_name="python_learning_roadmap.pdf",
            mime="application/pdf"
        )
