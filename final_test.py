import sys, traceback
sys.path.insert(0, ".")

f = open("error_log.txt", "w", encoding="utf-8")
f.write("=== START ===\n"); f.flush()

try:
    f.write("importing main...\n"); f.flush()
    from backend.main import app
    f.write(f"app OK: {app.title}\n")
    f.write("=== SUCCESS ===\n")
except Exception:
    f.write("=== FAIL ===\n")
    traceback.print_exc(file=f)
f.close()
print("done")