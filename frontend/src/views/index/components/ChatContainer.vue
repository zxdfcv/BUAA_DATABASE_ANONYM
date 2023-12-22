<template>
  <el-card shadow="hover" class="lg:w-1200px w-full mt-30px chat-container" style="margin-top: 30px; ">
    <el-row type="flex" class="w-full border-rounded-33px" style="border-rounded: 33px">
      <!-- 会话区域 -->

      <ChatDomain class="lg:block hidden" style="width: 25%"/>
      <a-divider type="vertical" style="height: 600px"/>
      <!-- 聊天区域 -->
          <ChatContent />
    </el-row>
  </el-card>

</template>

<script setup>

import ChatDomain from "/@/views/index/components/chat/ChatDomain.vue"
import ChatContent from "/@/views/index/components/chat/ChatContent.vue"


</script>

<style scoped>
:deep(.ep-drawer__header){
  padding: 10px;
  margin-bottom: 0;
}

.chat-container{
  min-height: 600px;
  :deep(.ep-card__body){
    padding-left: 0!important;
    @media (max-width: 1024px){
      padding-right: 0!important;
    }
  }
}
</style>