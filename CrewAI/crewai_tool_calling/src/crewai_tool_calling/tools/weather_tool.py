from crewai.tools import tool

@tool("weather_tool")
def weather_tool(city: str) -> str:
    """Get the weather for a city."""
    return f"Today in {city} it is 30 degrees celsius. Tomorrow it will be 32 degrees celsius." 