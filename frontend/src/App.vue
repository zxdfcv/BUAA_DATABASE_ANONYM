<script setup lang="ts">
import zhCN from 'ant-design-vue/es/locale/zh_CN'

</script>

<template>
  <a-config-provider :locale="zhCN">
    <div>
      <RouterView />
    </div>
  </a-config-provider>
</template>

<style lang="scss">
html,body #app{
    height: 100%;
    width: 100%
}
</style>
