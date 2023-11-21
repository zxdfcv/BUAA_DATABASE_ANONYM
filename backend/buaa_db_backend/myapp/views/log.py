from rest_framework.views import APIView

from ..utils import APIResponse


class TestView(APIView):

    def post(self, request, *args, **kwargs):
        s = str(request.user.__dict__)
        return APIResponse(code=0, msg='测试成功', data=s)
