import sys, traceback
f = open("error_log.txt", "w", encoding="utf-8")
f.write("1: importing chromadb...\n"); f.flush()
try:
    import chromadb
    f.write("2: chromadb imported\n")
except Exception:
    traceback.print_exc(file=f)
f.close()
print("done")