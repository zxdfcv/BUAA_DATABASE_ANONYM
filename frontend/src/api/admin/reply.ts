import {get, post} from '/@/utils/http/axios';

enum URL {
    list = '/myapp/admin/reply/list',
    create = '/myapp/admin/reply/create',
    delete = '/myapp/admin/reply/delete',
    listProductComments = '/api/reply/listThingComments',
    listUserComments = '/api/reply/listUserComments',
    like = '/api/comment/like'
}

const listApi = async (params: any) => get<any>({url: URL.list, params: params, data: {}, headers: {}});
const createApi = async (data: any) => post<any>({
    url: URL.create,
    params: {},
    data: data,
    headers: {'Content-Type': 'multipart/form-data;charset=utf-8'}
});
const deleteApi = async (params: any) => post<any>({url: URL.delete, params: params, headers: {}});
const listProductCommentsApi = async (params: any) => get<any>({url: URL.listProductComments, params: params, data: {}, headers: {}});
const listUserCommentsApi = async (params: any) => get<any>({url: URL.listUserComments, params: params, data: {}, headers: {}});
const likeApi = async (params: any) => post<any>({url: URL.like, params: params, headers: {}});

export {listApi, createApi, deleteApi, listProductCommentsApi, listUserCommentsApi, likeApi};
