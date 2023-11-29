import { get, post } from '/@/utils/http/axios';
enum URL {
    list = '/myapp/index/classification/list',
    addCollectCounter = '/myapp/index/classification/addCollectCounter',
    getCollectCounterListApi = '/myapp/index/classification/getCollectCounterList',
    removeCollectCounter = '/myapp/index/classification/removeCollectCounter',
    detail = '/myapp/index/classification/detail'
}

const detailApi = async (params: any) => get<any>({ url: URL.detail, params: params, headers: {} });
const listApi = async (params: any) => get<any>({ url: URL.list, params: params, data: {}, headers: {} });
const addCollectCounter = async (params: any) => post<any>({ url: URL.addCollectCounter, params: params, headers: {} });
const getCollectCounterListApi = async (params: any) => get<any>({ url: URL.getCollectCounterListApi, params: params, headers: {} });
const removeCollectCounter = async (params: any) => post<any>({ url: URL.removeCollectCounter, params: params, headers: {} });
export { listApi, addCollectCounter, getCollectCounterListApi, removeCollectCounter, detailApi};
