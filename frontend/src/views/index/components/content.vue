<template>
  <div class="home">
    <div class="content">
      <Card style="width:100%">
      <Row>
        <Col span="5">
      <div class="content-left">
        <div class="left-search-item">
          <Card>
            <h4>食堂列表</h4>
            <a-tree :tree-data="contentData.cData" :selected-keys="contentData.selectedKeys" @select="onSelect"
              :load-data="onLoadData" style="min-height: 220px;">
            </a-tree>
          </Card>
        </div>
        <div class="left-search-item">
          <Card>
            <h4>热门标签</h4>
            <div class="tag-view tag-flex-view">
              <span class="tag" :class="{ 'tag-select': contentData.selectTagId === item.id }"
                v-for="item in contentData.tagData" :key="item.id" @click="clickTag(item.id)">{{ item.title }}</span>
            </div>
          </Card>
        </div>
      </div>
        </Col>
      <div class="content-right">
        <div class="top-select-view flex-view">
          <div class="order-view">
            <span class="title"></span>
              <span class="tab" :class="contentData.selectTabIndex === index ? 'tab-select' : ''"
                v-for="(item, index) in contentData.tabData" :key="index" @click="selectTab(index)">
                <img :src="FoodIcon">
                {{ item }}
              </span>
            <span :style="{ left: contentData.tabUnderLeft + 'px' }" class="tab-underline"></span>
          </div>
        </div>
        <a-spin :spinning="contentData.loading" style="min-height: 200px;">
          <div class="pc-thing-list flex-view">
            <div v-for="item in contentData.pageData" :key="item.id"
              @click="handleDetail(item, contentData.selectTabIndex)" class="thing-item item-column-3"><!---->
              <div class="img-view">
                <img :src="item.cover">
                <!-- <div style="position: absolute; left: 10px; bottom: 10px;">
                <img :src="PlayIcon" style="width: 30px;height: 30px;">
              </div> -->
              </div>
              <Card>
                <div class="info-view">
                  <h3 class="thing-name">{{ item.title.substring(0, 12) }}</h3>
                  <h4 v-if="item.price !== undefined" class="price">{{ item.price }}元</h4>
                  <span style="color: #444; font-size: 11px;height: 11px;">{{ item.create_time.substring(0, 16) }}</span>
                  <br />
                  <span style="color: #444; font-size: 11px;height: 11px;">{{ item.pv }}次浏览</span>
                </div>
              </Card>
            </div>
            <div v-if="contentData.pageData.length <= 0 && !contentData.loading" class="no-data" style="">暂无数据</div>
          </div>
        </a-spin>
        <div class="page-view" style="">
          <a-pagination v-model="contentData.page" size="small" @change="changePage" :hideOnSinglePage="true"
            :defaultPageSize="contentData.pageSize" :total="contentData.total" :showSizeChanger="false" />
        </div>
      </div>
      </Row>
      </Card>
    </div>
  </div>
</template>

<script setup>
import { listApi as listClassificationList } from '/@/api/index/classification'
import { listApi as listCanteenList } from '/@/api/index/canteen'
import { listApi as listTagList } from '/@/api/index/tag'
import { listApi as listThingList } from '/@/api/index/thing'
import { BASE_URL } from "/@/store/constants";
import { useUserStore } from "/@/store";
import { USER_ID, USER_NAME, USER_TOKEN, ADMIN_USER_ID, ADMIN_USER_NAME, ADMIN_USER_TOKEN } from "/@/store/constants";
import FoodIcon from '/@/assets/images/地道美食.svg';
import PlayIcon from '/@/assets/images/Play.png'


const userStore = useUserStore()
const router = useRouter();

const contentData = reactive({
  selectX: 0,
  selectTagId: -1,
  cData: [],
  bData: [],
  selectedKeys: [],
  tagData: [],
  loading: false,

  tabData: ['最新', '必吃', '推荐', '柜台', '食堂'],
  selectTabIndex: 0,
  tabUnderLeft: 12,

  thingData: [],
  pageData: [],
  value: [],
  page: 1,
  total: 0,
  pageSize: 6,
})

onMounted(() => {
  initSider()
  getThingList({})
})


const onLoadData = treeNode => {
  return new Promise(resolve => {
    listClassificationList({ canteen: treeNode.dataRef.id }).then(res => {
      treeNode.dataRef.children = []
      res.data.forEach(item => {
        item.key = `${treeNode.eventKey}-${item.id}`
        item.isLeaf = true
        treeNode.dataRef.children.push(item)
      })
      contentData.cData = [...contentData.cData]
      console.log(contentData.cData)
      resolve();
      return;
    })
  });
};


const initSider = () => {
  console.log(contentData)
  contentData.cData.push({ key: '10086', title: '全部', isLeaf: true })
  listCanteenList().then(res => {
    res.data.forEach(item => {
      item.key = item.id.toString()
      contentData.cData.push(item)
      contentData.bData.push(item)
    })
  })
  listTagList().then(res => {
    contentData.tagData = res.data
  })
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

const onSelect = (selectedKeys) => {
  console.log(selectedKeys)
  console.log(contentData)
  if (selectedKeys.length == 0) {
    if (contentData.selectedKeys[0] == '10086') {
      getThingList()
    } else {
      getThingList({ canteen: getSelectedKey() })
    }
  }
  else if (selectedKeys[0].includes("-")) {
    contentData.selectedKeys[0] = [selectedKeys[0].split("-")[1]]
    console.log("selectedKeys")
    console.log(contentData.selectedKeys)
    if (contentData.selectedKeys.length > 0) {
      console.log(getSelectedKey())
      getThingList({ c: getSelectedKey()[0] })
    }
  } else if (selectedKeys[0] == "10086") {
    contentData.selectedKeys[0] = '10086'
    console.log("10086")
    getThingList()
  } else {
    contentData.selectedKeys[0] = selectedKeys[0]
    getThingList({ canteen: getSelectedKey() })
  }
  contentData.selectTagId = -1
}

const clickTag = (index) => {
  contentData.selectedKeys = []
  contentData.selectTagId = index
  getThingList({ tag: contentData.selectTagId })
}

// 最新|必吃|推荐
const selectTab = (index) => {
  contentData.selectTabIndex = index
  contentData.tabUnderLeft = 12 + 70 * index
  if (index === 4) {
    getCanteenList()
  } else if (index === 3) {
    getClassificationList()
  } else {
    let sort = (index === 0 ? 'recent' : index === 1 ? 'hot' : index === 2 ? 'recommend' : index === 4 ? 'canteen' : 'classification')
    const data = { sort: sort }
    if (contentData.selectTagId !== -1) {
      data['tag'] = contentData.selectTagId
      console.log("tag")
    } else {
      console.log("c")
      if (getSelectedKey() != '10086') {
        data['c'] = getSelectedKey()
      }
    }
    data['username'] = getUserName()
    getThingList(data)
  }
}
const handleDetail = (item, index) => {
  // 跳转新页面
  if (index < 3) {
    let text = router.resolve({ name: 'detail', query: { id: item.id } })
    window.open(text.href, '_blank')
  } else if (index === 4) {
    let text = router.resolve({ name: 'detailCanteen', query: { id: item.id } })
    window.open(text.href, '_blank')
  } else {
    let text = router.resolve({ name: 'detailCounter', query: { id: item.id } })
    window.open(text.href, '_blank')
  }
}
// 分页事件
const changePage = (page) => {
  contentData.page = page
  let start = (contentData.page - 1) * contentData.pageSize
  contentData.pageData = contentData.thingData.slice(start, start + contentData.pageSize)
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


</script>

<style scoped lang="less">
.home {
  width: 100%;
  min-height: 100vh;
  background: url("https://s1.ax1x.com/2023/07/29/pPSra9A.jpg") center center no-repeat;
  background-size: 100% 100%;
  position:absolute;//绝对定位
}

.content {
  display: flex;
  flex-direction: row;
  width: 1330px;
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
    margin-top: 48px;
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
