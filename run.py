import subprocess
import multiprocessing
from pathlib import Path
import sys

def run_backend():
    try:
        subprocess.run(["python3", "-m", "flask", "--app", "backend.app", "run"])
    except KeyboardInterrupt:
        pass

def run_frontend():
    try:
        root = Path(__file__).resolve().parent
        frontend_dir = root / "frontend"
        subprocess.run(["npm", "run", "dev"], cwd=frontend_dir)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    backend_process = multiprocessing.Process(target=run_backend)
    frontend_process = multiprocessing.Process(target=run_frontend)
    
    backend_process.start()
    frontend_process.start()
    
    try:
        backend_process.join()
        frontend_process.join()
    except KeyboardInterrupt:
        print("\n⏹️  Остановка серверов...")
        backend_process.terminate()
        frontend_process.terminate()
        backend_process.join()
        frontend_process.join()
        print("✅ Серверы остановлены")
        sys.exit(0)
