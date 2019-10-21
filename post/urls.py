from django.conf.urls import url
from .views import put, get, getall
urlpatterns = [
    url(r'^put', put),
    url(r'^(/d+)$', get),
    url(r'^$', getall)
]
