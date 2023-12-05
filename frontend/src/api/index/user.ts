import {deletes, get, post} from '/@/utils/http/axios';

enum URL {
    userLogin = '/myapp/login/',
    userRegister = '/myapp/register/',
    getCollectList = '/myapp/product/collector/list',
    userDetail = '/myapp/user/detail',
    userUpdate = '/myapp/user/update',
    userPassword = '/myapp/user/update/pwd',
    userDelete = '/myapp/user/delete',

    /* TODO: 以下 UserApi 未实现 */
    detail = '/myapp/index/user/info',
    updateUserPwd = '/myapp/index/user/updatePwd',
    updateUserInfo = '/myapp/index/user/update'
}
interface LoginRes {
    token: string;
}

export interface LoginData {
    username: string;
    password: string;
}
/* 封装了用户相关 api */
const userLoginApi = async (data: any) => post<any>({ url: URL.userLogin, data, headers: { 'Content-Type': 'multipart/form-data;charset=utf-8' } });
const getCollectList = async (params: any) => get<any>({ url: URL.getCollectList, params: params, data: {}, headers: {} });
const userRegisterApi = async (data: any) => post<any>({ url: URL.userRegister, params: {}, data: data });
const userDetailApi = async (params: any) => get<any>({ url: URL.userDetail, params: params, data: {}});
const userUpdateApi = async (params: any, data: any) => post<any>({ url: URL.userUpdate, params: params, data: data });
const userPasswordApi = async (params: any, data: any) => post<any>({ url: URL.userPassword, params: params, data: data });
const userDeleteApi = async (params: any) => deletes<any>({ url: URL.userDelete, params: params, data: {} });

const detailApi = async (params: any) => get<any>({ url: URL.detail, params: params, data: {}, headers: {} });
const updateUserPwdApi = async (params: any, data:any) => post<any>({ url: URL.updateUserPwd, params: params, data:data });
const updateUserInfoApi = async (params: any,data: any) => post<any>({ url: URL.updateUserInfo, params:params, data: data, headers: { 'Content-Type': 'multipart/form-data;charset=utf-8' } });

export { 
    userRegisterApi, userLoginApi, /* 不直接调用 */
    getCollectList, userDetailApi, userUpdateApi, userPasswordApi, userDeleteApi,
    detailApi, updateUserPwdApi, updateUserInfoApi, /* 未实现 Api */
};
