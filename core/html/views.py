# -*- encoding: utf-8 -*-

from django.shortcuts import render


def html_grid(request):
    return render(request, 'grid.html', {})

def html_home(request):
    return render(request, 'home.html', {})
