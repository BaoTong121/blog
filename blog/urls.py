from django.conf.urls import url,include
from django.contrib import admin
from django.http import HttpRequest
from django.shortcuts import render

d = dict(zip('abcde', range(1, 6)))

def index(request:HttpRequest):
    return render(request, 'index.html', {'d': d})

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index$', index),
    url(r'^user/', include('user.urls')),
    url(r'^post/', include('post.urls'))
]
