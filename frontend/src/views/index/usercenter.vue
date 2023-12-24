<template>
  <div class="user">
    <Header />
    <div class="user-content">
      <div class="user-content-left" style="margin-left: 15px; margin-top: 15px;">
        <MineInfosView />
      </div>
      <div class="user-content-right">
        <router-view />
      </div>
    </div>
  </div>
</template>
<script>
import Header from "/@/views/index/components/header.vue";
import Footer from "/@/views/index/components/footer.vue";
import MineInfosView from "/@/views/index/user/mine-infos-view.vue";

export default {
  components: {
    MineInfosView,
    Footer,
    Header
  },
  data () {
    return {
      collapsed: false
    }
  }
}
</script>
<style scoped lang="less">

.user {
  display: block;
  background: #dae6f9;
}

.user-content {
  display: flex;
  flex-direction: row;
  background-color: #ffffff;
  max-width: 1400px;
  min-width: 800px;
  margin: 80px auto;
  .user-content-left {
  }
  .user-content-right{
     flex: 1;
    padding-right: 20px;
  }

}
</style>
