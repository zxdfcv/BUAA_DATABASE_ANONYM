<template>
  <div>
    <!--页面区域-->
    <div class="page-view">
      <div class="table-operations">
        <a-space>
          <a-button type="primary" @click="exportData">导出 CSV</a-button>
          <a-button @click="handleBatchDelete">批量删除</a-button>
        </a-space>
      </div>
      <a-table
          size="middle"
          rowKey="id"
          :loading="data.loading"
          :columns="columns"
          :data-source="data.list"
          :scroll="{ x: 'max-content' }"
          :row-selection="rowSelection"
          :pagination="{
          size: 'default',
          current: data.page,
          pageSize: data.pageSize,
          onChange: (current) => (data.page = current),
          showSizeChanger: false,
          showTotal: (total) => `共${total}条数据`,
        }"
      >
        <template #bodyCell="{ text, record, index, column }">
          <template v-if="column.key === 'operation'">
            <span>
              <a-divider type="vertical"/>
              <a-popconfirm title="确定删除?" ok-text="是" cancel-text="否" @confirm="confirmDelete(record)">
                <a href="#">删除</a>
              </a-popconfirm>
            </span>
          </template>
        </template>
      </a-table>
    </div>

  </div>
</template>

<script setup lang="ts">
import { message } from "ant-design-vue";
import { deleteApi, listApi } from "/@/api/admin/chat";
import { BASE_URL } from "/@/store/constants";
import { exportCsv } from "/@/utils/exportCsv";

const columns = reactive([
  {
    title: '序号',
    dataIndex: 'id',
    key: 'id',
    align: 'center'
  },
  {
    title: '商品名称',
    dataIndex: 'product_name',
    key: 'product_name',
    align: 'center'
  },
  {
    title: '发送者',
    dataIndex: 'sender_name',
    key: 'sender_name',
    align: 'center'
  },
  {
    title: '接收者',
    dataIndex: 'recipient_name',
    key: 'recipient_name',
    align: 'center'
  },
  {
    title: '评论内容',
    dataIndex: 'content',
    key: 'content',
    align: 'center'
  },
  {
    title: '创建时间',
    dataIndex: 'create_time',
    key: 'create_time',
    align: 'center',
  },
  {
    title: '是否已读',
    dataIndex: 'is_read',
    key: 'is_read',
    align: 'center',
  },
  {
    title: '内容',
    dataIndex: 'create_time',
    key: 'create_time',
    align: 'center',
  },
  {
    title: '操作',
    dataIndex: 'action',
    key: 'operation',
    align: 'center',
    fixed: 'right',
    width: 140,
  },
]);

// 页面数据
const data = reactive({
  list: [],
  loading: false,
  currentAdminUserName: '',
  keyword: '',
  selectedRowKeys: [] as any[],
  pageSize: 10,
  page: 1,
});

// 弹窗数据源
const modal = reactive({
  visile: false,
  editFlag: false,
  title: '',
  form: {
    id: undefined,
    image: undefined,
    link: undefined,
  },
  rules: {
    link: [{required: true, message: '请输入', trigger: 'change'}],
  },
});

onMounted(() => {
  getList();
});

const getList = () => {
  data.loading = true;
  listApi({
    keyword: data.keyword,
  })
      .then((res) => {
        data.loading = false;
        console.log(res);
        res.data.forEach((item: any, index: any) => {
          item.index = index + 1
          item.is_read =  item.is_read ? '1' : '0'
          if (item.image) {
            item.image = BASE_URL + item.image
            console.log(item.image)
          }
        });
        data.list = res.data;
      })
      .catch((err) => {
        data.loading = false;
        console.log(err);
      });
};

const exportData = () => {
  exportCsv(data.list, '私聊信息.csv')
};

const rowSelection = ref({
  onChange: (selectedRowKeys: (string | number)[], selectedRows: DataItem[]) => {
    console.log(`selectedRowKeys: ${selectedRowKeys}`, 'selectedRows: ', selectedRows);
    data.selectedRowKeys = selectedRowKeys;
  },
});

const confirmDelete = (record: any) => {
  console.log('delete', record);
  deleteApi({ids: record.id})
      .then((res) => {
        getList();
      })
      .catch((err) => {
        message.error(err.msg || '操作失败');
      });
};

const handleBatchDelete = () => {
  console.log(data.selectedRowKeys);
  if (data.selectedRowKeys.length <= 0) {
    console.log('hello');
    message.warn('请勾选删除项');
    return;
  }
  deleteApi({ids: data.selectedRowKeys.join(',')})
      .then((res) => {
        message.success('删除成功');
        data.selectedRowKeys = [];
        getList();
      })
      .catch((err) => {
        message.error(err.msg || '操作失败');
      });
};
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
