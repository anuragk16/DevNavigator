import streamlit as st
import requests
from time import sleep
from urllib.parse import unquote


def Ai_Chat():

    # --- API Endpoint ---
    API_URL = "http://localhost:5001/api/chat"  # Flask API endpoint

    # --- Function to fetch response from Flask API ---
    def get_response_from_api(user_input):
        try:
            response = requests.post(API_URL, json={"input": user_input})
            if response.status_code == 200:
                return response.json()
            else:
                st.error(f"Error: {response.status_code}, {response.text}")
                sleep(1)
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
        return {"response": "DevNavigator API is not connecting..."}

    # --- Initialize chat history ---
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # --- UI Heading ---
    st.title("🤖 AI Chat Assistant")
    st.markdown("""
    Chat with our AI assistant to generate personalized roadmaps for your projects or goals.
    > 💡 *To get a roadmap directly, just type your goal, timeframe, technologies, and experience in a single message.*
    """)
    st.markdown("<hr style='margin:4px 0;'>", unsafe_allow_html=True)
    # --- Chat history display ---
    chat_container = st.container()
    with chat_container:
        CHAT_FONT_SIZE = "18px"  # You can adjust this

        for chat in st.session_state.chat_history:
            if chat["role"] == "user":
                st.markdown(
                    f"<div style='font-size:{CHAT_FONT_SIZE}; padding:8px 0'><strong>😇 You:</strong> {chat['message']}</div>",
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"<div style='font-size:{CHAT_FONT_SIZE}; padding:8px 0'><strong>🤖 AI:</strong> {chat['message']}</div>",
                    unsafe_allow_html=True
                )
            st.markdown("<hr style='margin:4px 0;'>", unsafe_allow_html=True)


    # --- User input form ---
    st.divider()
    with st.container():
        with st.form(key="user_input_form", clear_on_submit=True):
            user_input = st.text_input("Type your message:", placeholder="e.g., I want to learn backend in 3 months with Django. I have some Python experience.", key="user_input")
            submit_button = st.form_submit_button("Send")

    # --- Handle submission ---
    if submit_button and user_input:
        st.session_state.chat_history.append({"role": "user", "message": user_input})

        # Call API and get response
        api_response = get_response_from_api(user_input)
        bot_response = api_response.get("response", "No response available.")
        file_path = api_response.get("file_path", None)

        st.session_state.chat_history.append({"role": "bot", "message": bot_response})

        # Show download button if document was generated
        if file_path:
            with open(file_path, "rb") as file:
                st.download_button(
                    label="📥 Download Roadmap as Word Document",
                    data=file,
                    file_name=file_path.split("/")[-1],
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )

        # Refresh UI to show updated chat
        st.rerun()
