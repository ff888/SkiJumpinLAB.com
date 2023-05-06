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
        speed_table = request.GET.get('sort_by', 'speed_table')
        ranking_table = request.GET.get('sort_by', 'ranking_table')

        if selected_file:
            # path to selected CSV file
            file_path = os.path.join(csv_folder, selected_file)
            # create a pandas dataframe
            df = pd.read_csv(file_path)
            # replace all spaces in columns names with underscores
            df.columns = df.columns.str.replace(' ', '_')
            # Convert the dataframe to a list of dictionaries representing each row
            rows = df.to_dict('records')
            if ranking_table:
                rows = rows

            if speed_table:
                speed_df = df[['NAME', 'NATIONALITY', 'SPEED_JUMP_1', 'SPEED_JUMP_2', 'RANKING']]
                speed_df['SPEED_JUMPS_SUM'] = df['SPEED_JUMP_1'] + df['SPEED_JUMP_2']
                speed_df = df.to_dict('records')
                rows = speed_df

            # Set the title
            title = f"Statistics - {selected_file}"
            # Set the table title
            table_title = selected_file
            # render the files list in your template

            return render(request, 'ski/statistics.html',
                          {'filtered_csv_files': filtered_csv_files, 'categories': categories, 'rows': rows,
                           'title': title, 'table_title': table_title})

        # render the files list in your template
        return render(request, 'ski/statistics.html',
                      {'filtered_csv_files': filtered_csv_files, 'categories': categories})


def blog(request):
    return render(request, 'ski/blog.html', {'title': 'Blog'})
