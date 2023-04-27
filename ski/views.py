import os
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
    csv_folder = 'media'
    csv_files = [f for f in os.listdir(csv_folder) if f.endswith('.csv')]

    if request.method == 'GET':
        csv_file = request.GET.get('csv_file', None)

        if csv_file:
            file_path = os.path.join(csv_folder, csv_file)
            df = pd.read_csv(file_path)
            df.columns = df.columns.str.replace(' ', '_')
            rows = df.to_dict('records')
            title = 'Statistics - ' + csv_file
            return render(request, 'ski/statistics.html', {'rows': rows, 'title': title})

    return render(request, 'ski/statistics.html', {'csv_files': csv_files, 'title': 'Statistics'})


def blog(request):

    return render(request, 'ski/blog.html', {'title': 'Blog'})
