from django.shortcuts import render


def index(request, id=''):
    return render(request, 'build/index.html')
