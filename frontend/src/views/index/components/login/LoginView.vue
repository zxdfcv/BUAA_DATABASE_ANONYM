<template>
  <a-spin :spinning="loading">
  <el-card :bordered="false" shadow="hover" style="top: 5%; left: auto; background-color: #f9f9f9; height: auto">
    <div style="text-align: left;font-size: 14px;margin-bottom: 30px"><b>BUAA Salty Fish Platform</b></div>
    <div class="login">
      <a-form
          @submit.prevent="doLogin"
          :rules="rules"
          :model="formState"
          class="login-form sign-in-form"
      >
        <a-form-item
            label="Username"
            name="username"
        >
          <a-input v-model:value="formState.username"/>
        </a-form-item>

        <a-form-item
            label="Password"
            name="password"
        >
          <a-input-password v-model:value="formState.password"/>
        </a-form-item>
        <a-col class="gutter-row" :span="8" style="margin-top: 10px">
            <a-form-item name="remember">
              <a-checkbox v-model:checked="formState.remember">Remember me</a-checkbox>
            </a-form-item>
          </a-col>

        <!--        <div>-->
        <!--          <a-alert type="error" :closable="true" v-show="error" :message="error" showIcon-->
        <!--                   style="margin-bottom: 24px;"></a-alert>-->
        <!--          <a-form-item-->
        <!--              fieldDecoratorId="name"-->
        <!--              :fieldDecoratorOptions="{rules: [{ required: true, message: '请输入账户名', whitespace: true}]}">-->
        <!--            <a-input size="large">-->
        <!--              <a-icon slot="prefix" type="user"></a-icon>-->
        <!--            </a-input>-->
        <!--          </a-form-item>-->
        <!--          <a-form-item-->
        <!--              fieldDecoratorId="password"-->
        <!--              :fieldDecoratorOptions="{rules: [{ required: true, message: '请输入密码', whitespace: true}]}">-->
        <!--            <a-input size="large" type="password">-->
        <!--              <a-icon slot="prefix" type="lock"></a-icon>-->
        <!--            </a-input>-->
        <!--          </a-form-item>-->
        <a-form-item>
          <a-button :loading="loading" style="width: 100%; margin-top: 4px" size="large" htmlType="submit"
                    type="primary">
            Login now
          </a-button>
        </a-form-item>
        <div style="float: right">
          Or... <a @click="$emit('toRegister')">Register here</a>
        </div>
      </a-form>
    </div>
  </el-card>
</a-spin>
</template>

<script setup lang="ts">

import router from '/@/router';
import { watch } from 'vue';
import { useUserStore } from '/@/store';
import { openNotification } from '/@/utils/notice'

const userStore = useUserStore();
const props = defineProps(['display']);

const rules = {
  username: [
    {required: true, message: 'Please input Activity name', trigger: 'change'},
    {min: 5, max: 15, message: 'Length should be 5 to 15', trigger: 'blur'},
  ],
  password: [
    {required: true, message: 'Please input password', trigger: 'change'},
    {min: 6, max: 16, message: 'Length should be 6 to 16', trigger: 'blur'}
  ]
};

const loading = ref(false);
const formState = reactive({
  username: '',
  password: '',
  remember: false
});


const fillUserInfo = () => {
  if (userStore.remember_me === true) {
    formState.username = userStore.user_name;
    formState.password = userStore.user_password;
    formState.remember = userStore.remember_me;
  }
};

const doLogin = () => {
  console.log(props.display);
  
  loading.value = true;
  userStore.login({
    username: formState.username,
    password: formState.password
  }).then(res => {
    loading.value = false;
    openNotification({
      type: 'success',
      message: '登录成功！',
      description: '你好，用户 ' + res.data.username + '！'
    })
    userStore.remember_me = formState.remember;
    userStore.user_password = formState.password;
    router.push({ name: 'portal' });
  }).catch(err => {
    console.log(err);
    loading.value = false;
    openNotification({
      type: 'error',
      message: 'Oops!',
      description: err.msg
    })
  });
}
watch(
  () => props.display,
  () => {
    console.log("filling");
    
    fillUserInfo();
  }
);

/* --------------- setup --------------- */
fillUserInfo();

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
