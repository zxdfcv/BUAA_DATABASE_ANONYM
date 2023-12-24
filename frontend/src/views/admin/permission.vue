<template>
  <div>
    <!--页面区域-->
    <div class="page-view">
      <div class="table-operations">
        <a-space>
          <a-button type="primary" @click="handleAdd">新增</a-button>
          <a-button @click="handleBatchDelete">批量删除</a-button>
        </a-space>
      </div>
      <a-table
          size="middle"
          rowKey="id"
          :loading="data.loading"
          :columns="columns"
          :data-source="data.groupList"
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
          <template v-if="column.key === 'permissions'">
            <span>
              <a-divider type="vertical"/>
              <a-dropdown :trigger="['click']">
                <a class="ant-dropdown-link" @click.prevent>
                  点我
                  <DownOutlined />
                </a>
                <template #overlay>
                  <a-menu>
                    <a-menu-item v-for="item in record.permissions" :key="item"> {{ item.id + ": "  + item.name }} </a-menu-item>
                  </a-menu>
                </template>
              </a-dropdown>
            </span>
          </template>
        </template>
      </a-table>
    </div>

    <!--弹窗区域-->
    <div>
      <a-modal
          :visible="modal.visile"
          :forceRender="true"
          :title="modal.title"
          ok-text="确认"
          cancel-text="取消"
          @cancel="handleCancel"
          @ok="handleOk"
      >
        <div>
          <a-form ref="myform" :label-col="{ style: { width: '80px' } }" :model="modal.form" :rules="modal.rules">
            <a-row :gutter="24">
              <a-col span="24">
                <a-form-item label="权限组名称" name="name">
                  <a-input placeholder="请输入" v-model:value="modal.form.name"></a-input>
                </a-form-item>
              </a-col>
            </a-row>
            <a-col offset="1" span="23">
              <p slot="title">修改权限组</p>
              <a-form :label-width="40">
                <a-form-item>
                  <a-transfer
                      :rowKey="record => record.id"
                      :list-style="{ width: '300px' }"
                      :dataSource="data.permList"
                      v-model:selected-keys="selectedKeys"
                      v-model:target-keys="modal.form.selectedKeys"
                      :render="item => item.name"
                      :titles="['可用分组', '当前分组']"
                      filterable
                  />
                </a-form-item>
              </a-form>
            </a-col>
          </a-form>
        </div>
      </a-modal>
    </div>
  </div>
</template>

<script setup lang="ts">
import { FormInstance, message } from "ant-design-vue";
import { createApi, deleteApi, listApi, updateApi } from "/@/api/admin/group";
import { listApi as listPermApi } from "/@/api/admin/permission";
import { DownOutlined } from "@ant-design/icons-vue";

const selectedKeys = ref<string[]>([]);

const columns = reactive([
  {
    title: '序号',
    dataIndex: 'id',
    key: 'id',
    align: 'center'
  },
  {
    title: '权限组名称',
    dataIndex: 'name',
    key: 'name',
    align: 'center'
  },
  {
    title: '权限组包含权限',
    dataIndex: 'permissions',
    key: 'permissions',
    align: 'center'
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
  permList: <string[]>[],
  groupList: [],
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
    permissions: <string[]>[], // arr
    name: undefined,
    selectedKeys: <string[]>[]
  },
  rules: {
    name: [{ required: true, message: '请输入', trigger: 'change' }],
  },
})

const myform = ref<FormInstance>();

onMounted(() => {
  getDataList();
  gentPermList(); // 初始化
});

const gentPermList = () => {
  data.loading = true;
  listPermApi({
    keyword: data.keyword,
  })
      .then((res) => {
        data.loading = false;
        console.log(res.data);
        data.permList = res.data
        data.permList.forEach((item) => {
          item['id'] = String(item['id']) as String
        })
        console.log(data.permList)
      })
      .catch((err) => {
        data.loading = false;
        console.log(err);
      });
}

const getDataList = () => {
  data.loading = true;
  listApi({
    keyword: data.keyword,
  })
      .then((res) => {
        data.loading = false;
        console.log(res);
        data.groupList = res.data;
      })
      .catch((err) => {
        data.loading = false;
        console.log(err);
      });
};

const onSearchChange = (e: Event) => {
  data.keyword = e?.target?.value;
  console.log(data.keyword);
};

const onSearch = () => {
  getDataList();
};

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
  modal.form.permissions.forEach((item) => {
    item['id'] = String(item['id']) as String
  })
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

  modal.form.permissions.forEach((item) => {
    item['id'] = String(item['id']) as String
  })

  console.log(modal.form.permissions)

  const tempArr = []

  for (let i = 0; i < modal.form.permissions.length; ++i) {
    tempArr.push(String(modal.form.permissions[i]['id'] as String))
  }
  modal.form.selectedKeys = tempArr
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
        const formData = new FormData();
        if (modal.form.name) {
          formData.append('name', modal.form.name)
        }
        if (modal.form.permissions) {
          // const descArray: { id: string; name: string }[] = []
          console.log(modal.form.permissions)
          console.log(data.permList)
          modal.form.selectedKeys.forEach(item => {
            formData.append('permissions', item)
            console.log(item)
          })
          // let descJson = JSON.stringify(descArray);
          // formData.append('permissions', descJson)
        }
        if (modal.editFlag) {
          updateApi({ group_id: modal.form.id }, formData)
              .then((res) => {
                hideModal();
                getDataList();
              })
              .catch((err) => {
                message.error(err.msg || '操作失败');
              });
        } else {
          createApi(modal.form)
              .then((res) => {
                hideModal();
                getDataList();
              })
              .catch((err) => {
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
};

// 关闭弹窗
const hideModal = () => {
  modal.visile = false;
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
