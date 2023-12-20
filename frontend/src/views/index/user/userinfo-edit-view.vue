<template>
  <div class="content-list">
    <div class="list-title">设置</div>
    <a-spin :spinning="loading" style="min-height: 200px;">
      <div class="list-content">
      <div class="edit-view">
        <div class="item flex-view">
          <div class="label">头像</div>
          <div class="right-box avatar-box flex-view">
            <img v-if="tData.form && tData.form.avatar" :src="BASE_URL + tData.form.avatar" class="avatar">
            <img v-else :src="AvatarIcon" class="avatar">
            <div class="change-tips flex-view">
                <a-upload
                  name="file"
                  accept="image/*"
                  :multiple="false"
                  :before-upload="beforeUpload"
                >
                  <label>点击更换头像</label>
                </a-upload>
              <p class="tip">图片格式支持 GIF、PNG、JPEG，尺寸不小于 200 PX，小于 4 MB</p>
            </div>
          </div>
        </div>
        <div class="item flex-view">
          <div class="label">昵称</div>
          <div class="right-box">
            <input type="text" v-model="tData.form.nickname" placeholder="请输入昵称" maxlength="20" class="input-dom">
            <p class="tip">支持中英文，长度不能超过 20 个字符</p>
          </div>
        </div>
        <div class="item flex-view">
          <div class="label">手机号</div>
          <div class="right-box">
            <input type="text" v-model="tData.form.mobile" placeholder="请输入手机号" maxlength="100" class="input-dom web-input">
          </div>
        </div>
        <div class="item flex-view">
          <div class="label">邮箱</div>
          <div class="right-box">
            <input type="text" v-model="tData.form.email" placeholder="请输入邮箱" maxlength="100" class="input-dom web-input">
          </div>
        </div>
        <div class="item flex-view">
          <div class="label">个人简介</div>
          <div class="right-box">
          <textarea v-model="tData.form.description" placeholder="请输入简介" maxlength="200" class="intro">
          </textarea>
            <p class="tip">限制200字以内</p>
          </div>
        </div>
        <button class="save mg" @click="submit()">保存</button>

        <form><div class="item flex-view" style="max-width: 400px; min-width: 250px;">
          <div class="label">当前密码</div>
          <div class="right-box">
            <a-input-password placeholder="输入当前密码" v-model:value="password.old" autocomplete="off"/>
          </div>
        </div>
        <div class="item flex-view" style="max-width: 400px; min-width: 250px;">
          <div class="label">新密码</div>
          <div class="right-box">
            <a-input-password placeholder="输入新密码" v-model:value="password.new1" autocomplete="off"/>
          </div>
        </div>
        <div class="item flex-view" style="max-width: 400px; min-width: 250px;">
          <div class="label">确认新密码</div>
          <div class="right-box">
            <a-input-password placeholder="重复输入密码" v-model:value="password.new2" autocomplete="off"/>
          </div>
        </div>
        </form>
        <button class="save mg" @click="modifyPassword">修改密码</button>
        <button class="save mg" @click="showDelete=true" style="background: red">注销账号</button>
        <a-modal v-model:open="showDelete" title="确认操作" :confirm-loading="confirmLoading" :closable='false' @ok="handleDelete">
          <p>确定要注销账号吗，这个操作不可撤销！您的数据将从数据库中永久删除！</p>
        </a-modal>
      </div>
    </div>
    </a-spin>
  </div>
</template>

<script setup>
import {message} from "ant-design-vue";
import {
  userDetailApi,
  userUpdateApi,
  userPasswordApi,
  userDeleteApi
} from '/@/api/index/user'
import {BASE_URL, USER_AVATAR} from "/@/store/constants";
import {useAppStore, useUserStore} from "/@/store";
import AvatarIcon from '/@/assets/images/avatar.jpg'
import {openNotification} from "/@/utils/notice";
// console.log("visit id=", useRoute().query.id.trim())

const router = useRouter();
const userStore = useUserStore();
const appStore = useAppStore();

const confirmLoading = ref(false);
const open = ref(false);
const showDelete = ref(false)

let loading = ref(false)
let tData = reactive({
  form:{
    avatar: undefined,
    avatarFile: undefined,
    nickname: undefined,
    email: undefined,
    mobile: undefined,
    description: undefined,
  }
})
const password = reactive({})

onMounted(() => {
  /* 判断当前浏览的用户是谁，无 query 默认跳自己，query 不是自己会转到该用户的公开界面 */
  if (useRoute().query.id) {
    if (useRoute().query.id.trim() !== String(userStore.user_id)) {
      router.push({name: 'wishThingView', query: {id: useRoute().query.id.trim()}}); /* TODO: router.go(-1) 时有 bug，回不到上一页 */
    }
  } else {
    router.push({name: 'userInfoEditView', query: {id: userStore.user_id}});
  }
  appStore.setViewId(userStore.user_id);
  getUserInfo()
})

const handleDelete = async () => {
  confirmLoading.value = true;
  await userDeleteApi({user_id: userStore.user_id}).then(res => {
    openNotification({
      type: 'success',
      message: '您已成功注销!',
      description: ''
    })
    userStore.delete()
  }).catch(err => {
    console.log(err)
    openNotification({
      type: 'error',
      message: 'Oops!',
      description: err.response.data.detail
    });
    confirmLoading.value = false;
    showDelete.value = false;
  })
  confirmLoading.value = false;
  showDelete.value = false;
};
const beforeUpload =(file)=> {
  // 改文件名
  const fileName = new Date().getTime().toString() + '.' + file.type.substring(6)
  const copyFile = new File([file], fileName)
  console.log(copyFile)
  tData.form.avatarFile = copyFile
  return false
}

const getUserInfo = () => {
  loading.value = true
  let userId = userStore.user_id
  userDetailApi({user_id: userId}).then(res => {
    tData.form = res.data
    console.log(tData.form)
    if (tData.form.avatar) {
      userStore.user_avatar = tData.form.avatar
      appStore.view_user_avatar = tData.form.avatar
      localStorage.setItem(USER_AVATAR, userStore.user_avatar)
    }
    loading.value = false
  }).catch(err => {
    console.log(err)
    loading.value = false
  })
}
const submit =()=> {
  let formData = new FormData()
  let userId = userStore.user_id
  if (tData.form.avatarFile) {
    formData.append('avatar', tData.form.avatarFile)
  }
  if (tData.form.nickname) {
    formData.append('nickname', tData.form.nickname)
  }
  if (tData.form.email) {
    formData.append('email', tData.form.email)
  }
  if (tData.form.mobile) {
    formData.append('phone', tData.form.mobile)
  }
  if (tData.form.description) {
    formData.append('description', tData.form.description)
  }
  formData.append('username', userStore.user_name)
  console.log(formData)
  userUpdateApi({user_id: userId}, formData).then(res => {
    openNotification({
      type: 'success',
      message: '用户信息修改成功！',
      description: ''
    })
    getUserInfo()
  }).catch(err => {
    openNotification({
      type: 'error',
      message: '用户信息修改失败',
      description: err.response.data.detail
    })
    console.log(err)
  })
}

const modifyPassword = () => {
  if (!(password.old) || !(password.new1) || !(password.new2)) {
    openNotification({
      type: 'error',
      message: '修改密码失败',
      description: '请输入字段！'
    })
  } else if (password.new1 !== password.new2) {
    openNotification({
      type: 'error',
      message: '修改密码失败',
      description: '两次输入的密码不一致！'
    })
  } else {
    userPasswordApi({user_id: userStore.user_id}, {old_password: password.old, new_password1: password.new1, new_password2: password.new2}).then(res => {
      console.log(res)
      openNotification({
        type: 'success',
        message: '修改密码成功！',
        description: res.msg
      });
      userStore.setPassword(password.new1);
        }
    ).catch(err => {
      console.log(err)
      let loger = '';
      if (err.response.data.data.old_password) {
        loger = err.response.data.data.old_password[0];
      } else if (err.response.data.data.new_password1) {
        loger = err.response.data.data.new_password1[0];
      } else if (err.response.data.data.new_password2) {
        loger = err.response.data.data.new_password2[0];
        console.log(loger)
      } else {
        loger = err.response.data.detail;
      }
      openNotification({
        type: 'error',
        message: '修改密码失败',
        description: loger
      });
    })
  }
}
</script>

<style scoped lang="less">
input, textarea {
  border-style: none;
  outline: none;
  margin: 0;
  padding: 0;
}

.flex-view {
  display: -webkit-box;
  display: -ms-flexbox;
  display: flex;
}

.content-list {
  -webkit-box-flex: 1;
  -ms-flex: 1;
  flex: 1;

  .list-title {
    color: #152844;
    font-weight: 600;
    font-size: 18px;
    line-height: 48px;
    height: 48px;
    margin-bottom: 4px;
    border-bottom: 1px solid #cedce4;
  }

  .edit-view {
    .item {
      -webkit-box-align: center;
      -ms-flex-align: center;
      align-items: center;
      margin: 24px 0;

      .label {
        width: 100px;
        color: #152844;
        font-weight: 600;
        font-size: 14px;
      }

      .right-box {
        -webkit-box-flex: 1;
        -ms-flex: 1;
        flex: 1;
      }

      .avatar {
        width: 64px;
        height: 64px;
        border-radius: 50%;
        margin-right: 16px;
      }

      .change-tips {
        -webkit-box-align: center;
        -ms-flex-align: center;
        align-items: center;
        -ms-flex-wrap: wrap;
        flex-wrap: wrap;
      }

      label {
        color: #4684e2;
        font-size: 14px;
        line-height: 22px;
        height: 22px;
        cursor: pointer;
        width: 100px;
        display: block;
      }

      .tip {
        color: #6f6f6f;
        font-size: 14px;
        height: 22px;
        line-height: 22px;
        margin: 0;
        width: 100%;
      }

      .right-box {
        -webkit-box-flex: 1;
        -ms-flex: 1;
        flex: 1;
      }

      .input-dom {
        width: 400px;
      }

      .input-dom {
        background: #f8fafb;
        border-radius: 4px;
        height: 40px;
        line-height: 40px;
        font-size: 14px;
        color: #152844;
        padding: 0 12px;
      }

      .tip {
        font-size: 12px;
        line-height: 16px;
        color: #6f6f6f;
        height: 16px;
        margin-top: 4px;
      }

      .intro {
        resize: none;
        background: #f8fafb;
        width: 100%;
        padding: 8px 12px;
        height: 82px;
        line-height: 22px;
        font-size: 14px;
        color: #152844;
      }
    }

    .save {
      background: #4684e2;
      border-radius: 32px;
      width: 96px;
      height: 32px;
      line-height: 32px;
      font-size: 14px;
      color: #fff;
      border: none;
      outline: none;
      cursor: pointer;
    }

    .mg {
      margin-left: 100px;
    }
  }
}

</style>
