<template>
  <div>
    <!--页面区域-->
    <div class="page-view">
      <div class="table-operations">
        <a-space>
          <a-button type="primary" @click="exportData">导出 CSV</a-button>
          <a-button type="primary" @click="handleAdd">新增</a-button>
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
              <a @click="handleEdit(record)">编辑</a>
              <a-divider type="vertical"/>
              <a-popconfirm title="确定删除?" ok-text="是" cancel-text="否" @confirm="confirmDelete(record)">
                <a href="#">删除</a>
              </a-popconfirm>
            </span>
          </template>
          <template v-if="column.key === 'likes'">
            <span>
              <a-divider type="vertical"/>
              <a-dropdown :trigger="['click']">
                <a class="ant-dropdown-link" @click.prevent>
                  点我
                  <DownOutlined />
                </a>
                <template #overlay>
                  <a-menu>
                    <a-menu-item v-for="item in record.likes" :key="item"> {{ item }} </a-menu-item>
                  </a-menu>
                </template>
              </a-dropdown>
            </span>
          </template>
        </template>
      </a-table>
    </div>

    <!-- 弹窗区域 -->
    <div>
      <a-modal
          :visible="modal.visile"
          :forceRender="true"
          :title="modal.title"
          width="880px"
          ok-text="确认"
          cancel-text="取消"
          @cancel="handleCancel"
          @ok="handleOk"
      >
        <template #footer>
          <a-button key="back" @click="handleCancel">取消</a-button>
          <a-button key="submit" type="primary" :loading="submitting" @click="handleOk">确认</a-button>
        </template>
        <div style="padding-right: 16px; max-height:480px; overflow-x: hidden;overflow-y: auto;">
          <a-form ref="myform" :label-col="{ style: { width: '80px' } }" :model="modal.form" :rules="modal.rules">
            <a-row :gutter="24">
              <a-col span="12">
                <a-form-item label="用户 id" name="receiver_id">
                  <a-input placeholder="请输入" v-model:value="modal.form.user"></a-input>
                </a-form-item>
              </a-col>
              <a-col span="12">
                <a-form-item label="@用户 id" name="product_id">
                  <a-input placeholder="请输入" v-model:value="modal.form.mentioned_user"></a-input>
                </a-form-item>
              </a-col>
              <a-col span="12">
                <a-form-item label="所在评论 id" name="product_id">
                  <a-input placeholder="请输入" v-model:value="modal.form.comment"></a-input>
                </a-form-item>
              </a-col>
              <a-col span="24">
                <a-form-item label="内容">
                  <a-textarea placeholder="请输入" v-model:value="modal.form.content"></a-textarea>
                </a-form-item>
              </a-col>
              <a-col span="24">
                <a-form-item label="点赞用户">
                  <a-select
                      v-model:value="modal.form.likes"
                      mode="multiple"
                      style="width: 100%"
                      placeholder="Please select"
                      :options="data.userList"
                      :field-names="{ label: 'username', value: 'id', options: 'permissions' }"
                      :render="item => item.name"
                  />
                </a-form-item>
              </a-col>
              <a-col span="8">
                <a-form-item label="评论已读" name="status">
                  <a-select placeholder="请选择" allowClear v-model:value="modal.form.comment_read">
                    <a-select-option key="0" :value="'0'">是</a-select-option>
                    <a-select-option key="1" :value="'1'">否</a-select-option>
                  </a-select>
                </a-form-item>
              </a-col>
              <a-col span="8">
                <a-form-item label="已读" name="status">
                  <a-select placeholder="请选择" allowClear v-model:value="modal.form.is_read">
                    <a-select-option key="0" :value="'0'">是</a-select-option>
                    <a-select-option key="1" :value="'1'">否</a-select-option>
                  </a-select>
                </a-form-item>
              </a-col>
            </a-row>
          </a-form>
        </div>
      </a-modal>
    </div>

  </div>
</template>

<script setup lang="ts">
import { FormInstance, message, SelectProps } from "ant-design-vue";
import { listApi as listUserApi } from "/@/api/admin/user";
import { createApi, deleteApi, listApi, updateApi } from "/@/api/admin/reply";
import { BASE_URL } from "/@/store/constants";
import { DownOutlined } from "@ant-design/icons-vue";
import { exportCsv } from "/@/utils/exportCsv";

const myform = ref<FormInstance>();

const submitting = ref<boolean>(false);

const columns = reactive([
  {
    title: '序号',
    dataIndex: 'id',
    key: 'id',
    align: 'center'
  },
  {
    title: '用户',
    dataIndex: 'user_name',
    key: 'user_name',
    align: 'center'
  }
  ,
  {
    title: '@用户 id',
    dataIndex: 'mentioned_user',
    key: 'mentioned_user',
    align: 'center'
  },
  {
    title: '商品名称',
    dataIndex: 'product_name',
    key: 'product_name',
    align: 'center'
  },
  {
    title: '回复内容',
    dataIndex: 'content',
    key: 'content',
    align: 'center'
  },
  {
    title: '点赞者id',
    dataIndex: 'likes',
    key: 'likes',
    align: 'center',
  },
  {
    title: '回复时间',
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
  userList: [],
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
    user: undefined,
    mentioned_user: undefined,
    comment: '',
    content: '',
    image: undefined,
    is_read: undefined,
    comment_read: undefined,
    likes: <SelectProps['options']>[],
    link: undefined,
  },
  rules: {
    link: [{required: true, message: '请输入', trigger: 'change'}],
  },
});

onMounted(() => {
  getUserList()
  getList();
});


const getUserList = () => {
  data.loading = true
  listUserApi({})
      .then((res) => {
        data.loading = false
        console.log(res)
        res.data.forEach((item: any, index: any) => {
          item.index = index + 1
        })
        data.userList = res.data
      })
      .catch((err) => {
        data.loading = false
        console.log(err)
      })
}

const getList = () => {
  data.loading = true;
  listApi({
    keyword: data.keyword,
  })
      .then((res) => {
        data.loading = false;
        console.log(res);
        res.data.forEach((item: any, index: any) => {
          item.index = index + 1;
          item.is_read =  item.is_read ? '1' : '0'
          item.comment_read =  item.comment_read ? '1' : '0'
          if (item.image) {
            item.image = BASE_URL + item.image
          }
          if (item.content) {
            if (item.content.length > 50) {
              item.content = item.content.substring(0, 50) + '...'
            }
          }
          if (item.canteen_title !== undefined) {
            item.title = item.canteen_title
          } else if (item.classification_title != undefined) {
            item.title = item.classification_title
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
  exportCsv(data.list, '回复信息.csv')
};

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


const handleOk = () => {
  myform.value
      ?.validate()
      .then(() => {
        const formData = new FormData()
        if (modal.form.mentioned_user) {
          formData.append('product', modal.form.mentioned_user)
        }
        if (modal.form.content) {
          formData.append('content', modal.form.content)
        }
        if (modal.form.user) {
          formData.append('user', modal.form.user)
        }
        if (modal.form.likes) {
          modal.form.likes.forEach((item) => {
            formData.append('likes', item)
          })
        }
        if (modal.form.is_read) {
          formData.append('is_read', modal.form.is_read === '1' ? "true" : "false")
        }
        if (modal.form.comment_read) {
          formData.append('comment_read', modal.form.comment_read === '1' ? "true" : "false")
        }
        if (modal.form.comment) {
          formData.append('comment', modal.form.comment)
        }
        if (modal.editFlag) {
          updateApi({
            reply_id: modal.form.id
          }, formData)
              .then((res) => {
                hideModal();
                getList();
              })
              .catch((err) => {
                console.log(err);
                message.error(err.msg || '操作失败');
              });
        } else {
          createApi(formData)
              .then((res) => {
                hideModal();
                getList();
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
