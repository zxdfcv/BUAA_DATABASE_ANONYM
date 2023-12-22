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
          :data-source="data.userList"
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

    <!--弹窗区域-->
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
              <a-col span="24">
                <a-form-item label="一级分类名称" name="title">
                  <a-input placeholder="请输入" v-model:value="modal.form.name"></a-input>
                </a-form-item>
              </a-col>
              <a-col span="24">
                <a-form-item label="封面">
                  <a-upload-dragger
                      name="file"
                      accept="image/*"
                      :multiple="false"
                      :before-upload="beforeUpload"
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
              <a-col span="24">
                <a-form-item label="内容简介">
                  <a-textarea placeholder="请输入" v-model:value="modal.form.description"></a-textarea>
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
import {FormInstance, message, SelectProps} from 'ant-design-vue';
import {createApi, listApi, updateApi, deleteApi} from '/@/api/admin/classification1';
import {BASE_URL} from "/@/store/constants";
import {FileImageOutlined, VideoCameraOutlined} from '@ant-design/icons-vue';

const columns = reactive([
  {
    title: '序号',
    dataIndex: 'id',
    key: 'id',
    width: 60
  },
  {
    title: '一级分类名称',
    dataIndex: 'name',
    key: 'name',
  },
  {
    title: '简介',
    dataIndex: 'description',
    key: 'description',
    customRender: ({text, record, index, column}) => text ? text.substring(0, 40) + '...' : '--',
    width: 600,
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
      const width = img.width
      const height = img.height
      modal.form.imageWidth = width
      modal.form.imageHeight = height
      console.log(modal.form.imageWidth)
      console.log(modal.form.imageHeight)
    }

    // 将文件的内容设置给图片对象
    img.src = event.target.result as string
  }

  reader.readAsDataURL(copyFile)

  modal.form.imageFile = copyFile
  return false;
};
// 文件列表
const fileList = ref<any[]>([]);
const fileList1 = ref<any[]>([]);

const submitting = ref<boolean>(false);

// 页面数据
const data = reactive({
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
    name: undefined,
    description: undefined,
    image: undefined,
    imageUrl: undefined,
    imageFile: undefined,
    imageWidth: undefined,
    imageHeight: undefined
  },
  rules: {
    name: [{required: true, message: '请输入', trigger: 'change'}],
  },
});

const myform = ref<FormInstance>();

onMounted(() => {
  getDataList();
});

const getDataList = () => {
  data.loading = true;
  listApi({
    keyword: data.keyword,
  })
      .then((res) => {
        data.loading = false;
        console.log(res);
        res.data.forEach((item: any, index: any) => {
          item.index = index + 1;
        });
        data.userList = res.data;
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

const handleAdd = () => {
  resetModal();
  modal.visile = true;
  modal.editFlag = false;
  modal.title = '新增';
  // 重置
  for (const key in modal.form) {
    modal.form[key] = undefined;
  }
  modal.form.image = undefined
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
  if (modal.form.image) {
    modal.form.imageUrl = BASE_URL + modal.form.image
    modal.form.image = undefined
  }
};

const confirmDelete = (record: any) => {
  console.log('delete', record);
  deleteApi({ids: record.id})
      .then((res) => {
        getDataList();
      })
      .catch((err) => {
        message.error(err.msg || '删除失败');
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
        getDataList();
      })
      .catch((err) => {
        message.error(err.msg || '删除失败');
      });
};

const handleOk = () => {
  myform.value
      ?.validate()
      .then(() => {
        const formData = new FormData();
        if (modal.editFlag) {
          formData.append('id', modal.form.id || '')
        }
        formData.append('name', modal.form.name || '')
        if (modal.form.imageFile) {
          formData.append('image', modal.form.imageFile)
        }
        formData.append('description', modal.form.description || '')
        if (modal.editFlag) {
          submitting.value = true
          updateApi({
            id: modal.form.id
          }, formData)
              .then((res) => {
                submitting.value = false
                hideModal();
                getDataList();
              })
              .catch((err) => {
                submitting.value = false
                console.log(err);
                message.error(err.msg || '操作失败');

              });
        } else {
          submitting.value = true
          createApi(formData)
              .then((res) => {
                submitting.value = false
                hideModal();
                getDataList();
              })
              .catch((err) => {
                submitting.value = false
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
  fileList.value = []
  fileList1.value = []
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
  