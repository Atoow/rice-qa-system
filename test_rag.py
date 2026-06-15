import requests, time

questions = [
    "水稻抽穗期怎么管理水肥？",
    "稻飞虱怎么防治？",
    "水稻播种前种子怎么处理？",
]

for q in questions:
    t0 = time.time()
    try:
        r = requests.post('http://localhost:8000/chat',
            json={'session_id': 'test4b', 'question': q}, timeout=130)
        dt = time.time() - t0
        data = r.json()
        print(f"\n{'='*50}")
        print(f"Q: {q}")
        print(f"Time: {dt:.1f}s  Status: {r.status_code}")
        print(f"A: {data['answer'][:150]}...")
        print(f"Sources: {len(data['sources'])}")
        for s in data['sources']:
            print(f"  - {s['title']} ({s['relevance']})")
    except Exception as e:
        print(f"ERROR: {e}")

print("\nDone!")
