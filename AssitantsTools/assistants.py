from openai import OpenAI

client = OpenAI()

# Creating a new assistant
assistant = client.beta.assistants.create(
    name="First Assistant",
    model="gpt-4o-mini",
    tools=[{"type":"code_interpreter"}],
    instructions="You are an AI assistant that can help with a variety of tasks. You can help with coding, writing, and more."
)
print(assistant.id)
# 

#Creatiing Thread
thread = client.beta.threads.create(

    # messages=[
    # {
    #     "role": "user",
    #     "content": "Tell me about india in 10 words?"
    # }
    # ]
)

# print(thread)

#Adding message to the thread

message = client.beta.threads.messages.create(
    thread_id = thread.id,
    role = "user",
    content = "Tell me about india in 10 words"
    
)

#Create a run

run = client.beta.threads.runs.create_and_poll(
    assistant_id= assistant.id,
    thread_id= thread.id,
    instructions="Address the user as Narcyy"

)

if run.status:
    message = client.beta.threads.messages.list(
        thread_id= thread.id
    )
    print(message.data[0].content[0].text.value)


# message = client.beta.threads.messages.retrieve(
# thread_id=thread.id,
# message_id=message.id
# )
run_steps = client.beta.threads.runs.steps.list(
thread_id=thread.id,
run_id=run.id
)
print(run_steps)