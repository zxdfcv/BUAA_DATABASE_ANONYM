<template>
  <div class="content-list">
    <div class="list-title">我的评论</div> <!-- TODO: 评论分页获取 -->
    <div class="list-content">
      <div class="comment-view">
        <a-spin :spinning="loading" style="min-height: 200px;">
          <a-tabs
              v-model:activeKey="activeKey"
              type="card"
              animated
              size="large"
          >
            <a-tab-pane key="1" tab="我的评论">
              <a-list item-layout="vertical" size="large" :data-source="commentData">
                <template #footer>
                  <div>
                    built by
                    <b>BUAA Database Project</b>
                  </div>
                </template>
                <template #renderItem="{ item }">
                  <a-list-item key="item.id">
                    <template #actions>
                  <span>
                    <component :is="LikeOutlined" style="margin-right: 8px" />
                    {{ item.likes_count }}
                  </span>
                      <span>
                    <component :is="MessageOutlined" style="margin-right: 8px" />
                    {{ item.reply_count }}
                  </span>
                  <span>
                  <component :is="DeleteOutlined" style="margin-right: 8px" @click="open=true; targetId=item.id"/>
                  </span>
                    </template>
                    <a-list-item-meta :description="item.create_time">
                      <template #title>
                        <a @click="push2product(item.product)">{{ item.product_name }}</a>
                      </template>
                      <template #avatar>
                        <a-avatar v-if="!(item.user_avatar === '' || item.user_avatar === null || item.user_avatar === undefined)" :size="40" :src="BASE_URL + '/upload/' + item.user_avatar" @click="push2user" />
                        <a-avatar v-else :src="AvatarIcon" @click="push2user" />
                      </template>
                    </a-list-item-meta>
                    {{ item.content }}
                    <a-modal :closable=false v-model:open="open" title="注意！" :confirm-loading="modalLoading" @ok="deleteComment" :maskStyle="{'opacity':'0.2','background':'#868686'}">
                      <p>真的要删除这条评论吗，这个操作不可恢复！</p>
                    </a-modal>
                  </a-list-item>
                </template>
              </a-list>
            </a-tab-pane>
            <a-tab-pane key="2" tab="我的回复">
              <a-list item-layout="vertical" size="large" :data-source="replyData">
              <template #footer>
                <div>
                  built by
                  <b>BUAA Database Project</b>
                </div>
              </template>
              <template #renderItem="{ item }">
                <a-list-item key="item.id">
                  <template #actions>
                    <span>
                      <component :is="LikeOutlined" style="margin-right: 8px" />
                      {{ item.likes_count }}
                    </span>
                    <span>
                      <component :is="DeleteOutlined" style="margin-right: 8px" @click="open2=true; targetId=item.id"/>
                    </span>
                  </template>
                  <a-list-item-meta :description="item.create_time">
                    <template #title>
                      <a @click="push2product(item.product_id)">{{ item.product_name }}</a>
                    </template>
                    <template #avatar>
                      <a-avatar v-if="!(item.user_avatar === '' || item.user_avatar === null || item.user_avatar === undefined)" :size="40" :src="BASE_URL + '/upload/' + item.user_avatar" @click="push2user" />
                      <a-avatar v-else :src="AvatarIcon" @click="push2user" />
                    </template>
                  </a-list-item-meta>
                  <a @click="jump2user(item.mentioned_user)">@{{ item.mentioned_name }}&nbsp;&nbsp;</a>{{ item.content }}
                  <a-modal :closable=false v-model:open="open2" title="注意！" :confirm-loading="modalLoading" @ok="deleteReply" :maskStyle="{'opacity':'0.2','background':'#868686'}">
                    <p>真的要删除这条回复吗，这个操作不可恢复！</p>
                  </a-modal>
                </a-list-item>
              </template>
            </a-list>
            </a-tab-pane>
          </a-tabs>

        </a-spin>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useAppStore, useUserStore } from "/@/store";
import { deleteCommentApi, deleteReplyApi, queryUserCommentApi, queryUserReplyApi } from "/@/api/index/comment";
import { BASE_URL } from "/@/store/constants";
import { DeleteOutlined, LikeOutlined, MessageOutlined } from "@ant-design/icons-vue";
import AvatarIcon from "/@/assets/images/avatar.jpg";
import { openNotification } from "/@/utils/notice";

const router = useRouter();
const userStore = useUserStore();
const appStore = useAppStore();

const open = ref(false);
const open2 = ref(false);
const modalLoading = ref(false);
const loading = ref(false);
const loadingCount = ref(0);
const targetId = ref(-1);

const commentData = ref([])
const replyData = ref([])
const activeKey = ref('1');

onMounted(()=>{
  if (useRoute().query.id) {
    if (useRoute().query.id.trim() !== String(userStore.user_id)) {
      router.push({name: 'wishThingView', query: {id: useRoute().query.id.trim()}});
    }
  } else {
    router.push({name: 'scoreView', query: {id: userStore.user_id}});
  }
  appStore.setViewId(userStore.user_id);
  getCommentList()
  getReplyList()
})

const push2user = () => {
  router.push({name: 'usercenter', query: {id: userStore.user_id}})
}

const jump2user = (user) => {
  router.push({name: 'usercenter', query: {id: user}})
}
const push2product = (product) => {
  router.push({name: 'detail', query: {id: product}})
}
const getCommentList = () => {
  loading.value = true
  loadingCount.value++;
  let userId = userStore.user_id
  queryUserCommentApi({user_id: userId}).then(res => {
    commentData.value = res.data
    loading.value = (--loadingCount.value !== 0);
  }).catch(err => {
    openNotification({
      type: 'error',
      message: 'Oops!',
      description: '获取评论列表失败！'
    })
    loading.value = (--loadingCount.value !== 0);
  })
}

const getReplyList = () => {
  loading.value = true
  loadingCount.value++;
  let userId = userStore.user_id
  queryUserReplyApi({user_id: userId}).then(res => {
    replyData.value = res.data
    loading.value = (--loadingCount.value !== 0);
    console.log(replyData.value)
  }).catch(err => {
    openNotification({
      type: 'error',
      message: 'Oops!',
      description: '获取评论列表失败！'
    })
    loading.value = (--loadingCount.value !== 0);
  })
}

const deleteComment = () => {
  modalLoading.value = true;
  deleteCommentApi({ids: targetId.value}).then(res => {
    if (res.code === 0) {
      openNotification({
        type: 'success',
        message: '成功删除评论！',
      })
    }
    modalLoading.value = false;
    open.value = false;
    getCommentList();
  }).catch(err => {
    openNotification({
      type: 'error',
      message: 'Oops!',
      description: '删除评论失败！'
    })
    modalLoading.value = false;
    open.value = false;
  })
}

const deleteReply = () => {
  modalLoading.value = true;
  deleteReplyApi({ids: targetId.value}).then(res => {
    if (res.code === 0) {
      openNotification({
        type: 'success',
        message: '成功删除回复！',
      })
    }
    modalLoading.value = false;
    open.value = false;
    getReplyList();
  }).catch(err => {
    openNotification({
      type: 'error',
      message: 'Oops!',
      description: '删除回复失败！'
    })
    modalLoading.value = false;
    open.value = false;
  })
}

</script>
<style scoped lang="less">
.flex-view {
  display: -webkit-box;
  display: -ms-flexbox;
  display: flex;
}

.content-list {
  flex: 1;

  .list-title {
    color: #152844;
    font-weight: 600;
    font-size: 18px;
    //line-height: 24px;
    height: 48px;
    margin-bottom: 4px;
    border-bottom: 1px solid #cedce4;
  }
}

.comment-view {
  overflow: hidden;

  .comment-list {
    margin: 8px auto;
  }

  .comment-item {
    padding: 15px 0;

    .avatar {
      width: 40px;
      height: 40px;
      border-radius: 50%;
      margin-right: 8px;
    }

    .infos {
      position: relative;
      -webkit-box-flex: 1;
      -ms-flex: 1;
      flex: 1;
    }

    .name {
      -webkit-box-align: center;
      -ms-flex-align: center;
      align-items: center;
      cursor: pointer;
    }

    h3 {
      color: #152844;
      font-weight: 600;
      font-size: 14px;
      margin: 0;
    }

    .traingle {
      width: 0;
      height: 0;
      border-left: 6px solid #c3c9d5;
      border-right: 0;
      border-top: 4px solid transparent;
      border-bottom: 4px solid transparent;
      margin: 0 12px;
    }

    .time {
      color: #5f77a6;
      font-size: 12px;
      line-height: 16px;
      height: 16px;
      margin: 2px 0 8px;
    }

    .content {
      color: #484848;
      font-size: 14px;
      line-height: 22px;
      padding-right: 30px;
    }
  }
}

</style>
