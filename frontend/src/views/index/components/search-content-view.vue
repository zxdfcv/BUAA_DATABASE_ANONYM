<template>
  <div class="content-margin">
    <h1 class="search-name-box">{{ tData.keyword }}</h1>
    <div style="background: #ffffff;">
    <div class="search-tab-nav clearfix">
      <div class="tab-text">
        <span>与</span>
        <span class="strong">{{ tData.keyword }}</span>
        <span>相关的内容</span>
      </div>
    </div>
    <div class="content-list">
      <div class="thing-list">

        <a-spin :spinning="tData.loading" style="min-height: 200px;">
          <div class="pc-thing-list">
            <ShopItemCard
                v-for="(item, index) in tData.thingData"
                :key="index"
                :shop-card="item"
                :loading="tData.loading"
                style="width: 30%; margin: 1%;"
            />

            <div v-if="tData.thingData.length <= 0 && !tData.loading" class="no-data" style="">暂无数据</div>
          </div>
        </a-spin>

        <div class="page-view" style="">
          <a-pagination v-model:current="tData.page" size="small" @change="changePage" :hideOnSinglePage="true"
                        :defaultPageSize="tData.pageSize" :total="tData.total"/>
        </div>
      </div>
    </div>
    </div>
  </div>
</template>

<script setup>
import { BASE_URL } from "/@/store/constants";
import { useAppStore, useUserStore } from "/@/store";
import ShopItemCard from "/@/views/index/components/ShopItemCard.vue";
import { getProductList } from "/@/api/index/product";

const userStore = useUserStore()
const router = useRouter();
const route = useRoute();

const tData = reactive({
  loading: false,
  keyword: '',
  thingData: [],
  pageData: [],

  page: 1,
  total: 0,
  pageSize: 12,
})

onMounted(() => {
  changePage(1);
})

// 监听query参数
watch(useRoute(), (to, from) => {
  router.go(0); // 相当于刷新当前页面
})

const fillData = (list) => {
  var res = [];
  for (var i = 0; i < list.results.length; i++) {
    var item = list.results[i];
    console.log(item)
    var data = {};
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
  return [res, list.count];
}

const search = () => {
  tData.keyword = route.query.keyword?.trim()
  tData.loading = true
  const params = {
    limit: tData.pageSize,
  };
  if (route.query.type === 'C_1') {
    params['classification1'] = useAppStore().checkC_1[tData.keyword];
  } else if (route.query.type === 'C_2') {
    params['classification2'] = useAppStore().checkC_2[tData.keyword];
  } else if (route.query.type === 'addr') {
    params['addr'] = (tData.keyword === '学院路校区' ? 1 : tData.keyword === '沙河校区' ? 2 : 3)
  } else if (route.query.type === 'status') {

    params['status'] = (tData.keyword === '全新') ? 'A' :
                       (tData.keyword === '几乎全新') ? 'B' :
                       (tData.keyword === '轻微使用痕迹') ? 'C' :
                       (tData.keyword === '明显使用痕迹') ? 'D' : 'E';
  } else {
    params['keyword'] = tData.keyword;

  }
  params['offset'] = tData.pageSize * (tData.page - 1);
  getProductList(params).then(res => {
    if (res.code === 0) {
      [ tData.thingData, tData.total ] = fillData(res.data);
    }
    console.log(tData.thingData)
    tData.loading = false
  }).catch(err => {
    console.log(err)
    tData.loading = false
  })
}

// 分页事件
const changePage = (page) => {
  tData.page = page;
  search();
}

</script>
<style scoped lang="less">
.content-margin {
  margin: 156px 0 100px;
}

.page-view {
  width: 85%;
  text-align: center;
  margin-top: 48px;
}

.search-name-box {
  background: #f5f9fb;
  height: 100px;
  line-height: 100px;
  font-size: 20px;
  color: #152844;
  text-align: center;
  position: fixed;
  top: 56px;
  left: 0;
  z-index: 1;
  width: calc(100% - 8px);
}

.search-tab-nav {
  position: relative;
  padding: 24px 0 16px;
  text-align: center;

  .tab-text {
    float: left;
    color: #5f77a6;
    font-size: 14px;
  }

  .strong {
    color: #152844;
    font-weight: 600;
    margin: 0 4px;
  }
}

.thing-list{
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
}

.pc-thing-list {
  width: 1100px;
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
}

.thing-item {
  min-width: 300px;
  max-width: 300px;
  position: relative;
  flex: 1;
  height: fit-content;
  overflow: hidden;
  cursor: pointer;
  box-shadow: 4px 4px 4px   rgba(200, 200, 200, 0.3) ,-4px 4px 4px  rgba(200, 200, 200, 0.3) ;


  .img-view {
    //text-align: center;
    position: relative;
    height: 200px;
    width: 300px;

    img {
      height: 200px;
      width: 300px;
      margin: 0 auto;
      background-size: cover;
      object-fit: cover;
    }
  }

  .info-view {
    //background: #f6f9fb;
    overflow: hidden;
    padding: 16px 16px;

    .thing-name {
      line-height: 32px;
      color: #0F1111 !important;
      font-size: 20px !important;
    }

    .price {
      color: #ff7b31;
      font-size: 20px;
      line-height: 20px;
      margin-top: 4px;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }

    .translators {
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


.a-price-symbol {
  top: -0.5em;
  font-size: 12px;
}

.a-price {
  color: #0F1111;
  font-size: 21px;
}

</style>
