from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny

from ..models import Tag


class Classification1ListView(generics.ListAPIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    pagination_class = LimitOffsetPagination

    def get(self, request, *args, **kwargs):
        tags = Tag.objects.all().order_by('-create_time')

