import os


class OpenAiSecretManager:

    def get_secret(self):
        return os.environ["OPENAI_API_KEY"]
