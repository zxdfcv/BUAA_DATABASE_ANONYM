<template>
  <div class="lg:w-73% w-100%" style="height: fit-content; margin-left: 10px; width: 71%;">
    
    <!-- 聊天区域 -->
    <div
      v-if="socketStore.sessionSelectId !== -1 && socketStore.chat_list.length !== 0"
    >
      <!-- 聊天头部 -->
      <header class="text-left px-20px h-35px" style="font-size: 20px; height: 35px; text-align: left; margin-top: 5px;">
        <span class="fw-600" style="margin-left: 10px; font-weight: 600;">
          {{chatNow.product_name}} - 用户： {{ (chatNow.sender === userStore.user_id) ? chatNow.recipient_name : chatNow.sender_name }}
        </span>
        <a-button
          @click="router.push({name: 'purchase', query: {product: chatNow.product}});"
          type="primary"
          v-if="showBuy"
        style="margin-top: -5px; margin-left: 20px;">购买商品</a-button>
        <a-divider />
      </header>

      <!-- 聊天内容 -->
      <div class="px-20px h-500px" style="background-image: linear-gradient(whitesmoke, white);">

        <el-scrollbar class="rounded-6px box-border" max-height="350px" ref="chatScrollbar" style="background: var(--el-color-primary-light-9);">
          <div
           class="p-20px">
            <template v-for="(item, index) in conversationList" :key="index">
            <!-- 聊天时间 -->

              <div class="text-12px my-20px text-center" style="color: var(--el-color-primary); text-align: center; margin-top: 10px;">
                {{renderMessageDate(item, index, conversationList)}}
              </div>
              <el-row type="flex" class="mb-20px" :style="item.sender === userStore.user_id ? 'flex-direction: row-reverse;' : ''" style="margin-bottom: 10px">
                <a-avatar v-if="!(item.sender_avatar === '' || item.sender_avatar === null || item.sender_avatar === undefined)"
                          :src="BASE_URL + '/upload/'+ item.sender_avatar"
                style="margin-left: 10px; margin-right: 10px;"/>
                <a-avatar v-else style="margin-left: 10px; margin-right: 10px;" :src="AvatarIcon" />
                <div v-if="item.image === null" :class="item.sender === userStore.user_id ? 'mr-10px': 'ml-10px'"
                     class="text break-words px-15px rounded-6px text-left py-12px"
                     style="display:inline-block; padding: 7px 12px 7px 12px; box-sizing: border-box; border-radius: 8px; position: relative;  word-break: break-all;"
                     :style="item.sender !== userStore.user_id ? 'background-color: #fefefe' : ''"
                >{{ item.content }}</div>
                <div v-else :class="item.sender === userStore.user_id ? 'mr-10px': 'ml-10px'">
                  <el-image
                    class="w-200px ha max-h-200px"
                    style="width: 200px; max-height: 200px; height: auto"
                    :src="BASE_URL + item.image"
                    fit="cover"
                  />
                </div>
                <el-icon v-if="item.content !== ''" :class="item.sender === userStore.user_id ? 'mr-10px': 'ml-10px'" class="is-loading pt-5px" size="40px">
                  <i i="ep-loading" style="color: var(--el-color-primary-light-3)"></i>
                </el-icon>
              </el-row>
            </template>
          </div>
        </el-scrollbar>
      </div>

      <!-- 聊天底部 -->
      <ChatFoot class="mt-20px" style="max-height: 230px; bottom: 0; position: absolute"></ChatFoot>
    </div>

    <!-- 显示个人信息 -->
    <a-empty v-else style="align-self: center; vertical-align: center"/>
  </div>
</template>

<script setup>
import { formatTime } from "/@/utils/myTimeFormat"
import {useUserStore, useWebSocketStore} from "/@/store";
import ChatFoot from "/@/views/index/components/chat/ChatFoot.vue";
import { BASE_URL } from "/@/store/constants";
import AvatarIcon from "/@/assets/images/avatar.jpg";
import router from "/@/router";
import { getProductDetail } from "/@/api/index/product";

const userStore = useUserStore();
const socketStore = useWebSocketStore();
const chatScrollbar = ref(null)
const showBuy = ref(false);

onMounted(() => {
  nextTick(() => {
    socketStore.chatScrollbar = chatScrollbar.value
    socketStore.chatScrollbar?.setScrollTop(9999);
  })
})

watch(
  () => socketStore.sessionSelectId,
  () => {
    nextTick(() => {
      socketStore.chatScrollbar = chatScrollbar.value
      socketStore.chatScrollbar?.setScrollTop(9999);
    })
  });

// 获取会话列表
const conversationList = computed(() => {
  let list = [];
  for (let i = socketStore.message_list.length - 1; i >= 0; i--) {
    list.push(socketStore.message_list[i]);
  }
  return list;
});

const chatNow = computed(() => {
  buyable(socketStore.chat_list[socketStore.sessionSelectId].product);
  return socketStore.chat_list[socketStore.sessionSelectId];
})

// 渲染时间每隔5分钟显示一次
const renderMessageDate = computed(() => {
  return (message, index, messages) =>{
    if ((message && index === 0) || (message && Date.parse(message.create_time) - Date.parse(messages[index - 1].create_time) > 5 * 60 * 1000)) {
      return `- - ${formatTime(Date.parse(message.create_time))} - -`
    }
    return "";
  }
})

  onUnmounted(() => {
    socketStore.sessionSelectId = -1;
  })
// 发送消息
function readySend() {
  // socketStore.sessionSelectId = socketStore.readyRecipient.id
  // socketStore.recipient = socketStore.readyRecipient
  // socketStore.navId = '1'
  // socketStore.initEditor()
  // let len =
  //   socketStore.sessionList.filter((x: any) => x.id == socketStore.readyRecipient?.id)
  //     ?.length ?? 0
  // if (!len) {
  //   socketStore.sessionList.push(socketStore.readyRecipient)
  //   let query = {
  //     recipient: socketStore.readyRecipient
  //   }
  //   socketStore.socket.emit("insertHistorySession", query)
  // }
  // socketStore.toBottom()
  // socketStore.changeReaded(socketStore.readyRecipient.id)
}

const buyable = async (product) => {
  const merchant = await queryMerchant(product);
  console.log(merchant !== userStore.user_id);
  showBuy.value = merchant !== userStore.user_id;
}

const queryMerchant = async (product) => {
  const res = await getProductDetail({product_id: product})
  return res.data.merchant;
}
</script>

<style scoped lang="scss">
.emo-image {
  height: 30px;
  width: 30px;
  vertical-align: middle;
  display: inline-block;
}

.text{
  background: var(--el-color-primary-light-3);
  max-width: calc(100% - 140px);
  line-height: 20px;
  :deep(p){
    margin: 0;
  }
}

:deep(.ant-divider-horizontal) {
  margin: 10px 0 !important;
}
</style>
