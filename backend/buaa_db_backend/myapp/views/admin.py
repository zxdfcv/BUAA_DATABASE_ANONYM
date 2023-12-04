from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView

from ..models import User, Product, Classification1, Classification2, ProductImage
from ..serializers import UserAllDetailSerializer, UserListSerializer, ProductAllDetailSerializer, \
    ProductImageSerializer, ProductCreateSerializer
from ..utils import APIResponse, make_error_log


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
