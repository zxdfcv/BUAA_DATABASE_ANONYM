<template>
  <a-card :bordered="false" hoverable style="top: 5%; left: auto; background-color: #f9f9f9; height: auto">
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
  </a-card>
</template>

<script>
import {mapMutations} from 'vuex'
import SIdentify from './SIdentify.vue'
import ls from "../../utils/localstorage.js";

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

export default {
  name: 'Login',
  components: {SIdentify},
  props: ['display'],
  data() {
    return {
      loading: false,
      error: '',
      formState: {
        username: '',
        password: '',
      },
      rules: Object.freeze(rules)
    }
  },
  computed: {
    systemName() {
      return this.$store.state.setting.systemName
    },
    copyright() {
      return this.$store.state.setting.copyright
    }
  },
  created() {
    // this.$db.clear()
    this.$router.options.routes = []
  },
  mounted() {
    this.fillUserInfo()
  },
  watch: {
    display: function () {
      this.fillUserInfo()
    }
  },
  methods: {
    fillUserInfo() {
      console.log(JSON.stringify(ls.get('PASSWORD')))
      if (JSON.stringify(ls.get('USERNAME')) !== '{}') {
        console.log("fill")
        this.formState.username = ls.get('USERNAME')
        this.formState.remember = true
      }
      if (JSON.stringify(ls.get('PASSWORD')) !== '{}') {
        this.formState.password = ls.get('PASSWORD')
      }
    },
    doLogin() {
      console.log(this.formState)
       // 用户名密码登录
      this.loading = true
      let username = this.formState['username']
      let password = this.formState['password']
      this.$post('login', {
        username: username,
        password: password
      }).then((res) => {
        this.$notice.success("Login successfully", "")
        let data = res.data.data
        // TODO: return data regulation
        this.saveLoginData(data)
        setTimeout(() => {
          this.loading = false
        }, 1000)
        this.$router.push('/index')
      }).catch((e) => {
        console.error(e)
        this.$notice.error(e.name, e.message)
        setTimeout(() => {
          this.loading = false
        }, 500)
        // TODO: cancel this line.
        let data = {
          "token": '114514',
          "EXPIRE_TIME": new Date().getTime() + 30000
        }
        console.log(data)
        this.saveLoginData(data)
        this.$router.push('/index')
      })
    },
    register() {
      this.$router.push('/register')
    },
    ...mapMutations({
      setToken: 'account/setToken',
      setExpireTime: 'account/setExpireTime',
      setPermissions: 'account/setPermissions',
      setRoles: 'account/setRoles',
      setUser: 'account/setUser',
      setPassword: 'account/setPassword',
      setTheme: 'setting/setTheme',
      setLayout: 'setting/setLayout',
      setMultipage: 'setting/setMultipage',
      fixSiderbar: 'setting/fixSiderbar',
      fixHeader: 'setting/fixHeader',
      setColor: 'setting/setColor'
    }),
    saveLoginData(data) {
      this.setToken(data.token)
      this.setExpireTime(data.EXPIRE_TIME)
      if (this.formState.remember) {
        this.setUser(this.formState.username)
        this.setPassword(this.formState.password)
      } else {
        ls.remove('USERNAME')
        ls.remove('PASSWORD')
      }
    }
  }
}
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
