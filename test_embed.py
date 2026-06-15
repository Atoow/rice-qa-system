import sys, traceback
sys.path.insert(0, ".")

f = open("error_log.txt", "w", encoding="utf-8")
f.write("1: import ollama\n"); f.flush()
try:
    import ollama
    f.write("2: ollama OK\n"); f.flush()
    c = ollama.Client(host="http://localhost:11434")
    f.write("3: client OK\n"); f.flush()
    r = c.embed(model="shaw/dmeta-embedding-zh", input="测试")
    f.write(f"4: embed OK, dim={len(r['embeddings'][0])}\n")
except Exception:
    traceback.print_exc(file=f)
f.close()
print("done")