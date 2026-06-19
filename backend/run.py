import os

import uvicorn

if __name__ == "__main__":
    # Ensure hidden logs directory exists to avoid crash
    os.makedirs(".logs", exist_ok=True)

    # Run uvicorn programmatically to exclude .logs and prevent spam reload loops
    uvicorn.run(
        "backend.app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_excludes=[".logs/*", "*.log"],
    )
