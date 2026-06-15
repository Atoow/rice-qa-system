import sys, traceback
sys.path.insert(0, ".")

f = open("error_log.txt", "w", encoding="utf-8")

def test(step, code):
    f.write(f"step {step}: "); f.flush()
    try:
        exec(code)
        f.write("OK\n"); f.flush()
    except:
        f.write("FAIL\n")
        traceback.print_exc(file=f)
        f.flush()

test(1, "from backend.config import DATABASE_URL")
test(2, "from backend.llm.provider import OllamaProvider")
test(3, "from backend.rag.embedding import OllamaEmbedding")
test(4, "import numpy; print('numpy ok', file=f)")
test(5, "from backend.rag.retriever import Retriever")
test(6, "from backend.llm.prompts import build_prompt")
test(7, "from backend.db.models import init_db")
test(8, "from backend.routes.chat import router")
test(9, "from backend.routes.admin import router")

f.write("\n=== all imports done ===\n")
f.close()
print("done, check error_log.txt")