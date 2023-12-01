import { defineStore } from 'pinia';
import piniaStore from '/@/store/index';
import {viewC1Api, viewC2Api} from "/@/api/index/classification";

/**
 * 应用状态信息留存
 */
export const useAppStore = defineStore(
  // 唯一ID
  'app',
  {
    state: () => ({
        classificationReNewed: false,
        classification1: undefined,
        classification2: undefined,
    }),
    getters: {},
    actions: {
        async reNewClass() {
            const result1 = await viewC1Api();
            const result2 = await viewC2Api();
            if (result1.code === 0) {
                const res1 = result1.data;
                console.log(res1);
                this.$patch((state)=> {
                    state.classification1 = res1;
                    state.classificationReNewed = true;
                    console.log('Storage state ==> ', this)
                })
            }
            if (result2.code === 0) {
                const res2 = result1.data;
                console.log(res2);
                this.$patch((state)=> {
                    state.classification2 = res2;
                    console.log('Storage state ==> ', this)
                })
            }
            return result1.data;
        }
    },
    persist: {
        key: 'app',
        storage: sessionStorage,
    },
  },
);

export function useAppOutsideStore() {
  return useAppStore(piniaStore);
}
