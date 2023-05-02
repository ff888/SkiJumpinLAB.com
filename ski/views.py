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
    # directory where CSV files are located
    csv_folder = 'media'
    # list of CSV files
    csv_files = [f for f in os.listdir(csv_folder) if f.endswith('.csv')]

    # Check if the request method is GET
    if request.method == 'GET':
        # Get the value of the 'csv_file' parameter from the request's GET dictionary
        csv_file = request.GET.get('csv_file')

        # if parameter was passed in the request
        if csv_file in csv_files:
            # path to selected CSV file
            file_path = os.path.join(csv_folder, csv_file)
            # create a pandas dataframe
            df = pd.read_csv(file_path)
            # replace all spaces in columns names with underscores
            df.columns = df.columns.str.replace(' ', '_')
            # Convert the dataframe to a list of dictionaries representing each row
            rows = df.to_dict('records')
            # Set the title
            title = f"Statistics - {csv_file}"
            # Set the table title
            table_title = csv_file
            return render(request, 'ski/statistics.html', {'rows': rows, 'title': title, 'table_title': table_title})

    return render(request, 'ski/statistics.html', {'csv_files': csv_files, 'title': 'Statistics'})


def blog(request):

    return render(request, 'ski/blog.html', {'title': 'Blog'})
