from openai import OpenAI


class OpenAIService:

    def __init__(self, api_key: str, model: str):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def generate_embedding(self, text: str) -> list[float]:
        response = self.client.embeddings.create(
            model=self.model,
            input=text,
        )

        return response.data[0].embedding
    
    def generate_response(self, prompt: str) -> str:
        
        response = self.client.responses.create(
            model=self.model,
            input=prompt,
        )

        return response.output_text