from ollama import chat
from ollama import ChatResponse
import dashscope
from dashscope.api_entities.dashscope_response import Message

def ollama_chat(model: str, messages) -> str:
    response: ChatResponse = chat(
        model=model,
        messages=messages
    )
    return response.message.content or ""
    

def dashscope_chat(model: str, messages) -> str:
    response = dashscope.Generation.call(
        model=model,
        messages=messages
    )
    answer: str = response.output.text # type: ignore
    return answer

def llm_translate(m_type: str, m_name: str, text: str) -> str:
    if m_type == "remote":
        messages = [
            Message(role="system", content="将以下内容翻译成英语，除此之外不要输出任何额外信息。"),
            Message(role="user", content=text)
        ]
        return dashscope_chat(m_name, messages)
    else:
        messages = [
            {"role": "system", "content": "/no_think 将以下内容翻译成英语，除此之外不要输出任何额外信息。"},
            {"role": "user", "content": text}
        ]
        return ollama_chat(m_name, messages)