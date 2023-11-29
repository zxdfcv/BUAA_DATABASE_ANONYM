import {get, post} from '/@/utils/http/axios';

enum URL {
    create = '/myapp/index/comment/create',
    listThingComments = '/myapp/index/comment/list',
    listUserComments = '/myapp/index/comment/listMyComments',
    listReceiveComments = '/myapp/index/comment/notices',
    like = '/myapp/index/comment/like',
    SetStateToReaded = '/myapp/index/comment/read'
}

const createApi = async (data: any, data1: any) => post<any>({
    url: URL.create,
    params: {...data1},
    data: data,
    headers: {'Content-Type': 'multipart/form-data;charset=utf-8'}
});
const listThingCommentsApi = async (params: any) => get<any>({url: URL.listThingComments, params: params, data: {}, headers: {}});
const listUserCommentsApi = async (params: any) => get<any>({url: URL.listUserComments, params: params, data: {}, headers: {}});
const listReceiveCommentsApi = async (params: any) => get<any>({url: URL.listReceiveComments, params: params, data: {}, headers: {}});
const likeApi = async (params: any) => post<any>({url: URL.like, params: params, headers: {}});
const SetStateToReadedApi = async (params: any) => post<any>({url: URL.SetStateToReaded, params: params, headers: {}});
export {createApi, listThingCommentsApi,listUserCommentsApi, likeApi, listReceiveCommentsApi, SetStateToReadedApi};
