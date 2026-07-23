from functools import wraps
from ..utils.logger import write_log
import sys, time
from ..messages import load_messages

msg = load_messages(lang="ko")

def handle_error(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError as e:
            print(msg["ERR_filenotfound"])
            print(f"원인 : {e}")
            print(msg["HINT_filenotfound"])
            sys.exit(1)

        except ValueError as e:
            print(msg["ERR_value"])
            print(f"원인 : {e}")
            print(msg["HINT_value"])
            sys.exit(2)

        except KeyboardInterrupt:
            print("\n" + msg["ERR_keyboardinter"])
            print(msg["HINT_keyboardinter"])
            sys.exit(130)

        except Exception as e:
            print(msg["ERR_except"])
            print(f"원인 : {e}")
            print(msg["HINT_except"])
            sys.exit(99)
    return wrapper

def log_command(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        write_log(" ".join(sys.argv))
        return func(*args, **kwargs)
    return wrapper

def measure_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"{func.__name__}: {end-start:.4f}s")
        return result
    return wrapper