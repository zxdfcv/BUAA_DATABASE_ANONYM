<template>
  <div :id="props.id" ref="chartContainer" class="column-chart-container"></div>
</template>

<script setup>
import * as echarts from 'echarts'

const chartContainer = ref()
const barChart = ref()

onMounted(() => {
  console.log('fuck')
  Object.defineProperty(document.getElementById(props.id), 'clientHeight', { get: function() { return 300 } })
  initBarChart()
  window.onresize = function () { // resize
    barChart.value.resize()
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
  id: String
})

console.log(props.dataSource)

watch(() => props.dataSource, () => {
  barChart.value.clear()
  initBarChart()
  barChart.value.series.type = 'bar'
  // window.onresize = function () { // resize
  //   barChart.value.resize()
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


const initBarChart = () => {
  const xData = []
  const yData = []
  const oldData = JSON.parse(JSON.stringify(props.dataSource))
  if (oldData.length > 0) {

    console.log(oldData)
    console.log(props.keyName)
    console.log(props.valueName)
    const nowData = convertData(oldData, props.keyName, props.valueName, 'key', 'value')
    console.log(nowData)
    nowData.map((item) => {
      xData.push(item.key)
      yData.push(item.value)
    })
    console.log(xData)
  }
  barChart.value = echarts.init(chartContainer.value)
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
        color: '#2F4F4F'
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
        color: 'rgba(10, 10, 10, 0.1)',
        width: 1,
        type: 'solid'
      }
    },
    toolbox: {
      show: true,
      feature: {
        mark: {show: true},
        dataView: {show: true, readOnly: false},
        // magicType: {
        //   type: ['line', 'bar'],
        //   option: {
        //     line: {},
        //     bar: {},
        //   }
        // },
        restore: {show: true},
        saveAsImage: {show: true}
      }
    },
    toolbox: {
      show: true,
      feature: {
        mark: {show: true},
        dataView: {show: true, readOnly: false},
        magicType: {show: true, type: ['line', 'bar']},
        restore: {show: true},
        saveAsImage: {show: true}
      }
    },
    series: [
      {
        data: yData,
        type: 'bar',
        itemStyle: {
          color: function (params) {
            // 柱图颜色
            return '#70B0EA'
          }
        }
      }
    ]
  }
  barChart.value.setOption(option)
}

</script>

<style scoped>
.column-chart-container {
  height: 300px // 高度设置要合理
}
</style>
