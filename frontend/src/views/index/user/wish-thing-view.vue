<template>
  <div class="content-list">
    <div class="list-title" v-if="appStore.view_user_id === userStore.user_id">我的发布</div>
    <div class="list-title" v-else>Ta的发布</div>
    <div role="tablist" class="list-tabs-view flex-view">
    </div>
    <div class="list-content">
      <div class="collect-thing-view">
        <a-spin :spinning="loading" style="min-height: 200px;">
          <div class="thing-list flex-view">
          <ShopItemCard
              v-for="(item,index) in pageData.collectData"
              :key="item.id"
              :shop-card="item"
              :loading="false"
              :editable="appStore.view_user_id === userStore.user_id"
              @deleteCollecter="getProduct"
              style="width: 30%; margin: 1%;"
          />
          <template v-if="!pageData.collectData || pageData.collectData.length <= 0">
            <a-empty style="width: 100%;margin-top: 200px;"/>
          </template>
        </div>
        </a-spin>
      </div>
    </div>
  </div>
</template>

<script setup>
import { BASE_URL } from "/@/store/constants";
import { useAppStore, useUserStore } from "/@/store";
import { openNotification } from "/@/utils/notice";
import { getProductList } from "/@/api/index/product";
import ShopItemCard from "/@/views/index/components/ShopItemCard.vue";

const router = useRouter();
const userStore = useUserStore();
const appStore = useAppStore();

const pageData = reactive({
  collectData: []
})

const loading = ref(false)

const fillData = (list) => {
  const res = [];
  for (var i = 0; i < list.length; i++) {
    const item = list[i];
    console.log(item)
    const data = {};
    data['name'] = item.name;
    data["id"] = item.id;
    data["price"] = item.price;
    data["url"] = (item.images.length !== 0) ? BASE_URL + item.images[0].image : null; /* TODO: 服务器端可以默认配置一个缺省的图片 url */
    data["avatarUrl"] = item.merchant_avatar;
    data["uploaderId"] = item.merchant;
    data["uploaderName"] = item.merchant_name;
    data["pv"] = item.views;
    data["off_shelve"] = item.off_shelve;
    data["is_sold"] = item.is_sold;
    res.push(data);
  }
  return res;
}

onMounted(() => {
  if (useRoute().query.id) {
  } else {
    router.push({name: 'wishThingView', query: {id: String(userStore.user_id)}});
  }
  appStore.setViewId(useRoute().query.id);
  getProduct();
})

const getProduct = async () => {
  loading.value = true;
  getProductList({user: appStore.view_user_id, sold: 2}).then(res => {
    const data = res.data;
    if (res.code === 0) {
      pageData.collectData = fillData(data);
    }
    loading.value = false;
  }).catch(err => {
    console.log(err)
    openNotification({
      type: 'error',
      message: 'Oops!',
      description: err
    });
    loading.value = false;
  });
}

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
