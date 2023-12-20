<template>
  <div>
  <!--页面区域-->
    <div class="page-view">
      <div class="table-operations">
        <a-space>
          <a-button type="primary" @click="handleAdd">新增</a-button>
          <a-button @click="handleBatchDelete">批量删除</a-button>
          <a-input-search addon-before="名称" enter-button @search="onSearch" @change="onSearchChange" />
        </a-space>
      </div>
      <a-table
          size="middle"
          rowKey="id"
          :loading="data.loading"
          :columns="columns"
          :data-source="data.dataList"
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
            <a @click="handleEdit(record)">编辑</a>
            <a-divider type="vertical" />
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
import {listApi, createApi, updateApi, cancelApi, deleteApi} from '/@/api/admin/order'
import {message} from "ant-design-vue";

onMounted(() => {
  getDataList()
})

const columns = reactive([
  {
    title: '序号',
    dataIndex: 'id',
    key: 'id',
    align: 'center'
  },
  {
    title: '卖家',
    dataIndex: 'merchant_name',
    key: 'merchant_name',
    align: 'center'
  },
  {
    title: '买家',
    dataIndex: 'receiver_name',
    key: 'receiver_name',
    align: 'center'
  },
  {
    title: '商品',
    dataIndex: 'product_name',
    key: 'product_name',
    align: 'center',
    // customRender: (text) => text ? text.substring(0, 10) + '...' : '--'
  },
  {
    title: '状态',
    dataIndex: 'status',
    key: 'status',
    align: 'center',
    scopedSlots: {customRender: 'status'}
  },
  {
    title: '创建时间',
    dataIndex: 'create_time',
    key: 'create_time',
    align: 'center'
  },
  {
    title: '支付时间',
    dataIndex: 'pay_time',
    key: 'pay_time',
    align: 'center'
  },
  {
    title: '金额',
    dataIndex: 'amount',
    key: 'amount',
    align: 'center'
  },
  {
    title: '操作',
    dataIndex: 'action',
    align: 'center',
    fixed: 'right',
    width: 140,
    scopedSlots: {customRender: 'operation'}
  }
])

// 页面数据
const data = reactive({
  dataList: [],
  loading: false,
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
    title: undefined,
  },
  rules: {
    title: [{ required: true, message: '请输入', trigger: 'change' }],
  },
});

const myform = ref<FormInstance>();

const getDataList = () => {
  data.loading = true
  listApi({
    keyword: data.keyword
  })
    .then((res) => {
      data.loading = false
      console.log(res)
      res.data.forEach((item: any, index: any) => {
        item.index = index + 1
      });
      data.dataList = res.data
    })
    .catch((err) => {
      data.loading = false
      console.log(err)
    })
}


const rowSelection = ref({
  onChange: (selectedRowKeys: (string | number)[], selectedRows: DataItem[]) => {
    console.log(`selectedRowKeys: ${selectedRowKeys}`, 'selectedRows: ', selectedRows);
    data.selectedRowKeys = selectedRowKeys;
  },
});

const handleAdd = () => {
  resetModal();
  modal.visile = true;
  modal.editFlag = false;
  modal.title = '新增';
  // 重置
  for (const key in modal.form) {
    modal.form[key] = undefined;
  }
};
const handleEdit = (record: any) => {
  resetModal();
  modal.visile = true;
  modal.editFlag = true;
  modal.title = '编辑';
  // 重置
  for (const key in modal.form) {
    modal.form[key] = undefined;
  }
  for (const key in record) {
    modal.form[key] = record[key];
  }
};

const confirmDelete = (record: any) => {
  console.log('delete', record);
  deleteApi({ ids: record.id })
      .then((res) => {
        getDataList();
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
  deleteApi({ ids: data.selectedRowKeys.join(',') })
      .then((res) => {
        message.success('删除成功');
        data.selectedRowKeys = [];
        getDataList();
      })
      .catch((err) => {
        message.error(err.msg || '操作失败');
      });
};

const handleOk = () => {
  myform.value
      ?.validate()
      .then(() => {
        if (modal.editFlag) {
          updateApi({
            id: modal.form.id
          },modal.form)
              .then((res) => {
                hideModal();
                getDataList();
              })
              .catch((err) => {
                console.log(err);
                message.error(err.msg || '操作失败');
              });
        } else {
          createApi(modal.form)
              .then((res) => {
                hideModal();
                getDataList();
              })
              .catch((err) => {
                console.log(err);
                message.error(err.msg || '操作失败');
              });
        }
      })
      .catch((err) => {
        console.log('不能为空');
      });
};

const handleCancel = () => {
  hideModal();
};

// 恢复表单初始状态
const resetModal = () => {
  myform.value?.resetFields();
}

// 关闭弹窗
const hideModal = () => {
  modal.visile = false;
}

</script>

<style lang="less" scoped>
.table-wrap {
  flex: 1;
}

.page-view {
  min-height: 100%;
  background: #FFF;
  padding: 24px;
  display: flex;
  flex-direction: column;
}

.table-operation {
  height: 50px;
  text-align: right;
}
</style>