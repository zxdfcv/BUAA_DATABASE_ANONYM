import {get, post} from '/@/utils/http/axios';

enum URL {
    commentMessage = '/myapp/comment/notice',
    replyMessage = '/myapp/reply/notice',
    mentionMessage = '/myapp/mention/notice',

    readComment = '/myapp/comment/read',
    readReply = '',
    readMention = '',
}

const getCommentMessageApi = async (params: any) => get<any>({url: URL.commentMessage, params: params, data: {}, headers: {}});
const getReplyMessageApi = async (params: any) => get<any>({url: URL.replyMessage, params: params, data: {}, headers: {}});
const getMentionMessageApi = async (params: any) => get<any>({url: URL.mentionMessage, params: params, data: {}, headers: {}});

const readCommentMessageApi = async (params: any) => post<any>({url: URL.readComment, params: params, data: {}, headers: {}});
const readReplyMessageApi = async (params: any) => post<any>({url: URL.readReply, params: params, data: {}, headers: {}});
const readMentionMessageApi = async (params: any) => post<any>({url: URL.readMention, params: params, data: {}, headers: {}});


export {
    getCommentMessageApi, getReplyMessageApi, getMentionMessageApi,
    readCommentMessageApi, readReplyMessageApi, readMentionMessageApi,
};
