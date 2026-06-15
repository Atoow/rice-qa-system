import sys, traceback
sys.path.insert(0, ".")
f = open("error_log.txt", "w", encoding="utf-8")
f.write("testing chromadb...\n"); f.flush()
try:
    import chromadb
    f.write(f"chromadb OK, version: {chromadb.__version__}\n")
except Exception:
    traceback.print_exc(file=f)
f.close()
print("done")