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
        </template>
      </a-table>
    </div>

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
                <a-form-item label="商品 id" name="product_id">
                  <a-input placeholder="请输入" v-model:value="modal.form.product"></a-input>
                </a-form-item>
              </a-col>
              <a-col span="12">
                <a-form-item label="发送用户 id" name="receiver_id">
                  <a-input placeholder="请输入" v-model:value="modal.form.sender"></a-input>
                </a-form-item>
              </a-col>
              <a-col span="12">
                <a-form-item label="接收用户 id" name="product_id">
                  <a-input placeholder="请输入" v-model:value="modal.form.recipient"></a-input>
                </a-form-item>
              </a-col>
              <a-col span="24">
                <a-form-item label="内容">
                  <a-textarea placeholder="请输入" v-model:value="modal.form.content"></a-textarea>
                </a-form-item>
              </a-col>
              <a-col span="24">
                <a-form-item label="图片">
                  <a-upload-dragger
                      name="file"
                      accept="image/*"
                      :multiple="false"
                      :before-upload="beforeUpload"
                      :max-count="1"
                      v-model:file-list="fileList"
                  >
                    <p class="ant-upload-drag-icon">
                      <template v-if="modal.form.imageUrl">
                        <img :src="modal.form.imageUrl" :style="{ width: `${160 * modal.form.imageWidth / modal.form.imageHeight}px`, height: '160px' }"/>
                      </template>
                      <template v-else>
                        <file-image-outlined/>
                      </template>
                    </p>
                    <p class="ant-upload-text">
                      请选择要上传的封面图片
                    </p>
                  </a-upload-dragger>
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
import {FormInstance, message, UploadProps} from "ant-design-vue";
import { deleteApi, listApi, createApi, updateApi} from "/@/api/admin/chat";
import { BASE_URL } from "/@/store/constants";
import { exportCsv } from "/@/utils/exportCsv";
import {FileImageOutlined} from "@ant-design/icons-vue";

const fileList = ref<any[]>([]);
const fileList1 = ref<any[]>([]);

const submitting = ref<boolean>(false);

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
    imageFile: undefined,
    imageUrl: '',
    imageHeight: 0,
    imageWidth: 0,
    product: undefined,
    link: undefined,
    is_read: undefined,
    recipient: undefined,
    sender: undefined,
    content: '',
  },
  rules: {
    link: [{required: true, message: '请输入', trigger: 'change'}],
  },
});

const myform = ref<FormInstance>()

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

const beforeUpload = (file: File) => {
  // 改封面文件名
  const fileName = new Date().getTime().toString() + '.' + file.type.substring(6);
  const copyFile = new File([file], fileName);
  console.log(copyFile);
  const reader = new FileReader();

  reader.onload = (event) => {
    const img = new Image();
    img.onload = () => {
      // 获取图片的宽高
      modal.form.imageUrl = String(event.target.result)
      console.log(modal.form.imageUrl)
      const width = img.width
      const height = img.height
      modal.form.imageWidth = width
      modal.form.imageHeight = height
    }

    // 将文件的内容设置给图片对象
    img.src = event.target.result as string
  }

  reader.readAsDataURL(copyFile)

  modal.form.imageFile = copyFile
  return false;
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

const resetModal = () => {
  myform.value?.resetFields()
  fileList.value = []
  fileList1.value = []
}

const handleEdit = (record: any) => {
  resetModal();
  modal.visile = true;
  modal.editFlag = true;
  modal.title = '编辑';
  // modal.canteen = '新增';
  // 重置
  for (const key in modal.form) {
    modal.form[key] = undefined;
  }
  for (const key in record) {
    if (record[key]) {
      modal.form[key] = record[key];
    }
  }
  modal.form.imageUrl = modal.form.image;
  console.log(modal.form.imageUrl)
  const img = new Image();
  img.onload = () => {
    modal.form.imageWidth = img.width;
    modal.form.imageHeight = img.height;
  };
  img.src = modal.form.imageUrl;
  modal.form.image = undefined;
};

const handleOk = () => {
  myform.value
      ?.validate()
      .then(() => {
        const formData = new FormData()
        if (modal.form.recipient) {
          formData.append('product', modal.form.recipient)
        }
        if (modal.form.imageFile) {
          formData.append('image', modal.form.imageFile)
        }
        if (modal.form.content) {
          formData.append('content', modal.form.content)
        }
        if (modal.form.sender) {
          formData.append('sender', modal.form.sender)
        }
        if (modal.form.recipient) {
          formData.append('recipient', modal.form.recipient)
        }
        if (modal.form.is_read) {
          formData.append('is_read', modal.form.is_read === '1' ? "true" : "false")
        }
        if (modal.form.product) {
          formData.append('product', modal.form.product)
        }

        if (modal.editFlag) {
          updateApi({
            chat_id: modal.form.id
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

const handleAdd = () => {
  resetModal();
  modal.visile = true;
  modal.editFlag = false;
  modal.title = '新增';
  // modal.form.canteen = '新增';
  // 重置
  for (const key in modal.form) {
    modal.form[key] = undefined;
  }
  modal.form.image = undefined
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
