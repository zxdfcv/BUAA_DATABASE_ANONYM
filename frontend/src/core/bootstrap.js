// TODO: Remove: 已实现 pinia 持久化，项目中已经不再需要 localStorage

import {useUserStore} from "/@/store";
import {USER_ID, USER_NAME, USER_ACCESS, ADMIN_USER_ID, ADMIN_USER_NAME, ADMIN_USER_TOKEN, USER_AVATAR, ADMIN_USER_AVATAR} from "/@/store/constants";

export default function Initializer () {
  const userStore = useUserStore()
  userStore.$patch((state)=>{
    // state.user_id = localStorage.getItem(USER_ID)
    // state.user_name = localStorage.getItem(USER_NAME)
    // state.user_access = localStorage.getItem(USER_ACCESS)
    // state.user_avatar = localStorage.getItem(USER_AVATAR)
    // state.admin_user_id = localStorage.getItem(ADMIN_USER_ID)
    // state.admin_user_name = localStorage.getItem(ADMIN_USER_NAME)
    // state.admin_user_token = localStorage.getItem(ADMIN_USER_TOKEN)
    // state.admin_user_avatar = localStorage.getItem(ADMIN_USER_AVATAR)
    console.log('恢复store完毕 ==> ', state)
  })

}