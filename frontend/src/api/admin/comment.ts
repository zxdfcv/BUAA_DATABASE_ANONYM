import { deletes, get, post, put } from "/@/utils/http/axios";

enum URL {
    list = '/myapp/admin/comment/list',
    create = '/myapp/admin/comment/create',
    delete = '/myapp/admin/comment/delete',
    update = '/myapp/admin/comment/update',
    listThingComments = '/api/comment/listThingComments',
    listUserComments = '/api/comment/listUserComments',
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
const listThingCommentsApi = async (params: any) => get<any>({url: URL.listThingComments, params: params, data: {}, headers: {}});
const listUserCommentsApi = async (params: any) => get<any>({url: URL.listUserComments, params: params, data: {}, headers: {}});
const likeApi = async (params: any) => post<any>({url: URL.like, params: params, headers: {}});

const updateApi = async (params: any, data: any) => post<any>({ url: URL.update, params: params, data: data, headers: { 'Content-Type': 'multipart/form-data;charset=utf-8' } });

export {listApi, createApi, deleteApi, updateApi, listThingCommentsApi, listUserCommentsApi, likeApi};
