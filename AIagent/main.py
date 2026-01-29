from google import genai

with genai.Client() as client:
    response_1 = client.models.generate_content(
        model = "gemma-3-27b-it",
        contents = "Say Hello World"
    )

print(response_1.text)