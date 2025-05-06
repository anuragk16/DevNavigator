import streamlit as st

def apply_custom_styles():
        
    # Custom CSS
    st.markdown("""
    <style>
        /* Background */
        .stApp {
            background: linear-gradient(to right, #1f1c2c, #928dab);
            font-family: 'Segoe UI', sans-serif;
            color: white;
        }
        .heading {
            font-size: 2.5rem;
            font-weight: bold;
            margin-bottom: 2rem;
            color: #fff;
        }
        .roadmap-card {
            background-color: #1f1f1f;
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 12px;
            box-shadow: 0 0 10px rgba(255, 255, 255, 0.05);
            color: #fff;
            transition: transform 0.3s ease;
        }
        .roadmap-card:hover {
            transform: scale(1.02);
            background-color: #2a2a2a;
        }
        .roadmap-card h4 {
            margin-top: 10px;
            margin-bottom: 5px;
        }
        .roadmap-card p {
            font-size: 0.9rem;
            color: #ccc;
        }
        .roadmap-image {
            width: 100%;
            height: 120px;
            object-fit: cover;
            border-radius: 8px;
        }
        /* Sidebar */
        section[data-testid="stSidebar"] {
            background: #1e1e2f;
            padding: 1rem;
        }
        .sidebar-title {
            font-size: 28px;
            font-weight: bold;
            color: #ffffff;
            margin-bottom: 0.5rem;
            text-align: center;
        }   
        div.stButton > button:first-child {
            background: #2e2e42;
            color: white;
            padding: 0.7rem 1rem;
            border-radius: 12px;
            margin: 10px 0;
            font-weight: 600;
            border: 1px solid #444;
            width: 100%;
            cursor: pointer;
            transition: all 0.3s ease;
            text-align: center;
        }
        div.stButton > button:first-child:hover {
            background: #4b6cb7;
        }
        .main-title {
            text-align: center;
            font-size: 50px;
            font-weight: bold;
            margin-top: 30px;
            text-shadow: 2px 2px 4px #000;
        }
        .section {
            background: rgba(255, 255, 255, 0.05);
            padding: 2rem;
            border-radius: 20px;
            margin: 2rem;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        }
        .card-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 2rem;
        }
        .card {
            background-color: #2e2e42;
            border-radius: 15px;
            padding: 1.5rem;
            box-shadow: 0px 10px 20px rgba(0,0,0,0.3);
            transition: transform 0.3s;
        }
        .card:hover {
            transform: translateY(-10px);
        }
        .card h3 {
            color: #ffcc00;
            margin-bottom: 0.5rem;
        }
        .card p {
            color: #ccc;
        }
    </style>
    """, unsafe_allow_html=True)
    

def apply_custom_logo_styles():
    st.markdown("""
    <style>
        /* App background */
        .stApp {
            background: radial-gradient(circle at top left, #0f1217, #101924);
            font-family: 'Segoe UI', sans-serif;
            color: #e6f1ff;
        }
        .heading {
            font-size: 2.5rem;
            font-weight: bold;
            margin-bottom: 2rem;
            color: #fff;
        }
        /* Sidebar */
        section[data-testid="stSidebar"] {
            background: #0e1016;
            padding: 1rem;
        }

        .sidebar-title {
            font-size: 28px;
            font-weight: bold;
            color: #00b4ff;
            margin-bottom: 0.5rem;
            text-align: center;
        }

        /* Main title */
        .main-title {
            text-align: center;
            font-size: 50px;
            font-weight: bold;
            margin-top: 30px;
            text-shadow: 2px 2px 4px #000;
            color: #fff;
        }

        /* Button styles */
        div.stButton > button:first-child {
            background: #10131b;
            color: #00b4ff;
            padding: 0.7rem 1rem;
            border-radius: 12px;
            margin: 10px 0;
            font-weight: 600;
            border: 1px solid #00b4ff44;
            width: 100%;
            cursor: pointer;
            text-align: center;
            transition: all 0.3s ease;
        }

        div.stButton > button:first-child:hover {
            background: #00b4ff22;
            border-color: #00b4ff;
        }

        /* Section wrapper */
        .section {
            background: rgba(255, 255, 255, 0.05);
            padding: 2rem;
            border-radius: 20px;
            margin: 2rem;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        }

        /* Card grid layout */
        .card-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 2rem;
        }

        /* General card styling */
        .card {
            background-color: #131722;
            border-radius: 15px;
            padding: 1.5rem;
            box-shadow: 0px 10px 20px rgba(0, 180, 255, 0.15);
            transition: transform 0.3s;
            color: #dbeaff;
        }

        .card:hover {
            transform: translateY(-10px);
            box-shadow: 0px 12px 22px rgba(0, 180, 255, 0.2);
        }

        .card h3 {
            color: #00b4ff;
            margin-bottom: 0.5rem;
        }

        .card p {
            color: #aac9f0;
        }

        /* Roadmap card styling */
        .roadmap-card {
            background-color: #0f121a;
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 12px;
            box-shadow: 0 0 10px rgba(0, 180, 255, 0.08);
            color: #e6f1ff;
            transition: transform 0.3s ease;
        }

        .roadmap-card:hover {
            transform: scale(1.02);
            background-color: #1b1e2b;
        }

        .roadmap-card h4 {
            margin-top: 10px;
            margin-bottom: 5px;
            color: #00b4ff;
        }

        .roadmap-card p {
            font-size: 0.9rem;
            color: #aac9f0;
        }

        .roadmap-image {
            width: 100%;
            height: 120px;
            object-fit: cover;
            border-radius: 8px;
        }

    </style>
    """, unsafe_allow_html=True)
