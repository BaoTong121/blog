from django.http import HttpResponse, HttpResponseBadRequest, HttpRequest,Http404,JsonResponse
from user.views import authenticate
import simplejson
import datetime
from .models import Post, Content

@authenticate
def put(request: HttpRequest):
    post = Post()
    content = Content()
    try:
        payload = simplejson.loads(request.body)
        post.title = payload["title"]
        post.author = request.user
        post.postdate = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))
        post.save()
        content.content = payload["content"]
        content.post = post
        content.save()
        return HttpResponse("put")
    except Exception as e:
        print(e)
        return HttpResponseBadRequest()

def get(request:HttpRequest):
    return HttpResponse("get")

def getall(request:HttpRequest):
    return HttpResponse('getall')

