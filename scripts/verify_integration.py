"""Run production frontend browser tests against both real FastAPI services."""
import os
from pathlib import Path
import subprocess
import time
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
PYTHON = ROOT / ".venv" / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
env = {**os.environ, "AGENT_KEY": "local-integration-only", "AGENT_URL": "http://127.0.0.1:8001/rpc", "ORCHESTRATOR_URL": "http://127.0.0.1:8000", "INTEGRATION": "1"}
processes = []
try:
    for service, port in [("agent", 8001), ("orchestrator", 8000)]:
        processes.append(subprocess.Popen([str(PYTHON), "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", str(port)], cwd=ROOT / "backend" / service, env=env))
    for port in [8001, 8000]:
        for attempt in range(50):
            try:
                urllib.request.urlopen(f"http://127.0.0.1:{port}/openapi.json", timeout=1)
                break
            except OSError:
                time.sleep(0.2)
        else:
            raise RuntimeError(f"Service {port} did not start")
    subprocess.run(["node", "node_modules/@playwright/test/cli.js", "test"], cwd=ROOT / "frontend", env=env, check=True)
finally:
    for process in processes:
        process.terminate()
    for process in processes:
        process.wait(timeout=10)
