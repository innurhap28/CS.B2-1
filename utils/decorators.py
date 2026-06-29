from functools import wraps
from utils.logger import write_log
import sys

def handle_error(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"[ERROR] {e}")
    return wrapper

def log_command(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        write_log(" ".join(sys.argv))
        return func(*args, **kwargs)
    return wrapper