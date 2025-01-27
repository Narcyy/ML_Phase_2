from typing import List
from pydantic import BaseModel
from openai import OpenAI
import json
class EntitiesModel(BaseModel):
    attributes: List[str]
    colors: List[str]
    animals: List[str]

client = OpenAI()

with client.beta.chat.completions.stream(
    model="gpt-4o-mini",
    messages=[
      {"role": "system", "content": "Extract entities from the input text"},
      {
          "role": "user",
          "content": "The quick brown fox jumps over the lazy dog with piercing blue eyes",
      },
  ],
  response_format=EntitiesModel,

) as stream:
    
    for event in stream:
      if event.type == "content.delta":
          if event.parsed is not None:
              # Print the parsed data as JSON
              print("content.delta parsed:", event.parsed)
      elif event.type == "content.done":
          print("content.done")
      elif event.type == "error":
          print("Error in stream:", event.error)

final_completion = stream.get_final_completion()
data = final_completion.choices[0].message.content
print(data)