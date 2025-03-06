from dotenv import load_dotenv
from litellm import completion

load_dotenv()

if __name__ == "__main__":

    response = completion(
            model="gemini/gemini-1.5-flash",
            messages=[{"role": "user", "content": "generate a random Pakistan's city name"}],)
        
    city = response.choices[0].message.content
    
    print("City = ", city)