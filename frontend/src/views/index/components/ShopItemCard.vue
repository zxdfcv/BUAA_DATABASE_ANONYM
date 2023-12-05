<template>
<a-card
    hoverable
    @click="toDetail"
>

  <template #cover style="display: flex;
    justify-content: space-around;">
    <Button
        type="primary"
        shape="circle"
        icon="md-close"
        style="position: absolute; right: 10px; top: 10px;"
        @click.stop="deleteCollect"
        v-if="props.deletable"/>
    <img
        v-if="props.shopCard.url"
        alt="example"
        :src="props.shopCard.url"
        style="margin: 0 auto; background-size: cover; object-fit: contain; height: 160px"
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
      <div v-if="props.shopCard.avatarUrl !== undefined" class="wrap" @click.stop="pushToMerchant">
        <el-avatar :size="40" :src="props.shopCard.avatarUrl" />
      <span style="color: #444; font-size: 13px; width: 100px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; margin-left: 8px">{{ props.shopCard.uploaderName }}</span>
      </div>
      <div v-if="props.shopCard.pv !== undefined" style="color: #444; font-size: 11px; margin-left: 50px; margin-top: -5px">{{ props.shopCard.pv }} 次浏览</div>
    </div>
  </div>
  </a-spin>
</a-card>
</template>



<script setup lang="ts">
import router from "/@/router";
import placeHolder from "/@/assets/images/placeHolder.svg";
import close from "/@/assets/images/close.svg";
import {deleteFromCollect} from "/@/api/index/product";

const props = defineProps(['shopCard', 'loading', 'deletable']);
const emits = defineEmits(['deleteCollecter'])
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

watch(useRoute(), (to, from) => {
    router.go(0); // 相当于刷新当前页面
})
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