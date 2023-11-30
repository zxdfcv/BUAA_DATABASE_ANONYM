import { get, post } from '/@/utils/http/axios';

enum URL {
    userLogin = '/login/',
    userRegister = '/register/',

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

const detailApi = async (params: any) => get<any>({ url: URL.detail, params: params, data: {}, headers: {} });
const userRegisterApi = async (data: any) => post<any>({ url: URL.userRegister, params: {}, data: data });
const updateUserPwdApi = async (params: any, data:any) => post<any>({ url: URL.updateUserPwd, params: params, data:data });
const updateUserInfoApi = async (params: any,data: any) => post<any>({ url: URL.updateUserInfo, params:params, data: data, headers: { 'Content-Type': 'multipart/form-data;charset=utf-8' } });

export { 
    userRegisterApi, userLoginApi, /* 不直接调用 */
    detailApi, updateUserPwdApi, updateUserInfoApi, /* 未实现 Api */
};
