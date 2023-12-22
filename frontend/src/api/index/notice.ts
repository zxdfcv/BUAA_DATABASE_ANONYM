import { get, post, put } from "/@/utils/http/axios";

enum URL {
    commentMessage = '/myapp/comment/notice',
    replyMessage = '/myapp/reply/notice',
    mentionMessage = '/myapp/mention/notice',

    readComment = '/myapp/comment/read',
    readReply = '/myapp/reply/read',
    readMention = '/myapp/mention/read',

    chatList = '/myapp/chat/notice',
    chatContent = '/myapp/chat/list',
    chatCreate = '/myapp/chat/create',
}

const getCommentMessageApi = async (params: any) => get<any>({url: URL.commentMessage, params: params, data: {}, headers: {}});
const getReplyMessageApi = async (params: any) => get<any>({url: URL.replyMessage, params: params, data: {}, headers: {}});
const getMentionMessageApi = async (params: any) => get<any>({url: URL.mentionMessage, params: params, data: {}, headers: {}});

const readCommentMessageApi = async (params: any) => post<any>({url: URL.readComment, params: params, data: {}, headers: {}});
const readReplyMessageApi = async (params: any) => post<any>({url: URL.readReply, params: params, data: {}, headers: {}});
const readMentionMessageApi = async (params: any) => post<any>({url: URL.readMention, params: params, data: {}, headers: {}});

const getChatListApi = async (params: any) => get<any>({url: URL.chatList, params: params, data: {}, headers: {}});
const getChatDetailApi = async (params: any) => get<any>({url: URL.chatContent, params: params, data: {}, headers: {}});
const sendChatMessageApi = async (data: any) => put<any>({url: URL.chatCreate, params: {}, data: data, headers: {}});



export {
    getCommentMessageApi, getReplyMessageApi, getMentionMessageApi,
    readCommentMessageApi, readReplyMessageApi, readMentionMessageApi,
    getChatListApi, getChatDetailApi, sendChatMessageApi,
};
