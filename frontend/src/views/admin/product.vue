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
                <a-form-item label="商品名称" name="title">
                  <a-input placeholder="请输入" v-model:value="modal.form.name"></a-input>
                </a-form-item>
              </a-col>
              <a-col span="12">
                <a-form-item label="一级分类" name="classification1">
                  <a-select placeholder="请选择"
                            allowClear
                            :options="appStore.classificationTree"
                            :field-names="{ label: 'label', value: 'id',}"
                            v-model:value="modal.form.classification_1">
                  </a-select>
                </a-form-item>
              </a-col>
              <a-col span="12">
                <a-form-item label="二级分类" name="classification2">
                  <a-select placeholder="请选择"
                            allowClear
                            :options="option2"
                            :field-names="{ label: 'label', value: 'id',}"
                            v-model:value="modal.form.classification_2">
                  </a-select>
                </a-form-item>
              </a-col>
              <a-col span="12">
                <a-form-item label="标签">
                  <a-select mode="multiple" placeholder="请选择" allowClear v-model:value="modal.form.tag">
                    <template v-for="item in modal.tagData">
                      <a-select-option :value="item.id">{{item.title}}</a-select-option>
                    </template>
                  </a-select>
                </a-form-item>
              </a-col>
              <!-- <a-col span="12">
                <a-form-item label="食堂" name="canteen">
                  <a-select placeholder="请选择"
                            allowClear
                            :options="modal.bData"
                            :field-names="{ label: 'title', value: 'id',}"
                            v-model:value="modal.form.canteen">
                  </a-select>
                </a-form-item>
              </a-col> -->
              <a-col span="12">
                <a-form-item label="价格">
                  <a-input placeholder="请输入" v-model:value="modal.form.price"></a-input>
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
                      <template v-if="modal.form.coverUrl">
                        <img :src="modal.form.coverUrl"  style="width: 60px;height: 80px;"/>
                      </template>
                      <template v-else>
                        <file-image-outlined />
                      </template>
                    </p>
                    <p class="ant-upload-text">
                      请选择要上传的封面图片
                    </p>
                  </a-upload-dragger>
                </a-form-item>
              </a-col>
              <a-col span="24">
                <a-form-item label="商品文件">
                  <a-upload-dragger
                      name="file"
                      accept=".mp4"
                      :multiple="false"
                      :before-upload="beforeUpload1"
                      v-model:file-list="fileList1"
                  >
                    <p class="ant-upload-drag-icon">
                      <video-camera-outlined />
                    </p>
                    <p class="ant-upload-text">
                      请选择要上传的文件（mp4格式）
                    </p>
                  </a-upload-dragger>
                </a-form-item>
              </a-col>
              <a-col span="24">
                <a-form-item label="内容简介">
                  <a-textarea placeholder="请输入" v-model:value="modal.form.description"></a-textarea>
                </a-form-item>
              </a-col>
              <a-col span="12">
                <a-form-item label="是否下架" name="status">
                  <a-select placeholder="请选择" allowClear v-model:value="modal.form.off_shelf">
                    <a-select-option key="0" value="false">是</a-select-option>
                    <a-select-option key="1" value="true">否</a-select-option>
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
import { FormInstance, message, SelectProps } from 'ant-design-vue';
import { createApi, listApi, updateApi, deleteApi } from '/@/api/admin/product';
import {listApi as listClassification1Api} from '/@/api/admin/classification1'
import {listApi as listClassification2Api} from '/@/api/admin/classification2'
import {listApi as listTagApi} from '/@/api/admin/tag'
import {BASE_URL} from "/@/store/constants";
import { FileImageOutlined, VideoCameraOutlined } from '@ant-design/icons-vue';
import {useAppStore, useUserStore} from "/@/store";

const userStore = useUserStore()
const appStore = useAppStore()
const isFirst = ref(true)

const columns = reactive([

  {
    title: '序号',
    dataIndex: 'id',
    key: 'id',
    width: 60
  },
  {
    title: '商品名称',
    dataIndex: 'name',
    key: 'name'
  },
  {
    title: '是否下架',
    dataIndex: 'off',
    key: 'status',
    customRender: ({ text, record, index, column }) => text === "true" ? '是' : '否'
  },
  {
    title: '所属一级分类',
    dataIndex: 'classification_1_name',
    key: 'classification_1'
  },
  {
    title: '所属二级分类',
    dataIndex: 'classification_2_name',
    key: 'classification_2'
  },
  {
    title: '简介',
    dataIndex: 'description',
    key: 'description',
    customRender: ({ text, record, index, column }) => text ? text.substring(0, 40) + '...' : '--',
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
  modal.form.imageFile = copyFile;
  return false;
};

const beforeUpload1 = (file: File) => {
  // 改商品文件名
  const fileName = new Date().getTime().toString() + '.' + file.type.substring(6);
  const copyFile = new File([file], fileName);
  console.log(copyFile);
  modal.form.rawFile = copyFile;
  return false;
};

// 文件列表
const fileList = ref<any[]>([]);
const fileList1 = ref<any[]>([]);

const submitting = ref<boolean>(false);

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
  cData: [],
  bData: [],
  tagData: [{}],
  form: {
    product_id: undefined,
    name: undefined,
    classification1: undefined,
    classification2: undefined,
    classification_1: undefined,
    classification_2: undefined,
    merchant: undefined,
    addr: undefined,
    tag: [],
    repertory: undefined,
    price: undefined,
    status: undefined,
    off_shelf: undefined,
    is_sold: undefined,
    cover: undefined,
    coverUrl: undefined,
    imageFile: undefined,
    rawFile: undefined,
    description: undefined
  },
  rules: {
    name: [{ required: true, message: '请输入名称', trigger: 'change' }],
    classification_1: [{ required: true, message: '请选择一级分类', trigger: 'change' }],
    classification_2: [{ required: true, message: '请选择二级分类', trigger: 'change' }],
    repertory: [{ required: true, message: '请输入库存', trigger: 'change' }],
    price: [{ required: true, message: '请输入定价', trigger: 'change' }],
    status: [{ required: true, message: '请选择状态', trigger: 'change' }],
  },
})

const myform = ref<FormInstance>()

onMounted(() => {
  getDataList();
  getCDataList();
  getBDataList();
  getTagDataList();
  appStore.setViewId(userStore.user_id);
})

let option2 = computed(() => {
  console.log(modal.form)
  for (let i = 0; i < appStore.classificationTree.length; i++) {
    if (modal.form.classification_1 === appStore.classificationTree[i].id) {
      console.log(appStore.classificationTree[i].children)
      return appStore.classificationTree[i].children;
    }
  }
  return null;
})

watch(option2, val => {
  console.log(val)
  if (isFirst.value) { // 后面改
    isFirst.value = false;
  } else {
    modal.form.classification_2 = val[0].id;
  }
})

const getDataList = () => {
  data.loading = true;
  listApi({
    keyword: data.keyword,
  })
      .then((res) => {
        data.loading = false
        console.log(res)
        res.data.forEach((item: any, index: any) => {
          item.index = index + 1
        })
        data.dataList = res.data
      })
      .catch((err) => {
        data.loading = false
        console.log(err)
      })
}

const getCDataList = () => {
  listClassification2Api({}).then(res => {
    modal.cData = res.data
    console.log(res.data)
  })
  console.log(modal.cData)
}
const getBDataList = () => {
  listClassification1Api({}).then(res => {
    modal.bData = res.data
  })
}
const getTagDataList = ()=> {
  listTagApi({}).then(res => {
    res.data.forEach((item, index) => {
      item.index = index + 1
    })
    modal.tagData = res.data
  })
}

const onSearchChange = (e: Event) => {
  data.keyword = e?.target?.value
  console.log(data.keyword)
};

const onSearch = () => {
  getDataList();
}

const rowSelection = ref({
  onChange: (selectedRowKeys: (string | number)[], selectedRows: DataItem[]) => {
    console.log(`selectedRowKeys: ${selectedRowKeys}`, 'selectedRows: ', selectedRows);
    data.selectedRowKeys = selectedRowKeys;
  },
})

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
  modal.form.cover = undefined
};
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
    if(record[key]) {
      modal.form[key] = record[key];
    }
  }
  modal.form.product_id = record['id']
  if(modal.form.cover) {
    modal.form.coverUrl = BASE_URL + modal.form.cover
    modal.form.cover = undefined
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
}

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
}

const handleOk = () => {
  myform.value
      ?.validate()
      .then(() => {
        const formData = new FormData();
        if(modal.editFlag) {
          formData.append('product_id', modal.form.product_id || "")
        }
        formData.append('name', modal.form.name || "")
        if (modal.form.classification_1) {
          formData.append('classification_1', modal.form.classification_1 || "")
        }
        if (modal.form.classification_2) {
          formData.append('classification_2', modal.form.classification_2 || "")
        }
        if (modal.form.addr) {
          formData.append('addr', modal.form.addr || "")
        }
        if (modal.form.merchant) {
          formData.append('merchant', modal.form.merchant || "")
        }
        if (modal.form.tag) {
          modal.form.tag.forEach(function (value) {
            if(value){
              formData.append('tag', value)
            }
          })
        }
        if (modal.form.imageFile) {
          formData.append('cover', modal.form.imageFile)
        }
        if(modal.form.rawFile) {
          formData.append('raw', modal.form.rawFile)
        }
        formData.append('description', modal.form.description || '')
        formData.append('price', modal.form.price || '')
        if (modal.form.repertory >= 0) {
          formData.append('repertory', modal.form.repertory)
        }
        if (modal.form.status) {
          formData.append('status', modal.form.status)
        }
        if (modal.editFlag) {
          submitting.value = true
          updateApi({
            product_id: modal.form.product_id
          },formData)
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
        console.log('不能为空')
      })
}

const handleCancel = () => {
  hideModal()
}

// 恢复表单初始状态
const resetModal = () => {
  myform.value?.resetFields()
  fileList.value = []
  fileList1.value = []
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
