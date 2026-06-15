import time, sys, traceback
sys.path.insert(0, '.')
f = open("error_log.txt", "w", encoding="utf-8")

def step(n, desc, code):
    f.write(f"step {n}: {desc}... "); f.flush()
    t0 = time.time()
    try:
        exec(code)
        f.write(f"OK ({time.time()-t0:.1f}s)\n"); f.flush()
    except Exception:
        f.write(f"FAIL\n"); f.flush()
        traceback.print_exc(file=f)
        f.flush()

step(1, "config", "from backend.config import DATABASE_URL")
step(2, "llm.provider", "from backend.llm.provider import OllamaProvider")
step(3, "rag.embedding", "from backend.rag.embedding import OllamaEmbedding")
step(4, "numpy", "import numpy")
step(5, "rag.retriever", "from backend.rag.retriever import Retriever")
step(6, "llm.prompts", "from backend.llm.prompts import build_prompt")
step(7, "db.models", "from backend.db.models import init_db")
step(8, "routes.chat", "from backend.routes.chat import router")
step(9, "routes.admin", "from backend.routes.admin import router")
step(10, "main app", "from backend.main import app")

f.write("\nALL IMPORTS OK\n")
f.close()
print("done, check error_log.txt")
