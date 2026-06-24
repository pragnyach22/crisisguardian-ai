#!/usr/bin/env python
"""
CrisisGuardian AI - System Verification Script
Tests all components and ensures proper setup.
"""

import os
import sys
import subprocess
import time
from pathlib import Path
from dotenv import load_dotenv

# Colors for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'
CHECK = '✓'
CROSS = '✗'

def print_header(text: str):
    """Print section header."""
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}{text.center(60)}{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")

def print_check(text: str, status: bool, details: str = ""):
    """Print check result."""
    symbol = f"{GREEN}{CHECK}{RESET}" if status else f"{RED}{CROSS}{RESET}"
    print(f"{symbol} {text}")
    if details:
        print(f"  → {details}")

def check_python_version():
    """Check Python version."""
    print_header("PYTHON VERSION CHECK")
    version = sys.version_info
    required = (3, 10)
    is_valid = version >= required
    print_check(
        f"Python version >= 3.10",
        is_valid,
        f"Current: {version.major}.{version.minor}.{version.micro}"
    )
    return is_valid

def check_environment_file():
    """Check .env file exists and has required keys."""
    print_header("ENVIRONMENT CONFIGURATION")
    env_path = Path(".env")
    env_template = Path(".env.template")
    
    has_env = env_path.exists()
    print_check(".env file exists", has_env)
    
    if has_env:
        load_dotenv()
        gemini_key = os.getenv("GEMINI_API_KEY")
        has_key = gemini_key and gemini_key != "your_gemini_api_key_here"
        print_check("GEMINI_API_KEY configured", has_key)
        
        backend_host = os.getenv("BACKEND_HOST", "127.0.0.1")
        backend_port = os.getenv("BACKEND_PORT", "8000")
        print_check(
            "Backend configured",
            True,
            f"{backend_host}:{backend_port}"
        )
        return has_env and has_key
    else:
        if env_template.exists():
            print(f"\n  {YELLOW}Hint:{RESET} Copy .env.template to .env and add your API keys")
        return False

def check_dependencies():
    """Check if all required packages are installed."""
    print_header("DEPENDENCIES CHECK")
    
    required_packages = [
        ("langchain", "langchain", "LLM Framework"),
        ("langgraph", "langgraph", "Agent Orchestration"),
        ("fastapi", "fastapi", "Backend Framework"),
        ("streamlit", "streamlit", "Frontend Framework"),
        ("pydantic", "pydantic", "Data Validation"),
        ("requests", "requests", "HTTP Library"),
        ("python-dotenv", "dotenv", "Environment Config")
    ]
    
    all_installed = True
    for package_name, import_name, description in required_packages:
        try:
            __import__(import_name)
            print_check(f"{description} ({package_name})", True)
        except ImportError:
            print_check(f"{description} ({package_name})", False)
            all_installed = False
    
    return all_installed

def check_directory_structure():
    """Check if project directories exist."""
    print_header("PROJECT STRUCTURE")
    
    required_dirs = {
        "agents": "AI Agents",
        "tools": "Crisis Tools",
        "workflows": "LangGraph Workflows",
        "backend": "Backend Server",
        "frontend": "Frontend UI",
        "docs": "Documentation",
    }
    
    all_exist = True
    for directory, description in required_dirs.items():
        exists = Path(directory).is_dir()
        print_check(f"{description} ({directory}/)", exists)
        all_exist = all_exist and exists
    
    return all_exist

def check_api_connectivity():
    """Check if backend API is running."""
    print_header("API CONNECTIVITY")
    
    try:
        import requests
        response = requests.get("http://127.0.0.1:8000/health", timeout=2)
        is_healthy = response.status_code == 200
        print_check("Backend API running", is_healthy)
        if is_healthy:
            data = response.json()
            print(f"  → Service: {data.get('service', 'Unknown')}")
        return is_healthy
    except requests.exceptions.ConnectionError:
        print_check("Backend API running", False, "Start with: python main.py")
        return False
    except Exception as e:
        print_check("Backend API running", False, str(e))
        return False

def check_agents():
    """Check if agent modules can be imported."""
    print_header("AGENTS MODULE CHECK")
    
    agents = [
        "FloodAgent",
        "CycloneAgent",
        "EarthquakeAgent",
        "FireAgent",
        "EmergencySupervisorAgent"
    ]
    
    all_loaded = True
    try:
        from agents.disaster_agents import (
            FloodAgent, CycloneAgent, EarthquakeAgent,
            FireAgent, EmergencySupervisorAgent
        )
        for agent in agents:
            print_check(f"{agent}", True)
    except ImportError as e:
        print_check("Agents module", False, str(e))
        all_loaded = False
    
    return all_loaded

def check_tools():
    """Check if tool modules can be imported."""
    print_header("TOOLS MODULE CHECK")
    
    tools = ["WeatherTool", "NewsTool", "ResourceTool"]
    
    all_loaded = True
    try:
        from tools.weather_tool import WeatherTool
        from tools.news_tool import NewsTool
        from tools.resource_tool import ResourceTool
        
        print_check("WeatherTool", True)
        print_check("NewsTool", True)
        print_check("ResourceTool", True)
        
        # Test instantiation
        wt = WeatherTool()
        nt = NewsTool()
        rt = ResourceTool()
        print_check("Tool instantiation", True)
    except Exception as e:
        print_check("Tools module", False, str(e))
        all_loaded = False
    
    return all_loaded

def check_workflow():
    """Check if workflow can be created."""
    print_header("WORKFLOW CHECK")
    
    try:
        from workflows.crisis_workflow import create_crisis_workflow
        workflow = create_crisis_workflow()
        print_check("Workflow creation", workflow is not None)
        return True
    except Exception as e:
        print_check("Workflow creation", False, str(e))
        return False

def run_quick_tests():
    """Run quick unit tests."""
    print_header("RUNNING QUICK TESTS")
    
    try:
        import pytest
        
        # Run specific test file via Python executable to avoid missing PATH issues
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "tests/test_agents_tools.py", "-v", "--tb=short", "-x"],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        if result.returncode == 0:
            print_check("Unit tests passed", True)
            # Count passed tests
            passed = result.stdout.count(" PASSED")
            print(f"  → {passed} tests passed")
            return True
        else:
            print_check("Unit tests", False)
            print(result.stdout[-500:] if len(result.stdout) > 500 else result.stdout)
            return False
    except FileNotFoundError:
        print_check("pytest installed", False, "Install with: pip install pytest")
        return False
    except subprocess.TimeoutExpired:
        print_check("Unit tests", False, "Timeout")
        return False
    except Exception as e:
        print_check("Unit tests", False, str(e))
        return False

def main():
    """Run all verification checks."""
    print(f"\n{BLUE}")
    print("╔════════════════════════════════════════════════════════╗")
    print("║         CrisisGuardian AI - System Verification         ║")
    print("╚════════════════════════════════════════════════════════╝")
    print(f"{RESET}")
    
    results = {}
    
    # Run all checks
    results["Python Version"] = check_python_version()
    results["Environment"] = check_environment_file()
    results["Dependencies"] = check_dependencies()
    results["Directory Structure"] = check_directory_structure()
    results["Agents Module"] = check_agents()
    results["Tools Module"] = check_tools()
    results["Workflow"] = check_workflow()
    results["API Connectivity"] = check_api_connectivity()
    
    # Optional: run tests if all basics pass
    if all([results["Python Version"], results["Dependencies"], results["Directory Structure"]]):
        results["Unit Tests"] = run_quick_tests()
    
    # Summary
    print_header("VERIFICATION SUMMARY")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for check_name, status in results.items():
        symbol = f"{GREEN}{CHECK}{RESET}" if status else f"{RED}{CROSS}{RESET}"
        print(f"{symbol} {check_name}")
    
    print(f"\n{BLUE}Results: {passed}/{total} checks passed{RESET}")
    
    if passed == total:
        print(f"\n{GREEN}✓ All checks passed! System is ready to use.{RESET}")
        print(f"\n{BLUE}Next steps:{RESET}")
        print("1. Run backend: python main.py")
        print("2. Run frontend: streamlit run frontend/app.py")
        print("3. Open http://localhost:8501 in your browser")
        return 0
    else:
        print(f"\n{YELLOW}⚠ Some checks failed. Please review the issues above.{RESET}")
        if not results.get("API Connectivity"):
            print(f"\n{BLUE}Hint:{RESET} Start the backend server in another terminal:")
            print("  python main.py")
        return 1

if __name__ == "__main__":
    sys.exit(main())
