import sys, traceback
sys.path.insert(0, ".")

f = open("error_log.txt", "w", encoding="utf-8")
f.write("step3 starting import...\n")
f.flush()

try:
    from backend.rag.embedding import OllamaEmbedding
    f.write("embedding imported\n")
    f.flush()
    e = OllamaEmbedding()
    f.write("instance created, embedding test text...\n")
    f.flush()
    v = e.embed("测试")
    f.write(f"embed OK!!! dim: {len(v)}\n")
except Exception:
    traceback.print_exc(file=f)
f.close()
print("check error_log.txt")