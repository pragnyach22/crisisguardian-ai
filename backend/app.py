"""
Legacy entry point — the active backend is backend.api (used by main.py).
Re-exports the FastAPI app for backward compatibility.
"""

from backend.api import app

__all__ = ["app"]
