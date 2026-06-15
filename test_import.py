import traceback, sys
sys.path.insert(0, ".")
try:
    from backend.main import app
    print("SUCCESS")
except Exception:
    traceback.print_exc()
