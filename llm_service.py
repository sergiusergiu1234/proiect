import os
from haystack.components.generators import OpenAIGenerator
from haystack.utils import Secret
from dotenv import load_dotenv



load_dotenv()

class llm_service:
    def __init__(self, model_name):
        
        self.__client = OpenAIGenerator(model=model_name, api_key=Secret.from_token(os.getenv("OPENAI_API_KEY")),
                                        generation_kwargs={ "temperature": 0.1})

    def generate_response(self, prompt) -> str:
        response = self.__client.run(prompt)
        return response["replies"][0]