# RAG Philosophy Chatbot (Llama.cpp Server Version)

The **RAG Philosophy Chatbot** is an intelligent chatbot application leveraging the **RAG (Retrieval-Augmented Generation)** architecture. The system allows users to converse with virtual "philosophers" representing various schools of thought (Stoicism, Existentialism, Nihilism, Pessimism, and Marxism-Leninism). 

A Large Language Model (LLM) is hosted locally via a **llama.cpp server** to act as the generative backbone, which is dynamically augmented with contextual knowledge embedded and retrieved using **FAISS** and **LangChain**.

## 🚀 Key Features

- **Multiple Philosophical Schools**: Roleplay options across 5 distinct ideologies—Stoicism, Existentialism, Nihilism, Pessimism, and Marxism-Leninism—each with its own specific persona and core messages.
- **Efficient RAG Mechanism**: Automatically handles text chunking, generates embeddings using the `all-MiniLM-L6-v2` model, and manages local vector similarity searches via the `FAISS` library.
- **Local LLM Integration**: Connects seamlessly to an OpenAI-compatible API endpoint provided by a local `llama.cpp` server running open-source models (such as Qwen 2.5).
- **Chat History Management**: Keeps track of recent conversation context, ensuring that the bot delivers logical, consistent, and context-aware responses.
- **Intuitive Web UI**: Features a clean web user interface built with HTML/CSS/JS, rendered via Jinja2 templates, and powered by a high-performance FastAPI backend.

## 🛠️ Tech Stack

- **Backend Framework**: FastAPI (Uvicorn server)
- **LLM Orchestration**: LangChain (`ChatOpenAI`, `SystemMessage`, `HumanMessage`)
- **Vector Database**: FAISS (Facebook AI Similarity Search)
- **Embedding Model**: `sentence-transformers/all-MiniLM-L6-v2` via HuggingFace Embeddings
- **LLM Server**: Llama.cpp (configured by default to listen at `http://localhost:8080/v1`)

## 📁 Project Directory Structure

```text
rag-philosophy-chatbot/
│
├── app.py              # Main application file (Initializes API endpoints, configures RAG)
├── config.py           # Stores raw knowledge base text and philosophical personas
├── .env                # Environment variables configuration file (if applicable)
├── requirements.txt    # List of project dependencies
│
├── static/             # Static assets directory
│   ├── css/
│   │   └── style.css   # Chatbot frontend stylesheet
│   └── js/
│       └── chat.js     # Frontend logic for API calls and UI state
│
└── templates/          # Jinja2 templates directory
    └── index.html      # Home page containing the chat interface
```

Installation and Setup on the local device:
**Step 1:**

Before launching the Python application, make sure your llama.cpp server is up and running on port 8080 (or update the LLAMACPP_API_URL variable inside app.py to match your custom endpoint).
Example command to run the server locally:
```markdown
llama-server -m /path/to/qwen2.5-1.5b-instruct.Q4_K_M.gguf -c 4096 --port 8080
```
**Step 2: Setup the environment**
1. Clone this repository and navigate to the project's root folder.
2. Create a virtual environment (Recommended):
```markdown
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```
3. Install the Dependencies:
```markdown
pip install -r requirements.txt
```
**Step 3: Run the project**
Execute ``app.py`` fire up the FastAPI backend web server:
```markdown
python app.py
```

You can then access the interface at this link: ```http://localhost:5000```.
