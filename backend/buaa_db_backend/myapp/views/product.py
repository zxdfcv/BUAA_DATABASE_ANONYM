from rest_framework import generics
from rest_framework.decorators import permission_classes
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from ..models import Product, ProductImage
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
        queryset = self.filter_queryset(self.get_queryset())
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
