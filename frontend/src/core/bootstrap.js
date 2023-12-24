// Remove: 已实现 pinia 持久化，项目中已经不再需要 localStorage

import { useAppStore, useUserStore, useWebSocketStore } from "/@/store";

export default async function Initializer() {
  const userStore = useUserStore()
  userStore.$patch((state) => {
    // state.token_expire_time = localStorage.getItem(TOKEN_EXPIRE_TIME)
    // state.user_name = localStorage.getItem(USER_NAME)
    // state.user_access = localStorage.getItem(USER_ACCESS)
    // state.user_avatar = localStorage.getItem(USER_AVATAR)
    // state.admin_user_id = localStorage.getItem(ADMIN_USER_ID)
    // state.admin_user_name = localStorage.getItem(ADMIN_USER_NAME)
    // state.admin_user_token = localStorage.getItem(ADMIN_USER_TOKEN)
    // state.admin_user_avatar = localStorage.getItem(ADMIN_USER_AVATAR)
    console.log('恢复userStore完毕 ==> ', state)
  })

  const appStore = useAppStore()
  appStore.$patch((state) => {
    // state.token_expire_time = localStorage.getItem(TOKEN_EXPIRE_TIME)
    // state.user_name = localStorage.getItem(USER_NAME)
    // state.user_access = localStorage.getItem(USER_ACCESS)
    // state.user_avatar = localStorage.getItem(USER_AVATAR)
    // state.admin_user_id = localStorage.getItem(ADMIN_USER_ID)
    // state.admin_user_name = localStorage.getItem(ADMIN_USER_NAME)
    // state.admin_user_token = localStorage.getItem(ADMIN_USER_TOKEN)
    // state.admin_user_avatar = localStorage.getItem(ADMIN_USER_AVATAR)
    console.log('恢复AppStore完毕 ==> ', state)
  })

  const webSocketStore = useWebSocketStore()
  webSocketStore.$patch((state) => {
    console.log('恢复WebSocketStore完毕 ==> ', state)
  })

  if (userStore.user_access) {
    await webSocketStore.attachSocket();
  }
}
