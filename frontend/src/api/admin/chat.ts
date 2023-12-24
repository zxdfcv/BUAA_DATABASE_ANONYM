import { deletes, get, post, put } from "/@/utils/http/axios";

enum URL {
    list = '/myapp/admin/chat/list',
    create = '/myapp/admin/chat/create',
    delete = '/myapp/admin/chat/delete',
    update = '/myapp/admin/chat/update',
    like = '/api/comment/like'
}

const listApi = async (params: any) => get<any>({url: URL.list, params: params, data: {}, headers: {}});
const createApi = async (data: any) => put<any>({
    url: URL.create,
    params: {},
    data: data,
    headers: {'Content-Type': 'multipart/form-data;charset=utf-8'}
});
const deleteApi = async (params: any) => deletes<any>({url: URL.delete, params: params, headers: {}});

const updateApi = async (params:any, data: any) =>
    post<any>({ url: URL.update,params: params, data: data, headers: { 'Content-Type': 'multipart/form-data;charset=utf-8' } });

export {listApi, createApi, deleteApi, updateApi};
