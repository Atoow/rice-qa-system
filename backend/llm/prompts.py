"""Prompt 模板和构建函数。"""
from backend.config import RETRIEVAL_TOP_K

# 每个知识片段最多喂给 LLM 的字符数（4b 小模型不能太多）
MAX_CHUNK_CHARS = 250

SYSTEM_PROMPT = """你是一个专业的水稻种植顾问。请严格遵守以下规则回答问题：

1. 基于知识库内容直接回答，不要写"参考来源：xxx"（来源由系统自动标注）
2. 如果知识库内容不包含相关信息，请回答："这个问题我暂时无法回答，建议咨询当地农技站或拨打12316农业服务热线。"
3. 回答要通俗易懂，适合农民理解。使用短句，避免长段落。
4. 如果涉及农药使用，务必提醒："用药前请阅读说明书，注意安全间隔期。"
5. 尽量给出可操作的具体建议（时间、用量、方法），而不是笼统的原则。"""


def build_prompt(
    user_question: str,
    retrieved_chunks: list[str],
    sources: list[str],
    history: list[dict] | None = None
) -> list[dict]:
    """构建发给 LLM 的完整 messages 列表。

    Args:
        user_question: 用户当前问题
        retrieved_chunks: 从向量库检索到的相关文档片段
        sources: 每个 chunk 的来源文件名
        history: 对话历史 [{"role":"user","content":"..."}, ...]

    Returns:
        OpenAI 格式的 messages 列表
    """
    knowledge_text = ""
    for i, (chunk, source) in enumerate(zip(retrieved_chunks, sources), 1):
        # 截断过长片段，避免小模型超上下文窗口
        truncated = chunk[:MAX_CHUNK_CHARS]
        if len(chunk) > MAX_CHUNK_CHARS:
            truncated += "…"
        knowledge_text += f"\n--- 知识片段 {i}（来源：{source}）---\n{truncated}\n"

    system_content = SYSTEM_PROMPT + "\n\n以下是知识库中的相关内容：" + knowledge_text

    messages = [{"role": "system", "content": system_content}]

    if history:
        messages.extend(history)

    messages.append({"role": "user", "content": user_question})

    return messages
