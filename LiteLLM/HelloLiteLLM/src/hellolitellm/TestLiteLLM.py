from litellm import completion 
import os
from dotenv import load_dotenv

load_dotenv()

print("Inside TestLiteLLM.py") 
print("Calling completion function from litellm package")   

response = completion(
    model="gemini/gemini-1.5-flash",
    messages=[{"role": "user", "content": "100 words summary about france"}],
)

print(response['choices'][0]['message']['content'])
