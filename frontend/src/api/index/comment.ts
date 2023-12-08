import {deletes, get, post, put} from '/@/utils/http/axios';

enum URL {
    createComment = '/myapp/comment/create',
    deleteComment = '/myapp/comment/delete',
    queryProductComment = '/myapp/comment/list',
    queryUserComment = '/myapp/comment/my_list',
    likeComment = '/myapp/comment/like',
    dislikeComment = '/myapp/comment/dislike',

    createReply = '/myapp/reply/create',
    deleteReply = '/myapp/reply/delete',
    queryCommentReply = '/myapp/reply/list',
    queryUserReply = '/myapp/reply/my_list',
    likeReply = '/myapp/reply/like',
    dislikeReply = '/myapp/reply/dislike',

    create = '/myapp/index/comment/create',
    listThingComments = '/myapp/index/comment/list',
    listUserComments = '/myapp/index/comment/listMyComments',
    listReceiveComments = '/myapp/index/comment/notices',
    like = '/myapp/index/comment/like',
    SetStateToReaded = '/myapp/index/comment/read'
}

const createCommentApi = async (data: any) => put<any>({url: URL.createComment, params: {}, data: data, headers: {}})
const deleteCommentApi = async (params: any) => deletes<any>({url: URL.deleteComment, params: params, data: {}, headers: {}})
const queryProductCommentApi = async (params: any) => get<any>({url: URL.queryProductComment, params: params, data: {}, headers: {}})
const queryUserCommentApi = async (params: any) => get<any>({url: URL.queryUserComment, params: params, data: {}, headers: {}})
const likeCommentApi = async (params: any) => post<any>({url: URL.likeComment, params: params, data: {}, headers: {}})
const dislikeCommentApi = async (params: any) => deletes<any>({url: URL.dislikeComment, params: params, data: {}, headers: {}})


const createReplyApi = async (data: any) => put<any>({url: URL.createReply, params: {}, data: data, headers: {}})
const deleteReplyApi = async (params: any) => deletes<any>({url: URL.deleteReply, params: params, data: {}, headers: {}})
const queryCommentReplyApi = async (params: any) => get<any>({url: URL.queryCommentReply, params: params, data: {}, headers: {}})
const queryUserReplyApi = async (params: any) => get<any>({url: URL.queryUserReply, params: params, data: {}, headers: {}})
const likeReplyApi = async (params: any) => post<any>({url: URL.likeReply, params: params, data: {}, headers: {}})
const dislikeReplyApi = async (params: any) => deletes<any>({url: URL.dislikeReply, params: params, data: {}, headers: {}})


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
export {
    createCommentApi, deleteCommentApi, likeCommentApi, dislikeCommentApi, queryProductCommentApi, queryUserCommentApi, /* comment */
    createReplyApi, deleteReplyApi, likeReplyApi, dislikeReplyApi, queryCommentReplyApi, queryUserReplyApi,             /*  reply  */
    createApi, listThingCommentsApi,listUserCommentsApi, likeApi, listReceiveCommentsApi, SetStateToReadedApi /* old */
};
