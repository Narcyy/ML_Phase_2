from pydantic import BaseModel
from openai import OpenAI
from typing import List

client = OpenAI()

class CalendeEvent(BaseModel):
    name: str
    date: str
    participants: list[str]

messages = [{"role": "system", "content": "Extract the event information."},
        {"role": "user", "content": "Alice and Bob are going to a science fair on Friday."}]


completion = client.beta.chat.completions.parse(
    model="gpt-4o-mini",
    messages = messages,
    response_format=CalendeEvent
    )

event =completion.choices[0].message.parsed

print(event)