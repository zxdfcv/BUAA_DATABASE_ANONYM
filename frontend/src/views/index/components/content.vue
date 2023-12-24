<template>
  <div class="home">
    <div class="content">
      <a-card style="width:100%; height: fit-content">
        <Row>
          <Col span="5">
            <div class="content-left">
              <div class="left-search-item">
                <Card>
                  <h3>商品分类</h3>
                  <el-scrollbar>
                    <el-tree
                        :data="contentData.classifyData"
                        :props="defaultProps"
                        accordion
                        highlight-current
                        @node-click="clickTag"
                        style="max-height: 300px; min-height: 200px;
                       margin-left: 5px; margin-top: 10px"
                    />
                  </el-scrollbar>
                </Card>
              </div>
              <div>
                <Card style="max-height: 360px; min-height: 150px;
                          margin: 24px 0 12px;">
                  <h3>分类标签</h3>
                  <div style="margin-top: 12px; margin-bottom: 12px">
                    <!-- TODO: use a-tag to rewrite it -->
                    <a-space :size="[0, 8]" wrap>
                      <a-checkable-tag
                          v-for="(tag, index) in contentData.tagData"
                          :key="tag"
                          v-model:checked="contentData.selectData[index]"
                          @change="checked => handleChange(index, checked)"
                      >
                        {{ tag }}
                      </a-checkable-tag>
                    </a-space>
<!--                    <Button-->
<!--                        v-for="item in contentData.tagData"-->
<!--                        :key="item.id"-->
<!--                        @click="clickTag(item)"-->
<!--                        style="margin: 5px" size="small" shape="circle">-->
<!--                      {{ item }}-->
<!--                    </Button>-->
<!--                    <div>-->
<!--                      <el-check-tag checked style="margin-right: 8px">Checked</el-check-tag>-->
<!--                      <el-check-tag :checked="false" @change="onChange">Toggle me</el-check-tag>-->
<!--                    </div>-->
                  </div>
                </Card>
              </div>
            </div>
          </Col>
          <div class="content-right">
            <div class="top-select-view flex-view">
              <div class="order-view">
                <span class="title" style="top: -20px;"></span>
                <a-tabs
                  v-model:activeKey="contentData.selectTabIndex"
                  >
                  <a-tab-pane v-for="(item, index) in contentData.tabData" :key="index" :tab=item @click="" />
                </a-tabs>
              </div>
            </div>
            <a-spin :spinning="contentData.loading" style="min-height: 200px;">
              <div class="pc-thing-list flex-view">
                <ShopItemCard
                  v-for="item in contentData.thingData"
                  :key="item.id"
                  :shop-card="item"
                  :loading="contentData.loading"
                  style="width: 30%; height: 400%; margin: 1%;" />

                <div v-if="contentData.thingData.length <= 0 && !contentData.loading" class="no-data" style="">暂无数据</div>
              </div>
            </a-spin>
            <div class="page-view" style="">
              <a-pagination v-model:current="contentData.page" size="small" @change="changePage"
                            :defaultPageSize="contentData.pageSize" :total="contentData.total"
                            show-quick-jumper
                            :showSizeChanger="false"/>
            </div>
          </div>
        </Row>
      </a-card>
    </div>
  </div>
</template>

<script setup>
import { listApi as listClassificationList } from '/@/api/index/classification'
import { listApi as listCanteenList } from '/@/api/index/canteen'
import { listApi as listTagList } from '/@/api/index/tag'
import { listApi as listThingList } from '/@/api/index/thing'
import { BASE_URL } from "/@/store/constants";
import { useAppStore, useUserStore } from "/@/store";
import { USER_ID, USER_NAME, USER_ACCESS, ADMIN_USER_ID, ADMIN_USER_NAME, ADMIN_USER_TOKEN } from "/@/store/constants";
import FoodIcon from '/@/assets/images/地道美食.svg';
import { Button } from "view-ui-plus";
import ShopItemCard from "/@/views/index/components/ShopItemCard.vue";
import {getProductList} from "/@/api/index/product";
import {openNotification} from "/@/utils/notice";

const appStore = useAppStore();
const userStore = useUserStore();
const router = useRouter();

const contentData = reactive({
  selectX: 0,
  selectTagId: -1,
  cData: [],

  bData: [],
  selectedKeyss: ['0-0-0', '0-0-1'],
  checkedKeys: ['0-0-0', '0-0-1'],
  tagData: [],
  selectData: [],
  loading: false,

  tabData: ['最新', '推荐', '学院路校区', '沙河校区', '两校区均可'],
  selectTabIndex: 0,
  tabUnderLeft: 12,

  thingData: [],
  pageData: [],
  value: [],
  page: 1,
  total: 0,
  pageSize: 6,

  classifyData: [],
  expandedKeys: [],
})

const defaultProps = {
  children: 'children',
  label: 'label',
}

onMounted(() => {
  initSide()
  // getThingList({})
})


const searchParams = reactive({
  keyword: "",
  classification1: "",
  classification2: "",
  status: "",
  addr: "",
  price: "",
  sort: "",
  limit: 6,
});

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

const handleChange = (index, checked) => {
  if (index <= 4) {
    if (checked) {
      for (var i = 0; i <= 4; i++) {
        contentData.selectData[i] = false;
      }
      contentData.selectData[index] = true; /* 确保单选 */
      switch (index) {
        case 0: searchParams.status = 'A'; break;
        case 1: searchParams.status = 'B'; break;
        case 2: searchParams.status = 'C'; break;
        case 3: searchParams.status = 'D'; break;
        case 4: searchParams.status = 'E'; break;
      }
    } else {
      searchParams.status = '';
    }
  } else {
    if (checked) {
      for (var i = 5; i <= 10; i++) {
        contentData.selectData[i] = false;
      }
      contentData.selectData[index] = true; /* 确保单选 */
      searchParams.price = String(index - 4);
    } else {
      searchParams.price = '';
    }
  }
  changePage(1);
};

const searchData = () => {
  contentData.page = 1;
  fetchData();
}
const fetchData = async () => {
  contentData.loading = true;
  searchParams['offset'] = (contentData.page - 1) * contentData.pageSize;
  getProductList(searchParams).then(res => {
    if (res.code === 0) {
      [ contentData.thingData, contentData.total ] = fillData(res.data);
    } else {
      openNotification({
        type: 'error',
        message: 'Oops!',
        description: res.msg
      })
    }
    contentData.loading = false;
  }).catch(err => {
    contentData.loading = false;
    openNotification({
      type: 'error',
      message: 'Oops!',
      description: err.msg
    })
  });
}
const initSide = async () => {
  contentData.classifyData = await appStore.getCTree()
  /* SET HOT-TAG by HAND */
  contentData.tagData = ['全新', '几乎全新', '轻微使用痕迹', '明显使用痕迹', '有一定问题',
                          '0~49元', '50~99元', '100~199元', '200~499元', '500~999元', '1000~元'];
  contentData.selectData = [false, false, false, false, false, false, false, false, false, false];
  /* TODO: 从接口返回的数据数量尚未控制，需要调整 params */
  await changePage(1);
  console.log(contentData.total);
}

const getSelectedKey = () => {
  if (contentData.selectedKeys.length > 0) {
    return contentData.selectedKeys[0]
  } else {
    return -1
  }
}
const getUserName = () => {
  return userStore.user_name
}

const clickTag = (index) => {
  console.log(index.key.split('-'))
  contentData.selectedKeys = []
  contentData.selectTagId = index
  if (index.key.split('-').length === 2) {
    /* 一级搜索类 */
    searchParams.classification1 = appStore.checkC_1[index.label];
    searchParams.classification2 = ""
  } else {
    searchParams.classification1 = ""
    searchParams.classification2 = appStore.checkC_2[index.label];
  }
  changePage(1);
}

const selectTab = () => {
  switch (contentData.selectTabIndex) {
    case 0: searchParams.sort = "create_time"; searchParams.addr = ""; break;
    case 1: searchParams.sort = "hot"; searchParams.addr = ""; break;
    case 2: searchParams.addr = "1"; break;
    case 3: searchParams.addr = "2"; break;
    case 4: searchParams.addr = "3"; break;
  }
  changePage(1);
}
const handleDetail = (item, index) => {
  // 跳转新页面
  if (index < 3) {
    let text = router.resolve({name: 'detail', query: {id: item.id}})
    window.open(text.href, '_blank')
  } else if (index === 4) {
    let text = router.resolve({name: 'detailCanteen', query: {id: item.id}})
    window.open(text.href, '_blank')
  } else {
    let text = router.resolve({name: 'detailCounter', query: {id: item.id}})
    window.open(text.href, '_blank')
  }
}
// 分页事件
const changePage = async (page) => {
  contentData.page = page
  await fetchData();
  console.log('第' + contentData.page + '页')
}

const getCanteenList = () => {
  contentData.loading = true
  listCanteenList().then(res => {
    contentData.loading = false
    res.data.forEach((item, index) => {
      if (item.cover) {
        item.cover = BASE_URL + item.cover
      }
    })
    console.log(res)
    contentData.thingData = res.data
    contentData.total = contentData.thingData.length
    changePage(1)
  }).catch(err => {
    console.log(err)
    contentData.loading = false
  })
}

const getClassificationList = () => {
  contentData.loading = true
  listClassificationList().then(res => {
    contentData.loading = false
    res.data.forEach((item, index) => {
      if (item.cover) {
        item.cover = BASE_URL + item.cover
      }
    })
    console.log(res)
    contentData.thingData = res.data
    contentData.total = contentData.thingData.length
    changePage(1)
  }).catch(err => {
    contentData.loading = false
  })
}

const getThingList = (data) => {
  // console.log(data['username'])
  contentData.loading = true
  listThingList(data).then(res => {
    contentData.loading = false
    res.data.forEach((item, index) => {
      if (item.cover) {
        item.cover = BASE_URL + item.cover
      }
    })
    console.log(res)
    contentData.thingData = res.data
    contentData.total = contentData.thingData.length
    changePage(1)
  }).catch(err => {
    console.log(err)
    contentData.loading = false
  })
}

watch(
    () => contentData.selectTabIndex,
    () => {
      console.log(contentData.selectTabIndex);
      selectTab();
    }
);
</script>

<style scoped lang="less">
.home {
  width: 100%;
  height: auto;
  min-height: 100vh;
  max-height: 750px;
  background: #dae6f9;
  background-size: 100% 100%;
  position: absolute; //绝对定位
}

.content {
  width: 80%;
  height: 750px;
  margin: 80px auto;
}

.content-left {
  width: 220px;
  margin-right: 32px;
}

.left-search-item {
  overflow: hidden;
  border-bottom: 1px solid #cedce4;
  margin-top: 24px;
  padding-bottom: 24px;
}

h4 {
  color: #4d4d4d;
  font-weight: 600;
  font-size: 16px;
  line-height: 24px;
  height: 24px;
}

.category-item {
  cursor: pointer;
  color: #333;
  margin: 12px 0 0;
  padding-left: 16px;
}

ul {
  margin: 0;
  padding: 0;
}

ul {
  list-style-type: none;
}

li {
  margin: 4px 0 0;
  display: list-item;
  text-align: -webkit-match-parent;
}

.child {
  color: #333;
  padding-left: 16px;
}

.child:hover {
  color: #4684e2;
}

.select {
  color: #4684e2;
}

.flex-view {
  -webkit-box-pack: justify;
  -ms-flex-pack: justify;
  //justify-content: space-between;
  display: flex;
}

.name {
  font-size: 14px;
}

.name:hover {
  color: #4684e2;
}

.count {
  font-size: 14px;
  color: #999;
}

.check-item {
  font-size: 0;
  height: 18px;
  line-height: 12px;
  margin: 12px 0 0;
  color: #333;
  cursor: pointer;
  -webkit-box-align: center;
  -ms-flex-align: center;
  align-items: center;
}

.check-item input {
  cursor: pointer;
}

.check-item label {
  font-size: 14px;
  margin-left: 12px;
  cursor: pointer;
  -webkit-box-flex: 1;
  -ms-flex: 1;
  flex: 1;
}

.tag-view {
  -ms-flex-wrap: wrap;
  flex-wrap: wrap;
  margin-top: 4px;
}

.tag-flex-view {
  display: -webkit-box;
  display: -ms-flexbox;
  display: flex;
}

.tag {
  background: #fff;
  border: 1px solid #a1adc6;
  -webkit-box-sizing: border-box;
  box-sizing: border-box;
  border-radius: 16px;
  height: 20px;
  line-height: 18px;
  padding: 0 8px;
  margin: 8px 8px 0 0;
  cursor: pointer;
  font-size: 12px;
  color: #152833;
}

.tag:hover {
  background: #4684e3;
  color: #fff;
  border: 1px solid #4684e3;
}

.tag-select {
  background: #4684e3;
  color: #fff;
  border: 1px solid #4684e3;
}

.content-right {
  -webkit-box-flex: 1;
  -ms-flex: 1;
  flex: 1;
  padding-top: 12px;

  .pc-search-view {
    margin: 0 0 24px;
    -webkit-box-align: center;
    -ms-flex-align: center;
    align-items: center;

    .search-icon {
      width: 20px;
      height: 20px;
      -webkit-box-flex: 0;
      -ms-flex: 0 0 20px;
      flex: 0 0 20px;
      margin-right: 16px;
    }

    input {
      outline: none;
      border: 0px;
      -webkit-box-flex: 1;
      -ms-flex: 1;
      flex: 1;
      border-bottom: 1px solid #cedce4;
      color: #152844;
      font-size: 14px;
      height: 22px;
      line-height: 22px;
      -ms-flex-item-align: end;
      align-self: flex-end;
      padding-bottom: 8px;
    }

    .clear-search-icon {
      position: relative;
      left: -20px;
      cursor: pointer;
    }

    button {
      outline: none;
      border: none;
      font-size: 14px;
      color: #fff;
      background: #288dda;
      border-radius: 32px;
      width: 88px;
      height: 32px;
      line-height: 32px;
      margin-left: 2px;
      cursor: pointer;
    }

    .float-count {
      color: #999;
      margin-left: 24px;
    }
  }

  .flex-view {
    display: flex;
  }

  .top-select-view {
    -webkit-box-pack: justify;
    -ms-flex-pack: justify;
    justify-content: space-between;
    -webkit-box-align: center;
    -ms-flex-align: center;
    align-items: center;
    height: 40px;
    line-height: 40px;

    .type-view {
      position: relative;
      font-weight: 400;
      font-size: 18px;
      color: #5f77a6;

      .type-tab {
        margin-right: 32px;
        cursor: pointer;
      }

      .type-tab-select {
        color: #152844;
        font-weight: 600;
        font-size: 20px;
      }

      .tab-underline {
        position: absolute;
        bottom: 0;
        //left: 22px;
        width: 16px;
        height: 4px;
        background: #4684e2;
        -webkit-transition: left .3s;
        transition: left .3s;
      }
    }

    .order-view {
      position: relative;
      color: #6c6c6c;
      font-size: 14px;

      .title {
        margin-right: 8px;
      }

      .tab {
        color: #999;
        margin-right: 20px;
        cursor: pointer;
      }

      .tab-select {
        color: #152844;
      }

      .tab-underline {
        position: absolute;
        bottom: 0;
        left: 84px;
        width: 16px;
        height: 4px;
        background: #4684e2;
        -webkit-transition: left .3s;
        transition: left .3s;
      }
    }

  }

  .pc-thing-list {
    -ms-flex-wrap: wrap;
    flex-wrap: wrap;
    margin-top: 30px;
    margin-left: -10px;


    .thing-item {
      min-width: 300px;
      max-width: 300px;
      position: relative;
      flex: 1;
      margin-right: 20px;
      height: fit-content;
      overflow: hidden;
      margin-top: 26px;
      margin-bottom: 36px;
      cursor: pointer;
      box-shadow: 4px 4px 4px rgba(200, 200, 200, 0.3), -4px 4px 4px rgba(200, 200, 200, 0.3);


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
        // background: #f6f9fb;
        // background: pink;
        overflow: hidden;
        padding: 16px 16px 16px 16px;
        // width: 50%;

        .thing-name {
          line-height: 32px;
          color: #0F1111;
          font-size: 20px;
          display: flex;
        }

        .price {
          color: #ff3131;
          font-size: 20px;
          line-height: 20px;
          margin-top: 4px;
          overflow: hidden;
          text-overflow: ellipsis;
          white-space: nowrap;
          display: flex;
          float: right;
        }

        .translators {
          color: #6f6f6f;
          font-size: 12px;
          line-height: 14px;
          margin-top: 4px;
          overflow: hidden;
          text-overflow: ellipsis;
          white-space: nowrap;
          float: right;
          width: 50%;
        }
      }
    }

    .no-data {
      height: 200px;
      line-height: 200px;
      text-align: center;
      width: 100%;
      font-size: 16px;
      color: #152844;
    }
  }

  .page-view {
    width: 100%;
    text-align: center;
    margin-top: 8px;
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
