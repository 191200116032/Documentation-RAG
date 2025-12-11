from groq import Groq

class GroqLLMProvider:
    def __init__(self, model="llama-3.3-70b-versatile"):
        self.model = model
        self.client = Groq()

    def generate(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
