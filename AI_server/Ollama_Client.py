import ollama

class Ollama_Client:
    def __init__(self, model_name="llama3.1:latest"):
        self.model_name = model_name

    def ask_ollama(self, question: str) -> str:
        response = ollama.generate(
            model=self.model_name,
            prompt=question
        )
        return response["response"]