# CrisisGuardian AI 🛡️

CrisisGuardian AI is a premium, multi-agent emergency response assistant designed to guide users safely through natural disasters and domestic hazards. Utilizing **Gemini 2.5 Flash**, **LangGraph**, and **FastAPI**, it routes emergency questions to specialized agents (Flood, Cyclone, Earthquake, Fire) and queries real-time information using built-in crisis tools.

---

## 🌟 Key Features
- **Supervisor-Led Dispatcher Routing**: Automatically classifies inquiries and delegates response tasks to specialized agents.
- **Crisis Specialists**: Four distinct AI agents pre-conditioned with life-saving safety policies (Floods, Cyclones, Earthquakes, Fires).
- **Integrated Action Tools**: Supports finding shelter locations, querying USGS for live earthquake alerts, retrieving weather bulletins, and triggering SOS emergency broadcasts.
- **Glassmorphic Streamlit UI**: A premium dark-themed dashboard presenting live warnings, simulated SOS triggers, dynamic crisis scenario panels, and interactive chat.
- **Graceful Offline Fallbacks**: Automatically falls back to mock logic if external APIs are unavailable.

---

## 📂 Project Structure

```
crisisguardian-ai/
├── agents/                 # Specialized LLM Agents (Gemini 2.5 Flash + LangChain)
│   ├── base_agent.py       # Core base class configuration
│   ├── disaster_agents.py  # Flood, Cyclone, Earthquake, Fire & Supervisor agents
│   └── coordinator_agent.py
├── workflows/              # LangGraph multi-agent coordination state chart
│   └── crisis_workflow.py
├── tools/                  # Custom tools (Weather, News, Resources, Disaster utils)
│   ├── weather_tool.py
│   ├── news_tool.py
│   ├── resource_tool.py
│   └── disaster_tools.py
├── backend/                # FastAPI backend (entry: backend/api.py)
│   └── api.py
├── frontend/               # Streamlit interactive UI dashboard
│   ├── app.py
│   └── pages/              # 7 multi-page app views
├── docs/                   # System design, architecture diagrams, and guides
├── tests/                  # Unit tests
├── error_handling.py       # Graceful fallbacks and offline mode
├── logging_config.py       # Centralized logging setup
├── verify_setup.py         # Automated setup verification
├── Dockerfile              # Backend container
├── Dockerfile.streamlit    # Frontend container
├── docker-compose.yml      # Multi-container deployment
├── requirements.txt
├── .env.template           # Environment config template
├── main.py                 # Backend runner entrypoint
└── README.md
```

---

## ⚡ Quickstart Guide

### 1. Prerequisites
Ensure you have Python 3.10+ installed.

### 2. Environment Configuration
```bash
cp .env.template .env
# Edit .env and set GEMINI_API_KEY (and optionally OPENWEATHER_API_KEY)
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Verify Setup
```bash
python verify_setup.py
```

### 5. Launch the Backend API
```bash
python main.py
```
The API listens on `http://127.0.0.1:8000`.

### 6. Run the Streamlit Interface
In another terminal:
```bash
streamlit run frontend/app.py
```
Open `http://localhost:8501`.

### 7. Docker (optional)
```bash
docker-compose up -d
```

---

## 🛠️ Tech Stack
- **AI Engine**: Google Gemini 2.5 Flash via `langchain-google-genai`
- **Orchestration**: LangGraph StateGraph
- **Backend**: FastAPI (Uvicorn server)
- **Frontend**: Streamlit Web UI
- **Vector DB**: FAISS (document RAG)
- **APIs**: OpenWeatherMap, USGS, OpenStreetMap Nominatim

---

## 📖 Documentation
- [Getting Started](GETTING_STARTED.md)
- [API Reference](docs/API_DOCUMENTATION.md)
- [Deployment Guide](docs/DEPLOYMENT_GUIDE.md)
- [Architecture](docs/architecture.md)

---

## License
MIT — see [LICENSE](LICENSE).
