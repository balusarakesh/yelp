from views import index
from views import collect
from django.conf.urls import url

app_name = 'collector'

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^collect$', collect, name='collect')
    ]