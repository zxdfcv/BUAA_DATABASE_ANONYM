import { createPinia } from "pinia";
import { useAppStore } from "./modules/app";
import { useUserStore } from "./modules/user";
import { useWebSocketStore } from "/@/store/modules/webSocket";

import piniaPluginPersistedstate from "pinia-plugin-persistedstate";

const pinia = createPinia();
pinia.use(piniaPluginPersistedstate);

export { useAppStore, useUserStore, useWebSocketStore };
export default pinia;
