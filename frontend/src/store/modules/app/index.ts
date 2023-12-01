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
        classification1: [],
        classification2: [],
    }),
    getters: {},
    actions: {
        async reNewClass() {
            if (this.classificationReNewed !== true) {
                const result1 = await viewC1Api();
                const result2 = await viewC2Api();
                if (result1.code === 0) {
                    const res1 = result1.data;
                    console.log(res1);
                    this.$patch((state) => {
                        for (var i = 0; i < res1.length; i++) {
                            // @ts-ignore
                            state.classification1.push(res1[i].name);
                        }
                        state.classificationReNewed = true;
                        console.log('Storage state ==> ', this)
                    })
                }
                if (result2.code === 0) {
                    const res2 = result1.data;
                    console.log(res2);
                    this.$patch((state) => {
                        for (var i = 0; i < res2.length; i++) {
                            // @ts-ignore
                            state.classification2.push(res2[i].name);
                        }
                        console.log('Storage state ==> ', this)
                    })
                }
            }
            return this.classification1;
        },

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
