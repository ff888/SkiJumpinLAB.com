import os
from .utils.ststistics_helpers import get_categories
import pandas as pd

from django.shortcuts import render


def home(request):
    return render(request, 'ski/home.html')


def about(request):
    return render(request, 'ski/about.html', {'title': 'About'})


def live(request):
    return render(request, 'ski/live.html', {'title': 'LIVE'})


def fantasy_league(request):
    return render(request, 'ski/fantasy-league.html', {'title': 'Fantasy League'})


def statistics(request):
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

        # Filter the csv_files based on the filter values
        filtered_csv_files = [file for file in csv_files if
                              (city_filter is None or city_filter in file) and
                              (hill_filter is None or hill_filter in file.split('_')[-3]) and
                              (season_filter is None or season_filter in file) and
                              (tournament_filter is None or tournament_filter in file.split('_')[-4]) and
                              (gender_filter is None or gender_filter in file.split('_')[-2]) and
                              (team_filter is None or team_filter in file)]

        # Sort list from the most recent tournament
        filtered_csv_files = sorted(filtered_csv_files, key=lambda file: file.split('_')[0], reverse=True)

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

            # Retrieve the 'sort_by' parameter from the request's GET parameters
            sort_by = request.GET.get('sort_by')

            # Sort the DataFrame based on the value of 'sort_by'
            if sort_by == 'ranking_table':
                df = df.sort_values(by='RANKING', ascending=True)
            elif sort_by == 'speed_table':
                df = df.sort_values(by='SPEED JUMPS SUM', ascending=True)
            elif sort_by == 'style_table':
                df = df.sort_values(by='STYLE RANKING', ascending=True)
            elif sort_by == 'luck_table':
                df = df.sort_values(by='LUCK RANKING', ascending=True)

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
            return render(request, 'ski/statistics.html',
                          {'filtered_csv_files': filtered_csv_files, 'categories': categories, 'rows': rows,
                           'title': title, 'table_title': table_title})

        # render the files list in your template
        return render(request, 'ski/statistics.html',
                      {'filtered_csv_files': filtered_csv_files, 'categories': categories})


def blog(request):
    return render(request, 'ski/blog.html', {'title': 'Blog'})
