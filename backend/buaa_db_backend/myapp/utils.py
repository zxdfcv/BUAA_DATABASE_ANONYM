from rest_framework.response import Response


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
