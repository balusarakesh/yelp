from django.shortcuts import render
from yelp import get_all_restaurants
from yelp import get_db_status
from yelp import set_db_status
from multiprocessing import Process


def index(request):
    if get_db_status():
        return render(request, 'collector/wait.html')
    else:
        return render(request, 'collector/index.html')


def collect(request):
    """
    Collects data from the given places and locations.
    """
    if not get_db_status():
        locations = request.POST.get('locations')
        places = request.POST.get('places')
        p = Process(target=get_all_restaurants, args=(locations.split(','), places.split(',')))
        p.start()
        return render(request, 'collector/wait2.html')
    else:
        return render(request, 'collector/wait.html')
