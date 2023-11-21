<template>
  <a-card :bordered="false" hoverable style="top: 5%; left: auto; background-color: #f9f9f9; height: auto">
    <div style="text-align: left;font-size: 14px;margin-bottom: 30px"><b>BUAA Salty Fish Platform</b></div>
    <div class="login">
      <a-form
          @submit.prevent="doRegister"
          :rules="rules"
          :model="formState"
          class="register-form sign-up-form"
      >
        <a-form-item
            label="Username"
            name="username"
            :rules="[{required: true, message: 'Please input username'},{min: 5, max: 15, message: 'Length should be 5 to 15'}]"
        >
          <a-input v-model:value="formState.username" autocomplete="off"/>
        </a-form-item>

        <a-form-item
            label="Password"
            name="password"
            :rules="[{required: true, message:'Please input password'},{min: 6, max: 16, message: 'Length should be 6 to 16' }]"
        >
          <a-input-password v-model:value="formState.password" autocomplete="off"/>
        </a-form-item>
        <a-form-item
            label="Repeat Password"
            name="repeatPassword"
            :rules="[{required: true, message:'Please repeat password'},{min: 6, max: 16, message: 'Length should be 6 to 16' },{ validator: this.handlePasswordCheck }]"
        >
          <a-input-password v-model:value="formState.repeatPassword" autocomplete="off"/>
        </a-form-item>
        <a-row :gutter="10" justify="start">

          <a-col class="gutter-row" :span="8" @click="refreshIdentifyCode">
            <s-identify :identifyCode="identifyCode"></s-identify>
          </a-col>
          <p style="margin-top: 5px">verifyCode:</p>
          <a-col class="gutter-row" :span="4" :offset="1">
            <a-input v-model:value="identifyCodeCheck"></a-input>
          </a-col>
        </a-row>

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
            Register now
          </a-button>
        </a-form-item>
        <div style="float: right">
          Have an account? <a @click="$emit('toLogin')">Login here</a>
        </div>
      </a-form>
    </div>
  </a-card>
</template>

<script>
import {mapMutations} from 'vuex'
import SIdentify from './SIdentify.vue'
// const ;
const rules = {};

export default {
  name: 'Register',
  components: {SIdentify},
  data() {
    return {
      loading: false,
      error: '',
      activeKey: '1',
      identifyCode: '',
      identifyCodeCheck: '',
      identifyCodes: '1234567890',
      formState: {
        username: '',
        password: '',
        repeatPassword: '',
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
    // 初始化验证码
    this.identifyCode = ''
    this.makeIdentifyCode(4)
  },
  methods: {
    handlePasswordCheck(rule, value, callback) {
      let password = this.formState['password']
      if (value && password && value.trim() !== password.trim()) {
        callback(new Error('Passwords have diff!'))
      }
      callback()
    },
    // 刷新验证码
    refreshIdentifyCode() {
      this.identifyCode = ''
      this.makeIdentifyCode(4)
    },
    // 生成4位数的随机验证码
    makeIdentifyCode(l) {
      for (let i = 0; i < l; i++) {
        this.identifyCode +=
            this.identifyCodes[this.randomNum(0, this.identifyCodes.length)]
      }
    },
    // 生成单个验证码
    randomNum(min, max) {
      return Math.floor(Math.random() * (max - min) + min)
    },
    doRegister() {
      console.log(this.formState)
      if (this.activeKey === '1') {
        if (this.identifyCodeCheck === '') {
          this.$notice.error('Error', 'input identify code please!')
          return false
        }
        if (this.identifyCodeCheck !== this.identifyCode) {
          this.$notice.error('Error', 'Check your input please!')
          this.identifyCodeCheck = ''
          this.refreshIdentifyCode()
          return false
        }
        // 用户名密码注册
        this.loading = true
        let username = this.formState['username']
        let password = this.formState['password']
        // TODO: api connection & information encoding
        this.$post('register', {
          username: username,
          password: password
        }).then((res) => {
          this.$notice.success("register successfully", "")
          let data = res.data.data
          // TODO: return data regulation
          this.saveLoginData(data)
          setTimeout(() => {
            this.loading = false
          }, 300)
          this.$emit('toLogin')
        }).catch((e) => {
          console.error(e)
          this.$notice.error(e.name, e.message)
          setTimeout(() => {
            this.loading = false
          }, 500)
          // TODO: cancel this line.
          let data = {
            "token": '114514',
            "expireTime": new Date().getTime() + 60000,
            "username":this.formState.username,
            "password":this.formState.password,
          }
          this.saveLoginData(data)
          console.log(data)
          this.$emit('toLogin')
        })
        // this.$post('login', {
        //   username: username,
        //   password: password
        // }).then((res) => {
        //   this.$notice.success("Login successfully", "")
        //   let data = res.data.data
        //   // TODO: return data regulation
        //   this.saveLoginData(data)
        //   setTimeout(() => {
        //     this.loading = false
        //   }, 1000)
        //   this.$router.push('/index')
        // }).catch((e) => {
        //   console.error(e)
        //   this.$notice.error(e.name, e.message)
        //   setTimeout(() => {
        //     this.loading = false
        //   }, 500)
        //   // TODO: cancel this line.
        //   let data = {
        //     "token": '114514',
        //     "EXPIRE_TIME": new Date().getTime() + 60000
        //   }
        //   console.log(data)
        //   this.saveLoginData(data)
        //   this.$router.push('/index')
        // })
      }
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
      this.setExpireTime(data.expireTime)
      this.setUser(this.formState.username)
      this.setPassword(this.formState.password)
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
