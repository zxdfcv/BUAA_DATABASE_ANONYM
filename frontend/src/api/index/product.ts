// 权限问题后期增加
import { deletes, get, post, put } from "/@/utils/http/axios";

// import axios from 'axios';
enum URL {
    list = '/myapp/product/list',
    detail = '/myapp/product/detail',
    addCollect = '/myapp/product/collector/add',
    deleteFromCollect = '/myapp/product/collector/remove',
    addProduct = '/myapp/product/create',
    deleteProduct = '/myapp/product/delete',
    updateProduct = '/myapp/product/update',
}

/**
 * const detailApi = async (params: any) => get<any>({ url: URL.detail, params: params, headers: {} });
 * const addWishUserApi = async (params: any) => post<any>({ url: URL.addWishUser, params: params, headers: {} });
 */

const getProductList = async (params: any) => get<any>({ url: URL.list, params: params, headers: {} });

const getProductDetail = async (params: any) => get<any>({url: URL.detail, params: params, headers: {}});

const addToCollect = async (params: any) => post<any>({url: URL.addCollect, params: params, headers: {}});

const deleteFromCollect = async (params: any) => deletes<any>({url: URL.deleteFromCollect, params: params, headers: {}});
const addProduct = async (data: any) => put<any>({url: URL.addProduct, params: {}, data: data, headers: { 'Content-Type': 'multipart/form-data;charset=utf-8' }});
const updateProduct = async (params: any, data: any) => post<any>({url: URL.updateProduct, params: params, data: data, headers: {}});
const deleteProduct = async (params: any, data: any) => deletes<any>({url: URL.deleteProduct, params: params, data: data, headers: {}});

export {
    getProductList, getProductDetail,            /* 商品信息查询 */
    addProduct, updateProduct, deleteProduct,    /* 单一商品增删改 */
    addToCollect, deleteFromCollect,             /* 商品收藏 */
};
