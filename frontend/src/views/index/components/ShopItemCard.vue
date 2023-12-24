<template>
<a-card
    hoverable
    style="cursor: default"
    @click="toDetail"
>

  <template #cover style="display: flex;
    justify-content: space-around;">
    <Button
        type="error"
        shape="circle"
        icon="md-close"
        style="position: absolute; right: 10px; top: 40px; width: fit-content"
        @click.stop="deleteCollect"
        v-if="props.deletable">删除收藏
    </Button>
    <el-tag
        type="warning"
        class="mx-1"
        effect="dark"
        style="position: absolute; right: 10px; top: 10px; width: fit-content"
        v-if="props.shopCard.off_shelve"
    >
      已下架
    </el-tag>
    <el-tag
        type="info"
        class="mx-1"
        effect="dark"
        style="position: absolute; right: 10px; top: 10px; width: fit-content"
        v-else-if="props.shopCard.is_sold"
    >
      已卖出
    </el-tag>
    <el-tag
        class="mx-1"
        effect="dark"
        style="position: absolute; right: 10px; top: 10px; width: fit-content"
        v-else
    >
      可购买
    </el-tag>
    <img
        v-if="props.shopCard.url"
        alt="example"
        :src="props.shopCard.url"
        style="margin: 0 auto; background-size: cover; object-fit: contain; height: 160px"
        @error="handleImgError"
    />
    <img
        v-else
        alt="example"
        :src="placeHolder"
        style="margin: 0 auto; background-size: cover; object-fit: contain; height: 160px"
    />

  </template>
  <a-spin :spinning="props.loading">
  <div style="height: 90px">
    <div style="font-size: 18px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis">
      {{ props.shopCard.name }}
    </div>
    <div class="info-view">
      <h4 v-if="props.shopCard.price !== undefined" class="price">{{ props.shopCard.price }} 元</h4>
      <div class="wrap" @click.stop="pushToMerchant" v-if="!props.editable">
        <el-avatar style="cursor: pointer" v-if="!(props.shopCard.avatarUrl === '' || props.shopCard.avatarUrl === null || props.shopCard.avatarUrl === undefined)" :size="40" :src="BASE_URL + '/upload/' + props.shopCard.avatarUrl" />
        <el-avatar style="cursor: pointer" v-else :src="AvatarIcon" />
      <span style="color: #444; font-size: 13px; width: 100px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; margin-left: 8px">{{ props.shopCard.uploaderName }}</span>
        <div v-if="props.shopCard.pv !== undefined" style="color: #444; font-size: 11px; margin-left: 50px; margin-top: -5px">{{ props.shopCard.pv }} 次浏览</div>
      </div>
      <div v-else class="wrap">
        <ButtonGroup shape="circle">
          <Button type="primary" style="font-size: 12px" @click.stop="modifier">
            修改信息
          </Button>
          <Button type="error" style="font-size: 12px" @click.stop="deleter">
            删除商品
          </Button>
        </ButtonGroup>
      </div>
    </div>
  </div>
  </a-spin>
  <a-modal :closable=false v-model:visible="open" centered title="注意！" :confirm-loading="loading" @ok="deletePro">
    <p>真的要删除这个商品吗，这个操作不可恢复！</p>
  </a-modal>
  <a-modal :closable=false :footer="null" v-model:visible="open2" centered :confirm-loading="loading2" style="width: 80%">
    <add-product
    :modify=true
    :mid=props.shopCard.id
    @close="closeModifier"/>
  </a-modal>
</a-card>
</template>



<script setup lang="ts">
import router from "/@/router";
import placeHolder from "/@/assets/images/placeHolder.svg";
import failedHolder from "/@/assets/images/failedHolder.svg";
import { deleteFromCollect, deleteProduct } from "/@/api/index/product";
import AvatarIcon from "/@/assets/images/avatar.jpg";
import { useUserStore } from "/@/store";
import { openNotification } from "/@/utils/notice";
import AddProduct from "/@/views/index/user/addProduct.vue";
import { BASE_URL } from "/@/store/constants";

const props = defineProps(['shopCard', 'loading', 'deletable', 'editable']);
const emits = defineEmits(['deleteCollecter'])
const loading = ref(false);
const loading2 = ref(false);
const open = ref(false);
const open2 = ref(false);

const deleter = () => {
  open.value = true;
}

const modifier = () => {
  open2.value = true;
}

const toDetail = () => {
  router.push({name: 'detail', query: {id: props.shopCard.id}})
}

const deleteCollect = async () => {
  await deleteFromCollect({ids: props.shopCard.id});
  emits('deleteCollecter', props.shopCard.id);
}

const pushToMerchant = () => {
  router.push({name: 'usercenter', query: {id: props.shopCard.uploaderId}})
}

const deletePro = async () => {
  loading.value = true;
  let datas = new FormData();
  datas.append('merchant', useUserStore().user_id);
  deleteProduct({product_id: props.shopCard.id}, datas).then(res => {
    if (res.code === 0) {
      openNotification({
        type: 'success',
        message: '成功删除商品',
        description: '成功删除商品！'
      })
    }
    loading.value = false;
    open.value = false;
    emits("deleteCollecter", props.shopCard.id);
  }).catch(err => {
    console.log(err);
    openNotification({
      type: 'error',
      message: 'Oops!',
      description: err
    })
    loading.value = false;
    open.value = false;
  });
}

const closeModifier = () => {
  open2.value = false;
  emits('deleteCollecter')
}

const handleImgError = (e) => {
  e.target.src = failedHolder;
}

watch(useRoute(), (to, from) => {
    router.go(0); // 相当于刷新当前页面
})

// console.log(props.shopCard)
</script>



<style scoped lang="less">
.info-view {
  // background: #f6f9fb;
  // background: pink;
  overflow: hidden;
  padding-top: 10px;
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
  top: -10px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  display: flex;
  float: right;
}

.wrap {
  /* 可无需设置高度，靠图片高度 或者 文字的上下padding撑开高度 */
}
.wrap span{
  display: inline-block;
  vertical-align: middle;
}
.wrap img{
  height: auto;
  vertical-align: middle;
}
</style>