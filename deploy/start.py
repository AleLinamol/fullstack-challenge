"""Run two independent FastAPI processes in one free instance.

Only Orchestrator is public; Agent listens on loopback. Exit if either fails
so the hosting platform can restart the whole instance.
"""
import os
from pathlib import Path
import signal
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]

def main():
    if not os.environ.get("AGENT_KEY", "").strip():
        raise SystemExit("AGENT_KEY must be configured")
    port = int(os.environ.get("PORT", "8000"))
    if port == 8001:
        raise SystemExit("PORT 8001 is reserved for the internal Agent")
    env = {**os.environ, "AGENT_URL": "http://127.0.0.1:8001/rpc"}
    processes = []
    stopping = False

    def stop(signum, frame):
        nonlocal stopping
        stopping = True

    for sig in (signal.SIGINT, signal.SIGTERM, *([signal.SIGBREAK] if hasattr(signal, "SIGBREAK") else [])):
        signal.signal(sig, stop)
    try:
        for service, host, service_port in [("agent", "127.0.0.1", 8001), ("orchestrator", "0.0.0.0", port)]:
            processes.append(subprocess.Popen([sys.executable, "-m", "uvicorn", "app.main:app", "--host", host, "--port", str(service_port)], cwd=ROOT / "backend" / service, env=env))
        while not stopping:
            for process in processes:
                if process.poll() is not None:
                    return process.returncode or 1
            time.sleep(0.2)
        return 0
    finally:
        for process in processes:
            if process.poll() is None:
                process.terminate()
        for process in processes:
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()

if __name__ == "__main__":
    sys.exit(main())
