print("step2 start")
import sys, traceback
sys.path.insert(0, ".")
try:
    from backend.rag.embedding import OllamaEmbedding
    print("step2 embedding imported")
    e = OllamaEmbedding()
    print("step2 instance created, testing embed...")
    v = e.embed("测试文本")
    print("step2 embed OK, dim:", len(v))
except Exception:
    traceback.print_exc()