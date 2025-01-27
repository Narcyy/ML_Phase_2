from openai import OpenAI
import json
from functions import get_weather  # Importing the Function

client = OpenAI()

tools = [{
    "type": "function",
    "function":{
        "name":"get_weather",
        "description":"Get the weather information.",
        "parameters":{
            "type":"object",
            "properties":{
                "latitude":{"type":"number"},
                "longitude":{"type":"number"}
            },
            "required":["latitude","longitude"],
            "additionalProperties": False
        },
        "strict": True

    }
}]

messages= [{
        "role":"user",
        "content": "what is the weather in Paris and Hyderabad?"
    }]

# CREATING CHAT COMPLETION FOR INITIATING THE FUNCTION CALLING
# model returns the name and input arguments.
completion = client.chat.completions.create(
    model= "gpt-4o-mini",
    messages= messages,
    tools= tools,
)
# print(completion)

# # PARSE THE MODELS'S RESPONSE AND HANDLING FUNCTION CALLS
messages.append(completion.choices[0].message)

for tool_call in completion.choices[0].message.tool_calls:
    call_id = tool_call.id
    name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)
    result = get_weather(*args)
    messages.append(
        {
            "role": "tool",
            "tool_call_id": call_id,
            "content":str(result)
            
        }
    )
print(messages)
# PARSING THE MODELS'S RESPONSE
# # tool_call = completion.choices[0].message.tool_calls[0]
# # args = json.loads(tool_call.function.arguments)

# # # HANDLING THE FUNCTION CALL
# # result = get_weather(**args)

# # # APPENDING THE FUNCTION RESULT TO THE CONVERSATION
# # messages.append(completion.choices[0].message)
# # # print(messages)
# # messages.append({
# #     "role":"tool",
# #     "tool_call_id": tool_call.id,
# #     "content": str(result)
# #     })
# # print(messages)

# # # GET THE MODEL'S FINAL RESPONSE
completion_2 = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
    tools =tools
)

response = completion_2.choices[0].message.content
print(response)