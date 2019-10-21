from django.http import HttpRequest, JsonResponse, HttpResponse,HttpResponseBadRequest
import simplejson
from .models import User
from django.conf import settings
import bcrypt
import jwt
import datetime
AUTH_EXPIRE = 8*60*60

def gen_token(user_id):
    return jwt.encode({
        'user_id': user_id,
        'exp': int(datetime.datetime.now().timestamp()) + AUTH_EXPIRE
    }, settings.SECRET_KEY, 'HS256').decode()

def reg(request: HttpRequest):
    try:
        payload = simplejson.loads(request.body)
        email = payload['email']
        name = payload['name']
        password = payload['password']
        qs = User.objects.filter(email=email)
        if qs:
            return HttpResponseBadRequest()
        else:
            user = User()
            user.email = email
            user.name = name
            user.password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            try:
                user.save()
                return JsonResponse({'token': gen_token(user.id)})
            except:
                raise
    except Exception as e:
        print(e)
        return HttpResponseBadRequest()

def login(request: HttpRequest):
    payload = simplejson.loads(request.body)
    try:
        email = payload['email']
        password = payload['password']
        user = User.objects.filter(email=email).get()
        token = gen_token(user.id)
        if not user:
            return HttpResponseBadRequest("用户名错误")
        if not bcrypt.checkpw(password.encode(), user.password.encode()):
            return HttpResponseBadRequest("密码错误")
        return JsonResponse({
            'user_id':user.id,
            'user_email':user.email,
            'user_name':user.name,
            'token':token

        })
    except Exception as e:
        print(e)
        return HttpResponseBadRequest()

def authenticate(view):
    def wrapper(request: HttpRequest):
        token = request.META.get('HTTP_JWK')
        if not token:
            return HttpResponse(status=401)
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload['user_id']
            user = User.objects.filter(pk=user_id).get()
            request.user = user
        except Exception as e:
            print(e)
            return HttpResponse(status=401)
        return view(request)
    return wrapper


@authenticate
def test(request:HttpRequest):
    return HttpResponse('test')

