<template>
  <a-layout id="components-layout-demo-custom-trigger">
    <a-layout-header style="background: #fff; padding: 0">
      <div class="header">
        <menu-unfold-outlined
            v-if="collapsed"
            class="trigger"
            @click="() => (collapsed = !collapsed)"
        />
        <menu-fold-outlined v-else class="trigger" @click="() => (collapsed = !collapsed)" />
        <img class="header-logo" :src="logo">
        <span class="header-title">北航闲鱼商城后台管理系统</span>
        <div class="empty"></div>
        <a-button style="margin-right: 24px;" @click="handlePreview">前台预览</a-button>
        <span>管理员[{{ userStore.user_name }}]</span>
        <a class="header-quit" @click="handleLogout">退出</a>
      </div>
    </a-layout-header>
    <a-layout>
      <a-layout-sider v-model:collapsed="collapsed" :trigger="null" collapsible>
        <a-menu style="overflow:auto; overflow-x: hidden;" v-model:selectedKeys="selectedKeys" theme="dark" mode="inline" @click="handleClick">

          <a-menu-item key="product">
            <database-outlined/>
            <span>商品管理</span>
          </a-menu-item>
          <a-menu-item key="order">
            <database-outlined/>
            <span>订单管理</span>
          </a-menu-item>
          <a-menu-item key="classification1">
            <layout-outlined/>
            <span>一级分类管理</span>
          </a-menu-item>
          <a-menu-item key="classification2">
            <layout-outlined/>
            <span>二级分类管理</span>
          </a-menu-item>
          <a-menu-item key="tag">
            <tag-outlined/>
            <span>标签管理</span>
          </a-menu-item>
          <a-menu-item key="comment">
            <comment-outlined/>
            <span>评论管理</span>
          </a-menu-item>
          <a-menu-item key="reply">
            <message-outlined/>
            <span>回复管理</span>
          </a-menu-item>
          <a-menu-item key="chat">
            <message-outlined/>
            <span>私聊管理</span>
          </a-menu-item>
          <a-menu-item key="user">
            <user-outlined/>
            <span>用户管理</span>
          </a-menu-item>
          <a-menu-item key="permission">
            <user-outlined/>
            <span>权限管理</span>
          </a-menu-item>
          <!-- <a-sub-menu>
            <template #icon>
              <folder-outlined/>
            </template>
            <template #title>运营管理</template>
            <a-menu-item key="ad">
              <appstore-outlined/>
              <span>广告管理</span>
            </a-menu-item>
            <a-menu-item key="notice">
              <appstore-outlined/>
              <span>通知公告</span>
            </a-menu-item>
          </a-sub-menu> -->
          <a-sub-menu>
            <template #icon>
              <folder-outlined/>
            </template>
            <template #title>日志管理</template>
            <a-menu-item key="loginLog">
              <appstore-outlined/>
              <span>登录日志</span>
            </a-menu-item>
            <a-menu-item key="opLog">
              <appstore-outlined/>
              <span>操作日志</span>
            </a-menu-item>
            <a-menu-item key="errorLog">
              <appstore-outlined/>
              <span>错误日志</span>
            </a-menu-item>
          </a-sub-menu>
          <a-menu-item key="overview">
            <home-outlined/>
            <span>统计分析</span>
          </a-menu-item>
          <a-menu-item key="sysInfo">
            <info-circle-outlined/>
            <span>系统信息</span>
          </a-menu-item>
        </a-menu>
      </a-layout-sider>
      <a-layout-content :style="{ margin: '16px 16px', minHeight: '200px' }">
        <router-view/>
      </a-layout-content>
    </a-layout>
  </a-layout>

</template>
<script setup lang="ts">
import { useRoute, useRouter } from "vue-router";
import logo from "/@/assets/images/logo_b.png";

import {
  AppstoreOutlined,
  CommentOutlined,
  DatabaseOutlined,
  FolderOutlined,
  HomeOutlined,
  InfoCircleOutlined,
  LayoutOutlined,
  MenuFoldOutlined,
  MenuUnfoldOutlined,
  MessageOutlined,
  TagOutlined,
  UserOutlined
} from "@ant-design/icons-vue";

import { ref } from "vue";
import { useAppStore, useUserStore } from "/@/store";

const userStore = useUserStore();

const selectedKeys = ref<any[]>([])
const collapsed = ref<boolean>(false)

const router = useRouter()
const route = useRoute()

const handleClick = ({item, key, keyPath}) => {
  console.log('点击路由===>', key)
  router.push({
    name: key,
  })
}

const handlePreview = ()=>{
  let text = router.resolve({name: 'index'})
  window.open(text.href, '_blank')
}

onMounted(() => {
  console.log('当前路由===>', route.name)
  useAppStore().getC1()
  selectedKeys.value = [route.name]
})


const handleLogout = () => {
  userStore.adminLogout().then(res => {
    router.push({name: 'adminLogin'})
  })
}

</script>
<style scoped lang="less">

// header样式
.header {
  display: flex;
  flex-direction: row;
  align-items: center; // 垂直居中
  padding-left: 24px;
  padding-right: 24px;

  .header-logo {
    width: 32px;
    height: 32px;
    cursor: pointer;
  }

  .header-title {
    margin-left: 16px;
    font-size: 20px;
    font-weight: bold;
    text-align: center;
  }

  .empty {
    flex: 1;
  }

  .header-quit {
    margin-left: 12px;
  }
}


#components-layout-demo-custom-trigger {
  height: 100%;
}

#components-layout-demo-custom-trigger .trigger {
  font-size: 18px;
  line-height: 64px;
  padding: 0 24px;
  cursor: pointer;
  transition: color 0.3s;
}

#components-layout-demo-custom-trigger .trigger:hover {
  color: #1890ff;
}

#components-layout-demo-custom-trigger .trigger {
  font-size: 18px;
  line-height: 64px;
  padding: 0 24px;
  cursor: pointer;
  transition: color 0.3s;
}

#components-layout-demo-custom-trigger .trigger:hover {
  color: #1890ff;
}

#components-layout-demo-custom-trigger .logo {
  height: 32px;
  background: rgba(255, 255, 255, 0.3);
  margin: 16px;
}

.site-layout .site-layout-background {
  background: #fff;
}

:deep(.ant-layout-content) {
  overflow-x: hidden;
}

:deep(.ant-layout-sider) {
  padding: 16px 0;
  background-color: #f0f2f5;
}

:deep(.ant-menu) {
  padding-top: 16px;
  height: 100%;
}

</style>
