import requests, time
t0 = time.time()
r = requests.post('http://localhost:8000/chat', json={'session_id':'test_bug','question':'稻飞虱怎么防治'}, timeout=130)
dt = time.time() - t0
print(f"Time: {dt:.1f}s")
print(f"Status: {r.status_code}")
data = r.json()
print(f"Answer: {data['answer'][:300]}")
print(f"Sources: {len(data['sources'])}")
for s in data['sources']:
    print(f"  - {s['title']} (relevance: {s['relevance']})")
