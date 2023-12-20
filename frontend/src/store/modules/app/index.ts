import { defineStore } from 'pinia';
import piniaStore from '/@/store/index';
import {viewC1Api, viewC2Api} from "/@/api/index/classification";
import {userDetailApi} from "/@/api/index/user";

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
        classificationTree: [],
        checkC_1: {},
        checkC_2: {},
        view_user_id: undefined,
        view_user_username: undefined,
        view_user_avatar: undefined,
    }),
    getters: {},
    actions: {
        async setViewId(view_id) {
            // @ts-ignore
            this.view_user_id = Number(view_id);
            userDetailApi({user_id: view_id}).then(res => {
                this.view_user_username = res.data.username;
                this.view_user_avatar = res.data.avatar;
            }).catch(err => {
                console.log("网络错误！")
            })
        },

        async reNewClass() {
            if (this.classificationReNewed !== true) {
                this.classificationReNewed = true;
                const result1 = await viewC1Api();
                const result2 = await viewC2Api();
                if (result1.code === 0) {
                    const res1 = result1.data;
                    console.log(res1);
                    this.$patch((state) => {
                        for (var i = 0; i < res1.length; i++) {
                            // @ts-ignore
                            state.classification1.push(res1[i].name);
                            state.checkC_1[res1[i].name] = res1[i].id;
                        }

                    })
                } else {
                    this.classificationReNewed = false;
                }
                if (result2.code === 0) {
                    const res2 = result2.data;
                    console.log(res2);

                    this.$patch((state) => {
                        for (var j = 0; j < state.classification1.length; j++) {
                            // @ts-ignore
                            state.classificationTree[state.classification1[j]] = [];
                            // @ts-ignore
                            state.classificationTree.push({
                                label: state.classification1[j],
                                id: this.checkC_1[state.classification1[j]],
                                key: j + "-0",
                                children: []
                            });
                        }
                        for (var k = 0; k < res2.length; k++) {
                            // @ts-ignore
                            state.classification2.push(res2[k].name);
                            for (var l = 0; l < state.classificationTree.length; l++) {
                                if (state.classificationTree[l]['label'] === res2[k].classification_1_name) {
                                    // @ts-ignore
                                    state.classificationTree[l]['children'].push({
                                        label: res2[k].name,
                                        id: res2[k].id,
                                        // @ts-ignore
                                        key: state.classificationTree[l]['key'] + '-' + state.classificationTree[l]['children'].length
                                    });
                                }
                            }
                            state.checkC_2[res2[k].name] = res2[k].id;
                        }
                        console.log('Storage state ==> ', this)
                    })
                }
            }
            return this.classification1;
        },

        async getC1() {
            await this.reNewClass();
            return this.classification1;
        },

        async getC2() {
            if (this.classificationReNewed === true) {
                return this.classification2;
            } else {
                await this.reNewClass();
                return this.classification2;
            }
        },

        async getCTree() {
            if (this.classificationReNewed === true) {
                return this.classificationTree;
            } else {
                await this.reNewClass();
                return this.classificationTree;
            }
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
