from openai import OpenAI
# import traceback


def chat_oai_stream(
    base_url="http://127.0.0.1:8000/v1",
    api_key="dummy_key",
    model="/data/models/Qwen-7B-Chat-Int4",
    prompt="",
    stream=True
):
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