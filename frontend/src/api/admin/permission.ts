import {get} from '/@/utils/http/axios';

enum URL {
    list = '/myapp/admin/permission/list',
    create = '/myapp/admin/tag/create',
    update = '/myapp/admin/tag/update',
    delete = '/myapp/admin/tag/delete',
}

const listApi = async (params: any) =>
    get<any>({url: URL.list, params: params, data: {}, headers: {}});

export {listApi};

// 权限不能修改，只能列举