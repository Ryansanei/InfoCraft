# main.py
from openai_client import client, assistant
from assistant_handler import EventHandler
import config
from process_bridge import process_pdf, clean_and_sort_text

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
    # Get the PDF file path from the user
    pdf_path = input("Enter the full path to your PDF file: ").strip()
    if not pdf_path:
        print("No PDF path provided. Exiting.")
        exit(1)

    # Process the PDF and get the extracted text
    extracted_text = process_pdf(pdf_path)
    cleaned_text = clean_and_sort_text(extracted_text)

    print("\n--- Extracted, Cleaned & Sorted Text ---\n")
    print(cleaned_text)

    # Use the entire cleaned text as the input to chat_with_gpt
    chat_with_gpt(cleaned_text)
