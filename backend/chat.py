import json
import os
from flask import Flask, request, jsonify
from langchain_ollama import OllamaLLM
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from googlesearch import search

# Initialize Flask app
app = Flask(__name__)
llm = OllamaLLM(model="llama3.2")

# Lambda to create Google Search URL
search_url = lambda title: f"https://www.google.com/search?q={'+'.join(title.strip().split())}"
def get_first_result(query):
    try:
        lis = [""," "]
        for result in search(query, num=10):
            if result in lis:
                continue
            return result
    except Exception as e:
        return f"Error occurred: {e}"
# Prompt to collect user goals
requirement_prompt = ChatPromptTemplate.from_messages([
    ("system", 
     "You are an intelligent assistant from DevNavigator, helping users create computer science related project or skill learning roadmaps. "
     "Collect details about the user's goal, preferred timeframe, technologies, and experience. "
     "Ask questions one by one until all the information is collected and don't repeat questions. "
     "Force the user to answer all the questions in detail. If the user doesn't specify technologies, extract them from the goal. "
     "Don't say things like 'It seems like you repeated the same information.' "
     "After collecting all the necessary details, output them in the following JSON format (all values should be in double quotes):\n\n"
     "{{\n"
     "  \"goal\": \"...\",\n"
     "  \"timeframe\": \"...\",\n"
     "  \"technologies\": \"...\",\n"
     "  \"experience\": \"...\"\n"
     "}}\n"
     "Only output this JSON dictionary when the user confirms all the specifications. No text or explanation before or after."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}")
])

# Prompt to generate roadmap
roadmap_prompt = ChatPromptTemplate.from_messages([
    ("user", """
Create a detailed JSON roadmap in this format:

{{
  "title": "{goal}",
  "description": "A roadmap to achieve the goal: {goal} within {timeframe}.",
  "sections": [
    {{
      "title": "Section 1 Title",
      "topics": [
        {{
          "name": "Topic Name",
          "url": "https://example.com"
        }}
      ]
    }}
  ]
}}

Just generate a JSON based on:
Goal: {goal}
Timeframe: {timeframe}
Technologies: {technologies}
Experience level: {level}

Use emojis relevant to the topics in title, description, and topic names.

Only output valid JSON — no explanations or markdown.
""")
])

chat_history = []

@app.route("/api/chat", methods=["POST"])
def chat():
    global chat_history
    data = request.json
    user_input = data.get("input", "")
    chat_history.append(HumanMessage(content=user_input))

    # Phase 1: Collect user info
    response = llm.invoke(requirement_prompt.format(chat_history=chat_history, input=user_input))
    
    try:
        user_data = json.loads(response)
    except json.JSONDecodeError:
        chat_history.append(AIMessage(content=response))
        return jsonify({"response": response})  # Keep collecting data

    # Prepare tech list
    techs = user_data['technologies']
    if isinstance(techs, str):
        technologies_list = [tech.strip().lower() for tech in techs.split(",")]
    else:
        technologies_list = [tech.strip().lower() for tech in techs]

    # Phase 2: Generate roadmap
    while True:
        roadmap_response = llm.invoke(roadmap_prompt.format(
            goal=user_data['goal'],
            timeframe=user_data['timeframe'],
            technologies=', '.join(technologies_list),
            level=user_data['experience']
        ))

        try:
            roadmap_json = json.loads(roadmap_response)
            break
        except json.JSONDecodeError:
            continue  # Retry generating if output is not valid JSON

    # Phase 3: Replace all placeholder URLs
    print("Roadmap before replacement:", roadmap_json)

    for section in roadmap_json.get("sections", []):
        for topic in section.get("topics", []):
            topic_name = topic.get("name", "learn topic")
            topic["url"] = get_first_result(search_url(topic_name))

    # Save roadmap
    os.makedirs("pages_/Roadmaps/others", exist_ok=True)
    filename = f"pages_/Roadmaps/others/{roadmap_json['title'].replace(' ', '_')}.txt"
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(roadmap_json, file, indent=4, ensure_ascii=False)

    chat_history.append(AIMessage(content=json.dumps(roadmap_json, indent=2)))
    title = roadmap_json['title']
    return jsonify({
        "response": f"✅ Roadmap generated successfully!\n\nSee this roadmap in your Roadmap page → Others section.\n\n📘 Roadmap Name - {title}"
    })


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
