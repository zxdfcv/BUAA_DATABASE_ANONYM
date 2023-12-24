<template>

  <a-spin :spinning="showSpin">
    <div class="main">

      <a-card title="最近一周访问量">
        <div style="height: 300px;" ref="visitChartDiv"></div>
      </a-card>

      <a-row :gutter="[20,20]">
        <a-col :sm="24" :md="24" :lg="12">
          <a-card title="热门商品排名" style="flex:1;">
            <BarChartComponent :dataSource="tdata.data.product_rank_data" :title="'热门商品排名'" :keyName="'name'" :valueName="'count'" :id="'1'"/>
          </a-card>
        </a-col>
        <a-col :sm="24" :md="24" :lg="12">
          <a-card title="热门分类比例" style="flex:1;">
            <PieChartComponent :dataSource="tdata.data.classification1_rank_data" :title="'热门一级分类比例'" :keyName="'name'" :valueName="'count'" />
          </a-card>
        </a-col>
      </a-row>

      <a-row :gutter="[20,20]">
        <a-col :sm="24" :md="24" :lg="12">
          <a-card title="热门地址排名" style="flex:1;">
            <BarChartComponent :dataSource="tdata.data.product_addr_rank_data" :title="'热门地址排名'" :keyName="'addr'" :valueName="'count'" :id="'3'" />
          </a-card>
        </a-col>
        <a-col :sm="24" :md="24" :lg="12">
          <a-card title="热门分类比例" style="flex:1;">
            <PieChartComponent :dataSource="tdata.data.classification2_rank_data" :title="'热门二级分类比例'" :keyName="'name'" :valueName="'count'" />
          </a-card>
        </a-col>
      </a-row>

      <a-row :gutter="[20,20]">
      <a-col :sm="24" :md="24" :lg="12">
        <a-card title="商品价格统计" style="flex:1;">
          <BarChartComponent :dataSource="tdata.data.product_price_rank_data" :title="'商品价格统计'" :keyName="'price_range'" :valueName="'count'" :id="'4'" />
        </a-card>
      </a-col>
      <a-col :sm="24" :md="24" :lg="12">
        <a-card title="用户性别比例" style="flex:1;">
          <PieChartComponent :dataSource="tdata.data.user_gender_rank_data" :title="'用户性别比例'" :keyName="'gender'" :valueName="'count'" />
        </a-card>
      </a-col>
      </a-row>

      <a-row :gutter="[20,20]">
        <a-col :sm="24" :md="24" :lg="12">
          <a-card title="买家排名" style="flex:1;">
            <BarChartComponent :dataSource="tdata.data.user_purchase_rank_data" :title="'买家排名'" :keyName="'username'" :valueName="'count'" :id="'5'" />
          </a-card>
        </a-col>
        <a-col :sm="24" :md="24" :lg="12">
          <a-card title="卖家排名" style="flex:1;">
            <PieChartComponent :dataSource="tdata.data.user_sell_rank_data" :title="'卖家排名'" :keyName="'username'" :valueName="'count'" />
          </a-card>
        </a-col>
      </a-row>
      <a-row :gutter="[20,20]">
        <a-col :sm="24" :md="24" :lg="12">
          <a-card title="标签排名" style="flex:1;">
            <BarChartComponent :dataSource="tdata.data.tag_rank_data" :title="'标签排名'" :keyName="'name'" :valueName="'count'" :id="'6'" />
          </a-card>
        </a-col>
      </a-row>

    </div>
  </a-spin>

</template>

<script setup lang="ts">
import { ref } from "vue";
import * as echarts from "echarts";
import { listApi } from "/@/api/admin/overview";
import PieChartComponent from "/@/views/admin/components/pieChartComponent.vue";
import BarChartComponent from "/@/views/admin/components/barChartComponent.vue";

let showSpin = ref(true)

const visitChartDiv = ref()
let visitChart

const tdata = ref({ // 组合式 api，vue3 复习
  data: {
    visit_data: {},
    order_rank_data: {},
    product_rank_data: {},
    classification_rank_data: {}, // 后端得提供信息
    user_sell_rank_data: {},
    user_purchase_rank_data: {},
    tag_rank_data: {},
    user_gender_rank_data: {},
    hot_classification_data: {},
    product_addr_rank_data: {},
    product_price_rank_data: {},
    classification1_rank_data: {},
    classification2_rank_data: {}
  }
})

onMounted(() => {
  list()
  window.onresize = function () { // resize
    visitChart.resize()
  }
})

const list = () => {
  listApi({}).then(res => {
    console.log(res.data)
    tdata.value.data = res.data
    Object.keys(tdata.value.data.product_addr_rank_data).forEach(function(key) {
      const innerObj = tdata.value.data.product_addr_rank_data[key];
      switch (innerObj.addr) {
        case '1':
          innerObj.addr = '学院路'
          break
        case '2':
          innerObj.addr = '沙河'
          break
        case '3':
          innerObj.addr = '两校区均可'
          break
        default:
          break
      }
    })
    Object.keys(tdata.value.data.product_price_rank_data).forEach(function(key) {
      const innerObj = tdata.value.data.product_price_rank_data[key]
      console.log('price_range: ' + innerObj.price_range)
      switch (innerObj.price_range) {
        case 1:
          innerObj.price_range = '0-49'
          break
        case 2:
          innerObj.price_range = '50-99'
          break
        case 3:
          innerObj.price_range = '100-199'
          break
        case 4:
          innerObj.price_range = '200-499'
          break
        case 5:
          innerObj.price_range = '500-999'
          break
        case 6:
          innerObj.price_range = '1000+'
          break
        default:
          break
      }
      console.log('price_range: ' + innerObj.price_range)
    })
    initCharts()
    showSpin.value = false
  }).catch(err => {
    showSpin.value = false
  })
}

const initCharts = () => {
  let xData = []
  let uvData = []
  let pvData = []
  tdata.value.data.visit_data.forEach((item, index) => {
    xData.push(item.day)
    uvData.push(item.uv)
    pvData.push(item.pv)
  })
  echarts.init(visitChartDiv.value)
  visitChart = echarts.init(visitChartDiv.value)
  let option = {
    title: {
      text: ''
    },
    tooltip: {
      trigger: 'axis'
    },
    legend: {
      data: ['IP', 'visit'],
      top: '90%',
      left: 'center'
    },
    grid: {
      top: '30px',
      left: '20px',
      right: '20px',
      bottom: '40px',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      axisLabel: {
        textStyle: {
          color: '#2F4F4F'
        }
      },
      axisLine: {
        lineStyle: {
          color: '#2F4F4F'
        }
      },
      // boundaryGap: false,
      data: xData
    },
    yAxis: {
      type: 'value',
      axisLine: {show: false},
      axisTick: {show: false},
      splitLine: {
        show: true, // 网格线
        lineStyle: {
          color: 'rgba(10, 10, 10, 0.1)',
          width: 1,
          type: 'solid'
        }
      }
    },
    toolbox: {
      show: true,
      feature: {
        mark: {show: true},
        dataView: {show: true, readOnly: false},
        restore: {show: true},
        saveAsImage: {show: true}
      }
    },
    series: [
      {
        name: 'IP',
        type: 'line',
        stack: 'Total',
        data: uvData
      },
      {
        name: 'visit',
        type: 'line',
        stack: 'Total',
        data: pvData
      }
    ]
  }
  visitChart.setOption(option)
}

</script>

<style lang="less" scoped>

.main {
  height: 100%;
  display: flex;
  gap: 20px;
  flex-direction: column;

  .box {
    padding: 12px;
    display: flex;
    flex-direction: column;

    .box-top {
      display: flex;
      flex-direction: row;
      align-items: center;
    }

    .box-value {
      color: #000000;
      font-size: 32px;
      margin-right: 12px;

      .v-e {
        font-size: 14px;
      }
    }

    .box-bottom {
      margin-top: 24px;
      color: #000000d9;
    }
  }
}

</style>
