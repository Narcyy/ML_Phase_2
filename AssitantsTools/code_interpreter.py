from openai import OpenAI

client = OpenAI()

# UPLOADING FILES
upload_file = client.files.create(
    file = open("customers-100.csv", "rb"),
    purpose="assistants"
)

# CREATING ASSIATANT
# WE CAN ADD THE FILES AT THREAD LEVEL BUT THOSE ARE ONLY ACCESIBLE FOR THAT THREAD ONLY.

assistant = client.beta.assistants.create(
    name = "First Assistant",
    instructions= "You are an helpful assistant that reads the file and gain insights, and answer the question followed by.",
    model= "gpt-4o-mini",
    tools=[{"type": "code_interpreter"}],        # CHECK WHETHER THE TOOL SUPPORTS THE FORMAT OF THE FILE
    # ADDING FILES AT ASSISTANT LEVEL ARE ACCESSIBLE AT ANY WHERE, WHERE THE ASSISTANT USED
    tool_resources={
     "file_search": {       #TOOL NAME
    "file_ids": [upload_file.id]
    }
    }
)

# CREATE THREAD
my_thread = client.beta.threads.create (
    # WE CAN ADD USER MESSAGES AT THREADS
    messages=[ 
        { "role": "user",
          "content": "What is the context of file?", 

        # WE CAN ADD THE FILES AT THREAD LEVEL BUT THOSE ARE ONLY ACCESIBLE FOR THAT THREAD ONLY.
        "attachments": [
            {
                "file_id": upload_file.id,
                "tools": [{"type": "file_search"}]
            }
        ]
        }
    ],

)

# CREATE MESSAGE OBJECT
my_message = client.beta.threads.messages.create(
    thread_id=my_thread.id,
    role="user",
    content="What os the country most of the people are??",
)

# CREATE A RUN OBJECT
# CREATE_AND_POLL WAITS FOR THE COMPLETION AND RETRIVE THE TASK
run = client.beta.threads.runs.create_and_poll(
    assistant_id= assistant.id,
    thread_id= my_thread.id
)

# RETRIVING THE RESPONSE
message = client.beta.threads.messages.list(
        thread_id= my_thread.id
    )
print(message.data[0].content[0].text.value)




