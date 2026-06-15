"""LLM 抽象层：定义统一接口，后续可切换 Ollama / DeepSeek / 通义千问。"""
from abc import ABC, abstractmethod
import ollama
from backend.config import OLLAMA_HOST, LLM_MODEL


class LLMProvider(ABC):
    """所有 LLM 后端的抽象基类。"""

    @abstractmethod
    async def generate(self, messages: list[dict]) -> str:
        """接收 messages（OpenAI 格式），返回生成的文本。"""
        ...


class OllamaProvider(LLMProvider):
    """Ollama 本地模型实现。"""

    def __init__(self, host: str = OLLAMA_HOST, model: str = LLM_MODEL):
        self.client = ollama.AsyncClient(host=host)
        self.model = model

    async def generate(self, messages: list[dict]) -> str:
        response = await self.client.chat(
            model=self.model,
            messages=messages,
            options={"temperature": 0.3}
        )
        return response["message"]["content"]
