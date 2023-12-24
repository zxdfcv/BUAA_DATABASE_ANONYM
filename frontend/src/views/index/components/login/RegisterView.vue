<template>
  <a-spin :spinning="loading">
    <el-card :bordered="false" shadow="hover" style="top: 5%; left: auto; background-color: #f9f9f9; height: auto">
      <div style="text-align: left;font-size: 14px;margin-bottom: 30px">
        <b>北航二手交易平台</b>
      </div>
      <div class="login">
        <a-form @submit.prevent="doRegister" :rules="rules" :model="formState" class="register-form sign-up-form">
          <a-form-item label="用户名" name="username"
            :rules="[{ required: true, message: 'Please input username' }, { min: 5, max: 15, message: '长度需要介于 5~15 个字符' }]">
            <a-input v-model:value="formState.username" autocomplete="off" />
          </a-form-item>

          <a-form-item label="密码" name="password"
            :rules="[{ required: true, message: 'Please input password' }, { min: 6, max: 16, message: '长度需要介于 6~16 个字符' }, { validator: handlePassword }]">
            <a-input-password v-model:value="formState.password" autocomplete="off" />
          </a-form-item>
          <a-form-item label="重复密码" name="confirm_password"
            :rules="[{ required: true, message: 'Please repeat password' }, { min: 6, max: 16, message: '长度需要介于 6~16 个字符' }, { validator: handlePasswordCheck }]">
            <a-input-password v-model:value="formState.confirm_password" autocomplete="off" />
          </a-form-item>
          <a-form-item label="注册邮箱" name="email" :rules="[{ required: true, message: 'Please input email' }, {
            pattern: /^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$/,
            message: '无效的邮箱格式'
          }]">
            <a-input v-model:value="formState.email" autocomplete="off" />
          </a-form-item>
          <a-row :gutter="10" justify="start">

            <a-col class="gutter-row" :span="8" @click="refreshIdentifyCode">
              <s-identify :identifyCode="identifyCode"></s-identify>
            </a-col>
            <p style="margin-top: 5px">验证码:</p>
            <a-col class="gutter-row" :span="4" :offset="1">
              <a-input v-model:value="identifyCodeCheck"></a-input>
            </a-col>
          </a-row>
          <a-form-item>
            <a-button :loading="loading" style="width: 100%; margin-top: 4px" size="large" htmlType="submit"
              type="primary">
              注册
            </a-button>
          </a-form-item>
          <div style="float: right">
            已有账号？ <a @click="$emit('toLogin')">去登陆</a>
          </div>
        </a-form>
      </div>
    </el-card>
  </a-spin>
</template>

<script setup lang="ts">

import SIdentify from './SIdentify.vue';
import { useUserStore } from '/@/store';

import { openNotification } from '/@/utils/notice';
import { defineEmits } from 'vue';

const userStore = useUserStore();
const emits = defineEmits(['toLogin']);


const loading = ref(false);

const rules = Object.freeze({});
const identifyCodes = '1234567890';
const identifyCode = ref('');
const identifyCodeCheck = ref('');

const formState = reactive({
  username: '',
  password: '',
  confirm_password: '',
  email: ''
});



const randomNum = (min, max) => {
  return Math.floor(Math.random() * (max - min) + min);
};

const makeIdentifyCode = (l) => {
  for (let i = 0; i < l; i++) {
    identifyCode.value += identifyCodes[randomNum(0, identifyCodes.length)]
  }
};

const refreshIdentifyCode = () => {
  identifyCode.value = ''
  makeIdentifyCode(4)
};

const handlePassword = (rule, value, callback) => {
  if (!/(?=.*[0-9])(?=.*[a-zA-Z])/.test(value)) {
    callback('密码必须包含数字和字母');
    return;
  }
  callback();
};

const handlePasswordCheck = (rule, value, callback) => {
  let password = formState['password']
  if (value && password && value.trim() !== password.trim()) {
    callback(new Error('两次输入的密码不一致'))
  }
  callback()
};

const doRegister = () => {
  console.log(formState);
  if (identifyCodeCheck.value === '') {
    openNotification({
      message: 'Error',
      description: 'Please input identify code.',
      type: 'error'
    });
    return false;
  } else if (identifyCodeCheck.value !== identifyCode.value) {
    openNotification({
      message: 'Error',
      description: 'Identify code error.',
      type: 'error'
    });
    identifyCode.value = '';
    refreshIdentifyCode();
    return false;
  }
  /* ---------- start register here ---------- */
  loading.value = true;
  userStore.register({
    username: formState.username,
    password: formState.password,
    confirm_password: formState.confirm_password,
    email: formState.email
  }).then(res => {
    loading.value = false;
    openNotification({
      type: 'success',
      message: '注册成功！',
      description: '用户 ' + res.data.user.username + ' 创建成功！'
    })
    userStore.remember_me = true;
    emits('toLogin');
  }).catch(err => {
    console.log(err);
    loading.value = false;
    openNotification({
      type: 'error',
      message: 'Oops!',
      description: err.response.data.msg
    });
  });
}

/* --------------- setup --------------- */
identifyCode.value = '';
makeIdentifyCode(4);

</script>

<style lang="less" scoped>
.login {
  .icon {
    font-size: 24px;
    color: rgba(0, 0, 0, 0.2);
    margin-left: 16px;
    vertical-align: middle;
    cursor: pointer;
    transition: color 0.3s;

    &:hover {
      color: #1890ff;
    }
  }
}
</style>
