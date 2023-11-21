import time
import json

from django.utils.deprecation import MiddlewareMixin

from .. import utils
from ..serializers import OpLogSerializer


class OpLogs(MiddlewareMixin):

    def __init__(self, *args):
        super(OpLogs, self).__init__(*args)

        self.start_time = None  # 开始时间
        self.end_time = None  # 响应时间
        self.data = {}

    def process_request(self, request):

        self.start_time = time.time()  # 开始时间

        re_ip = utils.get_ip(request)
        re_method = request.method

        if request.method in ['GET', 'POST']:
            re_content = request.GET if re_method == 'GET' else request.POST
        else:

            try:
                re_content = json.loads(request.body.decode('utf-8'))
            except json.JSONDecodeError:
                re_content = None

        self.data.update(
            {
                're_url': request.path,
                're_method': re_method,
                're_ip': re_ip,
                're_content': json.dumps(re_content) if re_content else None,
            }
        )

    def process_response(self, request, response):
        self.end_time = time.time()  # 响应时间
        access_time = self.end_time - self.start_time
        self.data['access_time'] = round(access_time * 1000)

        serializer = OpLogSerializer(data=self.data)
        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)
        return response
