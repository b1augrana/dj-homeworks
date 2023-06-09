import csv
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse

from pagination.settings import BUS_STATION_CSV


def index(request):
    return redirect(reverse('bus_stations'))

def cont_reader():
    result = []
    with open(BUS_STATION_CSV, newline='', encoding='UTF-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for line in reader:
            result.append(line) 
    return result


CONTENT = cont_reader()        


def bus_stations(request):
    # получите текущую страницу и передайте ее в контекст
    # также передайте в контекст список станций на странице
    page_num = int(request.GET.get('page', 1))
    paginator = Paginator(CONTENT, 10)
    page = paginator.get_page(page_num)
    context = {
         'bus_stations': page.object_list,
         'page': page,
        
    }
    return render(request, 'stations/index.html', context)
