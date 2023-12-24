// 权限问题后期增加
import { deletes, get, post, put } from "/@/utils/http/axios";

// import axios from 'axios';
enum URL {
    list = '/myapp/admin/product/list',
    create = '/myapp/admin/product/create',
    update = '/myapp/admin/product/update',
    delete = '/myapp/admin/product/delete',
    detail = '/api/product/detail',
}

const listApi = async (params: any) => get<any>({ url: URL.list, params: params, data: {}, headers: {} });
const createApi = async (data: any) =>
    put<any>({ url: URL.create, params: {}, data: data, timeout:20000, headers: { 'Content-Type': 'multipart/form-data;charset=utf-8' } });
const updateApi = async (params:any, data: any) =>
    post<any>({ url: URL.update,params: params, data: data, headers: { 'Content-Type': 'multipart/form-data;charset=utf-8' } });
const deleteApi = async (params: any) => deletes<any>({ url: URL.delete, params: params, headers: {} });
const detailApi = async (params: any) => get<any>({ url: URL.detail, params: params, headers: {} });

export { listApi, createApi, updateApi, deleteApi, detailApi };
