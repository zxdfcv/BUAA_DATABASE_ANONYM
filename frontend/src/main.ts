import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import piniaStore from './store';
import bootstrap from './core/bootstrap';

import ViewUIPlus from 'view-ui-plus'
import ElementPlus from 'element-plus'
import Antd from 'ant-design-vue';
import UndrawUi from 'undraw-ui'

import '/@/styles/reset.less';
import '/@/styles/index.less';
import 'undraw-ui/dist/style.css'
import 'element-plus/dist/index.css'
import 'view-ui-plus/dist/styles/viewuiplus.css'


const app = createApp(App)

app.use(UndrawUi).use(Antd).use(ElementPlus).use(ViewUIPlus).
use(piniaStore).use(router).use(bootstrap).
mount('#app');

/* ----- Spin style ----- */
import { h } from 'vue'
import { Spin } from 'ant-design-vue'
import { LoadingOutlined } from '@ant-design/icons-vue';

Spin.setDefaultIndicator({
    indicator: h(LoadingOutlined, {
        style: {
          fontSize: '24px',
        },
        spin: true,
      }),
  });

