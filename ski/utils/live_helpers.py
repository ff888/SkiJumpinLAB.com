import datetime
import requests
from bs4 import BeautifulSoup


def get_date_list():
    # Get today's date and format it to extract the month and year
    today = datetime.date.today()
    formatted_date = today.strftime("%B %Y")

    # Extract the year and month from the formatted date
    year = formatted_date.split(' ')[1]
    month = formatted_date.split(' ')[0]

    # Construct the URL to the recent month's ski jumping events
    url_to_recent_month = f'https://www.fis-ski.com/DB/ski-jumping/calendar-results.html?eventselection=&place=&sectorcode=JP&seasoncode={year}&categorycode=&disciplinecode=&gendercode=&racedate=&racecodex=&nationcode=&seasonmonth={month}-{year}&saveselection=-1&seasonselection='

    # Make a request to the URL and parse the HTML response using BeautifulSoup
    response = requests.get(url_to_recent_month)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the div containing the select element for filtering by month and year
    select_month_div = soup.find('div', {'id': 'select_seasonmonth'})

    # Extract the list of available months and years from the select element
    select_date_list = [i for i in select_month_div.text.split('\n') if len(i) > 2]

    # Convert the list of month-year strings to a list of datetime objects
    datetime_list = [datetime.datetime.strptime(date, '%B %Y') for date in select_date_list]

    # Filter the datetime objects to include only dates from the current month or later
    today = datetime.datetime.now()
    datetime_list = [d for d in datetime_list if d >= datetime.datetime(today.year, today.month, 1)]

    # Sort the list of datetime objects in ascending order
    datetime_list.sort(reverse=False)

    # Convert the sorted datetime objects back to month-year strings
    sorted_date_list = [datetime.datetime.strftime(date, '%B %Y') for date in datetime_list]

    # Create a dictionary to group the month-year strings by year
    date_dict = {}
    for item in sorted_date_list:
        month, year = item.split()
        if year not in date_dict:
            date_dict[year] = []
        date_dict[year].append(month)

    # Return the dictionary of available months and years
    return date_dict


def get_event_info(date_dict):
    # Create an empty dictionary to store the event information
    info_dict = {}

    # Loop through each year and its corresponding months in the date dictionary
    for year, months in date_dict.items():
        # Create an empty list to store the event information for each month in the current year
        year_list = []

        # Loop through each month in the current year
        for month in months:
            # Construct the URL for the current month and year
            url_to_recent_month = f'https://www.fis-ski.com/DB/ski-jumping/calendar-results.html?eventselection=&place=&sectorcode=JP&seasoncode={year}&categorycode=&disciplinecode=&gendercode=&racedate=&racecodex=&nationcode=&seasonmonth={month}-{year}&saveselection=-1&seasonselection='

            # Use a session to get the HTML content of the page
            with requests.Session() as session:
                response = session.get(url_to_recent_month)

            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find the table with the event information
            events_table_id = soup.find('div', {'id': 'calendardata'})

            # Split the table contents by newline characters to create a list of table elements
            table_elements_list = events_table_id.text.strip().split('\n')

            # Append the list of table elements to the list for the current year and month
            year_list.append({month: table_elements_list})

        # Add the list of event information for the current year to the info dictionary
        info_dict[year] = year_list

    # Return the dictionary containing all event information
    return info_dict
