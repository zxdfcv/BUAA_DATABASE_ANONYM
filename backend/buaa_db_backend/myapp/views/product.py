from django.db.models import Q, ExpressionWrapper, F
from rest_framework import generics, fields
from rest_framework.decorators import permission_classes
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from django.db import models
from ..models import Product, ProductImage, User, Classification1, Classification2
from ..permissions import CanEditProductPermission
from ..serializers import ProductListSerializer, ProductCreateSerializer, ProductImageSerializer
from ..utils import APIResponse, make_error_log


class ProductWithImagesView(generics.ListAPIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    pagination_class = LimitOffsetPagination

    def get(self, request, *args, **kwargs):

        # tag要不要？
        keyword = request.GET.get("keyword", None)
        c_1 = request.GET.get("classification1", None)
        c_2 = request.GET.get("classification2", None)
        user = request.GET.get("user", None)
        is_sold = request.GET.get("sold", '0')
        status = request.GET.get("status", None)
        addr = request.GET.get("addr", None)
        price = request.GET.get("price", None)
        sort = request.GET.get("sort", 'create_time')

        queryset = self.filter_queryset(self.get_queryset()).filter(off_shelve=False)
        # page = self.paginate_queryset(queryset).filter(off_shelve=False)

        if is_sold == '0':
            queryset = queryset.filter(is_sold=False)
            # page = page.filter(is_sold=False)
        elif is_sold == '1':
            queryset = queryset.filter(is_sold=True)
            # page = page.filter(is_sold=True)
        elif is_sold and is_sold != '2':
            make_error_log(request, "is_sold参数不正确")
            return APIResponse(code=1,
                               msg='请传入正确的is_sold,取值为:0(在售),1(已售),2(全部)')

        if keyword:
            queryset = queryset.filter(name__contains=keyword)
            # page = page.filter(name__contains=keyword)

        if c_1:
            if not Classification1.objects.filter(id=c_1).exists():
                make_error_log(request, "查询商品时指定一级分类不存在")
                return APIResponse(code=1, msg='一级分类不存在')
            queryset = queryset.filter(classification_1_id=c_1)
            # page = page.filter(classification_1_id=c_1)

        if c_2:
            if not Classification2.objects.filter(id=c_2).exists():
                make_error_log(request, "查询商品时指定二级分类不存在")
                return APIResponse(code=1, msg='二级分类不存在')
            queryset = queryset.filter(classification_2_id=c_2)
            # page = page.filter(classification_2_id=c_2)

        if user:
            if not User.objects.filter(id=user).exists():
                make_error_log(request, "查询商品时指定用户不存在")
                return APIResponse(code=1, msg='指定用户不存在')
            queryset = queryset.filter(merchant_id=user)
            # page = page.filter(merchant_id=user)

        if status:
            if status not in ['A', 'B', 'C', 'D', 'E']:
                make_error_log(request, "查询商品时指定状态不存在")
                return APIResponse(code=1, msg='状态不正确,请确保值为以下之一:A,B,C,D,E')
            queryset = queryset.filter(status=status)
            # page = page.filter(status=status)

        if addr:
            if addr not in ['1', '2', '3']:
                make_error_log(request, "查询商品时指定地址不存在")
                return APIResponse(code=1, msg='地址不正确,请确保值为以下之一:1,2,3')
            queryset = queryset.filter(addr=addr)
            # page = page.filter(addr=addr)

        if price:
            price_ranges = {
                '1': (0, 49),
                '2': (50, 99),
                '3': (100, 199),
                '4': (200, 499),
                '5': (500, 999),
                '6': (1000, float('inf')),  # float('inf') 表示无穷大，即大于1000
            }
            if price not in price_ranges:
                make_error_log(request, "查询商品时指定价格区间不存在")
                return APIResponse(code=1,
                                   msg='价格区间不正确,请确保值为以下之一:1(<50),2(<100),3(<200),4(<500),5(<1000),6(>=1000)')
            selected_range = price_ranges.get(price)
            if selected_range:
                min_price, max_price = selected_range
                queryset = queryset.filter(Q(price__gte=min_price) & Q(price__lte=max_price))
                # page=page.filter(Q(price__gte=min_price) & Q(price__lte=max_price))

        if sort == 'hot':
            weighted_score = ExpressionWrapper(
                F('wants') * 6 + F('views'),
                output_field=models.IntegerField(),
            )
            queryset = queryset.annotate(weighted_score=weighted_score).order_by('-weighted_score',
                                                                                 '-create_time')
        else:
            queryset = queryset.order_by('-create_time')

        page = self.paginate_queryset(queryset)

        if page is not None:
            # serializer = self.get_serializer(page, many=True)
            product_images_data = []
            for product in page:
                images = ProductImageSerializer(product.product_image.all(), many=True).data
                product_data = ProductListSerializer(product).data
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
        # serializer = self.get_serializer(queryset, many=True)

        # 手动获取商品的图片信息并添加到序列化后的商品数据中
        product_images_data = []
        for product in queryset:
            images = ProductImageSerializer(product.product_image.all(), many=True).data
            product_data = ProductListSerializer(product).data
            product_data['images'] = images
            product_images_data.append(product_data)
        return APIResponse(code=0, msg='查询成功', data=product_images_data)


@permission_classes([CanEditProductPermission])
class EditProductView(APIView):
    def put(self, request):
        data = request.data.copy()
        excluded_fields = ['id', ]
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

        product_serializer = ProductCreateSerializer(data=data, partial=True)
        if product_serializer.is_valid():
            product_serializer.save()
            product_instance = product_serializer.instance

            images_data = request.data.getlist('images', [])
            for image_data in images_data:
                ProductImage.objects.create(product=product_instance, image=image_data)

            product_images = ProductImage.objects.filter(product=product_instance)
            product_images_serializer = ProductImageSerializer(product_images, many=True)
            product_data = product_serializer.data
            product_data['images'] = product_images_serializer.data

            return APIResponse(code=0, msg='商品创建成功', data=product_data)
        else:
            make_error_log(request, '创建商品失败')
            return APIResponse(code=1, msg='商品创建失败', data=product_serializer.errors)

# class ProductImageView(APIView):
#     def put(self, request, *args, **kwargs):
#         image_serializer = ProductImageSerializer(data=request.data)
#         if image_serializer.is_valid():
#             # 保存图片信息
#             image_serializer.save()
#
#             return APIResponse(code=0, msg='图片创建成功', data=image_serializer.data)
#         else:
#             return APIResponse(code=1, msg='图片创建失败', errors=image_serializer.errors)
