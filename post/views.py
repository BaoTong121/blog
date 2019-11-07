from django.http import HttpResponse, HttpResponseBadRequest, HttpRequest,Http404,JsonResponse
from user.views import authenticate
import simplejson
import datetime
from .models import Post, Content
import math

def validate(d:dict,name:str,type_func,default,vali_func):
    try:
        reg = type_func(d.get(name, default))
        reg = vali_func(reg, default)
    except:
        reg = default
    return reg

@authenticate
def put(request: HttpRequest):
    post = Post()
    content = Content()
    try:
        payload = simplejson.loads(request.body)
        post.title = payload['title']
        post.author = request.user
        post.postdate = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))
        post.save()
        content.content = payload['content']
        content.post = post
        content.save()
        return HttpResponse('put')
    except Exception as e:
        print(e)
        return HttpResponseBadRequest()

def get(request:HttpRequest,id):
    try:
        id = int(id)
        post = Post.objects.get(pk=id)
        return JsonResponse({
            'post_id': post.id,
            'title': post.title,
            'content': post.content.content,
            'author': post.author.name,
            'pubdate': post.postdate,
            'author_id': post.author_id,
        })
    except Exception as e:
        print(e)
        return HttpResponseBadRequest()

def getall(request:HttpRequest):
    page = validate(request.GET, 'page', int, 1, lambda x, y: x if x > 0 else y)
    size = validate(request.GET, 'size', int, 20, lambda x, y: x if x > 0 and x < 101 else y)
    try:
        start = (page - 1) * size
        posts = Post.objects.order_by('-id')
        count = posts.count()
        posts = posts[start:start + size]
        return JsonResponse({
            'posts': [{
                'post_id': post.id,
                'title': post.title
                } for post in posts
            ], 'pagination': {
                'page': page,
                'size': size,
                'count': count,
                'pages': math.ceil(count / size)
            }
        })
    except Exception as e:
        print(e)
        return HttpResponseBadRequest()

