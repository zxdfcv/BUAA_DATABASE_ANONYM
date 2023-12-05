<template>
  <div class="search">
    <Header />
    <div class="search-content">
    </div>
  </div>
</template>

<script setup>
import Header from '/@/views/index/components/header.vue'
import Footer from '/@/views/index/components/footer.vue'
import SearchContentView from '/@/views/index/components/search-content-view.vue'

</script>

<style scoped lang="less">

.search-content {
  width: 1200px;
}
</style>
