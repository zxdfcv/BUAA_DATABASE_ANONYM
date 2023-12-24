<template>
  <a-row justify="center">
    <a-col :span="24" style="height: 60px"><Header /></a-col>
    <a-col :span="10" style="padding-top: 20px;">
  <div style="top: 20px">
    <a-steps :current="current" style="padding-top: 60px;">
      <a-step v-for="item in steps" :key="item.title" :title="item.title" />
    </a-steps>
    <div class="steps-content">
      <div v-if="current === 0 || current === 1">
        <a-descriptions title="订单商品详情" bordered :column="1"  v-if="from_detail">
          <a-descriptions-item label="商品名">{{ detailData.title }}</a-descriptions-item>
          <a-descriptions-item label="可提货地点">{{ detailData.addr }}</a-descriptions-item>
          <a-descriptions-item label="所属分类">{{ detailData.Class1 }} 、{{ detailData.Class2 }}</a-descriptions-item>
          <a-descriptions-item label="发布者">{{ detailData.uploaderName }}</a-descriptions-item>
          <a-descriptions-item label="发布时间">{{ detailData.createTime }}</a-descriptions-item>
          <a-descriptions-item label="订单金额">{{ detailData.price }} 元</a-descriptions-item>
          <a-descriptions-item label="订单提交时间" v-if="current === 1">{{ createTime }}</a-descriptions-item>
        </a-descriptions>
      </div>
      <div v-if="current === 1" style="padding-top: 5%">请在跳转后页面完成支付后点击“我已完成支付”按钮
        <div>
        <a-button type="primary" style="margin: 15px" @click="raisePayment" :loading="loading">跳转到支付界面</a-button>
        </div>
      </div>
      <div v-if="current === 2" style="padding-top: 15%">您的订单已经支付完毕！</div>
    </div>
    <div class="steps-action">
      <a-button v-if="current === 0" type="primary" @click="raiseOrder" :loading="loading">{{ order_number === 0 ? '确认提交订单' : '继续提交订单' }}</a-button>
      <a-button v-if="current === 1" @click="prev" >返回查看订单信息</a-button>
      <a-button v-if="current === 1" danger style="margin-left: 8px" @click="cancelPayment" >取消订单</a-button>
      <a-button v-if="current === 1" type="primary" style="margin-left: 8px" @click="refreshOrder" :loading="loading">{{ loading === false ? '我已完成支付' : '正在更新订单信息' }}</a-button>
      <a-button v-if="current === steps.length - 1" type="primary" @click="finishPurchase">返回个人中心</a-button>
    </div>
  </div>

    </a-col>
  </a-row>
</template>

<script setup>
import Header from "/@/views/index/components/header.vue";
import { cancelOrderApi, createOrderApi, getOrderListApi, payOrderApi } from "/@/api/index/order";
import { useRoute } from "vue-router";
import { openNotification } from "/@/utils/notice";
import router from "/@/router";
import { useUserStore } from "/@/store";
import { getProductDetail } from "/@/api/index/product";
import { BASE_URL } from "/@/store/constants";
import { getFormatTime } from "/@/utils";

const route = useRoute();
const current = ref(0);
const userStore = useUserStore();

const productId = ref(0);
const order_number = ref(0);
const loading = ref(false);
let detailData = ref({})
const createTime = ref('');
const from_detail = ref(false);


onMounted(() => {
  productId.value = route.query.product.trim();
  if (route.query.order_number !== null && route.query.order_number !== undefined) {
    /* 来自用户中心支付已有订单 */
    order_number.value = route.query.order_number.trim();
    current.value = 1;
    raisePayment();
  } else {
    /* 来自商品详情页创建新订单 */
    getPostDetail();
  }
})

const getPostDetail = async () => {
  await getProductDetail({product_id: productId.value}).then(async res => {
    console.log(res)
    detailData.value['id'] = res.data.id;
    detailData.value['addr'] = res.data.addr;
    detailData.value['cover'] = res.data.images;
    detailData.value['title'] = res.data.name;
    detailData.value['pv'] = res.data.views;
    detailData.value['description'] = res.data.description;
    detailData.value['collect_count'] = res.data.collectors_count;
    detailData.value['wish_count'] = res.data.wants; /* TODO: 缺少是否卖出/下架在前端的展示点 */
    for (var i = 0; i < res.data.images.length; i++) {
      detailData.value['cover'][i] = BASE_URL + detailData.value['cover'][i].image;
    }
    detailData.value['onSale'] = true;
    detailData.value["uploaderId"] = res.data.merchant;
    detailData.value["avatarUrl"] = res.data.merchant_avatar;
    detailData.value["uploaderName"] = res.data.merchant_name;
    detailData.value["Class1"] = res.data.classification_1_name;
    detailData.value["Class2"] = res.data.classification_2_name;
    detailData.value["C_1"] = res.data.classification_1;
    detailData.value["C_2"] = res.data.classification_2;
    detailData.value["createTime"] = res.data.create_time;
    detailData.value["price"] = res.data.price;
    from_detail.value = true;
  }).catch(err => {
    console.log(err)
    openNotification({
      type: 'error',
      message: 'Oops!',
      description: err.msg
    })
  });
}

const raiseOrder = () => {
  if (order_number.value !== 0) {
    current.value++;
    return
  }
  loading.value = true;
  createTime.value = getFormatTime(Date.now(), true);
  createOrderApi({'product': productId.value}).then(res => {
    console.log(res.data)
    if (res.code === 0) {
      current.value++;
      order_number.value = res.data.order_number;
      openNotification({
        type: 'success',
        message: '订单创建成功'
      })
      payOrderApi({'order_number': order_number.value}).then(res => {
        if (res.code === 0) {
          console.log(res.data)
          window.open(res.data['支付url'], '_blank')
        }
        loading.value = false;
      }).catch(err => {
        console.log(err)
        openNotification({
          type: 'error',
          message: '支付跳转失败',
          description: '网络问题，请点击按钮重试'
        })
        loading.value = false;
      })
    }
    //
  }).catch(err => {
    console.log(err)
    openNotification({
      type: 'error',
      message: '订单创建失败',
      description: '商品已被购买或不可购哦'
    })
    loading.value = false;
  })
}

const raisePayment = () => {
  loading.value = true;
  console.log(order_number.value)
  payOrderApi({'order_number': order_number.value}).then(res => {
    if (res.code === 0) {
      console.log(res.data)
      window.open(res.data['支付url'], '_blank')
    }
    loading.value = false;
  }).catch(err => {
    console.log(err)
    openNotification({
      type: 'error',
      message: '支付跳转失败',
      description: '网络问题，请点击按钮重试'
    })
    loading.value = false;
  })
}
const cancelPayment = () => {
  cancelOrderApi({'order_number': order_number.value}).then(res => {
    if (res.code === 0) {
      openNotification({
        type: 'success',
        message: '订单取消成功',
      })
    }
    router.go(-1);
  }).catch(err => {
    openNotification({
      type: 'error',
      message: '网络错误！'
    })
  })
}

const refreshOrder = () => {
  loading.value = true;
  getOrderListApi({'user_type': 'receiver'}).then(res => {
    if (res.code === 0) {
      let list = res.data;
      console.log(list)
      let detail = [];
      for (let i = 0; i < list.length; i++) {
        if (list[i]['order_number'] === order_number.value) {
          detail = list[i];
          break;
        }
      }
      if (detail.length !== 0) {

        if (detail['status'] === '1') {
          console.log(detail['status'])
          current.value++;
        }
      }
    }
    loading.value = false;
  }).catch(err => {
    console.log(err);
    loading.value = false;
  })
};

const finishPurchase = () => {
  const userStore = useUserStore();
  router.push({name: 'usercenter', query: {id: userStore.user_id }})
}
const prev = () => {
  current.value--;
};
const steps = [
  {
    title: '订单确认',
  },
  {
    title: '订单支付',
  },
  {
    title: '支付完成',
  },
];
const items = steps.map(item => ({
  key: item.title,
  title: item.title,
}));
</script>

<style scoped>

.steps-content {
  margin-top: 16px;

  border: 1px dashed rgba(233, 233, 233, 0.18);
  border-radius: 6px;
  background-color: #fdfdfd;
  text-align: center;

}

.steps-action {
  margin-top: 24px;
}


[data-theme='dark'] .steps-content {
  background-color: #2f2f2f;
  border: 1px dashed #404040;
}

</style>