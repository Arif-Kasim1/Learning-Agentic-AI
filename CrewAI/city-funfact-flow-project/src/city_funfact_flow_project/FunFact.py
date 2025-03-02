from crewai.flow.flow import Flow, listen, start 
from dotenv import load_dotenv
from litellm import completion

load_dotenv()

class FunFact(Flow):
  
    @start()
    def start(self):
        print("This is a fun fact about a city")
        response = completion(
            model="gemini/gemini-1.5-flash",
            messages=[{"role": "user", "content": "generate a random city name"}],)

        print(response['choices'][0]['message']['content'])




def entry_point():
    print("entry_point():")
    fun_fact = FunFact()
    fun_fact.kickoff()