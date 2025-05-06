import streamlit as st
from utils import database, auth
import mysql.connector

def login():
    # Make sure the table exists
    database.create_users_table()

    # Title and UI
    st.title("🔐 Login System")
    auth_mode = st.sidebar.selectbox("Choose", ["Login", "Signup"])

    # SIGNUP
    if auth_mode == "Signup":
        st.subheader("🔐 Create Your Account")

        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        education_levels = [
            "Secondary Education",
            "High School",
            "Graduation",
            "Post Graduation",
            "Currently Working"
        ]
        education = st.selectbox("📚 Current Education Level", education_levels)
        interests = st.text_input("🎯 Field of Interest (e.g., Web Dev, Data Science)")

        if st.button("Create Account"):
            if not username or not email or not password or not education or not interests:
                st.warning("⚠️ All fields are required. Please fill out everything.")
            else:
                try:
                    created = auth.signup(username, email, password, education, interests)

                    if created:
                        st.session_state["user_name"] = username
                        st.session_state["user_email"] = email
                        st.session_state["education"] = education
                        st.session_state["interests"] = interests

                except mysql.connector.errors.IntegrityError:
                    st.warning("⚠️ Use a different Username, this one is already taken!")



    # LOGIN
    elif auth_mode == "Login":
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if auth.login(email, password):
                # Save login session
                st.session_state["logged_in"] = True
                st.session_state["user_email"] = email

                # Fetch full user data
                user_profile = database.get_full_user_profile(email)

                user_info = user_profile["user_info"]
                progress = user_profile["roadmap_progress"]

                st.session_state["user_name"] = user_info.get("username", "N/A")
                st.session_state["user_education"] = user_info.get("education", "N/A")
                st.session_state["user_interests"] = user_info.get("interests", "N/A")
                st.session_state["roadmap_progress"] = {
                    p['roadmap_name']: p['progress_percent'] for p in progress
                }

                st.success("✅ You’re logged in!")

            else:
                st.error("❌ Invalid email or password")




