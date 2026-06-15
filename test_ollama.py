import traceback
f = open("error_log.txt", "w", encoding="utf-8")
f.write("importing ollama...\n")
f.flush()
try:
    import ollama
    f.write(f"ollama imported, version: {ollama.__version__}\n")
    c = ollama.Client(host="http://localhost:11434")
    f.write("client created, listing models...\n")
    f.write(str(c.list()))
except Exception as e:
    f.write(f"ERROR: {e}\n")
    traceback.print_exc(file=f)
f.close()
print("done")