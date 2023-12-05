<template>

  <a-spin :spinning="showSpin">
    <div class="main">

      <a-card title="最近一周访问量">
        <div style="height: 300px;" ref="visitChartDiv"></div>
      </a-card>

      <a-row :gutter="[20,20]">
        <a-col :sm="24" :md="24" :lg="12">
          <a-card title="热门商品排名" style="flex:1;">
            <div style="height: 300px;" ref="barChartDiv"></div>
          </a-card>
        </a-col>
        <a-col :sm="24" :md="24" :lg="12">
          <a-card title="热门分类比例" style="flex:1;">
            <div style="height: 300px;" ref="pieChartDiv1"></div>
          </a-card>
        </a-col>
      </a-row>

      <a-row :gutter="[20,20]">
        <a-col :sm="24" :md="24" :lg="12">
          <a-card title="热门评论排名" style="flex:1;">
            <div style="height: 300px;" ref="barChartDiv"></div>
          </a-card>
        </a-col>
        <a-col :sm="24" :md="24" :lg="12">
          <a-card title="用户性别比例" style="flex:1;">
            <PieChartComponent :dataSource="tdata.data.classification_rank_data" :title="'用户性别比例'" :key="'title'" :value="'count'" />
          </a-card>
        </a-col>
      </a-row>

      <a-row :gutter="[20,20]">
      <a-col :sm="24" :md="24" :lg="12">
        <a-card title="购买数量排名" style="flex:1;">
          <div style="height: 300px;" ref="barChartDiv"></div>
        </a-card>
      </a-col>
      <a-col :sm="24" :md="24" :lg="12">
        <a-card title="消费金额排名" style="flex:1;">
          <div style="height: 300px;" ref="pieChartDiv"></div>
        </a-card>
      </a-col>
      </a-row>

      <a-row :gutter="[20,20]">
        <a-col :sm="24" :md="24" :lg="12">
          <a-card title="销售数量排名" style="flex:1;">
            <div style="height: 300px;" ref="barChartDiv"></div>
          </a-card>
        </a-col>
        <a-col :sm="24" :md="24" :lg="12">
          <a-card title="销售金额排名" style="flex:1;">
            <div style="height: 300px;" ref="pieChartDiv"></div>
          </a-card>
        </a-col>
      </a-row>

    </div>
  </a-spin>

</template>

<script setup lang="ts">
import {ref} from 'vue';
import * as echarts from 'echarts'
import { InteractionOutlined, StarFilled, StarTwoTone } from '@ant-design/icons-vue'
import {listApi} from '/@/api/admin/overview'
import PieChartComponent from '/@/views/admin/components/pieChartComponent.vue'

let showSpin = ref(true)

const visitChartDiv = ref()
const barChartDiv = ref()
const pieChartDiv = ref()
const pieChartDivHotClassification = ref() // 热门分类比例
const pieChartUserSex = ref()

let visitChart, barChart, pieChart;

const getSexData = (() => {
  return tdata.value.data.sex_data
})
// const sex_data = ref({'male' : 505, 'female': 605})

const tdata = ref({ // 组合式 api，vue3 复习
  data: {
    visit_data: {},
    order_rank_data: {},
    classification_rank_data: {}, // 后端得提供信息
    sex_data: {'male' : 505, 'female': 605},
    hot_classification_data: {}
  }
})

onMounted(() => {
  list()
  window.onresize = function () { // resize
    visitChart.resize()
    barChart.resize()
    pieChart.resize()
  }
})

const list = () => {
  listApi({}).then(res => {
    console.log(res.data)
    tdata.value.data = res.data
    tdata.value.data.sex_data = {'male' : 505, 'female': 605}
    initCharts()
    initBarChart()
    initPieChart()

    //initPieChartTemplate(pieChartUserSex, tdata.value.data.sex_data, '性别比例图')
    // initPieChartTemplate(pieChartDivHotClassification, tdata.value.data.hot_classification_data, '热门分类比例')
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

const initBarChart = () => {
  // let xData = []
  // let yData = []
  // tdata.data.order_rank_data.forEach((item, index) => {
  //   xData.push(item.title)
  //   yData.push(item.count)
  // })
  const xData = ['遥远的救世主', '平凡的世界', '测试书籍12', '测试书籍13', '测试书籍14', '测试书籍15', '测试书籍16', '测试书籍17']
  const yData = [220, 200, 180, 150, 130, 110, 100, 80]
  barChart = echarts.init(barChartDiv.value)
  let option = {
    grid: {
      // 让图表占满容器
      top: '40px',
      left: '40px',
      right: '40px',
      bottom: '40px'
    },
    title: {
      text: '热门商品排名',
      textStyle: {
        color: '#aaa',
        fontStyle: 'normal',
        fontWeight: 'normal',
        fontSize: 18
      },
      x: 'center',
      y: 'top'
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      }
    },
    xAxis: {
      data: xData,
      type: 'category',
      axisLabel: {
        rotate: 30, // 倾斜30度,
        textStyle: {
          color: '#2F4F4F'
        }
      },
      axisLine: {
        lineStyle: {
          color: '#2F4F4F'
        }
      }
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
    series: [
      {
        data: yData,
        type: 'bar',
        itemStyle: {
          normal: {
            color: function (params) {
              // 柱图颜色
              return '#70B0EA'
            }
          }
        }
      }
    ]
  }
  barChart.setOption(option)
}

const initPieChart = () => {
  let pieData = []
  tdata.value.data.classification_rank_data.forEach((item, index) => {
    pieData.push({name: item.title, value: item.count})
  })
  pieChart = echarts.init(pieChartDiv.value)
  const option = {
    grid: {
      // 让图表占满容器
      top: '40px',
      left: '40px',
      right: '40px',
      bottom: '40px'
    },
    title: {
      text: '热门商品分类',
      textStyle: {
        color: '#aaa',
        fontStyle: 'normal',
        fontWeight: 'normal',
        fontSize: 18
      },
      x: 'center',
      y: 'top'
    },
    tooltip: {
      trigger: 'item'
    },
    legend: {
      top: '90%',
      left: 'center'
    },
    series: [
      {
        name: '分类',
        type: 'pie',
        itemStyle: {
          normal: {
            color: function (params) {
              const colorList = ['#70B0EA', '#B3A3DA', '#88DEE2', '#62C4C8', '#58A3A1']
              let index = params.dataIndex
              if (params.dataIndex >= colorList.length) {
                index = params.dataIndex - colorList.length
              }
              return colorList[index]
            }
          }
        },
        radius: ['40%', '70%'],
        avoidLabelOverlap: false,
        label: {
          show: false,
          position: 'center'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 20,
            fontWeight: 'bold'
          }
        },
        labelLine: {
          show: false
        },
        data: pieData
      }
    ]
  }
  pieChart.setOption(option)
}

const initPieChartTemplate = (dataRef, dataSource, title) => {
  let pieData = []
  // dataSource.data.classification_rank_data.forEach((item, index) => {
  //   //pieData.push({name: item.title, value: item.count})
  //   pieData.push({name: 'male', value: 500})
  //   pieData.push({name: 'female', value: 566})
  // })
  pieData.push({name: 'male', value: 500})
  pieData.push({name: 'female', value: 566})
  pieChart = echarts.init(dataRef.value)
  const option = {
    grid: {
      // 让图表占满容器
      top: '40px',
      left: '40px',
      right: '40px',
      bottom: '40px'
    },
    title: {
      text: title,
      textStyle: {
        color: '#aaa',
        fontStyle: 'normal',
        fontWeight: 'normal',
        fontSize: 18
      },
      x: 'center',
      y: 'top'
    },
    tooltip: {
      trigger: 'item'
    },
    legend: {
      top: '90%',
      left: 'center'
    },
    series: [
      {
        name: '分类',
        type: 'pie',
        itemStyle: {
          normal: {
            color: function (params) {
              const colorList = ['#70B0EA', '#B3A3DA', '#88DEE2', '#62C4C8', '#58A3A1']
              let index = params.dataIndex
              if (params.dataIndex >= colorList.length) {
                index = params.dataIndex - colorList.length
              }
              return colorList[index]
            }
          }
        },
        radius: ['40%', '70%'],
        avoidLabelOverlap: false,
        label: {
          show: false,
          position: 'center'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 20,
            fontWeight: 'bold'
          }
        },
        labelLine: {
          show: false
        },
        data: pieData
      }
    ]
  }
  pieChart.setOption(option)
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
