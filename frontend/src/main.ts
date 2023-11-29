import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import piniaStore from './store';
import ViewUIPlus from 'view-ui-plus'

import bootstrap from './core/bootstrap';
import '/@/styles/reset.less';
import '/@/styles/index.less';
import Antd from 'ant-design-vue';
import UndrawUi from 'undraw-ui'
import 'undraw-ui/dist/style.css'

const app = createApp(App)
import 'view-ui-plus/dist/styles/viewuiplus.css'



app.use(UndrawUi)
app.use(Antd);
app.use(router);
app.use(piniaStore);
app.use(ViewUIPlus);
app.use(bootstrap)
app.mount('#app');
