from openai import OpenAI

client = OpenAI()

# CREATING ASSIATANT
assiatant = client.beta.assistants.create(
    name="Customer Analysis",
    instructions="You are an helpful assistant that reads the file and gain insights, and answer the question followed by?.",
    model= "gpt-4o-mini",
    tools = [{"type":"file_search"}]
)
# CREATING VECTOR_STORE FOR STORING CONTENT
vector_store = client.beta.vector_stores.create(name="Customer Anylysis")
# print(vector_store)

file_path = ["sample.txt"]
file_streams = [open(path, "rb") for path in file_path]
# print(file_streams)

# CREATING FILE_BATCHES AND UPLOAD TO VECTOR_STORE FOR ANANLYSING DATA
file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
    vector_store_id=vector_store.id,
    files=file_streams

)
# CHECK THE STATUS
print(file_batch.status)
print(file_batch.file_counts)

# WE NEED TO UPDATE THE ASSISTANT WITH TOOL_RESOURCES WITH VECTORE_STORE FOR MAKING DATA ACCESSIBLE
assistant = client.beta.assistants.update(
    assistant_id= assiatant.id,
    tool_resources={"file_search":{"vector_store_ids":[vector_store.id]}}


)

# CREATING THREADS
thread = client.beta.threads.create(
    messages=[ 
        { "role": "user",
          "content": "What is the context of file?" 
        } 
    ],
)

# CREATING RUN OBJECT
run = client.beta.threads.runs.create_and_poll(
    thread_id = thread.id,
    assistant_id = assistant.id
)

# RETRIVING THE CONTENT FROM THE RESPONSE
message = client.beta.threads.messages.list(
    thread_id= thread.id
    )
print(message.data[0].content[0].text.value)