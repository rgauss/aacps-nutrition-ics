# AACPS Nutrition Page to ICS

Python script that scrapes Anne Arundel County Public Schools
nutrition pages to create an ICS calendar, currently only focused
on the main course of lunch.

The code is very specific to the current HTML structure of the pages so
it's very likely to break if/when AACPS changes their formatting.

(Created with help from [ChatGPT](https://chat.openai.com/))

## Running

Be sure the required dependencies are installed:

```
pip install requests beautifulsoup4 ics
```

Edit the `url` in `create_lunch_calendar.py` for the desired month.

Run the script:

```
python3 create_lunch_calendar.py
```

The result should be available in `lunch_calendar.ics`.