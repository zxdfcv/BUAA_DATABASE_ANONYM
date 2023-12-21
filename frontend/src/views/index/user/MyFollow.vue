<template>
  <div class="content-list">
    <div class="list-title" v-if="appStore.view_user_id === userStore.user_id">我的关注</div>
    <div class="list-title" v-else>Ta的关注</div>
    <div role="tablist" class="list-tabs-view flex-view">
    </div>
    <div class="list-content">
      <div class="collect-thing-view">
        <a-spin :spinning="loading" style="min-height: 200px;">
          <div class="">
            <a-list
                item-layout="vertical"
                size="large"
                :pagination="pagination"
                :data-source="listData"
                style="width: 90%; align-content: center">
              <template #footer>
                <div>
                  Built by
                  <b>BUAA DataBase</b>
                </div>
              </template>
              <template #renderItem="{ item }">
                <a-list-item key="item.title">
                  <template #extra v-if="appStore.view_user_id === userStore.user_id">
                    <a-button type="primary" shape="round" danger @click="deleteFollow(item.id)">取消关注</a-button>
                  </template>
                  <a-list-item-meta>
                    <template #title>
                      <a @click="router.push({name: 'wishThingView', query: {id: item.following}})">{{ item.following_name }}</a>
                    </template>
                    <template #avatar>
                      <a-avatar v-if="!(item.following_avatar === '' || item.following_avatar === null || item.following_avatar === undefined)" :src="BASE_URL + '/upload/'+ item.following_avatar"/>
                      <a-avatar v-else :src="AvatarIcon" />
                    </template>

                  </a-list-item-meta>
                  关注时间：{{ item.create_time }}
                </a-list-item>
              </template>
            </a-list>
            <template v-if="!listData || listData.length <= 0">
          </template>
          </div>
        </a-spin>
      </div>
    </div>
  </div>
</template>

<script setup>
import {getCollectThingListApi, removeCollectUserApi} from '/@/api/index/thing'
import {getCollectCounterListApi, removeCollectCounter} from '/@/api/index/classification'
import {getCollectCanteenListApi, removeCollectCanteen} from '/@/api/index/canteen'
import {BASE_URL} from "/@/store/constants";
import {useAppStore, useUserStore} from "/@/store";
import { StarOutlined, ShoppingCartOutlined, MessageOutlined } from '@ant-design/icons-vue';
import {getCollectList, userDeleteFollowApi, userFollowersApi} from "/@/api/index/user";
import {openNotification} from "/@/utils/notice";
import AvatarIcon from "/@/assets/images/avatar.jpg";
import {Button} from "view-ui-plus";

const router = useRouter();
const userStore = useUserStore();
const appStore = useAppStore();

const pageData = reactive({
  collectData: []
})
let listData = reactive([]);

const pagination = {
  pageSize: 5,
};

const loading = ref(false)

const queryFollow = async () => {
  loading.value = true;
  const res = await userFollowersApi({user_id: appStore.view_user_id});
  listData.length = 0;
  for (let i = 0; i < res.data.length; i++) {
    listData.push(res.data[i]);
  }
  loading.value = false;
}

const deleteFollow = async (targetId) => {
  userDeleteFollowApi({ids: targetId}).then(async res => {
    console.log(res.data);
    await queryFollow();
  }).catch(err => {
    console.log(err);
  });
}

const refreshDelete = () => {
  getCollectCounterList()
}
onMounted(async () => {
  //getCollectThingList()
  if (useRoute().query.id) { /* TODO: 用戶不存在时会出现问题，需要判断跳转后用户不存在的逻辑，in wishThingView，可能需要 go(-1) */
  } else {
    router.push({name: 'scoreView', query: {id: userStore.user_id}});
  }
  await appStore.setViewId(useRoute().query.id.trim());
  await queryFollow();
  //getCollectCanteenList()
})

const handleClickItem =(record) =>{
  let text = router.resolve({name: 'detailCanteen', query: {id: record.id}})
  window.open(text.href, '_blank')
}
const handleRemove =(record)=> {
  let username = userStore.user_name
  removeCollectCounter({username: username, classificationId: record.id}).then(res => {
    message.success('移除成功')
    getCollectCounterList()
  }).catch(err => {
    console.log(err)
  })
}

const fillData = (list) => {
  var res = [];
  for (var i = 0; i < list.length; i++) {
    var item = list[i];
    console.log(item)
    var data = {};
    data['name'] = item.name;
    data["id"] = item.id;
    data["price"] = item.price;
    data["url"] = (item.images.length !== 0) ? BASE_URL + item.images[0].image : null; /* TODO: 服务器端可以默认配置一个缺省的图片 url */
    data["avatarUrl"] = 'https://api.lolicon.app/assets/img/lx.jpg'; /* TODO: 缺少一个上传者的 avatar_URL */
    data["uploaderId"] = item.merchant;
    data["uploaderName"] = item.merchant_name;
    data["pv"] = item.views;
    data["off_shelve"] = item.off_shelve;
    data["is_sold"] = item.is_sold;
    res.push(data);
  }
  return res;
}

const getCollectCounterList = async () => {
  loading.value = true
  getCollectList({}).then(res => {
    const data = res.data;
    if (res.code === 0) {
      pageData.collectData = fillData(data);
      console.log(pageData.collectData)
    }
    loading.value = false;
  }).catch(err => {
    openNotification({
      type: 'error',
      message: 'Oops!',
      description: err.response.data.detail
    })
    loading.value = false;
  });
  // getCollectCounterListApi({username: username}).then(res => {
  //   res.data.forEach(item => {
  //     item.cover = BASE_URL + item.cover
  //   })
  //   console.log(res.data)
  //   pageData.collectData = res.data
  //   loading.value = false
  // }).catch(err => {
  //   console.log(err.msg)
  //   loading.value = false
  // })
}
// const getCollectCounterList =()=> {
//   console.log("test")
//   loading.value = true
//   let username = userStore.user_name
//   getCollectCounterListApi({username: username}).then(res => {
//     res.data.forEach(item => {
//       item.cover = BASE_URL + item.cover
//     })
//     console.log(res.data)
//     pageData.collectData += res.data
//     loading.value = false
//   }).catch(err => {
//     console.log(err.msg)
//     loading.value = false
//   })
// }
// const getCollectCanteenList =()=> {
//   console.log("test")
//   loading.value = true
//   let username = userStore.user_name
//   getCollectCanteenListApi({username: username}).then(res => {
//     res.data.forEach(item => {
//       item.cover = BASE_URL + item.cover
//     })
//     console.log(res.data)
//     pageData.collectData += res.data
//     loading.value = false
//   }).catch(err => {
//     console.log(err.msg)
//     loading.value = false
//   })
// }
</script>
<style scoped lang="less">
.flex-view {
  display: -webkit-box;
  display: -ms-flexbox;
  display: flex;
}

.content-list {
  -webkit-box-flex: 1;
  -ms-flex: 1;
  flex: 1;

  .list-title {
    color: #152844;
    font-weight: 600;
    font-size: 20px;
    line-height: 24px;
    height: 24px;
    margin-bottom: 4px;
  }

  .list-tabs-view {
    position: relative;
    border-bottom: 1px solid #cedce4;
    height: 12px;
    line-height: 42px;
  }
}

.thing-list {
  -ms-flex-wrap: wrap;
  flex-wrap: wrap;
  -webkit-box-pack: start;
  -ms-flex-pack: start;
  justify-content: flex-start;

  .thing-item {
    position: relative;
    -webkit-box-flex: 1;
    -ms-flex: 1;
    flex: 1;
    margin-right: 20px;
    min-width: 255px;
    max-width: 255px;
    height: fit-content;
    border-radius: 4px;
    overflow: hidden;
    margin-top: 16px;
    cursor: pointer;

    .remove {
      position: absolute;
      right: 8px;
      top: 8px;
      width: 48px;
      height: 20px;
      text-align: center;
      line-height: 20px;
      color: #fff;
      background: #a1adc5;
      border-radius: 32px;
      cursor: pointer;
    }

    .img-view {
      background: #eaf1f5;
      font-size: 0;
      text-align: center;
      height: 156px;
      padding: 8px 0;

      img {
        max-width: 100%;
        height: 100%;
        display: block;
        margin: 0 auto;
        border-radius: 4px;
        -webkit-box-sizing: border-box;
        box-sizing: border-box;
      }
    }

    .info-view {
      background: #f6f9fb;
      text-align: center;
      height: 108px;
      overflow: hidden;
      padding: 0 16px;

      h3 {
        color: #1c355a;
        font-weight: 500;
        font-size: 16px;
        line-height: 20px;
        overflow: hidden;
        text-overflow: ellipsis;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        margin: 12px 0 8px;
      }

      .authors, .translators {
        color: #6f6f6f;
        font-size: 12px;
        line-height: 14px;
        margin-top: 4px;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }
    }
  }
}
</style>
