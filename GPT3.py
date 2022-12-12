# Import libraries
from bs4 import BeautifulSoup
import requests
import csv
 
# Set the URL to scrape
url = "https://weather.com/weather/tenday/l/USCA0987:1:US"
 
# Send a GET request to the URL and store the response
response = requests.get(url)
 
# Parse the response using BeautifulSoup
soup = BeautifulSoup(response.text, "html.parser")
 
# Find the forecast container element
forecast_container = soup.find(class_="twc-table")
 
# Create an empty list to store the forecast data
forecast_data = []
 
# Loop through each row in the forecast table
for row in forecast_container.find_all("tr"):
  # Create an empty dictionary to store the forecast data for each day
  day_data = {}
 
  # Loop through each cell in the row
  for cell in row.find_all("td"):
    # Get the forecast date and store it in the dictionary
    if cell.get("headers")[0] == "date":
      day_data["date"] = cell.text
 
    # Get the forecast description and store it in the dictionary
    if cell.get("headers")[0] == "description":
      day_data["description"] = cell.text
 
    # Get the forecast high and low temperatures and store them in the dictionary
    if cell.get("headers")[0] == "hi-lo":
      temperatures = cell.text.split("/")
      day_data["high"] = temperatures[0]
      day_data["low"] = temperatures[1]
 
  # Add the day's forecast data to the list
  forecast_data.append(day_data)
 
# Open a new file to write the forecast data to
with open("forecast.csv", "w") as csv_file:
  # Create a CSV writer
  writer = csv.DictWriter(csv_file, fieldnames=["date", "description", "high", "low"])
 
  # Write the column headers
  writer.writeheader()
 
  # Write the forecast data to the file
  for day in forecast_data:
    writer.writerow(day)
