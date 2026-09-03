from langsmith import Client
import config.settings as settings

def langsimthPrompt():
    client = Client()
    prompt = client.pull_prompt(
        "test-2-with-chunks",
        include_model=True,
        secrets={"GROQ_API_KEY": settings.GROQ_API_KEY}
    )
    return prompt
# print(prompt)