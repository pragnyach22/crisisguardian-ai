"""
CrisisGuardian AI - Main Entrypoint
This script loads the environment variables and runs the FastAPI backend server using Uvicorn.
"""

import os
import uvicorn
from dotenv import load_dotenv

from logging_config import configure_logging

# Load environment variables from .env file
load_dotenv()
configure_logging()

if __name__ == "__main__":
    host = os.getenv("BACKEND_HOST", "127.0.0.1")
    port = int(os.getenv("BACKEND_PORT", "8000"))
    
    print(f"Starting CrisisGuardian AI Backend Server on {host}:{port}...")
    
    # Import the FastAPI application from backend module
    # Run Uvicorn server programmatically
    uvicorn.run(
        "backend.api:app",
        host=host,
        port=port,
        reload=True
    )

