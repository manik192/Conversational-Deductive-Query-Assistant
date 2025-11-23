# Conversational Deductive Query Assistant

A Streamlit-based application that allows users to query relational databases using natural language. The system generates SQL using AI models, executes queries on the selected database, and returns results in both tabular and visual formats.

Team Members
Manikanta Reddy Peram - 801450154
 Rishikesh Reddy Regatte - 801449827
 Shreya Sankireddy - 801452385
 Sweehoney Bojja - 801425033
 Veeru Saketh Ramireddigari - 801428970

The application is hosted at:
```
https://conversational-deductive-query-assistant-mvhd9wu2bkcxxya5z5c67.streamlit.app/
```

## Table of Contents
- [Installation and Setup](#installation-and-setup)
- [Running the Application](#running-the-application)
- [Folder Structure](#folder-structure)
- [Deployment](#deployment)

---

## Installation and Setup

### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)
- Git (optional)
- API keys for AI providers (optional)
- Local model files - GGUF or Hugging Face models (optional)

### Clone the Repository
```bash
git clone https://github.com/manik192/Conversational-Deductive-Query-Assistant.git
cd Conversational-Deductive-Query-Assistant
```

### Create a Virtual Environment

**MacOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows PowerShell:**
```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### Install Dependencies

Install main dependencies:
```bash
pip install -r requirements.txt
```

Install optional GGUF model support:
```bash
pip install -r requirements-gguf.txt
```

### Key Libraries
- streamlit
- pandas
- sqlalchemy
- python-dotenv
- Database drivers (SQLite/PostgreSQL/MySQL)
- Optional provider SDKs (OpenAI, Gemini, Anthropic, etc.)
- Optional local model libraries (gpt4all, transformers)

---

## Running the Application

Start the application:
```bash
streamlit run app.py
```

Streamlit will provide a local URL (usually `http://localhost:8501`). Open it in your browser.

### Usage Flow
1. Select a database from the sidebar
2. (Optional) Generate or refresh the database schema
3. Select an AI model
4. Enter a natural language question
5. View the generated SQL and results
6. Enable chart options (bar, pie, line) if desired

---

## Folder Structure

```
Conversational-Deductive-Query-Assistant/
│
├── app.py                        # Main Streamlit application
├── requirements.txt              # Dependency list
├── requirements-gguf.txt         # Optional GGUF dependencies
│
├── data/
│   ├── config/                   # Model and database configuration JSON files
│   ├── sample/                   # Example SQLite DBs or datasets
│   ├── models/                   # Local AI model files (e.g., .gguf)
│   └── schemas/                  # Auto-generated schema files
│
├── models/                       # AI model integration modules
│   ├── base_model.py
│   ├── openai_model.py
│   ├── gemini_model.py
│   ├── anthropic_model.py
│   ├── deep_seek_model.py
│   ├── grok_model.py
│   ├── local_model.py
│   └── local_gguf_model.py
│
├── helpers/                      # Utility functions
│   ├── chart.py
│   ├── db.py
│   ├── file.py
│   ├── model.py
│   ├── prompt.py
│   ├── response.py
│   ├── schema.py
│   └── string.py
│
├── db/                           # Database connection layer
│   ├── base_database.py
│   └── sql_database.py
│
├── charts/                       # Visualization modules
│   ├── bar_chart.py
│   ├── line_chart.py
│   ├── pie_chart.py
│   ├── heatmap_chart.py
│   └── map_chart.py
│
└── extras/                       # Images, icons, static assets
```

---

## Deployment

### Streamlit Community Cloud



**Deploy Your Own Version:**

1. Push your repository to GitHub
2. Go to [https://share.streamlit.io/](https://share.streamlit.io/) and create a new app
3. Configure:
   - Repository: your GitHub repository
   - Branch: main
   - Entry file: app.py
4. Add API keys under **Secrets** (App Settings → Secrets):
   ```ini
   OPENAI_API_KEY = "..."
   GEMINI_API_KEY = "..."
   ANTHROPIC_API_KEY = "..."
   DEEPSEEK_API_KEY = "..."
   GROK_API_KEY = "..."
   ```
5. Click **Deploy**

### Local Server Deployment

1. Clone the repository
2. Set environment variables (API keys if needed)
3. Install dependencies in a virtual environment
4. Run:
   ```bash
   streamlit run app.py
   ```
