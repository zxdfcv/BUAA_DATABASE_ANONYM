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
                :data-source="commentDisplay"
            >
              <template #loadMore>
                <div
                    :style="{ textAlign: 'center', marginTop: '12px', marginBottom: '12px', height: '32px', lineHeight: '32px' }"
                >
                  <a-button @click="fillComment" v-if="hasMore && commentDisplay.length !== 0">loading more</a-button>
                  <div v-else-if="commentDisplay.length !== 0">到底啦 ~</div>
                </div>
              </template>
              <template #renderItem="{ item }">
                <a-list-item
                    :class="item.is_read ? 'back_read' : 'back_unread'"
                    @click="readComment(item)"
                    style="margin-right: 15px; margin-left: 10px; cursor: pointer">
                    <a-list-item-meta
                        :description="item.create_time"
                    >
                      <template #title>
                        <a @click.stop="router.push({name: 'usercenter', query: {id: item.user}})">评论者：{{ item.user_name }}</a>
                      </template>
                      <template #avatar>
                        <a-avatar
                            @click.stop="router.push({name: 'usercenter', query: {id: item.user}})"
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
        <a-tab-pane key="2" tab="回复我的" style="height: 400px">
          <el-scrollbar> Content of Tab Pane 2 </el-scrollbar>
        </a-tab-pane>
        <a-tab-pane key="3" tab="@我" style="height: 400px">
          <el-scrollbar> Content of Tab Pane 3 </el-scrollbar>
        </a-tab-pane>
        <a-tab-pane key="4" tab="私聊消息" style="height: 400px">
          <el-scrollbar>
            <div style="margin: 30px; text-align: center">
              <a-button type="primary">前往聊天室</a-button>
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
  import {getCommentMessageApi, readCommentMessageApi, readReplyMessageApi} from "/@/api/index/notice";
  import {openNotification} from "/@/utils/notice";
  import {BASE_URL} from "/@/store/constants";
  import router from "/@/router";
  import AvatarIcon from "/@/assets/images/avatar.jpg";

  const newMessageCount = ref(100);
  const activeKey = ref('1');
  // const emits = defineEmits(['newMessage'])
  const commentList = ref([]);
  const commentDisplay = ref([]);
  const mentionList = reactive({});

  const commentChoice = ref("0");
  const commentCount = ref(0);
  const initLoading = ref(true);
  const loading = ref(false);
  const hasMore = ref(true);


  onMounted(async () => {
    console.log("in notice center")
    initMessages();
  })

  const initMessages = () => {
    fillComment();
  }

  const fillComment = () => {
    loading.value = true;
    getCommentMessageApi({get_all: commentChoice.value, limit: 5, offset: commentCount.value}).then(res => {
      const newData = commentList.value.concat(res.data.results);
      loading.value = false;
      initLoading.value = false;
      commentList.value = newData;
      commentDisplay.value = newData;
      commentCount.value += res.data.results.length;
      if (res.data.results.length !== 5) {
        hasMore.value = false;
      }
      // for (let i = 0; i < res.data.length; i++) {
      //   commentList.value.push(res.data[i]);
      //   commentDisplay.value.push(res.data[i]);
      // }
      console.log(commentDisplay.value)
    }).catch(err => {
      console.log(err)
      openNotification({ type: 'error', message: 'Oops!', description: '获取评论信息失败！' })
    })
  }


  const readComment = (item) => {
    readCommentMessageApi({ids: item.id})
        .then(res => console.log(res))
        .catch(err => console.log(err))
    push2product(item.product)
  }
  const push2product = (product) => {
    router.push({name: 'detail', query: {id: product}})
  }

  watch(
      () => commentChoice.value,
      () => {
        commentList.value.length = 0;
        commentCount.value = 0;
        hasMore.value = true;
        fillComment();
      }
  );
</script>

<style scoped>
.back_read {
  background-color: #f8f1e7
}

.back_unread {
  background-color: #ffffff
}
</style>
