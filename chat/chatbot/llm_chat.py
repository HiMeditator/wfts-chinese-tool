from ollama import chat
from ollama import ChatResponse
import dashscope
from dashscope.api_entities.dashscope_response import Message

def ollama_chat(model: str, messages):
    response: ChatResponse = chat(
        model=model,
        messages=messages
    )
    print(response.message.content)
    return Message(
        role='assistant',
        content=response.message.content or ""
    )

def dashscope_chat(model: str, messages):
    response = dashscope.Generation.call(
        model=model,
        messages=messages
    )
    answer: str = response.output.text # type: ignore
    return Message(
        role='assistant',
        content=answer
    )