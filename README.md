# 🚀 EPOCH: Agentic README Generator (Nasiko Hackathon)

This project features an intelligent AI Agent built to automatically generate comprehensive, well-structured `README.md` files by recursively scanning a provided directory path. 

Built with **FastAPI**, **LangChain**, and **Google Gemini 2.5 Flash**, it safely navigates local directories to synthesize project structures, setup instructions, and usage guides without hallucinating.

---

## 🛠️ Usage Instructions

### 1. Installation
Ensure you have Python 3 installed. Clone the repository and run the following commands:
```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment 
# Windows: venv\Scripts\activate 
# Mac/Linux: source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

#run
uvicorn app.__main__:app --reload

#run via docker
docker-compose up --build

#<------USE THIS BACKUP KEY IF THE PREVIOUs KEY get exhausted or expired --->

GOOGLE_API_KEY=AIzaSyBzygmbVKFKsMajudpiOohJ5dNdIopBXqI(THIS IS BACKUP KEY)

# GIVE INPUT AS this 
{
  "folder_path": "D:/CODING/CA"
}

----

## 🧠 Agent Design

The agent operates on a modular, tool-calling architecture:
* **Tool 1 (`get_project_structure`)**: Safely maps the directory tree, dynamically ignoring heavy utility folders.
* **Tool 2 (`read_project_files`)**: Reads file contents intelligently, explicitly designed to handle memory constraints and file-reading errors.
* **LLM Orchestration (`app/agents.py`)**: A highly optimized prompt strictly instructs the agent to analyze the extracted context and format it into professional Markdown.

---

## 🛡️ Edge Case Handling (My AI is capable of handling edge cases!)

This agent was specifically engineered to survive messy, real-world repositories without breaking the context window. **My AI is fully capable of handling the following edge cases natively:**

1. **Empty Files**: Handled cleanly. The agent reads 0-byte files and injects `[EMPTY FILE]` into the prompt to prevent the LLM from hallucinating functionality.
2. **Incomplete Code**: Handled via Prompt Engineering. If the agent detects stubbed functions (e.g., `pass` or `TODO`), it acknowledges them gracefully in a "Future Work" section rather than inventing fake logic.
3. **Large Folders / Nested Structures**: Heavily nested directories or dependency folders (like `.git`, `__pycache__`, `node_modules`, `venv`) are strictly filtered out during traversal to protect token limits.
4. **Massive Files**: Individual files exceeding 10,000 characters are gracefully truncated before being sent to the LLM to prevent context window overflow.
5. **🔒 Security & Secret Leakage**: The agent explicitly drops known secret files (like `.env`, `secrets.json`, `.env.local`) from the file reading process. Furthermore, the LLM is instruction-tuned to redact any hardcoded API keys it finds inside standard source code files.

---



