// 权限问题后期增加
import { get, post, put, deletes } from '/@/utils/http/axios';
import { UserState } from '/@/store/modules/user/types';
// import axios from 'axios';
enum URL {
    login = '/myapp/login/',
    userList = '/myapp/admin/user/list',
    detail = '/myapp/admin/user/detail',
    create = '/myapp/admin/user/create',
    update = '/myapp/admin/user/update',
    delete = '/myapp/admin/user/delete',
    userRegister = '/myapp/register/', // 管理员和用户注册接口实际上相同
}
interface LoginRes {
    token: string;
}

export interface LoginData {
    username: string;
    password: string;
}

const loginApi = async (data: LoginData) => post<any>({ url: URL.login, data, headers: { 'Content-Type': 'multipart/form-data;charset=utf-8' } });
const listApi = async (params: any) => get<any>({ url: URL.userList, params: params, data: {}, headers: {} });
const detailApi = async (params: any) => get<any>({ url: URL.detail, params: params, data: {}, headers: {} });
const createApi = async (data: any) => put<any>({ url: URL.create, params: {}, data: data, headers: { 'Content-Type': 'multipart/form-data;charset=utf-8' } });
const updateApi = async (params: any, data: any) => post<any>({ url: URL.update,params: params, data: data, headers: { 'Content-Type': 'multipart/form-data;charset=utf-8' } });
const deleteApi = async (params: any) => deletes<any>({ url: URL.delete, params: params, headers: {} });
const userRegisterApi = async (data: any) => post<any>({ url: URL.userRegister, params: {}, data: data, headers: { 'Content-Type': 'multipart/form-data;charset=utf-8' } });

export { loginApi, listApi, detailApi, createApi, updateApi, deleteApi, userRegisterApi};
