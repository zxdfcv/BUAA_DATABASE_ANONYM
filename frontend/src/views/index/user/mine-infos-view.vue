<template>
  <div class="mine-infos-view">
    <div class="info-box flex-view">
      <img v-if = "!(appStore.view_user_avatar === null || appStore.view_user_avatar === undefined)" :src="BASE_URL+appStore.view_user_avatar" class="avatar-img">
      <img v-else :src="AvatarImg" class="avatar-img">
      <div class="name-box">
        <h2 class="nick">{{ appStore.view_user_username }}</h2>
        <div class="age">
          <a-space warp v-if="!(appStore.view_user_id === userStore.user_id)">
            <Button v-if="userStore.user_access === undefined || userStore.user_access === null || !isFollowing" @click="follow" style="width: 90px">关注 Ta</Button>
            <Button v-else type="primary" @click="deleteFollow" style="width: 90px">取消关注</Button>
          </a-space>
        </div>
      </div>
    </div>
    <div class="order-box">
      <div class="list">
        <div class="mine-item flex-view" @click="clickMenu('wishThingView')">
          <img :src="PushIconImage">
          <span v-if="appStore.view_user_id === userStore.user_id">我的发布</span>
          <span v-else>Ta的发布</span>
        </div>
        <div class="mine-item flex-view" @click="clickMenu('myFollow')">
          <img :src="PushIconImage">
          <span v-if="appStore.view_user_id === userStore.user_id">我的关注</span>
          <span v-else>Ta的关注</span>
        </div>
        <div class="mine-item flex-view" @click="clickMenu('myFans')">
          <img :src="PushIconImage">
          <span v-if="appStore.view_user_id === userStore.user_id">我的粉丝</span>
          <span v-else>Ta的粉丝</span>
        </div>
      </div>
    </div>
    <div class="setting-box"  v-if="appStore.view_user_id === userStore.user_id">
      <div class="list">
        <div class="mine-item flex-view" @click="clickMenu('scoreView')">
          <img :src="PointIconImage">
          <span>商品收藏</span>
        </div>
        <div class="mine-item flex-view" @click="clickMenu('thingHistory')">
          <img :src="AddressIconImage">
          <span>我买到的</span>
        </div>
        <div class="mine-item flex-view" @click="clickMenu('commentView')">
          <img :src="CommentIconImg">
          <span>我的评论</span>
        </div>
        <div class="mine-item flex-view" @click="clickMenu('userInfoEditView')">
          <img :src="SettingIconImage" alt="编辑资料">
          <span>编辑资料</span>
        </div>
        <!-- <div class="mine-item flex-view" @click="clickMenu('pushView')">
          <img :src="PushIconImage" alt="推送设置">
          <span>推送设置</span>
        </div>
        <div class="mine-item flex-view" @click="clickMenu('messageView')">
          <img :src="MessageIconImage" alt="消息管理">
          <span>消息管理</span>
        </div> -->
      </div>
    </div>
  </div>
</template>

<script setup>
import AvatarImg from '/@/assets/images/avatar.jpg'
import MyOrderImg from '/@/assets/images/order-icon.svg'
import CommentIconImg from '/@/assets/images/order-thing-icon.svg'
import AddressIconImage from '/@/assets/images/order-address-icon.svg'
import PointIconImage from '/@/assets/images/order-point-icon.svg'
import SettingIconImage from '/@/assets/images/setting-icon.svg'
import SafeIconImage from '/@/assets/images/setting-safe-icon.svg'
import PushIconImage from '/@/assets/images/setting-push-icon.svg'
import MessageIconImage from '/@/assets/images/setting-msg-icon.svg'

import {getCollectThingListApi} from '/@/api/index/thing'
import {getWishThingListApi} from '/@/api/index/thing'
import {useAppStore, useUserStore} from '/@/store';
import { BASE_URL } from '/@/store/constants';
import { userDeleteFollowApi, userFollowApi, userFollowersApi } from "/@/api/index/user";
import {openNotification} from "/@/utils/notice";
const userStore = useUserStore();
const appStore = useAppStore();
const router = useRouter();

const view_id = ref(0);
let collectCount = ref(0)
let wishCount = ref(0)
const isFollowing = ref(false);
const followId = ref(0);

onMounted(async () => {
  view_id.value = appStore.view_user_id;
  await queryFollow();

  // getCollectThingList()
  // getWishThingList()
})

const queryFollow = async () => {
  if (appStore.view_user_id === null || appStore.view_user_id === undefined) {
    isFollowing.value = false;
  }
  const res = await userFollowersApi({user_id: userStore.user_id});
  let query = []
  for (var i = 0; i < res.data.length; i++) {
    query.push(res.data[i].following);
    if (res.data[i].following === appStore.view_user_id) {
      followId.value = res.data[i].id;
    }
  }
  console.log(query, query.includes(appStore.view_user_id))
  isFollowing.value = query.includes(appStore.view_user_id);
}

const follow = async () => {
  if (userStore.user_access) {
    userFollowApi({follower_id: appStore.view_user_id}).then(async res => {
      console.log(res.data);
      await queryFollow();
    }).catch(err => {
      console.log(err);
    });
  } else {
    openNotification({
      type: 'error',
      message: 'Oops!',
      description: '你必须先登录才能进行关注操作！'
    })
  }
}

const deleteFollow = async () => {
  userDeleteFollowApi({ids: followId.value}).then(async res => {
    console.log(res.data);
    await queryFollow();
  }).catch(err => {
    console.log(err);
  });
}
const SelfAvatar = (avatar) => {
  return !(avatar === "null" || avatar === null);
}

const clickMenu = (name) => {
  router.push({name: name, query: {id: appStore.view_user_id}})
}
const getCollectThingList =()=> {
  let username = userStore.user_name
  getCollectThingListApi({username: username}).then(res => {
    collectCount.value = res.data.length
  }).catch(err => {
    console.log(err.msg)
  })
}

const getWishThingList =()=> {
  let username = userStore.user_name
  getWishThingListApi({username: username}).then(res => {
    wishCount.value = res.data.length
  }).catch(err => {
    console.log(err.msg)
  })
}

</script>

<style scoped lang="less">
.flex-view {
  display: flex;
}

.mine-infos-view {
  width: 235px;
  margin-right: 20px;
  border: 1px solid #cedce4;
  height: fit-content;

  .info-box {
    -webkit-box-align: center;
    -ms-flex-align: center;
    align-items: center;
    padding: 16px 16px 0;
    overflow: hidden;
  }

  .avatar-img {
    width: 48px;
    height: 48px;
    margin-right: 16px;
    border-radius: 50%;
  }

  .name-box {
    -webkit-box-flex: 1;
    -ms-flex: 1;
    flex: 1;
    overflow: hidden;

    .nick {
      color: #152844;
      font-weight: 600;
      font-size: 18px;
      line-height: 24px;
      height: 24px;
      text-overflow: ellipsis;
      white-space: nowrap;
      margin: 0;
      overflow: hidden;
    }

    .age {
      font-size: 12px;
      color: #6f6f6f;
      height: 36px;
      line-height: 16px;
      margin-top: 8px;
    }

    .give-point {
      color: #4684e2;
      cursor: pointer;
      float: right;
    }
  }

  .counts-view {
    border: none;
    padding: 16px;
  }

  .counts {
    margin-top: 12px;
    text-align: center;
    -webkit-box-align: center;
    -ms-flex-align: center;
    align-items: center;

    .flex-item {
      -webkit-box-flex: 1;
      -ms-flex: 1;
      flex: 1;
      cursor: pointer;
    }

    .text {
      height: 16px;
      line-height: 16px;
      color: #6f6f6f;
    }

    .num {
      height: 18px;
      line-height: 18px;
      color: #152844;
      font-weight: 600;
      font-size: 14px;
      margin-top: 4px;
    }

    .split-line {
      width: 1px;
      height: 24px;
      background: #dae6f9;
    }
  }

  .intro-box {
    border-top: 1px solid #cedce4;
    padding: 16px;

    .title {
      color: #6f6f6f;
      font-size: 12px;
      line-height: 16px;
    }

    .intro-content {
      color: #152844;
      font-size: 14px;
      line-height: 20px;
      overflow: hidden;
      text-overflow: ellipsis;
      margin: 8px 0;
    }
  }

  .create-box {
    cursor: pointer;
    border-top: 1px solid #cedce4;
    padding: 16px;

    .title {
      position: relative;
      color: #152844;
      font-weight: 600;
      font-size: 14px;
      line-height: 18px;
      height: 18px;
    }

    .counts {
      margin-top: 12px;
      text-align: center;
      -webkit-box-align: center;
      -ms-flex-align: center;
      align-items: center;

      .flex-item {
        -webkit-box-flex: 1;
        -ms-flex: 1;
        flex: 1;
        cursor: pointer;
      }

      .split-line {
        width: 1px;
        height: 24px;
        background: #dae6f9;
      }
    }
  }

  .order-box {
    margin-top: 24px;
    border-top: 1px solid #cedce4;
    padding: 16px;

    .title {
      color: #152844;
      font-weight: 600;
      font-size: 14px;
      line-height: 18px;
      height: 18px;
      margin-bottom: 8px;
    }

    .list {
      padding-left: 16px;

      .mine-item {
        border-top: 1px dashed #cedce4;
        cursor: pointer;
        height: 48px;
        -webkit-box-align: center;
        -ms-flex-align: center;
        align-items: center;

        img {
          width: 24px;
          margin-right: 8px;
          height: 24px;
        }

        span {
          color: #152844;
          font-size: 14px;
        }
      }

      .mine-item:first-child {
        border: none;
      }
    }
  }

  .setting-box {
    border-top: 1px solid #cedce4;
    padding: 16px;

    .title {
      color: #152844;
      font-weight: 600;
      font-size: 14px;
      line-height: 18px;
      height: 18px;
      margin-bottom: 8px;
    }

    .list {
      padding-left: 16px;
    }

    .mine-item {
      border-top: 1px dashed #cedce4;
      cursor: pointer;
      height: 48px;
      -webkit-box-align: center;
      -ms-flex-align: center;
      align-items: center;

      img {
        width: 24px;
        margin-right: 8px;
        height: 24px;
      }

      span {
        color: #152844;
        font-size: 14px;
      }
    }

    .mine-item:first-child {
      border: none;
    }
  }
}
</style>
