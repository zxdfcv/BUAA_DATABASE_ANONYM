<template>
  <div class="chat-session lg:w-20% w-70% p-8px box-border">
    <a-page-header
        sub-title="返回个人中心"
        @back="() => router.push({name: 'usercenter', query: {id: userStore.user_id}})"
    />
    <el-scrollbar max-height="500px" style="margin-left: 15px; margin-right: 15px;">
      <!-- 会话列表 -->
      <template v-for="(item, index) in chatroomList" :key="item" v-if="chatroomList.length !== 0">
        <div
          v-if="true"
          class="session-item"
          style="cursor: pointer;"
          :class="[
            (index === socketStore.sessionSelectId) ? 'session-active' : '',
          ]"
          @click="selectSession(item, index)"
          >
          <el-row type="flex" align="middle" style="min-height: 75px; margin-bottom: 1px; margin-left: 10px;">
            <a-badge :dot="!item.is_read">
              <div v-if="item.sender !== userStore.user_id">
                <a-avatar  size="40" v-if="!(item.sender_avatar === '' || item.sender_avatar === null || item.sender_avatar === undefined)" :src="BASE_URL + '/upload/'+ item.sender_avatar"/>
                <a-avatar v-else :src="AvatarIcon" />
              </div>
              <div v-else>
                <a-avatar  size="40" v-if="!(item.recipient_avatar === '' || item.recipient_avatar === null || item.recipient_avatar === undefined)" :src="BASE_URL + '/upload/'+ item.recipient_avatar"/>
                <a-avatar v-else :src="AvatarIcon" />
              </div>
            </a-badge>
            <div class=" text-left" style="margin-left: 10px;">
              <div class="truncate">{{item.product_name}} - {{ (item.sender === userStore.user_id) ? item.recipient_name : item.sender_name }}</div>
              <div style="color: #8d8d8d; font-size: 12px; width: 150px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis">
                {{ item.content }}
              </div>
            </div>
          </el-row>
<!--          <a-divider/>-->
        </div>

      </template>
      <el-empty v-else :image-size="100" description="当前列表为空"/>
    </el-scrollbar>
  </div>
</template>

<script setup>
import {useUserStore, useWebSocketStore} from "/@/store";
import {BASE_URL} from "/@/store/constants";
import AvatarIcon from "/@/assets/images/avatar.jpg";
import router from "/@/router";

  const socketStore = useWebSocketStore();
  const userStore = useUserStore();


  // 返回对应选择列表
  const chatroomList = computed(() => { return socketStore.chat_list; });

  // 选择聊天用户
  const selectSession = (item, index) => {
    socketStore.sessionSelectId = index
    // socketStore.recipient = item
    socketStore.fillMessage();
    // socketStore.initEditor()
    // socketStore.toBottom()

  }
</script>

<style scoped lang="scss">
  $selectBg: rgba(0, 0, 0, 0.08);
  .chat-session {
    :deep(p){
      margin: 0;
    }
    border-right: 1px solid var(--ep-border-color);
    @media (max-width: 1024px){
      border-right: none; 
    }
    .session-item {
      &:hover {
        background: $selectBg;
      }
    }
    .session-active {
      background: $selectBg;
    }
  }
</style>
