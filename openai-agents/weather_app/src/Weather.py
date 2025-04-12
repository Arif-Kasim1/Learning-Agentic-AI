import asyncio

from agents import Agent, Runner
from agents.tool import function_tool
from LLMConfig import model
from rich import print


@function_tool("get_weather")
async def get_weather(location: str, unit: str = "C") -> str:
  """
  Fetch the weather for a given location, returning a short description.
  """


  print(f"TOOL: Fetching weather for {location} in {unit}...")
  # Example logic

  
  return f"Temperature: The weather in {location} is 22 degrees {unit}."


@function_tool("get_air_quality")
def get_air_quality(location: str) -> str:
  """
  Fetch the air quality for a given location, returning a short description.
  """
  print(f"TOOL: Fetching air quality for {location}...")
  # Example logic
  return f"AQI: The air quality in {location} is good."


@function_tool("get_pollen_count")
def get_pollen_count(location: str) -> str:
  """
  Fetch the pollen count for a given location, returning a short description.
  """
  print(f"TOOL: Fetching pollen count for {location}...")
  # Example logic
  return f"Pollen: The pollen count in {location} is low."

async def main():
    agent = Agent(
        name="Assistant",
        instructions="use tools to answer the questions",
        tools=[get_weather, get_air_quality, get_pollen_count], # add tools here
        model=model
    )

    result = await Runner.run(agent, "Whats the weather in Karachi? Return the temperature in celsius? and " \
    "what is the air quality?")
    print("\n\n",result.final_output)

    result = await Runner.run(agent,  " pollen level in Karachi?")
    print("\n\n",result.final_output)

if __name__ == "__main__":
    asyncio.run(main())