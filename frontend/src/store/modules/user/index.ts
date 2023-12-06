import { defineStore } from 'pinia';
import { loginApi as adminLogin, userRegisterApi as adminRegister} from '/@/api/admin/user';
import { userLoginApi, userRegisterApi } from '/@/api/index/user';
import { UserState } from './types';
import {
  USER_ID,
  USER_NAME,
  USER_ACCESS,
  USER_AVATAR,
  ADMIN_USER_ID,
  ADMIN_USER_NAME,
  ADMIN_USER_TOKEN,
  ADMIN_USER_AVATAR,
  USER_REFRESH,
  TOKEN_EXPIRE_TIME,
  EXPIRE_FRESH_HOUR
} from "/@/store/constants";

/* 对外使用 UserStore 创建的异步方法，UserStore 再去调用登录相关 Api */
export const useUserStore = defineStore('user', {
  state: (): UserState => ({
    user_id: undefined,
    user_name: undefined,
    user_access: undefined,
    user_avatar: undefined,
    user_refresh: undefined,
    user_password: undefined,
    token_expire_time: undefined,

    admin_user_id: undefined,
    admin_user_name: undefined,
    admin_user_token: undefined,
    admin_user_avatar: undefined,

    remember_me: undefined,
    is_admin: undefined,
  }),
  getters: {},
  actions: {
    /* */
    async register(registerForm) {
      const result = await userRegisterApi(registerForm);
      console.log('Register results ==>', result.data);
      var res = result.data;
      if (result.code === 0) {
        this.$patch((state) => {
          state.user_refresh      = res.refresh
          state.user_access       = res.token
          state.token_expire_time = Date.parse(new Date(res.expire).toString())
          state.user_id           = res.user.id
          state.user_name         = res.user.username
          console.log('Storage state ==> ', state)
        });
      }
      return result;
    },

    /* 登录操作 */
    async login(loginForm) {
      var admin = loginForm;
      var result;
      admin['type'] = 1;
try {
  const res1 = await userLoginApi(admin);
  console.log(res1);
  if (res1.code === 0) {
    const res = res1.data
    this.$patch((state) => {
      this.user_refresh = res.refresh
      this.user_access = res.token
      this.user_id = res.id
      this.user_name = res.username
      this.token_expire_time = Date.parse(new Date(res.expire).toString())
      this.is_admin = true;
      /* TODO: email, phone 待处理 */
      console.log('Storage state ==> ', this)
    });
    result = res1;
  }
} catch (e) {
  delete admin.type;
  const res2 = await userLoginApi(admin);
  console.log(res2);
  if (res2.code === 0) {
    const res = res2.data
    this.$patch((state) => {
      this.user_refresh = res.refresh
      this.user_access = res.token
      this.user_id = res.id
      this.user_name = res.username
      this.token_expire_time = Date.parse(new Date(res.expire).toString())
      this.is_admin = false;
      /* TODO: email, phone 待处理 */
      console.log('Storage state ==> ', this)
    });
    result = res2;
  }
}




      return result;
    },

    /* 退出登录操作 */
    async logout() {
      // await userLogout();
      this.$patch((state) => {
        state.user_id           = undefined
        state.user_access       = undefined
        state.user_refresh      = undefined
        state.token_expire_time = undefined
        state.user_avatar       = undefined
        state.is_admin          = undefined
        if (state.remember_me !== true) {
          state.user_name         = undefined
          state.user_password     = undefined
          state.remember_me       = undefined
        }
      })
      localStorage.removeItem("user_avatar")
    },

    delete() {
      // await userLogout();
      this.$patch((state) => {
        state.user_id           = undefined
        state.user_access       = undefined
        state.user_refresh      = undefined
        state.token_expire_time = undefined
        state.user_name         = undefined
        state.user_password     = undefined
        state.remember_me       = undefined
        state.user_avatar       = undefined
        state.is_admin          = undefined
      })
      localStorage.removeItem("user_avatar")
    },

    /* TODO: 管理员登录/退出未操作 Pinia */
    // 管理员登录
    async adminLogin(loginForm) {
      const result = await adminLogin(loginForm);
      console.log('result==>', result)

      if(result.code === 0) {
        this.$patch((state)=>{
          state.admin_user_id = result.data.id
          state.admin_user_name = result.data.username
          state.admin_user_token = result.data.admin_token
          state.admin_user_avatar = result.data.avatar
          console.log('state==>', state)
        })

        localStorage.setItem(ADMIN_USER_TOKEN, result.data.admin_token)
        localStorage.setItem(ADMIN_USER_NAME, result.data.username)
        localStorage.setItem(ADMIN_USER_ID, result.data.id)
        localStorage.setItem(ADMIN_USER_AVATAR, result.data.avatar)
      }

      return result;
    },
    // 管理员登出
    async adminLogout() {
      // await userLogout();
      this.$patch((state)=>{
        localStorage.removeItem(ADMIN_USER_ID)
        localStorage.removeItem(ADMIN_USER_NAME)
        localStorage.removeItem(ADMIN_USER_TOKEN)
        localStorage.removeItem(ADMIN_USER_AVATAR)

        state.admin_user_id = undefined
        state.admin_user_name = undefined
        state.admin_user_token = undefined
        state.admin_user_avatar = undefined
      })
    },

    getPassword() {
      /* TODO: 解密密码读取 */
      return this.$state.user_password;
    },

    setPassword(password) {
      /* TODO: 加密密码存储 */
      this.$patch((state) => {
        state.user_password = password;
      })
    }
  },
  persist: true,
});
