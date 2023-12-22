<template>
  <el-popover
    :width="450"
    :height="600"
    trigger="click"
    popper-style="box-shadow: rgb(14 18 22 / 35%) 0px 10px 38px -10px, rgb(14 18 22 / 20%) 0px 10px 20px -15px; padding: 20px;"
  >
    <template #reference>
      <!--      <img :src="MessageIcon">-->
      <a-badge :count="newMessageCount">
        <a-avatar :src="MessageIcon" style="height: 25px" />
      </a-badge>
    </template>
    <template #default>
      <a-tabs v-model:activeKey="activeKey" size="large" centered>
        <a-tab-pane key="1" tab="评论我的" style="height: 450px">
          <a-radio-group v-model:value="commentChoice" button-style="solid" style="display: flex; justify-content: flex-end">
            <a-radio-button value="0">未读</a-radio-button>
            <a-radio-button value="1">全部</a-radio-button>
          </a-radio-group>
          <el-scrollbar style="height: 400px; margin-top: 5px;">
            <a-list
                :loading="initLoading"
                :data-source="commentChoice === '0' ? commentList : commentAllList"
            >
              <template #loadMore>
                <div
                    :style="{ textAlign: 'center', marginTop: '12px', marginBottom: '12px', height: '32px', lineHeight: '32px' }"
                >
                  <a-button @click="fillComment" v-if="(commentChoice === '0' ? hasMoreComment : hasMoreAllComment)">loading more</a-button>
                  <div v-else-if="commentChoice === '0' ? (commentList.length !== 0) : (commentAllList.length !== 0)">到底啦 ~</div>
                </div>
              </template>
              <template #renderItem="{ item }">
                <a-list-item
                    :class="item.is_read ? 'back_read' : 'back_unread'"
                    @click="comment_product(item)"
                    style="margin-right: 15px; margin-left: 10px; cursor: pointer">
                    <a-list-item-meta
                        :description="item.create_time"
                    >
                      <template #title>
                        <a @click.stop="comment_user(item)">评论者：{{ item.user_name }}</a>
                      </template>
                      <template #avatar>
                        <a-avatar
                            @click.stop="comment_user(item)"
                            v-if="!(item.user_avatar === '' || item.user_avatar === null || item.user_avatar === undefined)"
                            :src="BASE_URL + '/upload/'+ item.user_avatar"/>
                        <a-avatar
                            @click.stop="router.push({name: 'usercenter', query: {id: item.user}})"
                            v-else
                            :src="AvatarIcon" />
                      </template>
                    </a-list-item-meta>
                  {{ '您的商品 ' + item.product_name + ' 有新的评论啦，快来看看吧！' }}
                </a-list-item>
              </template>
            </a-list>
          </el-scrollbar>
        </a-tab-pane>
        <a-tab-pane key="2" tab="回复我的" style="height: 450px">
          <a-radio-group v-model:value="replyChoice" button-style="solid" style="display: flex; justify-content: flex-end">
            <a-radio-button value="0">未读</a-radio-button>
            <a-radio-button value="1">全部</a-radio-button>
          </a-radio-group>
          <el-scrollbar style="height: 400px; margin-top: 5px;">
            <a-list
                :loading="initLoading"
                :data-source="replyChoice === '0' ? replyList : replyAllList"
            >
              <template #loadMore>
                <div
                    :style="{ textAlign: 'center', marginTop: '12px', marginBottom: '12px', height: '32px', lineHeight: '32px' }"
                >
                  <a-button @click="fillReply" v-if="(replyChoice === '0' ? hasMoreReply : hasMoreAllReply)">loading more</a-button>
                  <div v-else-if="replyChoice === '0' ? (replyList.length !== 0) : (replyAllList.length !== 0)">到底啦 ~</div>
                </div>
              </template>
              <template #renderItem="{ item }">
                <a-list-item
                    :class="item.is_read ? 'back_read' : 'back_unread'"
                    @click="reply_product(item)"
                    style="margin-right: 15px; margin-left: 10px; cursor: pointer">
                  <a-list-item-meta
                      :description="item.create_time"
                  >
                    <template #title>
                      <a @click.stop="reply_user(item)">回复者：{{ item.user_name }}</a>
                    </template>
                    <template #avatar>
                      <a-avatar
                          @click.stop="reply_user(item)"
                          v-if="!(item.user_avatar === '' || item.user_avatar === null || item.user_avatar === undefined)"
                          :src="BASE_URL + '/upload/'+ item.user_avatar"/>
                      <a-avatar
                          @click.stop="router.push({name: 'usercenter', query: {id: item.user}})"
                          v-else
                          :src="AvatarIcon" />
                    </template>
                  </a-list-item-meta>
                  {{ '您在商品 ' + item.product_name + ' 的评论有新的回复啦，快来看看吧！' }}
                </a-list-item>
              </template>
            </a-list>
          </el-scrollbar>
        </a-tab-pane>
        <a-tab-pane key="3" tab="@我" style="height: 450px">
          <a-radio-group v-model:value="mentionChoice" button-style="solid" style="display: flex; justify-content: flex-end">
            <a-radio-button value="0">未读</a-radio-button>
            <a-radio-button value="1">全部</a-radio-button>
          </a-radio-group>
          <el-scrollbar style="height: 400px; margin-top: 5px;">
            <a-list
                :loading="initLoading"
                :data-source="mentionChoice === '0' ? mentionList : mentionAllList"
            >
              <template #loadMore>
                <div
                    :style="{ textAlign: 'center', marginTop: '12px', marginBottom: '12px', height: '32px', lineHeight: '32px' }"
                >
                  <a-button @click="fillMention" v-if="(mentionChoice === '0' ? hasMoreMention : hasMoreAllMention)">loading more</a-button>
                  <div v-else-if="mentionChoice === '0' ? (mentionList.length !== 0) : (mentionAllList.length !== 0)">到底啦 ~</div>
                </div>
              </template>
              <template #renderItem="{ item }">
                <a-list-item
                    :class="item.comment_read ? 'back_read' : 'back_unread'"
                    @click="mention_product(item)"
                    style="margin-right: 15px; margin-left: 10px; cursor: pointer">
                  <a-list-item-meta
                      :description="item.create_time"
                  >
                    <template #title>
                      <a @click.stop="mention_user(item)">回复者：{{ item.user_name }}</a>
                    </template>
                    <template #avatar>
                      <a-avatar
                          @click.stop="mention_user(item)"
                          v-if="!(item.user_avatar === '' || item.user_avatar === null || item.user_avatar === undefined)"
                          :src="BASE_URL + '/upload/'+ item.user_avatar"/>
                      <a-avatar
                          @click.stop="mention_user(item)"
                          v-else
                          :src="AvatarIcon" />
                    </template>
                  </a-list-item-meta>
                  {{ '有人在商品 ' + item.product_name + ' 的评论区@你，快来看看吧！' }}
                </a-list-item>
              </template>
            </a-list>
          </el-scrollbar>
        </a-tab-pane>
        <a-tab-pane key="4" tab="私聊消息" style="height: 400px">
          <el-scrollbar>
            <div style="margin: 30px; text-align: center">
              <a-button type="primary" @click="push2chat">前往聊天室</a-button>
            </div>
          </el-scrollbar>
        </a-tab-pane>
        <template #renderTabBar="{ DefaultTabBar, ...props }">
          <component :is="DefaultTabBar" v-bind="props" />
        </template>
      </a-tabs>
    </template>
  </el-popover>
</template>

<script setup>
  import MessageIcon from '/@/assets/images/message-icon.svg';
  import { reactive } from 'vue';
  import {
    getCommentMessageApi,
    readCommentMessageApi,
    readMentionMessageApi,
    readReplyMessageApi
  } from "/@/api/index/notice";
  import {openNotification} from "/@/utils/notice";
  import {BASE_URL} from "/@/store/constants";
  import router from "/@/router";
  import AvatarIcon from "/@/assets/images/avatar.jpg";
  import {useWebSocketStore} from "/@/store";

  const socketStore = useWebSocketStore();

  const newComment = socketStore.new_comment;
  const newReply = socketStore.new_reply;
  const newMention = socketStore.new_mention;
  const newMessageCount = computed(() => {
    console.log(newComment + newReply + newMention)
    return socketStore.new_comment + socketStore.new_reply + socketStore.new_mention;
  });

  const activeKey = ref('1');
  const initLoading = ref(false);
  const loading = ref(false);

  // const emits = defineEmits(['newMessage'])
  const commentList = computed(() => socketStore.comment_list);
  const commentAllList = computed(() => socketStore.comment_all_list);
  const replyList = computed(() => socketStore.reply_list);
  const replyAllList = computed(() => socketStore.reply_all_list);
  const mentionList = computed(() => socketStore.mention_list);
  const mentionAllList = computed(() => socketStore.mention_all_list);

  const commentChoice = ref("0");
  const replyChoice = ref("0");
  const mentionChoice = ref("0");

  const hasMoreComment = computed(() => socketStore.has_more_comment);
  const hasMoreAllComment = computed(() => socketStore.has_more_all_comment);
  const hasMoreReply = computed(() => socketStore.has_more_reply);
  const hasMoreAllReply = computed(() => socketStore.has_more_all_reply);
  const hasMoreMention = computed(() => socketStore.has_more_mention);
  const hasMoreAllMention = computed(() => socketStore.has_more_all_mention);

  const fillComment = async () => {
    loading.value = true;
    await socketStore.fillComment(commentChoice.value);
    loading.value = false;
  }

  const fillReply = async () => {
    loading.value = true;
    await socketStore.fillReply(replyChoice.value);
    loading.value = false;
  }

  const fillMention = async () => {
    loading.value = true;
    await socketStore.fillMention(mentionChoice.value);
    loading.value = false;
  }

  const readComment = async (item) => {
    await readCommentMessageApi({ids: item.id})
        .then(res => console.log(res))
        .catch(err => console.log(err))
  }

  const readReply = async (item) => {
    await readReplyMessageApi({ids: item.id})
        .then(res => console.log(res))
        .catch(err => console.log(err))
    push2product(item.product_id)
  }

  const readMention = async (item) => {
    await readMentionMessageApi({ids: item.id})
        .then(res => console.log(res))
        .catch(err => console.log(err))
    push2product(item.product_id)
  }

  const comment_product = async (item) => {
    await readComment(item);
    await socketStore.refreshMessage();
    push2product(item.product);
  }

  const comment_user = async (item) => {
    await socketStore.refreshMessage();
    router.push({name: 'usercenter', query: {id: item.user}});
  }

  const reply_product = async (item) => {
    await readReply(item);
    await socketStore.refreshMessage();
    push2product(item.product);
  }

  const reply_user = async (item) => {
    await socketStore.refreshMessage();
    router.push({name: 'usercenter', query: {id: item.user}});
  }

  const mention_product = async (item) => {
    await readMention(item);
    await socketStore.refreshMessage();
    push2product(item.product);
  }

  const mention_user = async (item) => {
    await socketStore.refreshMessage();
    router.push({name: 'usercenter', query: {id: item.user}});
  }

  const push2product = (product) => {
    router.push({name: 'detail', query: {id: product}})
  }

  const push2chat = () => {
    openNotification({type: 'error', message: '哈哈，太着急了吧！'})
    // router.push({name: 'detail', query: {id: product}})
  }
</script>

<style scoped>
.back_read {
  background-color: #f8f1e7
}

.back_unread {
  background-color: #ffffff
}
</style>
