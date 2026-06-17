"""集中管理所有配置项——改参数只改这一个文件。"""
import os

# === Ollama 配置 ===
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
LLM_MODEL = os.getenv("LLM_MODEL", "qwen2.5:3b")
EMBED_MODEL = os.getenv("EMBED_MODEL", "shaw/dmeta-embedding-zh")

# === Chroma 配置 ===
CHROMA_PERSIST_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "chroma_db")
CHROMA_COLLECTION_NAME = "rice_knowledge"
RETRIEVAL_TOP_K = 3  # 4b 小模型每次最多塞 3 个片段
MIN_RELEVANCE_SCORE = 0.35  # 最低相关度阈值，低于此分数的结果不返回给 LLM

# === 文档处理配置 ===
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

# === 数据库配置 ===
DATABASE_URL = os.path.join(os.path.dirname(__file__), "..", "rice-qa.db")

# === 会话配置 ===
MAX_HISTORY_TURNS = 6
