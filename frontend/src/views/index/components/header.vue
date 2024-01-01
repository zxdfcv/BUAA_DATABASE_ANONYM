<template>
  <div class="main-bar-view">
    <div class="logo">
      <img :src="logoImage" class="search-icon" @click="$router.push({name:'portal'})">
    </div>

    <div class="search-entry">
      <img :src="SearchIcon" class="search-icon">
      <input placeholder="今天想搜些什么？" ref="keywordRef" @keyup.enter="search"/>
    </div>
    <Button type="primary" shape="circle" icon="ios-search" style="margin-left: 15px;" @click="search">搜索</Button>
    <a-dropdown trigger="click">
      <Button type="default" style="margin-left: 15px;">
        全部分类
        <Icon type="ios-arrow-down" />
      </Button>
      <template #overlay>
        <a-menu>
          <!-- TODO: 可以修改成大分类栏 -->
          <a-menu-item v-for="(item) in search_index">
            <a @click="router.push({name: 'search', query: {keyword: item,type: 'C_1'}});">{{ item }}</a>
          </a-menu-item>
        </a-menu>
      </template>
    </a-dropdown>


    <div class="right-view" style="margin-right: 30px;">
      
      <template v-if="userStore.user_access">
        <!-- 确认有登陆权限 -->
        <Button v-if="userStore.is_admin" type="primary" @click="router.push({name: 'admin'})">后台入口</Button>
        <a-dropdown>
          <a class="ant-dropdown-link" @click="e => e.preventDefault()">
            <img v-if = "hasAvatar(userStore.user_avatar)" :src="BASE_URL + userStore.user_avatar" class="self-img">
            <img v-else :src="AvatarIcon" class="self-img">
          </a>
          <template #overlay >
            <a-menu style="width: 120px">
              <a-menu-item>
                <template #icon><WalletOutlined /></template>
                <a @click="router.push({name: 'addProduct', query: {id: userStore.user_id}})">我要发布</a>
              </a-menu-item>
              <a-menu-item>
                <template #icon><UserOutlined /></template>
                <a @click="router.push({name: 'userInfoEditView', query: {id: userStore.user_id}})">账号设置</a>
              </a-menu-item>
              <a-menu-item>
                <template #icon><LogoutOutlined /></template>
                <a @click="quit()">退出登录</a>
              </a-menu-item>
            </a-menu>
          </template>
        </a-dropdown>
      </template>
      <template v-else>
        <!-- 尚未登录，显示待登录和默认 -->
        <Button type="primary" shape="circle" icon="md-log-in" @click="goLogin">登录</Button>
      </template>

      <div class="right-icon" v-if="userStore.user_access">
        <NoticeCenter />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { LogoutOutlined, UserOutlined, WalletOutlined } from "@ant-design/icons-vue";

import { listReceiveCommentsApi } from "/@/api/index/comment";
import { useAppStore, useUserStore } from "/@/store";
import logoImage from "/@/assets/images/logo_b.png";
import SearchIcon from "/@/assets/images/search-icon.svg";
import AvatarIcon from "/@/assets/images/avatar.jpg";
import { BASE_URL } from "/@/store/constants";
import NoticeCenter from "/@/views/index/components/NoticeCenter.vue";

const router = useRouter();
const userStore = useUserStore();
const appStore = useAppStore();

const keywordRef = ref()

let loading = ref(false)
let msgVisible = ref(false)
let msgData = ref([] as any)
let HasNewMessage = ref(false)
let pointKey = 0

let search_index = ['hello', 'world'];

const hasAvatar = (avatar) => {
  return !(avatar === "null" || avatar === null || avatar === undefined);
}


onMounted(async () => {
  search_index = await appStore.getC1() as string[];
  console.log(search_index)
  // getMessageList()
  // console.log("avatar: ", userStore.user_avatar);
})

const getMessageList = () => {
  loading.value = true
  listReceiveCommentsApi({userId : userStore.user_id,}).then(res => {
    console.log("结果返回")
    console.log(res)
    msgData.value = res.data
    loading.value = false
    checkMessageList()
    console.log(HasNewMessage)
  }).catch(err => {
    console.log(err)
    loading.value = false
  })
}
const search = () => {
  const keyword = keywordRef.value.value
  if (keyword === '') {
    return;
  }
  router.push({name: 'search', query: {keyword: keyword}});
}

const goLogin = () => {
  router.push({name: 'login'})
}

const quit = () => {
  userStore.logout().then(res => {
    router.push({name: 'portal'})
  })
}

const checkMessageList = () => {
  if (msgData == undefined || msgData.value.length <= 0) {
    console.log("无")
    HasNewMessage.value = false
  } else {
    console.log("有")
    HasNewMessage.value = true
  }
}

</script>

<style scoped lang="less">
.main-bar-view {
  position: fixed;
  top: 0;
  left: 0;
  height: 60px;
  width: 100%;
  background: rgb(255, 255, 255);
  border-bottom: 2px solid #cedce4;
  padding-left: 48px;
  z-index: 16;
  display: flex;
  flex-direction: row;
  align-items: center;
}

.logo {
  margin-right: 24px;

  img {
    width: 48px;
    height: 48px;
    cursor: default;
  }
}

.search-entry {
  position: relative;
  width: 25%;
  max-width: 500px;
  min-width: 300px;
  height: 32px;
  background: #ecf3fc;
  padding: 0 12px;
  border-radius: 16px;
  font-size: 0;
  cursor: text;

  img {
    max-width: 100%;
    height: auto;
  }

  .search-icon {
    width: 18px;
    margin: 7px 8px 0 0;
  }

  input {
    position: absolute;
    top: 4px;
    width: 85%;
    height: 24px;
    border: 0px;
    outline: none;
    color: #000;
    background: #ecf3fc;
    font-size: 14px;
  }
}

.svg {
  vertical-align: top;
}
.right-view {
  padding-right: 10px;
  flex: 1;
  display: flex;
  flex-direction: row;
  gap: 40px;
  justify-content: flex-end; /* 内容右对齐 */

  .username {
    height: 32px;
    line-height: 32px;
    text-align: center;
  }

  button {
    outline: none;
    border: none;
    cursor: pointer;
  }

  img {
    cursor: pointer;
  }

  .right-icon {
    position: relative;
    width: 24px;
    margin: 4px 0 0 4px;
    cursor: pointer;
    display: inline-block;
    font-size: 0;

    span {
      position: absolute;
      right: -15px;
      top: -3px;
      font-size: 12px;
      color: #fff;
      background: #4684e2;
      border-radius: 8px;
      padding: 0 4px;
      height: 16px;
      line-height: 16px;
      font-weight: 600;
      min-width: 20px;
      text-align: center;
    }

    .msg-point {
      position: absolute;
      right: -4px;
      top: 0;
      min-width: 8px;
      width: 8px;
      height: 8px;
      background: #4684e2;
      border-radius: 50%;
    }
  }

  .self-img {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    vertical-align: middle;
    cursor: pointer;
  }

  // .btn {
  //   background: #4684e2;
  //   font-size: 14px;
  //   color: #fff;
  //   border-radius: 32px;
  //   text-align: center;
  //   width: 66px;
  //   height: 32px;
  //   line-height: 32px;
  //   vertical-align: middle;
  //   margin-left: 32px;
  // }
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

.notification-item {
  padding-top: 16px;

  .avatar {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    margin-right: 8px;
  }

  .content-box {
    -webkit-box-flex: 1;
    -ms-flex: 1;
    flex: 1;
    border-bottom: 1px dashed #e9e9e9;
    padding: 4px 0 16px;
  }

  .header {
    margin-bottom: 12px;
  }

  .title-txt {
    color: #315c9e;
    font-weight: 500;
    font-size: 14px;
    display: inline-block;
  }

  .time {
    color: #a1adc5;
    font-size: 14px;
  }

  .head-text {
    color: #152844;
    font-weight: 500;
    font-size: 14px;
    line-height: 22px;

    .name {
      margin-right: 8px;
    }
  }

  .content {
    margin-top: 4px;
    color: #484848;
    font-size: 14px;
    line-height: 22px;
  }

}

</style>
