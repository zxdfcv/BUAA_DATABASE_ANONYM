<!--<template>-->
<!--  <a-card :bordered="false" hoverable style="top: 15%; left: 50%; background-color: #f9f9f9; height: auto">-->
<!--    <div style="text-align: left;font-size: 14px;margin-bottom: 30px"><b>BUAA Salty Fish Platform</b></div>-->
<!--    <div class="register">-->
<!--      <a-form-->
<!--          ref="formRef"-->
<!--          name="custom-validation"-->
<!--          :model="formState"-->
<!--          :rules="rules"-->
<!--          @submit.prevent="doRegister"-->
<!--      >-->
<!--        <a-form-item label="Username" name="username">-->
<!--          <a-input v-model:value="formState.username" autocomplete="off"></a-input>-->
<!--        </a-form-item>-->
<!--        <a-form-item has-feedback label="Password" name="pass">-->
<!--          <a-input v-model:value="formState.password" type="password" autocomplete="off"/>-->
<!--        </a-form-item>-->
<!--        <a-form-item has-feedback label="Confirm" name="checkPass">-->
<!--          <a-input v-model:value="formState.checkPassword" type="password" autocomplete="off"/>-->
<!--        </a-form-item>-->
<!--        <a-form-item :wrapper-col="{ span: 14, offset: 4 }">-->
<!--          <a-button type="primary" html-type="submit">Submit</a-button>-->
<!--        </a-form-item>-->
<!--      </a-form>-->
<!--    </div>-->
<!--  </a-card>-->
<!--</template>-->

<!--<script>-->
<!--import {mapMutations} from 'vuex'-->
<!--import SIdentify from './SIdentify.vue'-->

<!--const rules = {-->
<!--  username: [-->
<!--    {required: true, message: 'Please input Activity name', trigger: 'change'},-->
<!--    {min: 5, max: 15, message: 'Length should be 5 to 15', trigger: 'blur'},-->
<!--  ],-->
<!--  password: [-->
<!--    {required: true, message: 'Please input password', trigger: 'change'},-->
<!--    {min: 6, max: 16, message: 'Length should be 6 to 16', trigger: 'blur'}-->
<!--  ]-->
<!--};-->

<!--export default {-->
<!--  name: 'Register',-->
<!--  components: {SIdentify},-->
<!--  data() {-->
<!--    return {-->
<!--      loading: false,-->
<!--      error: '',-->
<!--      activeKey: '1',-->
<!--      identifyCode: '',-->
<!--      identifyCodeCheck: '',-->
<!--      identifyCodes: '1234567890',-->
<!--      formState: {-->
<!--        username: '',-->
<!--        password: '',-->
<!--        checkPassword: ''-->
<!--      },-->
<!--      rules: Object.freeze(rules)-->
<!--    }-->
<!--  },-->
<!--  computed: {-->
<!--    systemName() {-->
<!--      return this.$store.state.setting.systemName-->
<!--    },-->
<!--    copyright() {-->
<!--      return this.$store.state.setting.copyright-->
<!--    }-->
<!--  },-->
<!--  created() {-->
<!--    this.$db.clear()-->
<!--    this.$router.options.routes = []-->
<!--    // 初始化验证码-->
<!--    this.identifyCode = ''-->
<!--    this.makeIdentifyCode(4)-->
<!--  },-->
<!--  methods: {-->
<!--    // 刷新验证码-->
<!--    refreshIdentifyCode() {-->
<!--      this.identifyCode = ''-->
<!--      this.makeIdentifyCode(4)-->
<!--    },-->
<!--    // 生成4位数的随机验证码-->
<!--    makeIdentifyCode(l) {-->
<!--      for (let i = 0; i < l; i++) {-->
<!--        this.identifyCode +=-->
<!--            this.identifyCodes[this.randomNum(0, this.identifyCodes.length)]-->
<!--      }-->
<!--    },-->
<!--    // 生成单个验证码-->
<!--    randomNum(min, max) {-->
<!--      return Math.floor(Math.random() * (max - min) + min)-->
<!--    },-->
<!--    doRegister() {-->
<!--      console.log(this.formState)-->
<!--      if (this.activeKey === '1') {-->
<!--        if (this.identifyCodeCheck === '') {-->
<!--          // this.$notice.error('Error', 'input identify code please!')-->
<!--          return false-->
<!--        }-->
<!--        if (this.identifyCodeCheck !== this.identifyCode) {-->
<!--          // this.$notice.error('Error', 'identify code is not correct!')-->
<!--          this.identifyCodeCheck = ''-->
<!--          this.refreshIdentifyCode()-->
<!--          return false-->
<!--        }-->
<!--        // 用户名密码登录-->
<!--        this.loading = true-->
<!--        let username = this.formState['username']-->
<!--        let password = this.formState['password']-->
<!--        // TODO: api connection & information encoding-->
<!--        this.$post('login', {-->
<!--          username: username,-->
<!--          password: password-->
<!--        }).then((res) => {-->
<!--          this.$notice.success("Login successfully", "")-->
<!--          let data = res.data.data-->
<!--          // TODO: return data regulation-->
<!--          this.saveLoginData(data)-->
<!--          setTimeout(() => {-->
<!--            this.loading = false-->
<!--          }, 1000)-->
<!--          this.$router.push('/index')-->
<!--        }).catch((e) => {-->
<!--          console.error(e)-->
<!--          this.$notice.error(e.name, e.message)-->
<!--          setTimeout(() => {-->
<!--            this.loading = false-->
<!--          }, 500)-->
<!--          // TODO: cancel this line.-->
<!--          let data = {-->
<!--            "token": '114514',-->
<!--            "EXPIRE_TIME": new Date().getTime() + 60000-->
<!--          }-->
<!--          console.log(data)-->
<!--          this.saveLoginData(data)-->
<!--          this.$router.push('/index')-->
<!--        })-->
<!--      }-->
<!--    },-->
<!--    register() {-->
<!--      this.$router.push('/register')-->
<!--    },-->
<!--    ...mapMutations({-->
<!--      setToken: 'account/setToken',-->
<!--      setExpireTime: 'account/setExpireTime',-->
<!--      setPermissions: 'account/setPermissions',-->
<!--      setRoles: 'account/setRoles',-->
<!--      setUser: 'account/setUser',-->
<!--      setTheme: 'setting/setTheme',-->
<!--      setLayout: 'setting/setLayout',-->
<!--      setMultipage: 'setting/setMultipage',-->
<!--      fixSiderbar: 'setting/fixSiderbar',-->
<!--      fixHeader: 'setting/fixHeader',-->
<!--      setColor: 'setting/setColor'-->
<!--    }),-->
<!--    saveLoginData(data) {-->
<!--      this.setToken(data.token)-->
<!--      this.setExpireTime(data.EXPIRE_TIME)-->
<!--    }-->
<!--  }-->
<!--}-->
<!--</script>-->

<!--<style lang="less" scoped>-->
<!--.register {-->
<!--  .icon {-->
<!--    font-size: 24px;-->
<!--    color: rgba(0, 0, 0, 0.2);-->
<!--    margin-left: 16px;-->
<!--    vertical-align: middle;-->
<!--    cursor: pointer;-->
<!--    transition: color 0.3s;-->

<!--    &:hover {-->
<!--      color: #1890ff;-->
<!--    }-->
<!--  }-->
<!--}-->
<!--</style>-->


<template>
  <div class="container" :class="{ 'sign-up-mode': signUpMode }" style="width: 100%">
    <!-- form表单容器 -->
    <div class="form-container">
      <div class="signin-signup">
        <!-- 登录 -->
        <h1>{{title}}</h1>
        <LoginView
            v-show="login"
            @toRegister="signUpMode = !signUpMode"
            :display="login"
            style="margin: 15px; width: 85%;"
            class="content"
        />
        <!-- 注册 -->
        <RegisterView
            v-show="!login"
            @toLogin="signUpMode = !signUpMode"
            style="margin: 15px; width: 85%;"
            class="content"
        />
      </div>
    </div>
    <!-- 左右切换动画 -->
    <div class="panels-container">
      <div class="panel left-panel">
        <div class="content">
          <h3>BUAA Salty Fish Platform</h3>
          <p>只因你太美</p>
          <button @click="signUpMode = !signUpMode" class="btn transparent">
            注册
          </button>
        </div>
        <!-- <img src="@/assets" alt=""> -->
      </div>
      <div class="panel right-panel">
        <div class="content">
          <h3>Merrily,merrily,merrily,merrily,</h3>
          <p>Life is but a dream</p>
          <button @click="signUpMode = !signUpMode" class="btn transparent">
            登录
          </button>
        </div>
        <!-- <img src="@/assets" alt=""> -->
      </div>
    </div>
  </div>
</template>

<script>
import {ref} from 'vue'
import LoginView from "./LoginView.vue"
import RegisterView from "./RegisterView.vue";

export default {
  name: 'LoginRegister',
  components: {LoginView, RegisterView},
  data() {
    return {
      login: true,
      signUpMode: false,
      title: '登录'
    }
  },
  watch: {
    signUpMode: function () {
      // console.log(newV)
      setTimeout(() => {
        if (this.title === '登录') {
          this.title = '注册'
        } else {
          this.title = '登录'
        }
        this.login = !this.login
      }, 1100)
    }
  }
}
</script>
<style scoped>
.container {
  position: absolute;
  width: 100%;
  min-height: 100vh;
  background-color: #fff;
  overflow: hidden;
}

.form-container {
  position: absolute;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
}

.signin-signup {
  position: relative;
  top: 50%;
  left: 75%;
  transform: translate(-50%, -50%);
  width: 44%;
  transition: 1s 0.7s ease-in-out;
  display: grid;
  grid-template-columns: 1fr;
  z-index: 5;
}

/* 左右切换动画 */
.social-text {
  padding: 0.7rem 0;
  font-size: 1rem;
}

.social-media {
  display: flex;
  justify-content: center;
}

.social-icon {
  height: 46px;
  width: 46px;
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 0 0.45rem;
  color: #333;
  border-radius: 50%;
  border: 1px solid #333;
  text-decoration: none;
  font-size: 1.1rem;
  transition: 0.3s;
}

.social-icon:hover {
  color: #4481eb;
  border-color: #4481eb;
}

.btn {
  width: 150px;
  background-color: #5995fd;
  border: none;
  outline: none;
  height: 49px;
  border-radius: 49px;
  color: #fff;
  text-transform: uppercase;
  font-weight: 600;
  margin: 10px 0;
  cursor: pointer;
  transition: 0.5s;
}

.btn:hover {
  background-color: #4d84e2;
}

.panels-container {
  position: absolute;
  height: 100%;
  width: 100%;
  top: 0;
  left: 0;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
}

.container:before {
  content: '';
  position: absolute;
  height: 2000px;
  width: 2000px;
  top: -10%;
  right: 48%;
  transform: translateY(-50%);
  background-image: linear-gradient(-45deg, #4481eb 0%, #04befe 100%);
  transition: 1.8s ease-in-out;
  border-radius: 50%;
  z-index: 6;
}

.image {
  width: 100%;
  transition: transform 1.1s ease-in-out;
  transition-delay: 0.4s;
}

.panel {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  justify-content: space-around;
  text-align: center;
  z-index: 6;
}

.left-panel {
  pointer-events: all;
  padding: 3rem 17% 2rem 12%;
}

.right-panel {
  pointer-events: none;
  padding: 3rem 12% 2rem 17%;
}

.panel .content {
  color: #fff;
  transition: transform 0.9s ease-in-out;
  transition-delay: 1.6s;
}

.panel h3 {
  font-weight: 600;
  line-height: 1;
  font-size: 1.5rem;
}

.panel p {
  font-size: 0.95rem;
  padding: 0.7rem 0;
}

.btn.transparent {
  margin: 0;
  background: none;
  border: 2px solid #fff;
  width: 130px;
  height: 41px;
  font-weight: 600;
  font-size: 0.8rem;
}

.right-panel .image,
.right-panel .content {
  transform: translateX(800px);
}

/* ANIMATION */

.container.sign-up-mode:before {
  transform: translate(100%, -50%);
  right: 52%;
}

.container.sign-up-mode .left-panel .image,
.container.sign-up-mode .left-panel .content {
  transform: translateX(-800px);
}

.container.sign-up-mode .signin-signup {
  left: 25%;
}

.container.sign-up-mode .sign-up-form {
  opacity: 1;
  z-index: 2;
}

.container.sign-up-mode .sign-in-form {
  opacity: 0;
  z-index: 1;
}

.container.sign-up-mode .right-panel .image,
.container.sign-up-mode .right-panel .content {
  transform: translateX(0%);
}

.container.sign-up-mode .left-panel {
  pointer-events: none;
}

.container.sign-up-mode .right-panel {
  pointer-events: all;
}

@media (max-width: 870px) {
  .container {
    min-height: 800px;
    height: 100vh;
  }

  .signin-signup {
    width: 100%;
    top: 95%;
    transform: translate(-50%, -100%);
    transition: 1s 0.8s ease-in-out;
  }

  .signin-signup,
  .container.sign-up-mode .signin-signup {
    left: 50%;
  }

  .panels-container {
    grid-template-columns: 1fr;
    grid-template-rows: 1fr 2fr 1fr;
  }

  .panel {
    flex-direction: row;
    justify-content: space-around;
    align-items: center;
    padding: 2.5rem 8%;
    grid-column: 1 / 2;
  }

  .right-panel {
    grid-row: 3 / 4;
  }

  .left-panel {
    grid-row: 1 / 2;
  }

  .image {
    width: 200px;
    transition: transform 0.9s ease-in-out;
    transition-delay: 0.6s;
  }

  .panel .content {
    padding-right: 15%;
    transition: transform 0.9s ease-in-out;
    transition-delay: 0.3s;
  }

  .panel h3 {
    font-size: 1.2rem;
  }

  .panel p {
    font-size: 0.7rem;
    padding: 0.5rem 0;
  }

  .btn.transparent {
    width: 110px;
    height: 35px;
    font-size: 0.7rem;
  }

  .container:before {
    width: 1500px;
    height: 1500px;
    transform: translateX(-50%);
    left: 30%;
    bottom: 68%;
    right: initial;
    top: initial;
    transition: 2s ease-in-out;
  }

  .container.sign-up-mode:before {
    transform: translate(-50%, 100%);
    bottom: 32%;
    right: initial;
  }

  .container.sign-up-mode .left-panel .image,
  .container.sign-up-mode .left-panel .content {
    transform: translateY(-300px);
  }

  .container.sign-up-mode .right-panel .image,
  .container.sign-up-mode .right-panel .content {
    transform: translateY(0px);
  }

  .right-panel .image,
  .right-panel .content {
    transform: translateY(300px);
  }

  .container.sign-up-mode .signin-signup {
    top: 5%;
    transform: translate(-50%, 0);
  }
}

@media (max-width: 570px) {
  .sign-in-form .sign-up-form {
    padding: 0 1.5rem;
  }

  .image {
    display: none;
  }

  .panel .content {
    padding: 0.5rem 1rem;
  }

  .container {
    padding: 1.5rem;
  }

  .container:before {
    bottom: 72%;
    left: 50%;
  }

  .container.sign-up-mode:before {
    bottom: 28%;
    left: 50%;
  }
}

/* 控制login & register显示 */
.sign-in-form .sign-up-form {
  padding: 0rem 5rem;
  transition: all 0.2s 0.7s;
  overflow: hidden;
}

.sign-in-form {
  z-index: 2;
}

.sign-up-form {
  opacity: 0;
  z-index: 1;
}

/* register */
.LoginView,
.RegisterView {
  margin-top: 20px;
  background-color: #fff;
  padding: 20px 40px 20px 20px;
  border-radius: 5px;
  box-shadow: 0px 5px 10px #cccc;
}

.submit-btn {
  width: 100%;
}

.tiparea {
  text-align: right;
  font-size: 12px;
  color: #333;
  width: 100%;
}

.tiparea a {
  color: #409eff;
}
</style>

