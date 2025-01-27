from openai import OpenAI

client = OpenAI()


file = client.files.create(
file=open("dog2.jpg", "rb"),
purpose="vision"
)

assistant = client.beta.assistants.create(
    name = "Image Reader",
    model = "gpt-4o-mini",
)


thread = client.beta.threads.create(
messages=[
  {
    "role": "user",
    "content": [
      {
        "type": "text",
        "text": "What is the image of?"
      },
      {
        "type": "image_file",
        "image_file": {"file_id": file.id}
      },
    ],
  }
]
)

run = client.beta.threads.runs.create_and_poll(
    thread_id= thread.id,
    assistant_id= assistant.id
)

message=client.beta.threads.messages.list(thread_id=thread.id)

print(message.data[0].content[0].text.value)
