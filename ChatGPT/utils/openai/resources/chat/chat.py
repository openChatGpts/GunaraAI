import requests
import os

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
ENDPOINT = os.environ.get("ENDPOINT")

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {OPENAI_API_KEY}",
}


class Completions:
    def __init__(self, api_key, proxy):
        self.api_key = api_key
        self.proxy = proxy

    def chat(self, messages, model="gpt-3.5-turbo-1106"):
        path = "/v1/chat/completions"
        data = {
            "messages": messages,
            "model": model,
            "max_tokens": 1000,
            "temperature": 0.5,
            "top_p": 1,
            "n": 1,
            "function_call": "auto",
            "stream": True,
        }
        response = requests.post(
            ENDPOINT + path, headers=headers, json=data, stream=True
        )
        return response

    def ChatTitle(self, messages, model="gpt-3.5-turbo-1106"):
        # 给用户对话起标题
        content = """
                You are an assistant who summarizes the content and generates a title for the conversation content,
                I will send you the conversation content between the user and ChatGPT in Python collection format,
                You need to generate a title for the content in the collection to facilitate user understanding
                Please note that the language of the title needs to be equal to the language of the conversation content
                Below, I will give you an example to illustrate:

                [{'role': 'user', 'content': '你好'},{'role': 'assistant', 'content': '你好有什么可以帮助你的吗？'}]
                
                You need to reply directly to me without citing or explaining the content of the title. Please provide the title directly:

                帮助用户请求

                It is best to control the title within 15 words

        """
        system = [
            {"role": "system", "content": content},
            {"role": "user", "content": str(messages)},
        ]

        path = "/v1/chat/completions"
        data = {
            "messages": system,
            "model": model,
            "max_tokens": 1000,
            "temperature": 0.5,
            "top_p": 1,
            "n": 1,
            "function_call": "auto",
        }
        response = requests.post(ENDPOINT + path, headers=headers, json=data)
        # print(response.json()["choices"][0]["message"]["content"])
        return response.json()["choices"][0]["message"]["content"]


ChatCompletion = Completions(OPENAI_API_KEY, ENDPOINT)
