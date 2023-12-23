import requests
from bs4 import BeautifulSoup
from ics import Calendar, Event
from datetime import datetime
import re

url = "https://aacpsschools.org/nutrition/jan2024/"

# Define a user agent string
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

# Fetch the HTML content of the website with the specified headers
response = requests.get(url, headers=headers)
html_content = response.content

# Parse HTML using BeautifulSoup
soup = BeautifulSoup(html_content, "html.parser")

# Find all strong elements containing the text "Lunch:"
lunch_strong_elements = soup.find_all("strong", string=re.compile(r"Lunch:"))

# Create an ICS calendar
calendar = Calendar()

# Extract lunch information and add events to the calendar
for lunch_strong in lunch_strong_elements:
    # Find the corresponding date in the preceding tr row
    date_tr = lunch_strong.find_previous("tr").find_previous_sibling("tr")
    if date_tr:
        date_td = date_tr.find("td", class_="has-text-align-center")
        if date_td:
            date_str = date_td.text.strip()

            # Get the entire text within the parent td element
            parent_td_text = lunch_strong.parent.get_text(strip=True)

            # Extract only the portion related to lunch and up to the first comma
            lunch_info_match = re.search(r'Lunch:(.*?),', parent_td_text)
            if lunch_info_match:
                lunch_info = lunch_info_match.group(1).strip()

                # Assume the year is 2024 (you can change this based on the actual URL)
                year = 2024

                # Check if the date string contains a comma
                if "," in date_str:
                    date_format = "%Y-%A, %B %d"
                else:
                    date_format = "%Y-%A %B %d"

                # Construct ISO 8601 date string
                iso_date_str = f"{year}-{date_str}"

                # Parse ISO 8601 date string into datetime object
                event_date = datetime.strptime(iso_date_str, date_format)

                # Create an event for each day
                event = Event()
                event.name = "Lunch: " + lunch_info
                event.begin = event_date
                event.make_all_day()

                calendar.events.add(event)

# Save the calendar to a file
with open("lunch_calendar.ics", "w") as f:
    f.writelines(calendar)

print("ICS calendar file has been created: lunch_calendar.ics")
