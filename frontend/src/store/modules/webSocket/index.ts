import {defineStore} from 'pinia';
import piniaStore, {useUserStore} from '/@/store/index';
import {MESSAGE_PER_PAGE, WEBSOCKET_URL} from "/@/store/constants";
import {
    getChatDetailApi,
    getChatListApi,
    getCommentMessageApi,
    getMentionMessageApi,
    getReplyMessageApi
} from "/@/api/index/notice";
import {openNotification} from "/@/utils/notice";

/**
 * 应用状态信息留存
 */
export const useWebSocketStore = defineStore(
  // 唯一ID
  'webSocket',
  {
    state: () => ({
        web_socket: undefined,
        init: false,

        comment_list: ref([]),
        reply_list: ref([]),
        mention_list: ref([]),

        comment_count: 0,
        reply_count: 0,
        mention_count: 0,

        has_more_comment: true,
        has_more_reply: true,
        has_more_mention: true,


        comment_all_list: ref([]),
        reply_all_list: ref([]),
        mention_all_list: ref([]),

        comment_all_count: 0,
        reply_all_count: 0,
        mention_all_count: 0,

        has_more_all_comment: true,
        has_more_all_reply: true,
        has_more_all_mention: true,

        new_comment: ref(0),
        new_reply: ref(0),
        new_mention: ref(0),
        new_chat: ref(0), // 拿出去 computed

        chat_list: ref([]),
        message_list: ref([]),
        sessionSelectId: 0,
        chatScrollbar: undefined,
    }),
    getters: {},
    actions: {
        attachSocket() {
            if (this.web_socket === undefined && useUserStore().user_access !== undefined) {
                // @ts-ignore
                this.web_socket = new WebSocket(WEBSOCKET_URL + "?token=" + useUserStore().user_access);

                // @ts-ignore
                this.web_socket.onopen = () => {
                    console.log('WebSocket连接成功');
                    this.refreshMessage();
                };

                // @ts-ignore
                this.web_socket.onerror = (error) => {
                    console.error('WebSocket连接遇到错误:', error);
                };

                // @ts-ignore
                this.web_socket.onmessage = (event) => {
                    // 收到服务器发来的消息
                    const message = JSON.parse(event.data);
                    switch (message.notification_type) {
                        case 'comment_notice': this.handleComment(message); break;
                        case 'reply_notice': this.handleReply(message); break;
                        case 'mentioned_notice': this.handleMention(message); break;
                        case 'chat_notice': this.handleChat(message); break;
                    }
                };

                // @ts-ignore
                this.web_socket.onclose = () => {
                    console.log('WebSocket连接关闭');
                };
            }
        },

        detachSocket() {
            if (this.web_socket) {
                try {
                    (this.web_socket as WebSocket).close();
                } catch (e) {
                    this.web_socket = undefined;
                }
                console.log("注销 webSocket 实例")
            }
            this.web_socket = undefined;
        },

        async initMessages() {
            if (!this.init) {
                await this.fillComment('0');
                await this.fillComment('1');
                await this.fillReply('0');
                await this.fillReply('1');
                await this.fillMention('0');
                await this.fillMention('1');
                await this.fillChat();
                this.init = true;
            }
        },

        discardMessages() {
            console.log("discardMessage");
            this.init = false;

            this.comment_list = [];
            this.reply_list = [];
            this.mention_list = [];

            this.comment_count = 0;
            this.reply_count = 0;
            this.mention_count = 0;

            this.has_more_comment = true;
            this.has_more_reply = true;
            this.has_more_mention = true;


            this.comment_all_list = [];
            this.reply_all_list = [];
            this.mention_all_list = [];

            this.comment_all_count = 0;
            this.reply_all_count = 0;
            this.mention_all_count = 0;

            this.has_more_all_comment = true;
            this.has_more_all_reply = true;
            this.has_more_all_mention = true;

            this.new_comment = 0;
            this.new_reply = 0;
            this.new_mention = 0;
            this.new_chat = 0;
        },

        async refreshMessage() {
            await this.discardMessages();
            await this.initMessages();
        },

        async fillComment(commentChoice: String) {
            getCommentMessageApi({
                get_all: commentChoice,
                limit: MESSAGE_PER_PAGE,
                offset: (commentChoice === '0') ? this.comment_count : this.comment_all_count}).then(res => {
                if (commentChoice === "0") {
                    /* only get un_read message */
                    console.log(this.new_comment)
                    this.new_comment = res.data.count;
                    this.comment_list = this.comment_list.concat(res.data.results);
                    this.comment_count += res.data.results.length;
                    if (res.data.results.length !== 5) {
                        this.has_more_comment = false;
                    }
                } else {
                    /* get all type message */
                    this.comment_all_list = this.comment_all_list.concat(res.data.results);
                    this.comment_all_count += res.data.results.length;
                    if (res.data.results.length !== 5) {
                        this.has_more_all_comment = false;
                    }
                }
            }).catch(err => {
                console.log(err)
                openNotification({ type: 'error', message: 'Oops!', description: '获取评论信息失败！' })
            })
        },

        async fillReply(replyChoice: String) {
            getReplyMessageApi({
                get_all: replyChoice,
                limit: MESSAGE_PER_PAGE,
                offset: (replyChoice === '0') ? this.reply_count : this.reply_all_count}).then(res => {
                if (replyChoice === "0") {
                    /* only get un_read message */
                    this.new_reply = res.data.count;
                    this.reply_list = this.reply_list.concat(res.data.results);
                    this.reply_count += res.data.results.length;
                    if (res.data.results.length !== 5) {
                        this.has_more_reply = false;
                    }
                } else {
                    /* get all type message */
                    this.reply_all_list = this.reply_all_list.concat(res.data.results);
                    this.reply_all_count += res.data.results.length;
                    if (res.data.results.length !== 5) {
                        this.has_more_all_reply = false;
                    }
                }
            }).catch(err => {
                console.log(err)
                openNotification({ type: 'error', message: 'Oops!', description: '获取评论信息失败！' })
            })
        },

        async fillMention(mentionChoice: String) {
            getMentionMessageApi({
                get_all: mentionChoice,
                limit: MESSAGE_PER_PAGE,
                offset: (mentionChoice === '0') ? this.mention_count : this.mention_all_count}).then(res => {
                if (mentionChoice === "0") {
                    /* only get un_read message */
                    this.new_mention = res.data.count;
                    this.mention_list = this.mention_list.concat(res.data.results);
                    this.mention_count += res.data.results.length;
                    if (res.data.results.length !== 5) {
                        this.has_more_mention = false;
                    }
                } else {
                    /* get all type message */
                    this.mention_all_list = this.mention_all_list.concat(res.data.results);
                    this.mention_all_count += res.data.results.length;
                    if (res.data.results.length !== 5) {
                        this.has_more_all_mention = false;
                    }
                }
            }).catch(err => {
                console.log(err)
                openNotification({ type: 'error', message: 'Oops!', description: '获取评论信息失败！' })
            })
        },

        async fillChat() {
            getChatListApi({})
                .then(res => this.chat_list = res.data)
                .catch(err => console.log(err))
        },

        async fillMessage() {
            const item = this.chat_list[this.sessionSelectId];
            // @ts-ignore
            getChatDetailApi({product_id: item.product, other_id: (item.sender === useUserStore().user_id) ? item.recipient : item.sender}).then(res => {
                console.log(res.data)
                this.message_list = res.data;
                this.chat_list[this.sessionSelectId].is_read = true;
                setTimeout(() => {
                    // @ts-ignore
                    this.chatScrollbar?.setScrollTop(9999);
                }, 20);
            }).catch(err => {
                console.log(err);
            })
        },

        handleComment(message) {
            console.log('get comment socket', message);
            this.comment_list = [];
            this.comment_count = 0;
            this.comment_all_list = [];
            this.comment_all_count = 0;
            this.has_more_all_comment = true;
            this.new_comment = 0;
            this.fillComment('0');
            this.fillComment('1');
        },

        handleReply(message) {
            console.log('get reply socket', message);
            this.reply_list = [];
            this.reply_count = 0;
            this.reply_all_list = [];
            this.reply_all_count = 0;
            this.has_more_all_reply = true;
            this.new_reply = 0;
            this.fillReply('0');
            this.fillReply('1');
        },

        handleMention(message) {
            console.log('get mention socket', message);
            this.mention_list = [];
            this.mention_count = 0;
            this.mention_all_list = [];
            this.mention_all_count = 0;
            this.has_more_all_mention = true;
            this.new_mention = 0;
            this.fillMention('0');
            this.fillMention('1');
        },

        async handleChat(message) {
            console.log('get chat socket', message);
            this.new_chat = 1;
            await this.fillChat();
            await this.fillMessage();
        },

        async modifySession(product) {
            console.log(product);
            for (let i = 0; i < this.chat_list.length; i++) {
                const chat: {product: any, recipient: any, sender: any} = this.chat_list[i];
                console.log(chat.product, product.id, chat.recipient, product.uploaderId, chat.sender, useUserStore().user_id);
                if (chat.product === product.id) {
                    if ((chat.recipient === product.uploaderId && chat.sender === useUserStore().user_id) ||
                      (chat.sender === product.uploaderId && chat.recipient === useUserStore().user_id)) {
                        this.sessionSelectId = i;
                        await this.fillMessage();
                        return;
                    }
                }
            }
            const item = {
                content: "",
                create_time: Date.now(),
                id: -114514,
                image: null,
                product: product.id,
                product_name: product.title,
                recipient: product.uploaderId,
                recipient_name: product.uploaderName,
                sender: useUserStore().user_id,
                sender_name: useUserStore().user_name,
                is_read: true,
                recipient_avatar: product.avatarUrl,
                sender_avatar: "",
            };
            this.chat_list = this.chat_list.filter(chat => chat.id !== -114514);
            console.log(this.chat_list);
            // @ts-ignore
            this.chat_list.unshift(item);
            this.message_list = [];
            this.sessionSelectId = 0;
            console.log(this.chat_list);
        }
    },
    persist: {
        key: 'webSocket',
        storage: sessionStorage,
    },
  },
);

export function useAppOutsideStore() {
  return useWebSocketStore(piniaStore);
}
