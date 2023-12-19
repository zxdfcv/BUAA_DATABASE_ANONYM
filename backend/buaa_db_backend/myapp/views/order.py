from datetime import datetime

from alipay import AliPay
from django.db.models import Max
from django.utils import timezone
from rest_framework import generics
from rest_framework.decorators import permission_classes
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from django.db import transaction

from ..models import Product, Order
from ..permissions import CanBuyPermission
from ..serializers import OrderSerializer
from ..utils import make_error_log, APIResponse
from django.conf import settings


@permission_classes([CanBuyPermission])
class EditOrderView(APIView):
    @transaction.atomic
    def put(self, request):

        product_id = request.data.get('product', '')
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            make_error_log(request, '下单时商品不存在')
            return APIResponse(code=1, msg='商品不存在')

        data = request.data.copy()
        excluded_fields = ['id', 'order_number', 'status', 'create_time', 'pay_time']
        for field in excluded_fields:
            data.pop(field, None)
        # receiver = request.user
        # if str(receiver.id) != data["receiver"]:
        #     make_error_log(request, '下单非本人')
        #     return APIResponse(code=1, msg='下单非本人')

        data['amount'] = str(product.price)
        data['merchant'] = str(product.merchant.id)
        data['receiver'] = str(request.user.id)
        # print(data['amount'])
        # print(data['merchant'])
        # print(data['receiver'])
        user_id = request.user.id
        max_order_id = Order.objects.aggregate(max_id=Max('id'))['max_id']
        if not max_order_id:
            max_order_id = 1
        else:
            max_order_id += 1
        order_number = datetime.now().strftime("%Y%m%d%H%M%S") + "%06d" % user_id + "%06d" % max_order_id
        data['order_number'] = str(order_number)

        serializer = OrderSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return APIResponse(code=1, msg='下单成功', data=serializer.data)

        make_error_log(request, '下单失败')
        return APIResponse(code=1, msg='下单失败', data=serializer.errors)

    # def post(self, request):

    @transaction.atomic
    def post(self, request):
        order_number = request.GET.get("order_number")
        try:
            order = Order.objects.get(order_number=order_number)
        except Order.DoesNotExist:
            make_error_log(request, '支付时订单不存在')
            return APIResponse(code=1, msg='订单不存在')
        receiver = request.user
        if receiver != order.receiver:
            make_error_log(request, '订单支付错误')
            return APIResponse(code=1, msg='不是你的订单')
        order.status = 2
        order.save()
        return APIResponse(code=0, msg='订单取消成功')


# @permission_classes([CanBuyPermission])
class OrderListView(generics.ListAPIView):
    pagination_class = LimitOffsetPagination

    @transaction.atomic
    def get(self, request, *args, **kwargs):
        user = request.user
        orders = Order.objects.all()
        user_type = request.GET.get("user_type")
        if user_type == 'merchant':
            orders = orders.filter(merchant=user).order_by('-create_time')
        else:
            orders = orders.filter(receiver=user).order_by('-create_time')
        page = self.paginate_queryset(orders)
        if page is not None:
            serializer = OrderSerializer(page, many=True)
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
        serializer = OrderSerializer(orders, many=True)
        return APIResponse(code=0, msg='查询成功', data=serializer.data)


class AlipayAPIView(APIView):
    def get(self, request):
        order_number = request.GET.get("order_number")
        try:
            order = Order.objects.get(order_number=order_number)
        except Order.DoesNotExist:
            make_error_log(request, '支付时订单不存在')
            return APIResponse(code=1, msg='订单不存在')

        if order.status == '2':
            make_error_log(request, '支付时订单已经取消')
            return APIResponse(code=1, msg='订单已取消')

        if order.status == '1':
            make_error_log(request, '支付时订单已经支付')
            return APIResponse(code=1, msg='订单已支付')

        receiver = request.user
        if receiver != order.receiver:
            make_error_log(request, '订单支付错误')
            return APIResponse(code=1, msg='不是你的订单')
        # 初始化支付对象
        alipay = AliPay(
            appid=settings.ALIAPY_CONFIG["appid"],
            app_notify_url=settings.ALIAPY_CONFIG["app_notify_url"],
            app_private_key_string=settings.ALIAPY_CONFIG["app_private_key_string"],
            alipay_public_key_string=settings.ALIAPY_CONFIG["alipay_public_key_string"],
            sign_type=settings.ALIAPY_CONFIG["sign_type"],
            debug=settings.ALIAPY_CONFIG["debug"]
            # debug=True
        )

        # 调用接口
        order_string = alipay.api_alipay_trade_page_pay(
            out_trade_no=order.order_number,
            total_amount=float(order.amount),
            subject=order.product.name,
            return_url=settings.ALIAPY_CONFIG["return_url"],
            notify_url=settings.ALIAPY_CONFIG["notify_url"]  # 可选, 不填则使用默认notify url
        )

        url = settings.ALIAPY_CONFIG["gateway_url"] + order_string

        return APIResponse(code=0, msg='操作成功', data={'支付url': url})


class AliPayResultAPIView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request):
        """处理支付宝同步通知结果"""
        # 初始化支付对象
        alipay = AliPay(
            appid=settings.ALIAPY_CONFIG["appid"],
            app_notify_url=settings.ALIAPY_CONFIG["app_notify_url"],  # 默认回调url
            app_private_key_string=settings.ALIAPY_CONFIG["app_private_key_string"],
            alipay_public_key_string=settings.ALIAPY_CONFIG["alipay_public_key_string"],
            sign_type=settings.ALIAPY_CONFIG["sign_type"],
            debug=settings.ALIAPY_CONFIG["debug"]  # 默认False
        )

        data = request.query_params.dict()
        signature = data.pop("sign")
        # verification
        success = alipay.verify(data, signature)
        if success:
            return self.change_order_status(data, request)
        make_error_log(request, "支付失败")
        return APIResponse(code=1, msg='支付失败')

    def post(self, request):
        """处理支付宝异步通知结果"""
        # 初始化支付对象
        alipay = AliPay(
            appid=settings.ALIAPY_CONFIG["appid"],
            app_notify_url=settings.ALIAPY_CONFIG["app_notify_url"],  # 默认回调url
            app_private_key_string=settings.ALIAPY_CONFIG["app_private_key_string"],
            alipay_public_key_string=settings.ALIAPY_CONFIG["alipay_public_key_string"],
            sign_type=settings.ALIAPY_CONFIG["sign_type"],
            debug=settings.ALIAPY_CONFIG["debug"]  # 默认False
        )

        data = request.data
        signature = data.pop("sign")
        success = alipay.verify(data, signature)
        if success and data["trade_status"] in ("TRADE_SUCCESS", "TRADE_FINISHED"):
            return self.change_order_status(data, request)

        make_error_log(request, "支付失败")
        return APIResponse(code=1, msg='支付失败')

    def change_order_status(self, data, request):
        # 补充支付成功以后的代码
        order_number = data.get("out_trade_no")
        try:
            order = Order.objects.get(order_number=order_number, status=0)
        except Order.DoesNotExist:
            make_error_log(request, "订单不存在")
            return APIResponse(code=1, msg='订单不存在')

        with transaction.atomic():
            save_id = transaction.savepoint()
            # 更新订单状态、记录支付时间
            try:
                order.pay_time = timezone.now()
                order.status = 1
                order.save()

                # 如果有使用优惠券或者积分，则修改优惠券的使用状态和扣除积分
                # user_coupon_id = order.coupon
                # if user_coupon_id > 0:
                #     user_coupon = UserCoupon.objects.get(pk=user_coupon_id, is_use=False, is_show=True,
                #                                          is_deleted=False)
                #     user_coupon.is_use = True
                #     user_coupon.save()

                # credit = order.credit
                # if credit > 0:
                #     user = order.user
                #     user.credit -= credit
                #     user.save()

                # 记录用户成功购买课程的记录, 增加课程的购买人数
                # order_detail_list = order.order_courses.all()
                # course_list = []
                # for order_detail in order_detail_list:
                #     """循环本次订单中所有购买的商品课程"""
                #     course = order_detail.course
                #     course.students += 1
                #     course.save()
                #
                #     course_list.append({
                #         "id": course.id,
                #         "name": course.name
                #     })

            except:
                # log.error("订单结果处理出现故障!无法修改订单相关记录的状态")
                make_error_log(request, "无法修改订单相关记录的状态")
                transaction.savepoint_rollback(save_id)
                return APIResponse(code=1, msg='更新订单相关记录失败')
        serializer = OrderSerializer(order)
        return APIResponse(code=0, msg="支付成功", data=serializer.data)
