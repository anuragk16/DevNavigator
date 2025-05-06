
# # Dummy function you want to trigger on card click
# def open_roadmap(path):
#     st.success(f"You clicked: {path}")
    
    # SANITIZED FILENAME FUNCTION
# import re

# Prompt for the roadmap genration 
# {
 # "prompt": "Create a roadmap for the topic specified, in the following JSON format. Do not include any extra explanation or text, only the JSON content. \n\nThe format should be:\n{\n  \"title\": \"<Roadmap Title>\",\n  \"description\": \"<Short description of the roadmap>\",\n  \"sections\": [\n    {\n      \"title\": \"<Section Title>\",\n      \"topics\": [\n        {\"name\": \"<Topic Name>\", \"url\": \"<Reference URL>\"},\n        ...\n      ]\n    },\n    ...\n  ]\n}\n\nEach section should represent a step or stage in learning the topic, and each topic should be a specific concept or skill with a relevant learning URL. Use popular and reliable sources like w3schools, geeksforgeeks, realpython, freecodecamp, etc.\n\nReplace <Roadmap Title> and <Short description of the roadmap> with appropriate values based on the given topic.\n\nExample input:\nTopic: Data Scientist\n\nOnly respond with the JSON roadmap as per the format above."
# }



# def sanitize_filename(filename):
#     # Remove emojis and special characters
#     filename = re.sub(r'[^\w\s-]', '', filename)  # Keeps only alphanumeric, space, underscore, dash
#     # Replace spaces with underscores
#     filename = filename.strip().replace(' ', '_')
#     return filename.lower()  # Optional: lowercase for consistency

import streamlit as st
import os
import json


def read_roadmaps_from_folder(folder_path):
    roadmaps = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".txt"):
            with open(os.path.join(folder_path, file_name), "r", encoding="utf-8") as file:
                content = file.read()
            title = file_name.replace(".txt", "").replace("_", " ").title()
            roadmaps.append({
                "title": title,
                "path": os.path.join(folder_path, file_name)
            })
    return roadmaps

def load_roadmap_metadata(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('title', 'No Title'), data.get('description', 'No Description')
    except Exception as e:
        return 'Error Loading Title', str(e)

def show_roadmap_cards(roadmaps):
    for i in range(0, len(roadmaps), 2):
        cols = st.columns(2)
        for j in range(2):
            if i + j < len(roadmaps):
                roadmap = roadmaps[i + j]
                filepath = roadmap['path']

                # Load title and description from the file
                title, description = load_roadmap_metadata(filepath)

                with cols[j]:
                    from urllib.parse import quote

                    # inside show_roadmap_cards():
                    user_email = st.session_state.get("user_email", "")
                    encoded_path = quote(filepath)
                    encoded_title = quote(title)
                    # Use hash fragment to pass user email manually
                    encoded_email = quote(user_email)  # URL-safe
                    st.markdown(f"""<a href="/view_roadmap?path={encoded_path}&title={encoded_title}&user={encoded_email}" target="_blank" style="text-decoration: none;">
                            <div class="roadmap-card">
                                <h4>{title}</h4>
                                <p style="color: #888;">{description}</p>
                            </div> 
                        </a>""", unsafe_allow_html=True)



def Roadmap_Page():
    st.markdown("<div class='heading'>🚀 Roadmaps Explorer</div>", unsafe_allow_html=True)
    selected_filter = st.radio("Choose category:", ["Languages", "Projects", "Jobs", "Others"], horizontal=True,key="category_filter")

    base_path = "pages_/Roadmaps"
    category_paths = {
        "Languages": os.path.join(base_path, "Languages"),
        "Projects": os.path.join(base_path, "Projects"),
        "Jobs": os.path.join(base_path, "Jobs"),
        "Others": os.path.join(base_path, "Others"),
    }

    if selected_filter in category_paths:
        roadmaps = read_roadmaps_from_folder(category_paths[selected_filter])
        if roadmaps:
            show_roadmap_cards(roadmaps)
        else:
            st.info("No roadmaps found in this category.")


