import './assets/main.css'
import 'element-plus/dist/index.css'
import 'ant-design-vue/dist/reset.css'

import { createApp } from 'vue'
import App from './App.vue'

import Antd from 'ant-design-vue'
import ElementPlus from 'element-plus'

import router from './router'
import store from './storage'
import ls from './utils/localstorage.js'
import request from './utils/request.js'
import notice from './utils/notification.js'

const app = createApp(App)

app.use(router).use(store).use(Antd).use(ElementPlus).use(ls).use({
  install (Vue) {
    app.config.globalProperties.$db = ls
  }
})

app.config.globalProperties.$post = request.post
app.config.globalProperties.$get = request.get
// app.config.globalProperties.$router
app.config.globalProperties.$notice = notice

app.mount('#app')
