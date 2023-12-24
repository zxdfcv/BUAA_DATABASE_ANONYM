<template>
  <div ref="chartContainer" class="pie-chart-container"></div>
</template>

<script setup>
import * as echarts from "echarts";

const chartContainer = ref()
const pieChart = ref()

onMounted(() => {
  console.log('fuck')
  initPieChart()
  window.onresize = function () { // resize
    pieChart.value.resize()
  }
})


const props = defineProps({
  dataSource: {
    type: Object,
    default: () => []
  },
  title: String,
  keyName: String,
  valueName: String,
})

console.log(props.dataSource)
//const data = ref(props.dataSource)


watch(() => props.dataSource, () => {
  console.log('here')
  console.log(props.keyName)
  console.log(props.dataSource)
  pieChart.value.clear()
  initPieChart()
  // window.onresize = function () { // resize
  //   pieChart.value.resize()
  // }
}, {
  deep: true
})

const convertData = (data, oldKeyName, oldValueName, newKeyName, newValueName) => {
  return data.map((item) => ({
    [newKeyName]: item[oldKeyName],
    [newValueName]: item[oldValueName]
  }))
}

console.log(props.dataSource)
const initPieChart = () => {
  let pieData = []
  console.log(props.dataSource)
  // const list = Object.keys(props.dataSource)
  const oldData = JSON.parse(JSON.stringify(props.dataSource))
  if (oldData.length > 0) {
    console.log(oldData)
    console.log(props.keyName)
    console.log(props.valueName)
    const nowData = convertData(oldData, props.keyName, props.valueName, 'key', 'value')
    console.log(nowData)
    nowData.map((item) => {
      pieData.push({name: item.key, value: item.value})
    })
    // pieData.push({name: '111', value: 6})
    // pieData.push({name: '121', value: 6})
    // pieData.push({name: '131', value: 6})
    // pieData.push({name: '141', value: 6})
  }
  console.log(pieData)
  pieChart.value = echarts.init(chartContainer.value)
  const option = {
    grid: {
      // 让图表占满容器
      top: '40px',
      left: '40px',
      right: '40px',
      bottom: '40px'
    },
    title: {
      text: props.title,
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
  pieChart.value.setOption(option)
}
// beforeCreate(() => {
//   console.log('here')
// })
</script>

<style scoped>
/* Add your component-specific styles here */
.pie-chart-container {
  /* Add styles for the chart container */
  height: 400px /* Set an appropriate height */
}
</style>
