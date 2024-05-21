from src.core.settings import openai_api_key
import openai


class ChatGPTAPIProvider:

    def __init__(self):
        self.openai_api_key = openai_api_key

    async def send_request(self, prompt):
        openai.api_key = openai_api_key
        response = openai.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        return response.choices[0].message.content
