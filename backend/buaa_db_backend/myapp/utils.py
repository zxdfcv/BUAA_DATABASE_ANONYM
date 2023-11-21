from rest_framework.response import Response

from .serializers import ErrorLogSerializer, LoginLogSerializer


class APIResponse(Response):
    def __init__(self, code=0, msg='', data=None, status=None, headers=None, content_type=None, **kwargs):
        dic = {'code': code, 'msg': msg}
        if data is not None:
            dic['data'] = data
        if status is None:
            status = 200 if code == 0 else 400
        dic.update(kwargs)
        super().__init__(data=dic, status=status,
                         template_name=None, headers=headers,
                         exception=False, content_type=content_type)


def get_ip(request):
    """
    获取请求者的IP信息
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_ua(request):
    """
    获取请求者的UA信息
    """
    ua = request.META.get('HTTP_USER_AGENT')
    return ua[0:200]


def login_log(request):
    username = request.data['username']
    data = {
        "username": username,
        "ip": get_ip(request),
        "ua": get_ua(request)
    }
    serializer = LoginLogSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
    else:
        print(serializer.errors)


def error_log(request, content):
    ip = get_ip(request)
    method = request.method
    url = request.path
    data = {
        'ip': ip,
        'method': method,
        'url': url,
        'content': content
    }
    serializer = ErrorLogSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
    else:
        print(serializer.errors)
