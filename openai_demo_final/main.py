from openai_client import client, assistant
from assistant_handler import EventHandler
import config

def chat_with_gpt(user_text):
    """Send user input to GPT and stream response."""
    thread = client.beta.threads.create()

    # Create a message in the thread
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_text
    )

    # Run the assistant and stream response
    with client.beta.threads.runs.stream(
        thread_id=thread.id,
        assistant_id=assistant.id,
        instructions=config.INSTRUCTIONS,
        event_handler=EventHandler(),
    ) as stream:
        stream.until_done()

if __name__ == "__main__":
    user_input = input("Enter your text: ")  # Get user input
    chat_with_gpt(user_input)  # Send to GPT
