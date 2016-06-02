from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim
import json
from models import DBStatusModel
from models import RestaurantModel
import requests
import re
from urllib2 import urlopen

def get_db_status():
    try:
        status = DBStatusModel.objects.get(pk=1)
        return status.status
    except Exception, e:
        print str(e)
        print 'Setting the status for the first time'
        DBStatusModel.objects.create(status=False)


def set_db_status(status):
    get_db_status()
    old_status = DBStatusModel.objects.get(pk=1)
    old_status.status = status
    old_status.save()


def get_city_from_address(address):
    try:
        geolocator = Nominatim()
        location = geolocator.geocode(address)
        if not location:
            for each in address.split(','):
                location = geolocator.geocode(each)
                if location:
                    break
        if location:
            lat = location.raw['lat']
            lon = location.raw['lon']
        else:
            print 'address invalid'
            return
        url = "http://maps.googleapis.com/maps/api/geocode/json?"
        url += "latlng=%s,%s&sensor=false" % (lat, lon)
        v = str(requests.get(url).content)
        j = json.loads(v)
        components = j['results'][0]['address_components']
        town = None
        for c in components:
            if "locality" in c['types']:
                town = c['long_name']
                if town:
                    break
        return town
    except Exception, e:
        print str(e) + 'get_location'
        set_db_status(False)
        


def replace_sp_with_plus(input):
    output = []
    try:
        for each in input:
            if ' ' in each:
                output.append(each.replace(' ', '+'))
            else:
                output.append(each)
        return output
    except Exception, e:
        print str(e) + 'replace'


def get_places_urls(LOCATIONS, PLACES):
    LOCATIONS = replace_sp_with_plus(LOCATIONS)
    PLACES = replace_sp_with_plus(PLACES)
    urls = []
    for location in LOCATIONS:
        for place in PLACES:
            urls.append('http://www.yelp.com/search?find_desc=' + place + '&find_loc=' + location)
    return urls


def get_no_of_pages(data):
    try:
        pg_data = BeautifulSoup(data).find('div', class_='pagination-block').text
        return re.findall('of[\s]*[0-9]*',pg_data)[0].replace('of', '').replace(' ','')
    except Exception, e:
        print str(e) + 'no pf pages'
        set_db_status(False)

def get_page_urls(url):
    try:
        pg_count = get_no_of_pages(get_text_from_url(url))
        count = 0
        url = url + '&start='
        urls = []
        for i in range(pg_count):
            index = url.find('&start=')
            url = url[0:index]
            url = url + '&start=' + str(count)
            urls.append(url)
            count = count + 10
        return urls
    except Exception, e:
        print str(e) + 'page urls'
        set_db_status(False)


def get_text_from_url(url):
    try:
        return str(requests.get(url).content)
    except Exception, e:
        set_db_status(False)
        print str(e) + 'text from url'


def get_restaurants(url):
    try:
        urls = get_page_urls(url)
        for url in urls:
            data = get_text_from_url(url)
            search_div = BeautifulSoup(str(data)).find('div', class_='search-results-content')
            uls = BeautifulSoup(str(search_div)).findAll('ul', class_='ylist ylist-bordered search-results')
            for restaurant in BeautifulSoup(str(uls[1])).findAll('li', class_='regular-search-result'):
                main_attrs = BeautifulSoup(str(restaurant)).find('div', class_='main-attributes')
    
                rating = BeautifulSoup(str(main_attrs)).find('div', class_='rating-large')
                rating_data = str(BeautifulSoup(str(rating)).find('i').attrs['title'])
                rating_data = rating_data.replace('star rating', '')
                
                review_count = str(BeautifulSoup(str(main_attrs)).find('span', class_='review-count rating-qualifier').text.strip())
                review_count = review_count.replace(' reviews', '')
    
                sub_url = BeautifulSoup(str(main_attrs)).find('a').attrs['href']
                url = 'http://www.yelp.com' + sub_url
    
                category_data = BeautifulSoup(str(main_attrs)).find('div', class_='price-category')
                category_str_list = BeautifulSoup(str(category_data)).findAll('span', class_='category-str-list')
                categories = ''
                for a in BeautifulSoup(str(category_str_list)).findAll('a'):
                    categories = categories +  a.text.strip() + ','
    
                expensive_level = BeautifulSoup(str(category_data)).find('span', 'business-attribute price-range').text
                
    
                h3 = BeautifulSoup(str(restaurant)).find('h3', class_='search-result-title')
                h3_a = BeautifulSoup(str(h3)).find('a').text
                name = h3_a.strip()
    
                sec_attrs = BeautifulSoup(str(restaurant)).find('div', class_='secondary-attributes')
                address = BeautifulSoup(str(sec_attrs)).find('address')
                if '<br/>' in str(address):
                    address = str(address).replace('<br/>', ' ')
                address = BeautifulSoup(str(address)).find('address').text.strip()
    
                city = get_city_from_address(address)
    
                if not str(city).lower() in address.lower():
                    print 'Invalid city detected'
                RestaurantModel.objects.create(
                    name=name,
                    expensivelevel=expensive_level,
                    city=city,
                    current_rating=float(rating_data),
                    url=url,
                    category=categories,
                    address=address,
                    reviewcount=review_count
                        )
        set_db_status(False)
    except Exception, e:
        print str(e) + 'get restturats'
        set_db_status(False)
    
def get_all_restaurants(LOCATIONS, PLACES):
    try:
        set_db_status(True)
        for url in get_places_urls(LOCATIONS, PLACES):
            get_restaurants(url)
    except Exception, e:
        print str(e) + 'get all restaturant'
        set_db_status(False)
