import { get, post } from '/@/utils/http/axios';
enum URL {
    list = '/myapp/index/canteen/list',
    addCollectCanteen = '/myapp/index/canteen/addCollectCanteen',
    getCollectCanteenListApi = '/myapp/index/canteen/getCollectCanteenList',
    removeCollectCanteen = '/myapp/index/canteen/removeCollectCanteen',
    detail = '/myapp/index/canteen/detail'
}

const detailApi = async (params: any) => get<any>({ url: URL.detail, params: params, headers: {} });
const listApi = async (params: any) => get<any>({ url: URL.list, params: params, data: {}, headers: {} });
const addCollectCanteen = async (params: any) => post<any>({ url: URL.addCollectCanteen, params: params, headers: {} });
const getCollectCanteenListApi = async (params: any) => get<any>({ url: URL.getCollectCanteenListApi, params: params, headers: {} });
const removeCollectCanteen = async (params: any) => post<any>({ url: URL.removeCollectCanteen, params: params, headers: {} });
export { listApi, addCollectCanteen, getCollectCanteenListApi, removeCollectCanteen, detailApi};

