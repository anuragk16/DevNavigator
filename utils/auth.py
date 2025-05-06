import bcrypt
import streamlit as st
from utils import database

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

def signup(username, email, password, education, interests):
    user = database.fetch_user(email)
    if user:
        st.warning("Email already registered.")
        return False
    else:
        hashed = hash_password(password)
        database.insert_user(username, email, hashed, education, interests)
        st.success("Account created! Please log in.")
        return True


def login(email, password):
    user = database.fetch_user(email)
    if user and check_password(password, user['password_hash']):
        st.session_state['user'] = user
        st.success(f"Welcome {user['username']}!")
        return True
    else:
        st.error("Invalid email or password")
        return False
