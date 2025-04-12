import python_weather

import asyncio
import os

async def getweather() -> str:
  # declare the client. the measuring unit used defaults to the metric system (celcius, km/h, etc.)
  async with python_weather.Client(unit=python_weather.METRIC) as client:
    # fetch a weather forecast from a city
    weather = await client.get('New York')
    
    # returns the current day's forecast temperature (int)
    #print(weather.temperature)
    
    # get the weather forecast for a few days
    # for daily in weather:
    #   print(daily)
      
    #   # hourly forecasts
    #   for hourly in daily:
    #     print(f' --> {hourly!r}')
    return weather

if __name__ == '__main__':
  # see https://stackoverflow.com/questions/45600579/asyncio-event-loop-is-closed-when-getting-loop
  # for more details
  if os.name == 'nt':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
  
  s = asyncio.run(getweather())
  print("s = ", s)