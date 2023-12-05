import datetime

from rest_framework.pagination import PageNumberPagination
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


def make_login_log(request):
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


def make_error_log(request, content):
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


class MyPageNumberPagination(PageNumberPagination):
    page_size = 36  # 设置每页显示的对象数量
    page_size_query_param = 'page_size'  # 通过 ?page_size= 指定每页的对象数量
    max_page_size = 100  # 设置最大允许的页面大小

    def get_paginated_response(self, data):
        return APIResponse(
            code=0,
            msg='查询成功',
            data={
                'count': self.page.paginator.count,
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
                'results': data,
            }
        )


def dict_fetchall(cursor):  # cursor是执行sql_str后的记录，作入参
    columns = [col[0] for col in cursor.description]  # 得到域的名字col[0]，组成List
    return [
        dict(zip(columns, row)) for row in cursor.fetchall()
    ]


def getWeekDays():
    """
    获取近一周的日期
    """
    week_days = []
    now = datetime.datetime.now()
    for i in range(7):
        day = now - datetime.timedelta(days=i)
        week_days.append(day.strftime('%Y-%m-%d %H:%M:%S.%f')[:10])
    week_days.reverse()  # 逆序
    return week_days


def get_monday():
    """
    获取本周周一日期
    """
    now = datetime.datetime.now()
    monday = now - datetime.timedelta(now.weekday())
    return monday.strftime('%Y-%m-%d %H:%M:%S.%f')[:10]
