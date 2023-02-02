import logging
import os

import aiofiles
import aiohttp
import openai


async def get_openai_api_key() -> str:
    """Returns the OpenAI API key"""
    return os.getenv("OPENAI_API_KEY")

class SuggestionHandler:
    def __init__(self, engine: str = os.getenv('OPENAI_ENGINE')):
        self.engine = engine
        self.logger = logging.getLogger(__name__)

    async def get_suggestions(self, prompt: str, temperature: float = 0.7, max_tokens: int = 2000, top_p: float = 1, frequency_penalty: float = 0, presence_penalty: float = 0) -> str:
        """Makes an API call to the OpenAI API and returns the suggestions for improvement"""
        try:
            openai.api_key = await get_openai_api_key()
            async with aiohttp.ClientSession() as session:
                async with session.post(f'https://api.openai.com/v1/engines/{self.engine}/completions',headers={'Authorization': f'Bearer {openai.api_key}'},
                                        json={'prompt': prompt,
                                              'temperature': temperature,
                                              'max_tokens': max_tokens,
                                              'top_p': top_p,
                                              'frequency_penalty': frequency_penalty,
                                              'presence_penalty': presence_penalty,
                                              'stop': ['\n\n### Suggestions', '\n\n### New']}) as resp:
                    response = await resp.json()
                    print(response)
                    return response['choices'][0]['text']
        except Exception as e:
            self.logger.error(f"Error getting suggestions: {e}")
            raise e