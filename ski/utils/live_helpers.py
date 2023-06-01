import datetime

import pandas as pd
import requests
from bs4 import BeautifulSoup


def get_coming_event_info():
    event_dict = {}
    # Get the current date
    today = datetime.date.today()
    # Format the date as "Month Year"
    formatted_date = today.strftime("%b %Y")
    # Create a dictionary to map month names to number
    # Format date
    month_mapper = {
        'Jan': '01',
        'Feb': '02',
        'Mar': '03',
        'Apr': '04',
        'May': '05',
        'Jun': '06',
        'Jul': '07',
        'Aug': '08',
        'Sep': '09',
        'Oct': '10',
        'Nov': '11',
        'Dec': '12'
    }

    # Extract the year and month from the formatted date
    month_name, year = formatted_date.split(' ')
    month_number = month_mapper[month_name]

    # month format engine
    months = [(month_number, year)]
    for i in range(12):
        month_number = '0' + str(int(month_number) + 1)
        if int(month_number) >= 13:
            month_number = '0' + str(int(month_number) - 12)
            year = str(int(year) + 1)
        elif month_number[0] == '0' and len(month_number) == 3:
            month_number = month_number[1:]

        months.append((month_number, year))

    for date in months:
        year = date[1]
        month = date[0]
        season = str(int(year) + 1)

        if year not in event_dict:
            event_dict[year] = {}
        if month not in event_dict[year]:
            event_dict[year][month] = []

        # Construct the URL to the recent month's ski jumping events
        url_to_recent_month = f'https://www.fis-ski.com/DB/ski-jumping/calendar-results.html?eventselection=&place=&sectorcode=JP&seasoncode={season}&categorycode=&disciplinecode=&gendercode=&racedate=&racecodex=&nationcode=&seasonmonth={month}-{year}&saveselection=-1&seasonselection='

        # Make a request to the URL and parse the HTML response using BeautifulSoup
        response = requests.get(url_to_recent_month)
        soup = BeautifulSoup(response.text, 'html.parser')

        calender_events_info = soup.find('div', {'id': 'calendardata'})

        event_info = calender_events_info.text.strip()

        if event_info == 'No events found':
            event_dict[year][month].append(event_info)

        if event_info != 'No events found':
            link_info = calender_events_info.find(href=True)
            link_info = link_info['href']

            response_info = requests.get(link_info)
            soup_info = BeautifulSoup(response_info.text, 'html.parser')

            city_name = soup_info.find('div', {'class': 'event-header'}).text.strip('\n')

            event_details = soup_info.find('div', {'id': 'eventdetailscontent'})

            table_row = event_details.find_all('div', {'class': 'table-row'})

            for row in table_row:
                info = row.text.split('\n')
                info = [i.replace(' ', '') for i in info if len(i) > 0]
                competition_date = info[4]
                competition_hill = info[6]
                competition_gender = info[-1]

                c_day = competition_date[:2]
                c_month = competition_date[2:5]
                c_year = competition_date[5:]

                c_date = f'{c_day} {c_month} {c_year}'

                month_number_fr = month_mapper[c_month]

                # Format hill information
                size = competition_hill.split('HS')[-1]
                if 'Normal' in competition_hill:
                    hill_info = f'Normal Hill HS{size}'
                elif 'Large' in competition_hill:
                    hill_info = f'Large Hill HS{size}'
                else:
                    # needs to be fixed for all hill sizes
                    hill_info = competition_hill

                # Format competition type
                if competition_gender == 'A':
                    c_type = 'Mixed Team'
                elif competition_gender == 'W':
                    c_type = 'Women'
                elif competition_gender == 'M':
                    c_type = 'Men'
                else:
                    # needs to be fixed for man/woman team
                    c_type = 'Team'

                # Skip if competition info is not in the same month
                if month != month_number_fr:
                    pass
                else:
                    event_info = [c_date, city_name, hill_info, c_type]
                    event_dict[year][month].append(event_info)
    return event_dict


def get_event_info(event_dict):
    event_info_dict = {}

    for year in event_dict:
        for months_keys in event_dict[year]:
            month_mapper = {
                '01': 'January',
                '02': 'February',
                '03': 'March',
                '04': 'April',
                '05': 'May',
                '06': 'June',
                '07': 'July',
                '08': 'August',
                '09': 'September',
                '10': 'October',
                '11': 'November',
                '12': 'December'
            }
            month_name = month_mapper[months_keys]
            event = event_dict[year][months_keys]

            if len(event) == 0:
                event = ['No events found']

            title = f'{year} {month_name}'
            if title not in event_info_dict:
                event_info_dict[title] = []

            event_info_dict[title] = event
    return event_info_dict
