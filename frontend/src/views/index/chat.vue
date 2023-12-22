<template>
  <div class="chat">
    <Header />
    <div class="chat-content">
      <ChatContainer />
    </div>
  </div>
</template>

<script setup>
import Header from '/@/views/index/components/header.vue'
import Footer from '/@/views/index/components/footer.vue'
import ChatContainer from "/@/views/index/components/ChatContainer.vue";

</script>

<style scoped lang="less">

.chat-content {
  width: 1100px;
  margin: 150px auto;
  max-height: 800px;
}
</style>
