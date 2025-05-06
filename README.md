# 🚀 DevNavigator: AI-Powered Roadmap Generator

DevNavigator is an intelligent assistant that helps users generate personalized learning or project roadmaps in the field of Computer Science. Using LangChain with Ollama LLM and dynamic Google Search integration, the system interacts with the user, understands their goal, and returns a structured, actionable roadmap in JSON format.

---

## 📌 Features

- 💬 **Interactive Chat System**: Collects detailed user inputs through step-by-step questioning.
- 🧠 **LLM-Driven Understanding**: Utilizes a locally hosted LLM (LLaMA3 via Ollama) to process user goals and generate a roadmap.
- 🔧 **Dynamic Prompting**: Uses LangChain's structured prompts to guide data collection and roadmap creation.
- 🌐 **Google Search Integration**: Enhances the roadmap with real-time relevant learning links.
- 📄 **JSON Roadmap Output**: Roadmaps are stored in a clean, structured JSON format.
- 📁 **Organized Storage**: Roadmaps are saved under categorized directories for future reference.
- 🧑‍💻 **Flask API Integration**: Easily scalable and can be used as a backend API service.

---

## 🛠️ Technologies Used

- Python 3.10+
- Flask
- LangChain
- Ollama (LLaMA3 model)
- Streamlit
- Google Search API (via `googlesearch-python`)
- JSON File Handling

---

## 🔧 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/anuragk16/DevNavigator.git
cd DevNavigator
```

## 🔧 Setup Instructions (Post-Clone)

Follow these steps to fully configure and run the project:

---

### 1. 🐬 Install MySQL Server

- Download and install MySQL Server from: [MySQL Official Downloads](https://dev.mysql.com/downloads/mysql/)
- Note down your **username**, **password**, and **host** (default is usually `localhost`).

### 2. 🔑 Update Database Configuration

Open the file:

```

Utils/database.py

````

Inside this file, update the database connection variables as shown below:

```python
host = "your_mysql_host"       # e.g., "localhost"
user = "your_mysql_username"   # e.g., "root"
password = "your_mysql_password"
````

Make sure your MySQL server is **running** before you launch the project.

---

### 3. 🦙 Install Ollama and LLaMA 3.2

* Download and install **Ollama** from the official site:
  👉 [https://ollama.com/](https://ollama.com/)

* After installation, open your terminal and run the following command to install and start LLaMA 3.2:

```bash
ollama run llama3.2
```

This will pull the model and prepare the LLM backend for generating roadmaps.

---

### 4. 📦 Install Python Dependencies

Ensure you're in the project root folder, then install all required modules:

```bash
pip install -r requirements.txt
```

This will install Flask, LangChain, MySQL connectors, and other required libraries.

---

### 5. ▶️ Run the Application

Now, start the Flask server:

```bash
python backend\chat.py
```
Then run the frontend:

```bash
python -m streamlit run main.py
```

The server will automatically run in default browser or run on:

```
http://localhost:5001/
```

You can send a `POST` request to this endpoint using tools like Postman, Thunder Client, or any frontend setup.

---

### ✅ Example Usage

**POST URL:**

```
http://localhost:5001/api/chat
```

**Body (JSON):**

```json
{
  "input": "I want to become a full stack web developer in 4 months"
}
```

The system will interact with you, ask more questions to understand your goal, and return a detailed roadmap saved as `.txt` and `.json`.

---

### 📂 Roadmap Storage

Once generated, roadmaps are stored here:

```
pages_/Roadmaps/others/<your_roadmap>.txt
```

These files contain a well-structured, categorized roadmap with clickable links to learning resources.

