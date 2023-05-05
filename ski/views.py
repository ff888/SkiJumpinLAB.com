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
    # list of CSV files target only tournaments after 2001
    csv_files = [f for f in os.listdir(csv_folder) if f.endswith('.csv') and f.split('_')[0] >= '2002']

    # Get category values for filters
    categories = get_categories(csv_files)

    # Check if the request method is GET
    if request.method == 'GET':
        # Get the filter values from the request's GET dictionary
        season_filter = request.GET.get('season_filter')
        city_filter = request.GET.get('city_filter')
        tournament_filter = request.GET.get('tournament_filter')
        hill_filter = request.GET.get('hill_filter')
        gender_filter = request.GET.get('gender_filter')
        team_filter = request.GET.get('team_filter')

        # Filter the csv_files based on the filter values
        filtered_csv_files = [file for file in csv_files if
                              (city_filter is None or city_filter in file) and
                              (hill_filter is None or hill_filter in file) and
                              (season_filter is None or season_filter in file) and
                              (tournament_filter is None or tournament_filter in file) and
                              (gender_filter is None or gender_filter in file) and
                              (team_filter is None or team_filter in file)]

        filtered_csv_files = sorted(filtered_csv_files, key=lambda file: file.split('_')[0], reverse=True)

        # render the files list in your template
        return render(request, 'ski/statistics.html',
                      {'filtered_csv_files': filtered_csv_files, 'categories': categories, 'csv_files': csv_files})


def blog(request):
    return render(request, 'ski/blog.html', {'title': 'Blog'})
