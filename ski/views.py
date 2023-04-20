from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return render(request, 'ski/home.html')


def about(request):
    return render(request, 'ski/about.html', {'title': 'About'})


def live(request):
    return render(request, 'ski/live.html', {'title': 'LIVE'})


def fantasy_league(request):
    return render(request, 'ski/fantasy-league.html', {'title': 'Fantasy League'})


def statistics(request):
    return render(request, 'ski/statistics.html', {'title': 'Statistics'})


def blog(request):
    return render(request, 'ski/blog.html', {'title': 'Blog'})
