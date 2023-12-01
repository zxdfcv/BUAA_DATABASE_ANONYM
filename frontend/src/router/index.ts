import { createRouter, createWebHistory } from 'vue-router'
import { ADMIN_USER_TOKEN, USER_ACCESS } from '/@/store/constants'
import { useUserStore } from '/@/store'

import root from './root'

/* 可直接访问的 page name WhiteList */
const whiteList = ['welcome', 'adminLogin', 'login', /* 'register' */, 'portal', 'search', 'detail', '403', '404', 'detailCanteen', 'detailCounter']
// 前台登录地址
const loginRoutePath = '/login'
// 后台登录地址
const adminLoginRoutePath = '/adminLogin'


const router = createRouter({
  history: createWebHistory(),
  routes: root,
});

/* 路由守卫验证是否登录 */
router.beforeEach(async (to, from, next) => {
  const userStore = useUserStore();
  console.log("Router: " + (from.name as string) + " ==> " + (to.name as string))
  // console.log(from);
  // console.log(to);
  
  

  /** 后台路由 **/
  if (to.path.startsWith('/admin')) {
    if (localStorage.getItem(ADMIN_USER_TOKEN)) {
      if (to.path === adminLoginRoutePath) {
        next({ path: '/' })
      } else {
        next()
      }
    } else {
      if (whiteList.includes(to.name as string)) {
        // 在免登录名单，直接进入
        next()
      } else {
        // next({ path: adminLoginRoutePath, query: { redirect: to.fullPath } })
        next()
      }
    }

    // next()
  } else {
    
    if (userStore.token_expire_time + 1000 * 60 * 24 * 21 > Date.now()) { /* 写假了，用 Access Token 过期后 3 周的时间用来表示 Refresh 的过期时间 */
    if (to.name === 'login') {
        next({ path: '/' })
      } else {
        next()
      }
    } else {
      // userStore.logout();
      
      if (whiteList.includes(to.name as string)) {
        // 在免登录名单，直接进入
        next()
      } else {
        console.log("Router: " + (to.name as string) + " ==> login(Forced)")
        next({ path: loginRoutePath, query: { redirect: to.fullPath } })
      }
    }
    // next()
  }

});

/* 导航后指向新页面的顶端 */
router.afterEach((_to) => { document.getElementById("html")?.scrollTo(0, 0) });

export default router;
