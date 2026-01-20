import subprocess
from pathlib import Path


def test_frontend_build():
    root = Path(__file__).resolve().parents[1]
    frontend_dir = root / "frontend"
    result = subprocess.run(
        ["npm", "run", "build"],
        cwd=frontend_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    assert result.returncode == 0, result.stdout
