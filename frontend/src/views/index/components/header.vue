<template>
  <div class="main-bar-view">
    <div class="logo">
      <img :src="logoImage" class="search-icon" @click="$router.push({name:'portal'})">
    </div>

    <div class="search-entry">
      <img :src="SearchIcon" class="search-icon">
      <input placeholder="今天想搜些什么？" ref="keywordRef" @keyup.enter="search"/>
    </div>
    <Button type="primary" shape="circle" icon="ios-search" style="margin-left: 15px;" @click="search">Search</Button>
    <a-dropdown trigger="click">
      <Button type="default" style="margin-left: 15px;">
        All Category
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


    <div class="right-view">
      
      <template v-if="userStore.user_access">
        <!-- 确认有登陆权限 -->
        <Button type="primary" @click="router.push({name: 'admin'})">后台入口</Button>
        <a-dropdown>
          <a class="ant-dropdown-link" @click="e => e.preventDefault()"> <!-- TODO: 头像的 url 格式需确定 -->
            <img v-if = "hasAvatar(userStore.user_avatar)" :src="BASE_URL + userStore.user_avatar" class="self-img">
            <img v-else :src="AvatarIcon" class="self-img">
          </a>
          <template #overlay >
            <a-menu style="width: 120px">
              <a-menu-item>
                <template #icon><WalletOutlined /></template>
                <a @click="router.push({name: 'createProductView'})">我要发布</a>
              </a-menu-item>
              <a-menu-item>
                <template #icon><UserOutlined /></template>
                <a @click="router.push({name: 'userInfoEditView'})">账号设置</a>
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

      <div class="right-icon">
        <el-popover
          :width="300"
          popper-style="box-shadow: rgb(14 18 22 / 35%) 0px 10px 38px -10px, rgb(14 18 22 / 20%) 0px 10px 20px -15px; padding: 20px;"
        >
          <template #reference>
            <img :src="MessageIcon">
            <span class="msg-point" v-show="HasNewMessage"></span>
          </template>
          <template #default>
            <div
              class="demo-rich-conent"
              style="display: flex; gap: 16px; flex-direction: column"
            >
              <el-avatar
                :size="60"
                src="https://avatars.githubusercontent.com/u/72015883?v=4"
                style="margin-bottom: 8px"
              />
              <div>
                <p
                  class="demo-rich-content__name"
                  style="margin: 0; font-weight: 500"
                >
                  Element Plus
                </p>
                <p
                  class="demo-rich-content__mention"
                  style="margin: 0; font-size: 14px; color: var(--el-color-info)"
                >
                  @element-plus
                </p>
              </div>

              <p class="demo-rich-content__desc" style="margin: 0">
                Element Plus, a Vue 3 based component library for developers,
                designers and product managers
              </p>
            </div>
          </template>
        </el-popover>
      </div>
      <div>
        <a-drawer
            title="我的消息"
            placement="right"
            :closable="true"
            :maskClosable="true"
            :visible="msgVisible"
            @close="onClose"
        >
          <a-spin :spinning="loading" style="min-height: 200px;">
            <div class="list-content">
              <div class="notification-view">
                <div class="list">
                  <div class="notification-item flex-view" v-for="item in msgData">
                    <!---->
                    <div class="content-box">
                      <div class="header">
                        <span v-if="item.title!==undefined" class="title-txt">
                          {{ item.title }}
                          <Button shape="circle"  @click="setReadState(item.id)">标为已读</Button>
                        </span>
                        <span v-else-if="item.canteen_title!==undefined" class="title-txt">
                          {{ item.canteen_title }}
                          <Button shape="circle"  @click="setReadState(item.id)">标为已读</Button>
                        </span>
                        <span v-else class="title-txt">
                          {{ item.classification_title }}
                          <Button shape="circle"  @click="setReadState(item.id)">标为已读</Button>
                        </span>
                        <br/>
                        <span class="time">{{ item.create_time }}</span>
                      </div>
                      <div class="head-text">
                      </div>
                      <div class="content">
                        <p>{{ item.content }}</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </a-spin>
        </a-drawer>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { UserOutlined, WalletOutlined, LogoutOutlined } from '@ant-design/icons-vue';

import {listReceiveCommentsApi, SetStateToReadedApi} from '/@/api/index/comment'
import { useUserStore, useAppStore } from "/@/store";
import logoImage from '/@/assets/images/logo_b.png';
import SearchIcon from '/@/assets/images/search-icon.svg';
import AvatarIcon from '/@/assets/images/avatar.jpg';
import MessageIcon from '/@/assets/images/message-icon.svg';
import {BASE_URL} from "/@/store/constants";

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
  // if (route.name === 'search') {
    
  // } else {
  //   let text = router.resolve({name: 'search', query: {keyword: keyword}})
  //   window.open(text.href, '_blank')
  // }
}
const goLogin = () => {
  router.push({name: 'login'})
}

const goUserCenter = (menuName) => {
  router.push({name: menuName})
}
const quit = () => {
  userStore.logout().then(res => {
    router.push({name: 'portal'})
  })
}
const onClose = () => {
  msgVisible.value = false;
}

const setReadState = (id) => {
  SetStateToReadedApi({ids:id}).then(res => {
    console.log("设置已阅状态成功")
    getMessageList()
  }).catch(err => {
    console.log(err)
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


const UpdateState = () => {
  if (HasNewMessage.value == true) {
    HasNewMessage.value = false
  } else {
    HasNewMessage.value = true
  }
  pointKey += 1
  console.log(pointKey)
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
