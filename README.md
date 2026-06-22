# CrisisGuardian AI 🛡️

CrisisGuardian AI is a premium, multi-agent emergency response assistant designed to guide users safely through natural disasters and domestic hazards. Utilizing **Gemini 2.5 Flash**, **LangGraph**, and **FastAPI**, it routes emergency questions to specialized agents (Flood, Cyclone, Earthquake, Fire) and queries real-time information using built-in crisis tools.

---

## 🌟 Key Features
- **Supervisor-Led Dispatcher Routing**: Automatically classifies inquiries and delegates response tasks to specialized agents.
- **Crisis Specialists**: Four distinct AI agents pre-conditioned with life-saving safety policies (Floods, Cyclones, Earthquakes, Fires).
- **Integrated Action Tools**: Supports finding shelter locations, query USGS for live earthquake alerts, retrieving weather bulletins, and triggering SOS emergency broadcasts.
- **Glassmorphic Streamlit UI**: A premium dark-themed dashboard presenting live warnings, simulated SOS triggers, dynamic crisis scenario panels, and interactive chat.
- **Graceful Offline Fallbacks**: Automatically falls back to mock logic if Gemini API keys are not supplied.

---

## 📂 Project Structure

```
crisisguardian-ai/
├── agents/                 # Specialized LLM Agents (Gemini 2.5 Flash + LangChain)
│   ├── __init__.py
│   ├── base_agent.py       # Core base class configuration
│   └── disaster_agents.py  # Flood, Cyclone, Earthquake, Fire & Supervisor agents
├── workflows/              # LangGraph multi-agent coordination state chart
│   ├── __init__.py
│   └── disaster_workflow.py
├── tools/                  # Custom tools (Weather warnings, USGS API, shelter locator, SOS alerts)
│   ├── __init__.py
│   └── disaster_tools.py
├── backend/                # FastAPI REST API controller
│   ├── __init__.py
│   └── app.py
├── frontend/               # Streamlit interactive UI dashboard
│   └── app.py
├── docs/                   # System design, architecture diagrams, and guides
│   └── architecture.md
├── screenshots/            # UI walkthrough visual assets
├── requirements.txt        # Project dependencies
├── .env                    # Environment config templates
├── main.py                 # Backend runner entrypoint
└── README.md
```

---

## ⚡ Quickstart Guide

### 1. Prerequisites
Ensure you have Python 3.10+ and the modern `uv` package manager installed.

### 2. Environment Configuration
Create a copy of `.env` or edit the template directly to add your Gemini API Key:
```env
GEMINI_API_KEY=AIzaSy...
```

### 3. Launching the Backend API
Start the FastAPI server via the root `main.py` entrypoint. The API will listen on `127.0.0.1:8000`:
```bash
python main.py
```

### 4. Running the Streamlit Interface
In another terminal session (with the virtual environment active), launch the dashboard:
```bash
streamlit run frontend/app.py
```

---

## 🛠️ Tech Stack
- **AI Engine**: Google Gemini 2.5 Flash via `langchain-google-genai`
- **Orchestration**: LangGraph StateGraph
- **Backend Frame**: FastAPI (Uvicorn server)
- **Frontend Panel**: Streamlit Web UI
- **Environment**: Python Dotenv, Uv package manager
