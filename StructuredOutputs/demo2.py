from pydantic import BaseModel, Field
from openai import OpenAI

client = OpenAI()

class Step(BaseModel):
    steps: str = Field(description="Detail explanation of the step to easily understand." )
    output: str
    

class MathResponse(BaseModel):
    steps: list[Step]
    final_answer: str
    

completion = client.beta.chat.completions.parse(
    model= "gpt-4o-mini",
    messages = [
        {"role": "system", "content": "You are a helpful math tutor. Guide the user through the solution step by step."},
        {"role": "user", "content": "how can I solve 8x + 7 = -23"}
    ],
    response_format=  MathResponse
)

math_reasoning = completion.choices[0].message.parsed

for i,step in enumerate(math_reasoning.steps, start=1):
   print(f"Step{i}: {step}")
   
print(f"Final Answer: {math_reasoning.final_answer}")