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
            messages=[{"role": "user", "content": "generate a random Pakistan's city name"}],)
        
        city = response.choices[0].message.content
        self.state["city"] = city

        print("City = ", city)

    @listen(start)
    def listen(self):
        print("listen():")
        print("city = ", self.state["city"])
        
        response = completion(
            model="gemini/gemini-1.5-flash",
            messages=[{"role": "user", "content": f"generate a fun fact about city name {self.state["city"]}"}],)
        
        fun_fact = response.choices[0].message.content
         

        print("fun_fact = ", fun_fact)



def entry_point():
    print("entry_point():")
    fun_fact = FunFact()
    fun_fact.kickoff()