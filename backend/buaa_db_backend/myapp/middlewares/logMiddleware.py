import time
import json
import chardet
from django.utils.deprecation import MiddlewareMixin

from .. import utils
from ..serializers import OpLogSerializer

def decode_request_body(request_body):
    # 使用 chardet 检测编码
    detected_encoding = chardet.detect(request_body)['encoding']

    # 如果检测到了编码，使用检测到的编码进行解码
    if detected_encoding:
        try:
            decoded_body = request_body.decode(detected_encoding)
            return json.loads(decoded_body)
        except (json.JSONDecodeError, UnicodeDecodeError):
            pass

    # 如果检测不到编码或解码失败，则返回 None
    return None

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

        # if request.method in ['GET', 'POST']:
        #     re_content = request.GET if re_method == 'GET' else request.POST
        # else:
        #
        #     try:
        #         re_content = json.loads(request.body.decode('utf-8'))
        #     except (json.JSONDecodeError, UnicodeDecodeError):
        #         re_content = None
        if request.method in ['GET', 'POST']:
            re_content = request.GET if re_method == 'GET' else request.POST
        else:
            request_body = request.body
            re_content = decode_request_body(request_body)
        # re_content只截了200个字符，有点暴力的处理，之后有时间再改吧
        self.data.update(
            {
                're_url': request.path,
                're_method': re_method,
                're_ip': re_ip,
                're_content': json.dumps(re_content)[:200] if re_content else None,
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
