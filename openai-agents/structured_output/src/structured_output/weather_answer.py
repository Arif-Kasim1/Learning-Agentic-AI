from pydantic import BaseModel

class WeatherAnswer(BaseModel):
  location: str
  temperature_c: float
  summary: str