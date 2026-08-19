"""Entrypoint to launch the MadadgaarAI Web Dashboard & API Server."""
import uvicorn
from src.config import API_HOST, API_PORT

if __name__ == "__main__":
    print("\n=======================================================")
    print("      🚀 Launching MadadgaarAI Funding Platform        ")
    print("=======================================================")
    print(f"  • Web Dashboard : http://localhost:{API_PORT}")
    print(f"  • API Docs      : http://localhost:{API_PORT}/docs")
    print("=======================================================\n")
    uvicorn.run("src.api.main:app", host=API_HOST, port=API_PORT, reload=True)
