import os
import pandas as pd

from .utils.statistics_helpers import get_categories, files_by_year, files_by_season, get_four_hills_files, \
    get_raw_air_files
from .utils.live_helpers import get_coming_event_info, get_event_info
from .utils.live_info_scraper import check_live_event_now
from django.shortcuts import render


def home(request):
    live_event = check_live_event_now()
    return render(request, 'ski/home.html', {'live_event': live_event})


def about(request):
    live_event = check_live_event_now()
    return render(request, 'ski/about.html', {'title': 'About', 'live_event': live_event})


def live(request):
    live_event = check_live_event_now()
    event_info = get_event_info(get_coming_event_info())
    return render(request, 'ski/live.html', {'title': 'LIVE', 'event_info': event_info, 'live_event': live_event})


def fantasy_league(request):
    live_event = check_live_event_now()
    return render(request, 'ski/fantasy-league.html', {'title': 'Fantasy League', 'live_event': live_event})


def statistics_main(request):
    live_event = check_live_event_now()
    return render(request, 'ski/statistics-main.html', {'title': 'Statistics', 'live_event': live_event})


def statistics_rankings(request):
    live_event = check_live_event_now()
    # directory where CSV files are located
    csv_folder = 'media/ski_db'
    # list of CSV files target only tournaments after 2002
    csv_files = [f for f in os.listdir(csv_folder) if f.endswith('.csv') and f.split('_')[0] >= '2002']

    # Get category values for filters
    categories = get_categories(csv_files)

    # Check if the request method is GET
    if request.method == 'GET':
        # Get values from the statistics filters
        season_filter = request.GET.get('season_filter')
        city_filter = request.GET.get('city_filter')
        tournament_filter = request.GET.get('tournament_filter')
        hill_filter = request.GET.get('hill_filter')
        gender_filter = request.GET.get('gender_filter')
        team_filter = request.GET.get('team_filter')

        # Get the sorting parameter from the request
        sort_by = request.GET.get('sort_by')

        # Filter the csv_files based on the filter values
        filtered_csv_files = [file for file in csv_files if
                              (city_filter is None or city_filter in file) and
                              (hill_filter is None or hill_filter in file.split('_')[-3]) and
                              (season_filter is None or season_filter in file) and
                              (tournament_filter is None or tournament_filter in file.split('_')[-4]) and
                              (gender_filter is None or gender_filter in file.split('_')[-2]) and
                              (team_filter is None or team_filter in file)]

        if tournament_filter == '4H':
            filtered_csv_files = get_four_hills_files(csv_files)
        if tournament_filter == 'RA':
            filtered_csv_files = get_raw_air_files(csv_files)

        # Sort list from the most recent tournament
        filtered_csv_files = sorted(filtered_csv_files, key=lambda file: file.split('_')[0], reverse=True)

        # Get values for displaying files
        divide_by_year = files_by_year(filtered_csv_files)
        divide_by_season = files_by_season(filtered_csv_files)

        # Get value if select (click) on tournament link and 'sort by' tabs
        selected_file = request.GET.get('selected_file')

        if selected_file:
            # path to selected CSV file
            file_path = os.path.join(csv_folder, selected_file)
            # create a pandas dataframe
            df = pd.read_csv(file_path)

            # Replace NaN values with 0 in all columns
            df.fillna(0, inplace=True)

            # Calculate the sum of the columns and add new columns do DF
            df['SPEED JUMPS SUM'] = (df['SPEED JUMP 1'] + df['SPEED JUMP 2']).round(2)

            df['COMPENSATION POINTS'] = (df['GATE COMPENSATION JUMP 1'] + df['WIND COMPENSATION JUMP 1'] + df[
                'GATE COMPENSATION JUMP 2'] + df['WIND COMPENSATION JUMP 2']).round(2)

            df['STYLE TOTAL POINTS'] = (df['JUDGE TOTAL POINTS JUMP 1'] + df['JUDGE TOTAL POINTS JUMP 2']).round(2)

            # Rank the DataFrame based on the SPEED_JUMPS_SUM column in descending order
            df['RANKING BY SPEED'] = df['SPEED JUMPS SUM'].rank(method='dense', ascending=False).astype(int)
            df['LUCK RANKING'] = df['COMPENSATION POINTS'].rank(method='dense', ascending=False).astype(int)
            df['STYLE RANKING'] = df['STYLE TOTAL POINTS'].rank(method='dense', ascending=False).astype(int)

            # Sort the DataFrame based on the value of 'sort_by'
            if sort_by == 'ranking_table' or sort_by == 'full_table':
                df = df.sort_values(by='RANKING', ascending=True)
            elif sort_by == 'speed_table':
                df = df.sort_values(by='SPEED JUMPS SUM', ascending=True)
            elif sort_by == 'style_table':
                df = df.sort_values(by='STYLE RANKING', ascending=True)
            elif sort_by == 'luck_table':
                df = df.sort_values(by='LUCK RANKING', ascending=True)
            elif sort_by == 'team_table':
                df = df.sort_values(by='TEAM RANKING', ascending=True)

            # replace all spaces in columns names with underscores
            df.columns = df.columns.str.replace(' ', '_')

            # Convert the dataframe to a list of dictionaries representing each row
            rows = df.to_dict('records')

            # Create list of file name elements and use them as a table name
            name_list = selected_file.split('_')
            name_date = name_list[0]
            name_city = name_list[1]
            name_codex = name_list[2]
            name_tour_type = name_list[3]
            name_hill = name_list[4]
            name_gender = name_list[5]
            name_team = name_list[6].split('.')[0]

            # Set the title
            title = f"Statistics - {selected_file}"
            # Set the table title
            table_title = f'{name_date} {name_city}'

            # render the files list in your template
            return render(request, 'ski/statistics-rankings.html',
                          {'filtered_csv_files': filtered_csv_files,
                           'categories': categories,
                           'rows': rows,
                           'title': title,
                           'table_title': table_title,
                           'live_event': live_event})

        # render the files list in your template
        return render(request, 'ski/statistics-rankings.html',
                      {'divide_by_year': divide_by_year,
                       'divide_by_season': divide_by_season,
                       'filtered_csv_files': filtered_csv_files,
                       'categories': categories,
                       'live_event': live_event})


def statistics_by_time(request):
    live_event = check_live_event_now()
    return render(request, 'ski/statistics-by-time.html', {'title': 'Statistics', 'live_event': live_event})


def statistics_jumper(request):
    live_event = check_live_event_now()
    return render(request, 'ski/statistics-jumper.html', {'title': 'Statistics', 'live_event': live_event})


def blog(request):
    live_event = check_live_event_now()
    return render(request, 'ski/blog.html', {'title': 'Blog', 'live_event': live_event})
