from langchain.tools import tool


@tool
def get_weather(city: str) -> str:
    """Get the current weather in a city."""
    fake_data = {
        "New York": "Cloudy, 25°C",
        "London": "Rainy, 18°C",
        "Delhi": "Sunny, 32°C",
        "Mumbai": "Humid, 30°C",
        "Bangalore": "Clear, 28°C",
    }
    return fake_data.get(city, "Weather data not available")