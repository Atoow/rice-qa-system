"""Prompt 模板和构建函数。"""

SYSTEM_PROMPT = """你是一个专业的水稻种植顾问。请严格遵守以下规则回答问题：

1. 如果提供的知识库内容中有相关信息，请基于知识库内容回答，并在末尾注明"参考来源：{source}"
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
        knowledge_text += f"\n--- 知识片段 {i}（来源：{source}）---\n{chunk}\n"

    system_content = SYSTEM_PROMPT + "\n\n以下是知识库中的相关内容：" + knowledge_text

    messages = [{"role": "system", "content": system_content}]

    if history:
        messages.extend(history)

    messages.append({"role": "user", "content": user_question})

    return messages
