#!/usr/bin/env python3
import sys
import urllib.request
import json
from datetime import datetime, timezone, timedelta

# Function to fetch sunrise, sunset, and solar noon times from an API
def get_sunrise_sunset_times(lat, lng):
    url = f"https://api.sunrise-sunset.org/json?lat={lat}&lng={lng}&formatted=0"
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode())
        
    return data["results"]["sunrise"], data["results"]["sunset"], data["results"]["solar_noon"]

# Function to determine the appropriate wallpaper based on the current time
def get_desktop_wallpaper(lat, lng):
    sunrise_utc, sunset_utc,solar_noon_utc  = get_sunrise_sunset_times(lat, lng)
    
    # Convert sunrise, sunset, and solar noon times to datetime objects
    sunrise_time = datetime.fromisoformat(sunrise_utc).time()
    sunset_time = datetime.fromisoformat(sunset_utc).time()
    solar_noon_time = datetime.fromisoformat(solar_noon_utc).time()
    
    # Get current UTC time (only time part)
    current_time = datetime.now(timezone.utc).time()
    
    # Define time periods
    sunrise_end = (datetime.combine(datetime.min, sunrise_time) + timedelta(minutes=30)).time()
    noon_start = (datetime.combine(datetime.min, solar_noon_time) - timedelta(hours=2)).time()
    noon_end = (datetime.combine(datetime.min, solar_noon_time) + timedelta(hours=4)).time()
    sunset_start = (datetime.combine(datetime.min, sunset_time) - timedelta(minutes=30)).time()
    
    
    # Determine the wallpaper based on the current time
    if sunrise_time <= current_time < sunrise_end:
        return "sunrise.png"
    elif sunrise_end <= current_time < noon_start:
        return "morning.png"
    elif noon_start <= current_time < noon_end:
        return "noon.png"
    elif noon_end <= current_time < sunset_start:
        return "evening.png"
    elif sunset_start <= current_time < sunset_time:
        return "sunset.png"
    else:
        return "night.png"


if __name__ == "__main__":
    # Check if the correct number of arguments is provided
    if len(sys.argv) != 3:
        print("Usage: ./script.py <latitude> <longitude>")
        sys.exit(1)
        
    lat = float(sys.argv[1])
    lng = float(sys.argv[2])
    
    wallpaper = get_desktop_wallpaper(lat, lng)
    print(wallpaper)

