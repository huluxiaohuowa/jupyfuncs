from openai import OpenAI
# import traceback


def chat_oai_stream(
    base_url="http://127.0.0.1:8000/v1",
    api_key="dummy_key",
    model="/data/models/Qwen-7B-Chat-Int4",
    prompt="",
    stream=True
):
    """Chat with OpenAI's GPT-3 model using the specified parameters.
    
    Args:
        base_url (str): The base URL for the OpenAI API. Default is "http://127.0.0.1:8000/v1".
        api_key (str): The API key for accessing the OpenAI API. Default is "dummy_key".
        model (str): The model ID to use for the chat. Default is "/data/models/Qwen-7B-Chat-Int4".
        prompt (str): The initial prompt for the chat conversation.
        stream (bool): If True, the function will yield responses in a streaming fashion. If False, it will return the full response.
    
    Yields:
        str: The generated content from the chat conversation.
    
    Returns:
        dict or str: The response from the OpenAI API. If stream is False, it returns the full response.
    """
    client = OpenAI(
        base_url=base_url,
        api_key=api_key,
    )
    response = client.chat.completions.create(
        model=model,
        messages=[{
            "role": "user",
            "content": prompt
        }],
        stream=stream
    )
    if not stream:
        return response
    else:
        for chunk in response:
            content = chunk.choices[0].delta.content
            yield content

# client = OpenAI(
#     base_url="http://127.0.0.1:8000/v1",
#     api_key="dummy_key"  # 使用虚拟的API Key
# )


# response = client.chat.completions.create(
#     model="/data/models/Qwen-7B-Chat-Int4",
#     messages=[{"role": "user", "content": "给我讲个鬼故事"}],
#     stream=True
# )
# for chunk in response:
#     content = chunk.choices[0].delta.content
#     if content:
#         print(content, end='', flush=True)
# print()