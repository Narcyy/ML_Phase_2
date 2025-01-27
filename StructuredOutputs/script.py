from pydantic import BaseModel
import openai
from openai import OpenAI
import requests
def get_weather(latitude, longitude):
    response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m")
    data = response.json()
    return data['current']['temperature_2m']

class GetWeather(BaseModel):
    city: str
    country: str


client = OpenAI()
with client.beta.chat.completions.stream(
    model="gpt-4o-mini",
    messages = [
      {
          "role": "user",
          "content": "What's the weather like in SF and London?",
      },
     ],
     tools = [openai.pydantic_function_tool(GetWeather, name="get_weather")],
     parallel_tool_calls = True,
) as stream:
    
    for event in stream:
        if event.type == "tool_calls.function.arguments.delta":
            print(event)

    response = stream.get_final_completion()
    print(response)