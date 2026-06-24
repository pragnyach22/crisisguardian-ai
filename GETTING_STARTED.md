# CrisisGuardian AI - Getting Started Guide

Welcome to CrisisGuardian AI! This guide will help you set up and run the application locally.

## 📋 Prerequisites

- **Python 3.10+** installed on your system
- **Git** for cloning the repository  
- **API Keys**:
  - Google Gemini API key (https://aistudio.google.com/app/apikey)
  - OpenWeatherMap API key (optional, https://openweathermap.org/api)

## 🚀 Quick Start (5 minutes)

### 1. Clone Repository
```bash
git clone https://github.com/crisisguardian-ai/crisisguardian-ai.git
cd crisisguardian-ai
```

### 2. Setup Environment
```bash
# Copy environment template
cp .env.template .env

# Edit .env with your API keys
# On Linux/Mac:
nano .env

# On Windows:
notepad .env
```

Add your Gemini API key:
```env
GEMINI_API_KEY=your_actual_key_here
BACKEND_HOST=127.0.0.1
BACKEND_PORT=8000
```

### 3. Install Dependencies
```bash
# Option A: Using uv (recommended)
uv sync
source .venv/bin/activate  # Mac/Linux
# or on Windows: .venv\Scripts\activate

# Option B: Using pip
pip install -r requirements.txt
```

### 4. Run Backend API
```bash
python main.py
```

You'll see:
```
Starting CrisisGuardian AI Backend Server on 127.0.0.1:8000...
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### 5. Run Frontend (in new terminal)
```bash
streamlit run frontend/app.py
```

You'll see:
```
  You can now view your Streamlit app in your browser.
  Local URL: http://localhost:8501
```

### 6. Test the Application
- Open http://localhost:8501 in your browser
- Navigate to "Disaster Analysis" page
- Enter a query like: "Is there a cyclone warning in Andhra Pradesh?"
- Click "Analyze Situation"

## 📚 Project Structure

```
crisisguardian-ai/
├── agents/                    # AI agents for different disaster types
├── backend/                   # FastAPI backend server
├── frontend/                  # Streamlit web dashboard
│   └── pages/                # Multi-page Streamlit app
├── tools/                     # Crisis tools (weather, news, resources)
├── workflows/                 # LangGraph orchestration
├── docs/                      # Documentation files
├── tests/                     # Unit tests
├── logging_config.py          # Centralized logging setup
├── error_handling.py          # Error handling & fallback utilities
├── main.py                    # Backend entrypoint
├── requirements.txt           # Python dependencies
├── .env.template              # Environment template
└── README.md                  # Project README
```

## 🔧 Configuration

### Environment Variables
Key variables in `.env`:

| Variable | Description | Required |
|----------|-------------|----------|
| `GEMINI_API_KEY` | Google Gemini API key | Yes |
| `OPENWEATHER_API_KEY` | OpenWeatherMap API key | No |
| `BACKEND_HOST` | Backend server host | No (default: 127.0.0.1) |
| `BACKEND_PORT` | Backend server port | No (default: 8000) |
| `LOG_LEVEL` | Logging level (INFO, WARNING, ERROR) | No (default: INFO) |

### Features Configuration
```env
ENABLE_MOCK_DATA=false              # Use mock data when APIs fail
ENABLE_DETAILED_LOGGING=false       # Enable detailed logging
```

## 🧪 Testing

### Run Unit Tests
```bash
pytest tests/ -v
```

### Run Specific Test
```bash
pytest tests/test_agents_tools.py::TestWeatherTool -v
```

### API Health Check
```bash
# In a new terminal
curl http://localhost:8000/health

# Response:
# {"status":"healthy","service":"CrisisGuardian AI"}
```

## 📡 API Endpoints

### Quick Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/system-status` | System operational status |
| GET | `/agent-status` | Individual agent status |
| POST | `/analyze` | Analyze disaster query |
| POST | `/resources` | Find emergency resources |
| POST | `/document-analysis` | Analyze uploaded PDF |
| POST | `/document-query` | Query uploaded document |
| POST | `/api/sos` | Trigger SOS alert |

### Example API Call
```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "message": "Heavy flooding in my area",
    "location": "Mumbai, India",
    "crisis_type": "flood"
  }'
```

Full API documentation: See `docs/API_DOCUMENTATION.md`

## 🐳 Docker Deployment

### Build and Run with Docker
```bash
# Build image
docker build -t crisisguardian-ai:latest .

# Run container
docker run -e GEMINI_API_KEY=your_key \
           -p 8000:8000 \
           -p 8501:8501 \
           crisisguardian-ai:latest
```

### Using Docker Compose
```bash
docker-compose up -d
```

## 🚨 Troubleshooting

### Issue: "GEMINI_API_KEY is not set"
**Solution:** 
- Edit `.env` file and add your actual API key
- Ensure you're using the correct key from https://aistudio.google.com

### Issue: "Port 8000 already in use"
**Solution:**
```bash
# Find and kill process using port 8000
lsof -i :8000
kill -9 <PID>

# Or change port in .env
BACKEND_PORT=8001
```

### Issue: "Module 'langchain' not found"
**Solution:**
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### Issue: Slow responses from agents
**Solution:**
- This is normal on first run (LLM initialization)
- Ensure GEMINI_API_KEY is valid and has quota
- Check network connectivity
- For testing, set `ENABLE_MOCK_DATA=true`

### Issue: Frontend can't connect to backend
**Solution:**
- Verify backend is running on http://localhost:8000
- Check BACKEND_URL in frontend code
- Ensure CORS is properly configured
- Check firewall settings

## 📖 Documentation

- **Architecture**: `docs/architecture.md`
- **API Docs**: `docs/API_DOCUMENTATION.md`
- **Deployment**: `docs/DEPLOYMENT_GUIDE.md`

## 🎯 Usage Examples

### Example 1: Flood Analysis
```
Query: "There's heavy flooding happening now in my locality. What should I do?"
Expected: Risk assessment + safety guidance + resource locations
```

### Example 2: Cyclone Verification
```
Query: "Is this true: Cyclone warning issued for Andhra Pradesh? I saw it on social media."
Expected: Verification status + weather updates + evacuation guidelines
```

### Example 3: Earthquake Response
```
Query: "Earthquake just happened. How should I ensure safety in my building?"
Expected: Immediate safety directive + aftershock warnings + resource locations
```

## 🔐 Security Notes

1. **Never commit `.env`** - It contains sensitive API keys
2. **Use HTTPS** in production
3. **Restrict CORS origins** in `.env`
4. **Implement rate limiting** for production
5. **Rotate API keys regularly**

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write tests for new features
5. Submit a pull request

## 📞 Support

- **Issues**: https://github.com/crisisguardian-ai/crisisguardian-ai/issues
- **Email**: support@crisisguardian.ai
- **Documentation**: https://crisisguardian-ai.readthedocs.io

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Google Gemini API for LLM capabilities
- LangGraph for agent orchestration
- Streamlit for the frontend framework
- FastAPI for the backend framework
- OpenWeatherMap for weather data
- OpenStreetMap for location services

---

**Happy Emergency Response! Stay Safe! 🛡️**
