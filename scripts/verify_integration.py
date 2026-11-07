"""Run production frontend browser tests against both real FastAPI services."""
import os
from pathlib import Path
import subprocess
import signal
import time
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
PYTHON = ROOT / ".venv" / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
env = {**os.environ, "AGENT_KEY": "local-integration-only", "AGENT_URL": "http://127.0.0.1:8001/rpc", "ORCHESTRATOR_URL": "http://127.0.0.1:8000", "INTEGRATION": "1"}
processes = []
try:
    combined = os.environ.get("COMBINED") == "1"
    if combined:
        processes.append(subprocess.Popen([str(PYTHON), "deploy/start.py"], cwd=ROOT, env={**env, "PORT": "8000"}, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == "nt" else 0))
    else:
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
    assert urllib.request.urlopen("http://127.0.0.1:8000/health").status == 200
    subprocess.run(["node", "node_modules/@playwright/test/cli.js", "test"], cwd=ROOT / "frontend", env=env, check=True)
finally:
    for process in processes:
        if os.environ.get("COMBINED") == "1" and os.name == "nt":
            process.send_signal(signal.CTRL_BREAK_EVENT)
        else:
            process.terminate()
    for process in processes:
        process.wait(timeout=20)
