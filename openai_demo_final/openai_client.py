from openai import OpenAI
import config

client = OpenAI(api_key=config.API_KEY)

assistant = client.beta.assistants.create(
    name="RASA AI",
    instructions=config.INSTRUCTIONS,
    tools=[{"type": "file_search"}],
    model="gpt-4o",
)
