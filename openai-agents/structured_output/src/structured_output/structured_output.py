from pydantic import BaseModel
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig
from LLMConfig import model, config
from weather_answer import WeatherAnswer



agent = Agent(
  name="StructuredWeatherAgent",
  instructions="Use the final_output tool with WeatherAnswer schema.",
  output_type=WeatherAnswer
)

async def main():
    out = await Runner.run(agent, "What's the temperature in Karachi?", run_config=config)
    print(type(out.final_output))
    # 
    print("location      = ", out.final_output.location)
    print("summary       = ",out.final_output.summary)
    print("temperature_c = ", out.final_output.temperature_c)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())