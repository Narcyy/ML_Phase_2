from openai import OpenAI
from functions import get_weather, get_something

import json

client = OpenAI()

functions = [{
    "type":"function",
    "function":{
            "name":"get_weather",
            "description":"Get the weather information every city mentioned.",
            "parameters":{
                "type":"object",
                "properties":{
                    "latitude":{"type":"number"},
                    "longitude":{"type":"number"}
                },
                "required":["latitude","longitude"],
            }
            }
    }

]
messages = [{
    "role":"user",
    "content":"What is the temparature in Kurnool and Hyderabad?",
}]


completion_1 = client.chat.completions.create(
    model= "gpt-4o-mini",
    messages=messages,
    tools=functions
)

# Creating function for asssigning function calls
def get_function(name, args):
    if name == "get_weather":
        return get_weather(**args)

    if name == "get_somethig":
        return get_something(name)


messages.append(completion_1.choices[0].message)  

for tool_call in completion_1.choices[0].message.tool_calls:
    print(f"Tool_call:{tool_call}")
    call_id = tool_call.id
    name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)
    result = get_function(name, args)
    messages.append(
        {
            "role": "tool",
            "tool_call_id": call_id,
            "content":str(result)
            
        }
    )


completion_2 = client.chat.completions.create(
    model="gpt-4o-mini",
    messages = messages,
    tools = functions

)
# # print(completion_2)
print(completion_2.choices[0].message.content)

