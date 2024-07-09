# bachat2.py
from openai import OpenAI, AssistantEventHandler
import requests

class EventHandler(AssistantEventHandler):
    def __init__(self):
        super().__init__()
        self.responses = []
        self.current_message = ""

    def on_text_delta(self, delta, snapshot):
        text_value = delta.value
        print(f"Received delta: {text_value}")
        self.current_message += text_value

        if text_value.endswith(('.', '?', '!')):
            self.responses.append(self.current_message.strip())
            self.current_message = ""

    def on_tool_call_created(self, tool_call):
        print(f"Tool call created: {tool_call.type}")

    def on_tool_call_delta(self, delta, snapshot):
        print("Received tool call delta")

def handle_user_message(client, thread_id, assistant_id):
    event_handler = EventHandler()
    with client.beta.threads.runs.stream(
        thread_id=thread_id,
        assistant_id=assistant_id,
        event_handler=event_handler,
    ) as stream:
        stream.until_done()

    responses = event_handler.responses
    return responses

