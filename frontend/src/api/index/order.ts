import { get, post, put } from "/@/utils/http/axios";

enum URL {
    createOrder='/myapp/order/create',
    payOrder = '/myapp/order/pay',
    cancelOrder = '/myapp/order/cancel',
    userOrderList = '/myapp/order/list',
}

const createOrderApi = async (data: any) => put<any>({url: URL.createOrder, data: data, headers: {}});
const payOrderApi = async (params: any) => get<any>({url: URL.payOrder, params: params, data: {}, headers: {}});

const cancelOrderApi = async (params: any) => post<any>({url: URL.cancelOrder, params: params, headers: {}});

const getOrderListApi = async (params: any) => get<any>({url: URL.userOrderList, params: params, data: {}, headers: {}});



export { createOrderApi, payOrderApi, cancelOrderApi, getOrderListApi };
