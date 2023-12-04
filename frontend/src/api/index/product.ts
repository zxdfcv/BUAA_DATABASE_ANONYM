// 权限问题后期增加
import { get, post } from '/@/utils/http/axios';
import { UserState } from '/@/store/modules/user/types';
// import axios from 'axios';
enum URL {
    list = '/myapp/product/list',
    detail = '/myapp/product/detail',
}

/**
 * const detailApi = async (params: any) => get<any>({ url: URL.detail, params: params, headers: {} });
 * const addWishUserApi = async (params: any) => post<any>({ url: URL.addWishUser, params: params, headers: {} });
 */

const getProductList = async (params: any) => get<any>({ url: URL.list, params: params, headers: {} });

const getProductDetail = async (params: any) => get<any>({url: URL.detail, params: params, headers: {}});

export {
    getProductList
};
