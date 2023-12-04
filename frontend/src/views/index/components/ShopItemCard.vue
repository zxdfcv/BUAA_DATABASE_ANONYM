<template>
<a-card
    hoverable
    @click="toDetail"
>

  <template #cover>
    <img
        alt="example"
        :src=props.shopCard.url
        style="margin: 0 auto; background-size: cover; object-fit: cover; height: 160px"
    />
  </template>
  <a-spin :spinning="props.loading">
  <div style="height: 90px">
    <div style="font-size: 18px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis">
      {{ props.shopCard.name }}
    </div>
    <div class="info-view">
      <h4 v-if="props.shopCard.price !== undefined" class="price">{{ props.shopCard.price }} 元</h4>
      <div v-if="props.shopCard.avatarUrl !== undefined" class="wrap">
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
const props = defineProps(['shopCard', 'loading']);

const toDetail = () => {
  router.push({name: 'detail', query: {id: props.shopCard.id}})
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