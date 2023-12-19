<template>
  <div class="content-list">
    <div class="list-title">我的订单</div> <!-- TODO: 订单分页获取 -->
    <div class="list-content">
      <div class="comment-view">
        <a-spin :spinning="loading" style="min-height: 200px;">
          <a-tabs
              v-model:activeKey="activeKey"
              animated
              size="large"
              type="card"
          >
            <a-tab-pane key="1" tab="我买到的">
              <a-table :columns="columns" :data-source="commentData">
                <template #headerCell="{ column }" >
                  <template v-if="column.key === 'product_name'">
                    <span>商品名</span>
                  </template>
                </template>

                <template #bodyCell="{ column, record }">
                  <template v-if="column.key === 'product_name'">
                    <a @click="router.push({name: 'detail', query: {id: record.product}})">
                      {{ record.product_name }}
                    </a>
                  </template>
                  <template v-if="column.key === 'merchant_name'">
                    <a @click="router.push({name: 'usercenter', query: {id: record.merchant}})">
                      {{ record.merchant_name }}
                    </a>
                  </template>
                  <template v-else-if="column.key === 'status'">
                    <span>
                      <a-tag
                          :color="record.status === '0' ? 'geekblue' : record.status === '1' ? 'green' : 'volcano' "
                      >
                        {{ record.status === '0' ? '等待支付' : record.status === '1' ? '支付成功' : '订单已取消' }}
                      </a-tag>
                    </span>
                  </template>
                  <template v-else-if="column.key === 'action'">
                    <span>
                      <a @click="viewOrderDetail(record)">查看订单详情</a>
                      <a-divider type="vertical"/>
                      <a @click="disableDelete">删除订单记录</a>
                    </span>
                  </template>
                </template>
              </a-table>
              <a-modal v-model:visible="visible" >
                <a-descriptions title="订单详情" bordered :column="1">
                <a-descriptions-item label="商品名">{{ detailData.product_name }}</a-descriptions-item>
                  <a-descriptions-item label="发布者">{{ detailData.merchant_name }}</a-descriptions-item>
                  <a-descriptions-item label="订单提交时间">{{ detailData.create_time }}</a-descriptions-item>
                  <a-descriptions-item label="订单支付时间" v-if="detailData.status === '1'">{{ detailData.pay_time }}</a-descriptions-item>
                  <a-descriptions-item label="订单状态"><a-tag
                      :color="detailData.status === '0' ? 'geekblue' : detailData.status === '1' ? 'green' : 'volcano' "
                  >
                    {{ detailData.status === '0' ? '等待支付' : detailData.status === '1' ? '支付成功' : '订单已取消' }}
                  </a-tag></a-descriptions-item>
                  <a-descriptions-item label="订单号">{{ detailData.order_number }}</a-descriptions-item>
              </a-descriptions>
                <template #footer>
                </template>
              </a-modal>
            </a-tab-pane>
            <a-tab-pane key="2" tab="我卖出的">
              <a-table :columns="columns2" :data-source="replyData">
                <template #headerCell="{ column }" >
                  <template v-if="column.key === 'product_name'">
                    <span>商品名</span>
                  </template>
                </template>

                <template #bodyCell="{ column, record }">
                  <template v-if="column.key === 'product_name'">
                    <a @click="router.push({name: 'detail', query: {id: record.product}})">
                      {{ record.product_name }}
                    </a>
                  </template>
                  <template v-if="column.key === 'receiver_name'">
                    <a @click="router.push({name: 'usercenter', query: {id: record.receiver}})">
                      {{ record.receiver_name }}
                    </a>
                  </template>
                  <template v-else-if="column.key === 'status'">
                    <span>
                      <a-tag
                          :color="record.status === '0' ? 'geekblue' : record.status === '1' ? 'green' : 'volcano' "
                      >
                        {{ record.status === '0' ? '等待支付' : record.status === '1' ? '支付成功' : '订单已取消' }}
                      </a-tag>
                    </span>
                  </template>
                  <template v-else-if="column.key === 'action'">
                    <span>
                      <a @click="viewOrderDetail2(record)">查看订单详情</a>
                      <a-divider type="vertical"/>
                      <a @click="disableDelete">删除订单记录</a>
                    </span>
                  </template>
                </template>
              </a-table>
              <a-modal v-model:visible="visible2" >
                <a-descriptions title="订单详情" bordered :column="1">
                  <a-descriptions-item label="商品名">{{ detailData2.product_name }}</a-descriptions-item>
                  <a-descriptions-item label="购买者">{{ detailData2.receiver_name }}</a-descriptions-item>
                  <a-descriptions-item label="订单提交时间">{{ detailData2.create_time }}</a-descriptions-item>
                  <a-descriptions-item label="订单支付时间" v-if="detailData2.status === '1'">{{ detailData2.pay_time }}</a-descriptions-item>
                  <a-descriptions-item label="订单状态"><a-tag
                      :color="detailData2.status === '0' ? 'geekblue' : detailData2.status === '1' ? 'green' : 'volcano' "
                  >
                    {{ detailData2.status === '0' ? '等待支付' : detailData2.status === '1' ? '支付成功' : '订单已取消' }}
                  </a-tag></a-descriptions-item>
                  <a-descriptions-item label="订单号">{{ detailData2.order_number }}</a-descriptions-item>
                </a-descriptions>
                <template #footer>
                </template>
              </a-modal>
            </a-tab-pane>
          </a-tabs>

        </a-spin>
      </div>
    </div>
  </div>
</template>

<script setup>
import {useAppStore, useUserStore} from "/@/store";

const router = useRouter();
const userStore = useUserStore();
const appStore = useAppStore();

import {
  deleteCommentApi,
  deleteReplyApi,
  listUserCommentsApi,
  queryUserCommentApi,
  queryUserReplyApi
} from '/@/api/index/comment'
import {BASE_URL} from "/@/store/constants";
import {getFormatTime} from '/@/utils'
import {DeleteOutlined, LikeOutlined, MessageOutlined} from "@ant-design/icons-vue";
import AvatarIcon from "/@/assets/images/avatar.jpg";
import {openNotification} from "/@/utils/notice";
import {getOrderListApi} from "/@/api/index/order";

const open = ref(false);
const open2 = ref(false);
const modalLoading = ref(false);
const loading = ref(false);
const loadingCount = ref(0);
const targetId = ref(-1);
const visible = ref(false);
const visible2 = ref(false);

const commentData = ref([])
const replyData = ref([])
const activeKey = ref('1');
let detailData = ref({});
let detailData2 = ref({});

const columns = [
  {
    name: '商品名',
    dataIndex: 'product_name',
    key: 'product_name',
  },
  {
    title: '卖家',
    dataIndex: 'merchant_name',
    key: 'merchant_name',
  },
  {
    title: '订单状态',
    dataIndex: 'status',
    key: 'status',
  },
  {
    title: '支付金额',
    key: 'amount',
    dataIndex: 'amount',
  },
  {
    title: '操作',
    key: 'action',
  },
];
const columns2 = [
  {
    name: '商品名',
    dataIndex: 'product_name',
    key: 'product_name',
  },
  {
    title: '买家',
    dataIndex: 'receiver_name',
    key: 'receiver_name',
  },
  {
    title: '订单状态',
    dataIndex: 'status',
    key: 'status',
  },
  {
    title: '支付金额',
    key: 'amount',
    dataIndex: 'amount',
  },
  {
    title: '操作',
    key: 'action',
  },
];

onMounted(() => {
  if (useRoute().query.id) {
    if (useRoute().query.id.trim() !== String(userStore.user_id)) {
      router.push({name: 'wishThingView', query: {id: useRoute().query.id.trim()}});
    }
  } else {
    router.push({name: 'scoreView', query: {id: userStore.user_id}});
  }
  appStore.setViewId(userStore.user_id);
  getCommentList()
  getReplyList()
})

const handleClickTitle = (record) => {
  let text = router.resolve({name: 'detail', query: {id: record.thing}})
  window.open(text.href, '_blank')
}

const push2user = () => {
  router.push({name: 'usercenter', query: {id: userStore.user_id}})
}

const jump2user = (user) => {
  router.push({name: 'usercenter', query: {id: user}})
}
const push2product = (product) => {
  router.push({name: 'detail', query: {id: product}})
}
const getCommentList = () => {
  loading.value = true
  loadingCount.value++;
  let userId = userStore.user_id
  getOrderListApi({user_type: 'receiver'}).then(res => {
    console.log(res.data)
    commentData.value = res.data
    loading.value = (--loadingCount.value !== 0);
  }).catch(err => {
    openNotification({
      type: 'error',
      message: 'Oops!',
      description: '获取购买列表失败！'
    })
    loading.value = (--loadingCount.value !== 0);
  })
}

const getReplyList = () => {
  loading.value = true
  loadingCount.value++;
  let userId = userStore.user_id
  getOrderListApi({user_type: 'merchant'}).then(res => {
    replyData.value = res.data
    loading.value = (--loadingCount.value !== 0);
    console.log(replyData.value)
  }).catch(err => {
    openNotification({
      type: 'error',
      message: 'Oops!',
      description: '获取卖出列表失败！'
    })
    loading.value = (--loadingCount.value !== 0);
  })
}

const disableDelete = () => {
  openNotification({
    type: 'error',
    message: 'Oops!',
    description: '普通用户不允许删除订单记录！'
  })
}

const viewOrderDetail = (record) => {
  detailData = record;
  console.log(detailData);
  visible.value = true;
}

const viewOrderDetail2 = (record) => {
  detailData2 = record;
  console.log(detailData2);
  visible2.value = true;
}

const deleteComment = () => {
  modalLoading.value = true;
  deleteCommentApi({ids: targetId.value}).then(res => {
    if (res.code === 0) {
      openNotification({
        type: 'success',
        message: '成功删除评论！',
      })
    }
    modalLoading.value = false;
    open.value = false;
    getCommentList();
  }).catch(err => {
    openNotification({
      type: 'error',
      message: 'Oops!',
      description: '删除评论失败！'
    })
    modalLoading.value = false;
    open.value = false;
  })
}

const deleteReply = () => {
  modalLoading.value = true;
  deleteReplyApi({ids: targetId.value}).then(res => {
    if (res.code === 0) {
      openNotification({
        type: 'success',
        message: '成功删除回复！',
      })
    }
    modalLoading.value = false;
    open.value = false;
    getReplyList();
  }).catch(err => {
    openNotification({
      type: 'error',
      message: 'Oops!',
      description: '删除回复失败！'
    })
    modalLoading.value = false;
    open.value = false;
  })
}
</script>
<style lang="less" scoped>
.flex-view {
  display: -webkit-box;
  display: -ms-flexbox;
  display: flex;
}

.content-list {
  flex: 1;

  .list-title {
    color: #152844;
    font-weight: 600;
    font-size: 18px;
    //line-height: 24px;
    height: 48px;
    margin-bottom: 4px;
    border-bottom: 1px solid #cedce4;
  }
}

.comment-view {
  overflow: hidden;

  .comment-list {
    margin: 8px auto;
  }

  .comment-item {
    padding: 15px 0;

    .avatar {
      width: 40px;
      height: 40px;
      border-radius: 50%;
      margin-right: 8px;
    }

    .infos {
      position: relative;
      -webkit-box-flex: 1;
      -ms-flex: 1;
      flex: 1;
    }

    .name {
      -webkit-box-align: center;
      -ms-flex-align: center;
      align-items: center;
      cursor: pointer;
    }

    h3 {
      color: #152844;
      font-weight: 600;
      font-size: 14px;
      margin: 0;
    }

    .traingle {
      width: 0;
      height: 0;
      border-left: 6px solid #c3c9d5;
      border-right: 0;
      border-top: 4px solid transparent;
      border-bottom: 4px solid transparent;
      margin: 0 12px;
    }

    .time {
      color: #5f77a6;
      font-size: 12px;
      line-height: 16px;
      height: 16px;
      margin: 2px 0 8px;
    }

    .content {
      color: #484848;
      font-size: 14px;
      line-height: 22px;
      padding-right: 30px;
    }
  }
}

</style>
