import {createRouter, createWebHistory} from 'vue-router'
import ls from '../utils/localstorage.js'
import request from '../utils/request.js'
import account from '../storage/modules/account.js'

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: 'base',
            redirect: '/index',
        },
        {
            path: '/login',
            name: 'login',
            component: () => import("@/views/login/LoginRegister.vue"),
        },
        {
            path: '/register',
            name: 'register',
            component: () => import("@/views/login/LoginRegister.vue")
        },
        {
            path: '/index',
            name: 'index',
            component: () => import("@/components/HelloWorld.vue"),
            children: [{
                path: 'self',
                name: 'self',
                component: () => import("@/components/TheWelcome.vue")
            },]
        },
        {
            path: '/index2',
            name: 'index2',
            component: () => import("@/components/HelloWorld.vue")
        },
        {
            path: '/admin',
            name: 'admin',
            component: () => import('@/views/AboutView.vue'),
        }
    ]
})

// router whiteList
const allowList = ['adminLogin', 'login', 'register', 'portal', 'search', 'detail', '403', '404',
    /* TODO: need to delete the line */'index2']
// frontend log in
const loginRoutePath = '/login'
// backend log in
const adminLoginRoutePath = '/adminLogin'

router.beforeEach(async (to, from, next) => {
    console.log(to, from)
    let token = ls.get('USER_TOKEN')
    let user = ls.get('USER')
    let password = ls.get('PASSWORD')
    let userRouter = JSON.parse(localStorage.getItem('USER_ROUTER'))
//
//   /** 后台路由 **/
//   if (to.path.startsWith('/admin')) {
//     if (localStorage.getItem(ADMIN_USER_TOKEN)) {
//       if (to.path === adminLoginRoutePath) {
//         next({ path: '/' })
//       } else {
//         next()
//       }
//     } else {
//       if (allowList.includes(to.name as string)) {
//         // 在免登录名单，直接进入
//         next()
//       } else {
//         next({ path: adminLoginRoutePath, query: { redirect: to.fullPath } })
//       }
//     }
//   }
//
    if (to.path.startsWith('/admin')) {

    } else {
        if (JSON.stringify(token) !== '{}') {
            // already log in
            if (to.path === loginRoutePath) {
                // console.log(token)
                // shall not go to login page
                next({path: '/'})
            } else {
                // directly go to target page
                next()
            }
        } else {
            // in allowList, directly go to
            if (allowList.includes(to.name as string)) {
                next()
            } else {
                // go to login page
                next({
                    path: loginRoutePath,
                    query: {
                        redirect: to.fullPath
                    }
                })
            }
        }
    }

});
export default router
