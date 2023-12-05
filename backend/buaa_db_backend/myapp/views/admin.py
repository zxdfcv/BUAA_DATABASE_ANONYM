from datetime import datetime
from random import random
from django.db import connection
from django.db.models import When, Count
from django.forms import IntegerField
from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from sqlparse.sql import Case

from ..models import User, Product, Classification1, Classification2, ProductImage
from ..serializers import UserAllDetailSerializer, UserListSerializer, ProductAllDetailSerializer, \
    ProductImageSerializer, ProductCreateSerializer
from ..utils import APIResponse, make_error_log, dict_fetchall, getWeekDays


class StatisticsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        # now = datetime.datetime.now()

        sql_str = "select id, name, views as count from buaa_db_product  order by views desc limit 10 "
        with connection.cursor() as cursor:
            cursor.execute(sql_str)
            product_rank_data = dict_fetchall(cursor)

        sql_str = "select B.name, count(B.name) as count from buaa_db_product A join buaa_db_classification_1 B on " \
                  "A.classification_1_id = B.id group by B.name order by count desc limit 5; "
        with connection.cursor() as cursor:
            cursor.execute(sql_str)
            classification1_rank_data = dict_fetchall(cursor)

        sql_str = "select B.name, count(B.name) as count from buaa_db_product A join buaa_db_classification_2 B on " \
                  "A.classification_2_id = B.id group by B.name order by count desc limit 5; "
        with connection.cursor() as cursor:
            cursor.execute(sql_str)
            classification2_rank_data = dict_fetchall(cursor)

        sql_str = "select gender, count(gender) as count from buaa_db_user group by gender order by " \
                  "count desc;"

        with connection.cursor() as cursor:
            cursor.execute(sql_str)
            user_gender_rank_data = dict_fetchall(cursor)

        sql_str = "select addr, count(addr) as count from buaa_db_product group by addr order by count " \
                  "desc;"
        with connection.cursor() as cursor:
            cursor.execute(sql_str)
            product_addr_rank_data = dict_fetchall(cursor)

        # price_statistics = Product.objects.annotate(
        #     price_range=Case(
        #         When(price__lt=50, then=Value(1)),
        #         When(price__gte=50, price__lt=100, then=Value(2)),
        #         When(price__gte=100, price__lt=200, then=Value(3)),
        #         When(price__gte=200, price__lt=500, then=Value(4)),
        #         When(price__gte=500, price__lt=1000, then=Value(5)),
        #         When(price__gte=1000, then=Value(6)),
        #         output_field=IntegerField(),
        #     )
        # ).values('price_range').annotate(product_count=Count('id')).order_by('price_range')
        #
        # # 将 QuerySet 转换为列表，构造包含字典的列表
        # statistics_list = [{item['price_range']: item['product_count']} for item in price_statistics]

        sql_str = "SELECT " \
                  "CASE " \
                  "WHEN price < 50 THEN 1 " \
                  "WHEN price >= 50 AND price < 100 THEN 2 " \
                  "WHEN price >= 100 AND price < 200 THEN 3 " \
                  "WHEN price >= 200 AND price < 500 THEN 4 " \
                  "WHEN price >= 500 AND price < 1000 THEN 5 " \
                  "WHEN price >= 1000 THEN 6 " \
                  "END AS price_range, " \
                  "COUNT(*) AS count " \
                  "FROM buaa_db_product " \
                  "GROUP BY price_range " \
                  "ORDER BY price_range;"
        with connection.cursor() as cursor:
            cursor.execute(sql_str)
            product_price_rank_data = dict_fetchall(cursor)

        # 统计最近一周访问量(sql语句)
        visit_data = []
        week_days = getWeekDays()
        for day in week_days:
            sql_str = "select re_ip, count(re_ip) as count from buaa_db_op_log where re_time like '" + day + "%' group by re_ip"
            with connection.cursor() as cursor:
                cursor.execute(sql_str)
                ip_data = dict_fetchall(cursor)
                uv = len(ip_data)
                pv = 0
                for item in ip_data:
                    pv = pv + item['count']
                visit_data.append({
                    "day": day,
                    "uv": uv,
                    "pv": pv
                })

        data = {
            'product_rank_data': product_rank_data,
            'classification1_rank_data': classification1_rank_data,
            'classification2_rank_data': classification2_rank_data,
            'user_gender_rank_data': user_gender_rank_data,
            'product_addr_rank_data': product_addr_rank_data,
            'product_price_rank_data': product_price_rank_data,
            'visit_data': visit_data
        }
        return APIResponse(code=0, msg='查询成功', data=data)


class UserAllDetailView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        try:
            user_id = request.GET.get('user_id', -1)
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            make_error_log(request, '用户不存在')
            return APIResponse(code=1, msg='用户不存在')
        serializer = UserAllDetailSerializer(user)
        return APIResponse(code=0, msg='查询成功', data=serializer.data)

    def post(self, request):
        try:
            user_id = request.GET.get('user_id', -1)
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            make_error_log(request, '用户不存在')
            return APIResponse(code=1, msg='用户不存在')
        data = request.data.copy()
        serializer = UserAllDetailSerializer(user, data=data,
                                             # partial=True
                                             )
        if serializer.is_valid():
            serializer.save()
            return APIResponse(code=0, msg='更新成功', data=serializer.data)
        make_error_log(request, '用户更新失败')
        return APIResponse(code=1, msg='更新失败', data=serializer.errors)


class UserListView(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    pagination_class = LimitOffsetPagination

    def get(self, request, *args, **kwargs):
        keyword = request.GET.get("keyword", '')
        users = User.objects.filter(username__contains=keyword).order_by('-date_joined')
        page = self.paginate_queryset(users)
        if page is not None:
            serializer = UserAllDetailSerializer(page, many=True)
            return APIResponse(
                code=0,
                msg='查询成功',
                data={
                    'count': self.paginator.count,
                    'next': self.paginator.get_next_link(),
                    'previous': self.paginator.get_previous_link(),
                    'results': serializer.data,
                }
            )
        serializer = UserAllDetailSerializer(users, many=True)
        return APIResponse(code=0, msg='查询成功', data=serializer.data)
        # serializer = UserListSerializer(users, many=True)
        # return APIResponse(code=0, msg='查询成功', data=serializer.data)

    def delete(self, request):
        ids = request.GET.get('ids')
        ids_arr = ids.split(',')
        users = User.objects.filter(id__in=ids_arr)
        if users.count() != len(ids_arr):
            make_error_log(request, '注销的用户不存在')
            return APIResponse(code=1, msg='注销的用户不存在')
        for user in users:
            user.is_active = False
            user.save()
        return APIResponse(code=0, msg='用户注销成功')


class ProductDetailListView(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    queryset = Product.objects.all()
    serializer_class = ProductAllDetailSerializer
    pagination_class = LimitOffsetPagination

    def get(self, request, *args, **kwargs):
        keyword = request.GET.get("keyword", None)
        queryset = self.filter_queryset(self.get_queryset()).order_by('-create_time')
        if keyword:
            queryset = queryset.filter(name__contains=keyword)
        page = self.paginate_queryset(queryset)

        if page is not None:
            product_images_data = []
            for product in page:
                images = ProductImageSerializer(product.product_image.all(), many=True).data
                product_data = ProductAllDetailSerializer(product).data
                product_data['images'] = images
                product_images_data.append(product_data)
            return APIResponse(
                code=0,
                msg='查询成功',
                data={
                    'count': self.paginator.count,
                    'next': self.paginator.get_next_link(),
                    'previous': self.paginator.get_previous_link(),
                    'results': product_images_data,
                }
            )

        product_images_data = []
        for product in queryset:
            images = ProductImageSerializer(product.product_image.all(), many=True).data
            product_data = ProductAllDetailSerializer(product).data
            product_data['images'] = images
            product_images_data.append(product_data)
        return APIResponse(code=0, msg='查询成功', data=product_images_data)


class EditProductDetailView(APIView):
    permission_classes = [IsAdminUser]

    def put(self, request):
        data = request.data.copy()
        user_ids = data.getlist('collectors', [])
        excluded_fields = ['id', 'collectors']

        for field in excluded_fields:
            data.pop(field, None)

        if 'classification_1' in data and 'classification_2' in data:
            classification_1_id = data['classification_1']
            classification_2_id = data['classification_2']
            try:
                classification_1 = Classification1.objects.get(pk=classification_1_id)
                classification_2 = Classification2.objects.get(pk=classification_2_id)
                if classification_2.classification_1 != classification_1:
                    make_error_log(request, "创建商品时二级分类不属于一级分类")
                    return APIResponse(code=1, msg='二级分类不属于一级分类')
            except Classification1.DoesNotExist:
                make_error_log(request, "创建商品时指定一级分类不存在")
                return APIResponse(code=1, msg='一级分类不存在')
            except Classification2.DoesNotExist:
                make_error_log(request, "创建商品时指定二级分类不存在")
                return APIResponse(code=1, msg='二级分类不存在')

        for user_id in user_ids:
            if not User.objects.filter(id=user_id).exists():
                make_error_log(request, '用户不存在')
                return APIResponse(code=1, msg='用户不存在')

        product_serializer = ProductAllDetailSerializer(data=data,
                                                        # partial=True
                                                        )
        if product_serializer.is_valid():
            product_instance = product_serializer.save()
        else:
            make_error_log(request, '创建商品失败')
            return APIResponse(code=1, msg='商品创建失败', data=product_serializer.errors)

        # product_id = product_instance.id

        for user_id in user_ids:
            user = User.objects.get(pk=user_id)
            product_instance.collectors.add(user)

        product_instance.save()

        images_data = request.data.getlist('images', [])
        for image_data in images_data:
            ProductImage.objects.create(product=product_instance, image=image_data)
        product_images = ProductImage.objects.filter(product=product_instance)
        product_images_serializer = ProductImageSerializer(product_images, many=True)

        product_data = ProductAllDetailSerializer(product_instance).data
        product_data['images'] = product_images_serializer.data
        return APIResponse(code=0, msg='商品创建成功', data=product_data)

    def post(self, request):

        product_id = request.GET.get('product_id')

        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            make_error_log(request, '修改商品时商品不存在')
            return APIResponse(code=1, msg='商品不存在')

        remove_images_ids = request.data.getlist('remove_images_ids', [])
        remove_collectors_ids = request.data.getlist('remove_collectors_ids', [])
        user_ids = request.data.getlist('collectors', [])
        images_data = request.data.getlist('images', [])

        product_images = ProductImage.objects.filter(product=product, id__in=remove_images_ids)
        if len(product_images) != len(remove_images_ids):
            make_error_log(request, '修改商品时删除的图片不存在或不属于该商品')
            return APIResponse(code=1, msg='删除的图片不存在或不属于该商品')

        for user_id in remove_collectors_ids:
            if not User.objects.filter(id=user_id).exists():
                make_error_log(request, '用户不存在')
                return APIResponse(code=1, msg='用户不存在')

        for user_id in user_ids:
            if not User.objects.filter(id=user_id).exists():
                make_error_log(request, '用户不存在')
                return APIResponse(code=1, msg='用户不存在')

        data = request.data.copy()
        excluded_fields = ['id', 'collectors']
        for field in excluded_fields:
            data.pop(field, None)

        if 'classification_1' in data and 'classification_2' in data:
            classification_1_id = data['classification_1']
            classification_2_id = data['classification_2']
            try:
                classification_1 = Classification1.objects.get(pk=classification_1_id)
                classification_2 = Classification2.objects.get(pk=classification_2_id)
                if classification_2.classification_1 != classification_1:
                    make_error_log(request, "更新商品时二级分类不属于一级分类")
                    return APIResponse(code=1, msg='二级分类不属于一级分类')
            except Classification1.DoesNotExist:
                make_error_log(request, "更新商品时指定一级分类不存在")
                return APIResponse(code=1, msg='一级分类不存在')
            except Classification2.DoesNotExist:
                make_error_log(request, "更新商品时指定二级分类不存在")
                return APIResponse(code=1, msg='二级分类不存在')

        product_serializer = ProductAllDetailSerializer(product, data=data,
                                                        # partial=True
                                                        )
        if product_serializer.is_valid():
            product_serializer.save()
        else:
            make_error_log(request, '更新商品失败')
            return APIResponse(code=1, msg='更新商品失败', data=product_serializer.errors)

        for user_id in remove_collectors_ids:
            user = User.objects.get(pk=user_id)
            product.collectors.remove(user)

        for user_id in user_ids:
            user = User.objects.get(pk=user_id)
            product.collectors.add(user)

        product.save()

        for product_image in product_images:
            product_image.image.delete()
            product_image.delete()

        for image_data in images_data:
            ProductImage.objects.create(product=product, image=image_data)

        product_images = ProductImage.objects.filter(product=product)
        product_images_serializer = ProductImageSerializer(product_images, many=True)
        product_data = ProductAllDetailSerializer(product).data
        product_data['images'] = product_images_serializer.data

        return APIResponse(code=0, msg='商品更新成功', data=product_data)

    def delete(self, request):
        ids = request.GET.get('ids')
        ids_arr = ids.split(',')
        products = Product.objects.filter(id__in=ids_arr)
        if products.count() != len(ids_arr):
            make_error_log(request, '删除的商品不存在')
            return APIResponse(code=1, msg='删除的商品不存在')
        for product in products:
            product_images = ProductImage.objects.filter(product=product)
            for product_image in product_images:
                product_image.image.delete()
                product_image.delete()
            product.delete()
        return APIResponse(code=0, msg='商品删除成功')
