<template>
  <div>
    <!--页面区域-->
    <div class="page-view">
      <a-table
          size="middle"
          rowKey="id"
          :loading="data.loading"
          :columns="columns"
          :data-source="data.dataList"
          :scroll="{ x: 'max-content' }"
          :pagination="{
          size: 'default',
          current: data.page,
          pageSize: data.pageSize,
          total: data.total,
          onChange: (current) => {data.page = current; getDataList();},
          showSizeChanger: false,
          showTotal: (total) => `共${total}条数据`,
        }"
      >
      </a-table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { listOpLogListApi } from "/@/api/admin/log";


const columns = reactive([
  {
    title: '序号',
    dataIndex: 'index',
    key: 'index',
    align: 'center'
  },
  {
    title: '请求方式',
    dataIndex: 're_method',
    key: 're_method',
    align: 'center'
  },
  {
    title: '请求URL',
    dataIndex: 're_url',
    key: 're_url',
    align: 'center'
  },
  {
    title: '操作IP',
    dataIndex: 're_ip',
    key: 're_ip',
    align: 'center'
  },
  {
    title: '操作时间',
    dataIndex: 're_time',
    key: 're_time',
    align: 'center'
  },
  {
    title: '耗时',
    dataIndex: 'access_time',
    key: 'access_time',
    align: 'center',
    customRender: ({ text, record, index, column }) => text + 'ms' ,
  }
]);

// 页面数据
const data = reactive({
  dataList: [],
  loading: false,
  keyword: '',
  selectedRowKeys: [] as any[],
  pageSize: 10,
  page: 1,
  total: 0,
});


onMounted(() => {
  getDataList();
});

const getDataList = () => {
  data.loading = true;
  listOpLogListApi({
    limit: data.pageSize,
    offset: data.pageSize * (data.page - 1),
    keyword: data.keyword,
  })
      .then((res) => {
        data.loading = false;
        console.log(res.data.results);
        let datas = res.data.results;
        datas.forEach((item: any, index: any) => {
          item.index = index + 1 + (data.pageSize * (data.page - 1));
        });
        data.dataList = datas;
        data.total = res.data.count;
      })
      .catch((err) => {
        data.loading = false;
        console.log(err);
      });
};


const rowSelection = ref({
  onChange: (selectedRowKeys: (string | number)[], selectedRows: DataItem[]) => {
    console.log(`selectedRowKeys: ${selectedRowKeys}`, 'selectedRows: ', selectedRows);
    data.selectedRowKeys = selectedRowKeys;
  },
});

</script>

<style scoped lang="less">
.page-view {
  min-height: 100%;
  background: #fff;
  padding: 24px;
  display: flex;
  flex-direction: column;
}

.table-operations {
  margin-bottom: 16px;
  text-align: right;
}

.table-operations > button {
  margin-right: 8px;
}
</style>
