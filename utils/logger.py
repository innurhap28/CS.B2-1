from pathlib import Path
from datetime import datetime

LOG_FILE = Path("logs/command.log")
LOG_FILE.parent.mkdir(exist_ok=True)

def write_log(command: str):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{now}] {command}\n")