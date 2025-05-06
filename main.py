import streamlit as st
from pages.Ai_Chat import Ai_Chat
from pages.Roadmap_Pg import Roadmap_Page
from utils.style import apply_custom_styles, apply_custom_logo_styles
from app import login
from pages.Profile import Profile
from pages.Generate_MCQs import gen_mcq

# Page configuration
st.set_page_config(page_title="DevNavigator", layout="wide")

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_email" not in st.session_state:
    st.session_state.user_email = "xoxoxo"


def main_app():

    def set_page(page_name):
        st.session_state["page"] = page_name

    # Initialize the page in session state
    if "page" not in st.session_state:
        st.session_state["page"] = "home"

    # Sidebar
    with st.sidebar:
        st.image("logo.png", use_container_width=True)
        # st.header("DevNavigator")
        if st.button("Home"):
            set_page("home")
        if st.button("Roadmaps"):
            set_page("roadmaps")
        if st.button("AI Chat"):
            set_page("ai_chat")
        if st.button("Profile"):
            set_page("profile")
        if st.button("Ai MCQ Test"):
            set_page("Generate_MCQs")
        st.markdown("---")
        def apply_custom_style():
            theme = st.sidebar.radio("🎨 Choose Theme", ("Light", "Dark"))
            if theme == "Dark":
                apply_custom_logo_styles()
            else:
                apply_custom_styles()
        apply_custom_style()
        st.markdown(f"<p style='text-align:center;'>Logged in as <strong>{st.session_state.user_email}</strong></p>", unsafe_allow_html=True)

    def Home():

        st.markdown("""
        <style>
        .stButton > button {
            background-color: #ffffff;
            color: black;
            padding: 20px;
            border-radius: 12px;
            width: 100%;
            text-align: left;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
            font-size: 16px;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        .stButton > button:hover {
            transform: scale(1.03);
            box-shadow: 0 6px 14px rgba(0, 0, 0, 0.15);
            background-color: #f8f8f8;
        }
        </style>
    """, unsafe_allow_html=True)
        # Main content
        # Main page content
        st.markdown('<div class="main-title">Welcome to DevNavigator</div>', unsafe_allow_html=True)
        st.markdown("""
    <div class="main-container">
                <h3 text-align="center" >Your Personal AI-Powered Tech Learning Assistant</h3>
                <p>
                DevNavigator isn’t just another coding tool — it’s your career co-pilot. Whether you’re a beginner stepping into tech or a professional exploring a new domain, DevNavigator guides you with custom roadmaps, expert resources, and AI-generated assessments to keep you on track and growing.
                </p>
                """, unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("📘 **Roadmaps**\n\n*Learn Python from scratch to advanced projects with hands-on coding exercises.*"):
                set_page("roadmaps")

        with col2:
            if st.button("🤖 **AI Chat**\n\n*Chat with an intelligent assistant for learning or building projects.*"):
                set_page("ai_chat")

        with col3:
            if st.button("🧠 **AI Generated Test**\n\n*Generate smart MCQ \n\n tests using AI.*"):
                set_page("Generate_MCQs")

        st.markdown("""<h2>🔍 What is DevNavigator?</h2>
                <p>
                DevNavigator is an AI-powered assistant that helps you plan, learn, and grow in tech — without the noise. It builds custom learning roadmaps, provides curated material, and helps you measure your progress with interactive tests and challenges.
                </p>
                <p>No coding tools. No app builders. Just pure learning, simplified.</p>
                <h2>✨ Key Features</h2>
                <ul>
                    <li>📌 <b>Personalized Learning Roadmaps</b> — Clear, step-by-step guides tailored to your goals.</li>
                    <li>📚 <b>Curated Learning Resources</b> — Handpicked content without the fluff.</li>
                    <li>🧠 <b>AI-Generated Quizzes & Tests</b> — Smart assessments to challenge and track your knowledge.</li>
                    <li>🎯 <b>Goal-Based Planning</b> — Get job-ready, portfolio-ready, or certification-ready.</li>
                    <li>🌐 <b>One Hub for All Learning</b> — Everything organized in one place.</li>
                </ul>
                <h2>💡 Why Use DevNavigator?</h2>
                <ul>
                    <li>🔄 <b>Clarity Over Chaos</b> — No more YouTube rabbit holes. Learn with structure.</li>
                    <li>⏱️ <b>Save Time</b> — We've done the research so you can start learning fast.</li>
                    <li>🧭 <b>Built for All Levels</b> — From beginner to pro, your journey is covered.</li>
                    <li>🧪 <b>Track Your Progress</b> — Real-time tracking with interactive assessments.</li>
                </ul>
                <h2>🥇 Why DevNavigator Over Other Learning Platforms?</h2>
                <table style="width: 100%; border-collapse: collapse;">
                    <tr><th>Feature</th><th>DevNavigator</th><th>YouTube / Blogs</th><th>Online Courses</th></tr>
                    <tr><td>Custom Roadmaps</td><td>✅ Yes</td><td>❌ No</td><td>❌ No</td></tr>
                    <tr><td>AI-Generated Tests & Feedback</td><td>✅ Yes</td><td>❌ No</td><td>🔶 Sometimes</td></tr>
                    <tr><td>All-in-One Learning Hub</td><td>✅ Yes</td><td>❌ No</td><td>❌ No</td></tr>
                    <tr><td>Resource Curation by AI</td><td>✅ Yes</td><td>❌ No</td><td>🔶 Basic</td></tr>
                    <tr><td>Adaptable to Career Goals</td><td>✅ Yes</td><td>❌ No</td><td>❌ No</td></tr>
                </table>
                <p><b>📌 DevNavigator doesn’t teach everything — it shows you the right path to learn any Technical.</b></p>
                <div style="margin-top: 2rem;">
                    <a href="/?page=roadmaps" target="_self">
                        <div class="sidebar-button" style="width: 200px; margin: auto;">Explore Roadmaps</div>
                    </a>
                    <a href="/?page=get_started" target="_self">
                        <div class="sidebar-button" style="width: 200px; margin: 1rem auto;">Get Started</div>
                    </a>
                </div>
            </div>
        """, unsafe_allow_html=True)



    if st.session_state["page"] == "home":
        Home()
    elif st.session_state["page"] == "roadmaps":
        Roadmap_Page()
    elif st.session_state["page"] == "ai_chat":
        Ai_Chat()
    elif st.session_state["page"] == "profile":
        Profile()
    elif st.session_state["page"] == "Generate_MCQs":
        gen_mcq()
    else:
        Home()

if st.session_state.logged_in:
    main_app()
else:
    login()
