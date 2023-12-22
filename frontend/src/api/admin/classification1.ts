import { get, post, deletes, put} from '/@/utils/http/axios';
enum URL {
    list = '/myapp/classification/viewC_1',
    create = '/myapp/classification/createC_1',
    update = '/myapp/classification/updateC_1',
    delete = '/myapp/classification/deleteC_1',
}

const listApi = async (params: any) => get<any>({ url: URL.list, params: params, data: {}, headers: {} });
const createApi = async (data: any) =>
    put<any>({ url: URL.create, params: {}, data: data, headers: { 'Content-Type': 'multipart/form-data;charset=utf-8' } });
const updateApi = async (params: any, data: any) =>
    post<any>({ url: URL.update, params: params, data: data, headers: { 'Content-Type': 'multipart/form-data;charset=utf-8' } });
const deleteApi = async (params: any) => deletes<any>({ url: URL.delete, params: params, headers: {} });

export { listApi, createApi, updateApi, deleteApi };
