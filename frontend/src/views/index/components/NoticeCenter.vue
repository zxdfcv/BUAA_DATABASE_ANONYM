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
        <a-tab-pane key="1" tab="评论消息" style="height: 300px">
          <el-scrollbar>
            <a-list item-layout="horizontal" :data-source="messageList.comment">
              <template #renderItem="{ item }">
                <a-list-item>
                  <template #actions>
                    <button>edit</button>
                    >
                    <a key="list-loadmore-more">more</a>
                  </template>
                  <a-list-item-meta :description="item">
                    <template #title>
                      <a href="https://www.antdv.com/">{{ item.name.last }}</a>
                    </template>
                    <template #avatar>
                      <a-avatar :src="item.picture.large" />
                    </template>
                  </a-list-item-meta>
                </a-list-item>
              </template>
            </a-list>
          </el-scrollbar>
        </a-tab-pane>
        <a-tab-pane key="2" tab="回复消息" style="height: 300px">
          <el-scrollbar> Content of Tab Pane 2 </el-scrollbar>
        </a-tab-pane>
        <a-tab-pane key="3" tab="私聊消息" style="height: 300px">
          <el-scrollbar> Content of Tab Pane 3 </el-scrollbar>
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

  const newMessageCount = ref(111);
  const activeKey = ref('1');
  // const emits = defineEmits(['newMessage'])
  const messageList = reactive({});
</script>

<style scoped></style>
