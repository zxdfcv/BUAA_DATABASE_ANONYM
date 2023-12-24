<template>
  <footer class="px-20px" style="width: 80%">
    <!--工具栏-->
    <a-divider />
    <el-row type="flex" class="mb-10px">
      <a-upload
          name="file"
          accept="image/*"
          :file-list="image"
          :multiple="false"
          :max-count="1"
          :before-upload="beforeUploadImage"
          @remove="removeImage"
      >
        <a-button shape="circle" >
          <template #icon>
            <CloudUploadOutlined />
          </template>
        </a-button>
      </a-upload>
    </el-row>
<!--    <ChatEditor-->
<!--      v-model="store.sendInfo"-->
<!--      ref="editor"-->
<!--      id="chatEditor"-->
<!--      :height="135"-->
<!--      class="answer-editor"-->
<!--      placeholder="请输入聊天"-->
<!--    ></ChatEditor>-->
    <div class="edit-box" style="display:flex">
        <div class="text-left">
          <div class="right-box">
          <textarea v-model="editor" placeholder="请输入消息内容" maxlength="200" class="intro">
          </textarea>
            <p class="tip">限制200字以内</p>
          </div>
        </div>
      <div class="text-right mt-10px" style="align-self: center; padding-left: 20px;">
        <a-button @click="sendMessage" >发 送</a-button>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { useUserStore, useWebSocketStore } from "/@/store";
import { CloudUploadOutlined } from "@ant-design/icons-vue";
import { openNotification } from "/@/utils/notice";
import { sendChatMessageApi } from "/@/api/index/notice";

const store = useWebSocketStore()
  const userStore = useUserStore();
  const editor = ref("")

  const image = ref([]);

  const sendMessage = () => {
    const item = store.chat_list[store.sessionSelectId];
    console.log(item);
    if (editor.value.length > 0 && image.value.length > 0) {
      openNotification({type: 'warning', message: '不允许同时发送图片和文字！'});
      return ;
    } else if (editor.value.length > 0) {
      sendChatMessageApi({
        recipient: (item.sender === userStore.user_id) ? item.recipient : item.sender,
        product: item.product,
        content: editor.value})
        .then(async res => {
          console.log(res.data);
          await store.fillChat();
          await store.fillMessage();
          editor.value = "";
        }).catch(err => {
        console.log(err);
      })
    } else if (image.value.length > 0) {
      let submitForm = new FormData();
      submitForm.append('recipient', (item.sender === userStore.user_id) ? item.recipient : item.sender);
      submitForm.append('product', item.product);
      submitForm.append('content', "[图片]");
      submitForm.append('image', image.value[0]);
      sendChatMessageApi(submitForm)
        .then(async res => {
          console.log(res.data);
          await store.fillChat();
          await store.fillMessage();
          image.value = [];
        }).catch(err => {
        console.log(err);
      })
    } else {
      openNotification({type: 'error', message: '需要至少发送图片和文字中的一种！'});
      return ;
    }
    console.log(editor.value);
  }

  const beforeUploadImage = (file) => {
    // 改文件名
    const fileName = new Date().getTime().toString() + '.' + file.type.substring(6)
    const copyFile = new File([file], fileName)
    console.log(copyFile)
    image.value = [...(image.value || []), copyFile];
    return false
  }

  const removeImage = () => {
    image.value = []
    return true;
  }

</script>

<style scoped>
.edit-box{
  .ep-scrollbar{
    border: 1px solid var(--el-border-color);
  }
  :deep(.w-e-toolbar){
    border: none!important;
  }
  :deep(.w-e-text-container) {
    border: none!important;
    background-color: transparent;
    height: auto!important;
    min-height: 88px;
  }
}

.intro {
  resize: none;
  background: #f8fafb;
  min-height: 100px;
  min-width: 620px;
  padding: 8px 12px;
  line-height: 22px;
  font-size: 14px;
  margin-top: 10px;
  color: #152844;
}

:deep(.ant-divider-horizontal) {
  margin: 10px 0 !important;
}
</style>