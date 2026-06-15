print("step1 start")
import sys, traceback
sys.path.insert(0, ".")
print("step1 path set")
try:
    from backend.config import OLLAMA_HOST
    print("step1 config OK:", OLLAMA_HOST)
except Exception as e:
    print("step1 ERROR:", e)
