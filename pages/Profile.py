import streamlit as st
from utils import database
from urllib.parse import quote

def Profile():
    st.title("👤 Your Profile")

    # --- User Info ---
    st.subheader("User Details")
    st.markdown(f"""
        <div class='section'>
            <h4>Username: {st.session_state.get('user_name', 'N/A')}</h4>
            <p>Email: {st.session_state.get('user_email', 'N/A')}</p>
            <p><strong>Education:</strong> {st.session_state.get('user_education', 'N/A')}</p>
            <p><strong>Interests:</strong> {st.session_state.get('user_interests', 'N/A')}</p>
        </div>
    """, unsafe_allow_html=True)
    
    ####################   roadmap add to profile   ####################
    if "user_email" in st.session_state:
        saved_roadmaps = database.get_user_roadmaps(st.session_state["user_email"])

        # Styled Header
        st.markdown("<h4 style='font-size: 24px;'>📌 Your Saved Roadmaps</h4>", unsafe_allow_html=True)
        with st.expander(label="Click to expand", expanded=True):
            if saved_roadmaps:
                for roadmap in saved_roadmaps:
                    title = roadmap["roadmap_title"]
                    path = roadmap["roadmap_path"]
                    progress = roadmap["progress_percent"]
                    st.markdown(f"""<a href="/view_roadmap?path={path}&title={title}&user={quote(st.session_state.get("user_email", ""))}" target="_blank" style="text-decoration: none;">
                                    <div class="roadmap-card">
                                        <h4>{title}</h4>
                                        <p>{progress}% Completed</p>
                                    </div> 
                                </a>""", unsafe_allow_html=True)
            else:
                st.info("You haven’t saved any roadmaps yet.")

        # Styled Header
        st.markdown("<h4 style='font-size: 24px;'>📍 Your Roadmap Progress</h4>", unsafe_allow_html=True)
        with st.expander(label="Click to expand", expanded=True):
            roadmap_progress = st.session_state.get("roadmap_progress", {})
            
            if roadmap_progress:
                for roadmap, progress in roadmap_progress.items():
                    st.markdown(f"**{roadmap} - {progress}% Completed**")
                    st.progress(progress)
            else:
                st.info("You haven't started any roadmaps yet.")
    else:
        st.warning("🔒 Login to view your saved roadmaps and progress.")


    # --- AI-Generated Test ---
    st.subheader("🧠 Take a Practice Test")

    st.markdown(f"""<a href="/Generate_MCQs" target="_blank" style="text-decoration: none;">
                                    <div class="roadmap-card">
                                        <h4>Generate MCQs</h4>
                                        <p>Test your knowledge with AI-generated questions!</p>
                                    </div> 
                                </a>""", unsafe_allow_html=True)
        # Add your test logic here


