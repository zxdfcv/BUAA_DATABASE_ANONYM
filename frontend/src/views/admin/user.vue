<template>
  <div>
    <!--页面区域-->
    <div class="page-view">
      <div class="table-operations">
        <a-space>
          <a-button type="primary" @click="exportData">导出 CSV</a-button>
          <a-button type="primary" @click="handleAdd">新增</a-button>
          <a-button @click="handleBatchDelete">批量注销</a-button>
          <a-input-search addon-before="用户名" enter-button @search="onSearch" @change="onSearchChange" />
        </a-space>
      </div>
      <a-table
        size="middle"
        rowKey="id"
        ref="tableRef"
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
        <template #bodyCell="{ text, record, index, column }"> <!-- slot 插槽的时使用 -->
          <template v-if="column.key === 'is_staff'">
            <span>
              <span v-if="text === '1'">管理员</span>
              <span v-else>普通用户</span>
            </span>
          </template>
          <template v-if="column.key === 'operation'">
            <span>
              <a @click="handleEdit(record)">编辑</a>
              <a-divider type="vertical" />
              <a-popconfirm title="确定注销?" ok-text="是" cancel-text="否" @confirm="confirmDelete(record)">
                <a href="#">注销</a>
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
        ok-text="确认"
        cancel-text="取消"
        @cancel="handleCancel"
        @ok="handleOk"
      >
        <div>
          <a-form ref="myform" :label-col="{ style: { width: '80px' } }" :model="modal.form" :rules="modal.rules">
            <a-row :gutter="24">
              <a-col span="24">
                <a-form-item label="用户名" name="username">
                  <a-input :disabled="modal.editFlag" placeholder="请输入" v-model:value="modal.form.username" allowClear />
                </a-form-item>
              </a-col>
              <a-col span="24" v-if="!modal.editFlag">
                <a-form-item label="密码" name="password">
                  <a-input placeholder="请输入" type="password" v-model:value="modal.form.password" allowClear />
                </a-form-item>
              </a-col>
              <a-col span="24">
                <a-form-item label="昵称" name="nickname">
                  <a-input placeholder="请输入" v-model:value="modal.form.nickname" allowClear />
                </a-form-item>
              </a-col>
              <a-col span="24">
                <a-form-item label="角色" name="is_staff">
                  <a-select placeholder="请选择" allowClear v-model:value="modal.form.is_staff">
                    <a-select-option key="0" :value="'1'">管理员</a-select-option>
                    <a-select-option key="1" :value="'0'">普通用户</a-select-option>
                  </a-select>
                </a-form-item>
              </a-col>
              <a-col span="24">
                <a-form-item label="状态" name="is_active">
                  <a-select placeholder="请选择" allowClear v-model:value="modal.form.is_active">
                    <a-select-option key="0" :value="'0'">封号</a-select-option>
                    <a-select-option key="1" :value="'1'">正常</a-select-option>
                  </a-select>
                </a-form-item>
              </a-col>
              <a-col span="24">
                <a-form-item label="邮箱" name="email">
                  <a-input placeholder="请输入" v-model:value="modal.form.email" allowClear />
                </a-form-item>
              </a-col>
              <a-col span="24">
                <a-form-item label="手机号" name="phone">
                  <a-input placeholder="请输入" v-model:value="modal.form.phone" allowClear />
                </a-form-item>
              </a-col>
              <a-col offset="1" span="23">
                <p slot="title">修改权限组</p>
                <a-form :label-width="40">
                  <a-form-item>
                    <a-transfer
                        :rowKey="record => record.name"
                        :list-style="{ width: '300px' }"
                        :dataSource="data.allGroups"
                        v-model:selected-keys="selectedKeys"
                        v-model:target-keys="modal.form.groups"
                        :render="item => item.name"
                        :titles="['可用分组', '当前分组']"
                        filterable
                    />
                  </a-form-item>
                </a-form>
              </a-col>
            </a-row>
          </a-form>
        </div>
      </a-modal>
    </div>
  </div>
</template>

<script setup lang="ts">
import {FormInstance, message} from 'ant-design-vue';
import {createApi, deleteApi, listApi, updateApi} from '/@/api/admin/user';
import {listApi as listGroupApi} from '/@/api/admin/group'


const columns = reactive([
    {
      title: '序号',
      dataIndex: 'id',
      key: 'id',
      align: 'center',
    },
    {
      title: '用户名',
      dataIndex: 'username',
      key: 'username',
      align: 'center',
    },
    {
      title: '昵称',
      dataIndex: 'nickname',
      key: 'nickname',
      align: 'center',
    },
    {
      title: '角色',
      dataIndex: 'is_staff',
      key: 'is_staff',
      align: 'center',
    },
    {
      title: '状态',
      dataIndex: 'is_active',
      key: 'is_active',
      align: 'center',
      customRender: ({ text, record, index, column }) => (text === '1' ? '正常' : '封号'),
    },
    {
      title: '邮箱',
      dataIndex: 'email',
      key: 'email',
      align: 'center',
    },
    {
      title: '手机号',
      dataIndex: 'phone',
      key: 'phone',
      align: 'center',
    },
    {
      title: '创建时间',
      dataIndex: 'date_joined',
      key: 'date_joined',
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

  const beforeUpload = (file: File) => {
    // 改文件名
    const fileName = new Date().getTime().toString() + '.' + file.type.substring(6);
    const copyFile = new File([file], fileName);
    console.log(copyFile);
    modal.form.image = copyFile;
    return false;
  };

  const tableRef = ref([])

  const fileList = ref([]);

  const targetKeys = ref<string[]>([]);

  const selectedKeys = ref<string[]>([]);

  // 页面数据
  const data = reactive({
    userList: [],
    allGroups: [],
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
    roleData: [
      {
        id: true,
        title: '管理员',
      },
      {
        id: false,
        title: '普通用户',
      },
    ],
    form: {
      id: undefined,
      username: undefined,
      password: undefined,
      is_staff: undefined,
      is_active: undefined,
      nickname: undefined,
      email: undefined,
      phone: undefined,
      groups: [],
      image: undefined,
      imageUrl: undefined,
      imageFile: undefined,
      imageWidth: undefined,
      imageHeight: undefined
    },
    rules: {
      username: [{ required: true, message: '请输入', trigger: 'change' }],
      password: [{ required: true, message: '请输入', trigger: 'change' }],
      is_staff: [{ required: true, message: '请选择', trigger: 'change' }],
      is_active: [{ required: true, message: '请选择', trigger: 'change' }],
    },
  });

  const myform = ref<FormInstance>();

  onMounted(() => {
    getUserList()
    getGroups()
  })

  const getGroups = () => {
    data.loading = true
    listGroupApi({})
        .then((res) => {
          data.loading = false
          console.log(res)
          res.data.forEach((item: any, index: any) => {
            item.index = index + 1
          });
          data.allGroups = res.data
          console.log(data.allGroups)
        })
        .catch((err) => {
          data.loading = false
          console.log(err)
        })
  }

  const getUserList = () => {
    data.loading = true
    listApi({
      keyword: data.keyword
    })
      .then((res) => {
        data.loading = false
        console.log(res)
        res.data.forEach((item: any, index: any) => {
          item.index = index + 1
          item.is_active = item.is_active ? '1' : '0'
          item.is_staff = item.is_staff ? '1' : '0'
          console.log(item.is_active)
        })
        data.userList = res.data
      })
      .catch((err) => {
        data.loading = false
        console.log(err)
      })
  }

  const onSearchChange = (e: Event) => {
    data.keyword = e?.target?.value
    console.log(data.keyword)
  };

  const onSearch = () => {
    getUserList();
  };

  const rowSelection = ref({
    onChange: (selectedRowKeys: (string | number)[], selectedRows: DataItem[]) => {
      console.log(`selectedRowKeys: ${selectedRowKeys}`, 'selectedRows: ', selectedRows);
      data.selectedRowKeys = selectedRowKeys;
    },
  });

  const exportData = () => {
    const csvContent = generateCsv(data.userList);
    downloadCsv(csvContent, '用户信息.csv');
  };

  const generateCsv = (data) => {
    const bom = '\uFEFF';
    const header = Object.keys(data[0]).join(',') + '\n';
    const rows = data.map(entry => {
      const values = Object.values(entry).map(value => {
        // 如果值包含逗号或数组，使用双引号括起来
        if (Array.isArray(value) || typeof value === 'string' && value.includes(',')) {
          return `"${value}"`;
        }
        return value;
      });
      return values.join(',');
    }).join('\n');

    return bom + header + rows;
  };

  const downloadCsv = (content, fileName) => {
    const blob = new Blob([content], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    link.href = url;
    link.setAttribute('download', fileName);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
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

  const confirmDelete = (record: any) => {
    console.log('delete', record);
    deleteApi({ ids: record.id })
      .then((res) => {
        getUserList();
      })
      .catch((err) => {
        message.warn(err.msg || "操作失败")
      });
  };

  const handleBatchDelete = () => {
    console.log(data.selectedRowKeys);
    if (data.selectedRowKeys.length <= 0) {
      console.log('hello');
      message.warn('请勾选注销项');
      return;
    }
    deleteApi({ ids: data.selectedRowKeys.join(',') })
      .then((res) => {
        message.success('注销成功');
        data.selectedRowKeys = [];
        getUserList();
      })
      .catch((err) => {
        message.warn(err.msg || "操作失败")
      });
  };

  const handleOk = () => {
    myform.value
      ?.validate()
      .then(() => {
        const formData = new FormData();
        if (modal.form.username) {
          formData.append('username', modal.form.username);
        }
        if (modal.form.password) {
          formData.append('password', modal.form.password);
        }
        if (modal.form.nickname) {
          formData.append('nickname', modal.form.nickname);
        }
        if (modal.form.is_staff) {
          formData.append('is_staff', modal.form.is_staff === '1' ? 'true' : 'false')
        }
        if (modal.form.is_active) {
          formData.append('is_active', modal.form.is_active === '1' ? 'true' : 'false')
        }
        if (modal.form.phone) {
          formData.append('phone', modal.form.phone);
        }
        if (modal.form.email) {
          formData.append('email', modal.form.email);
        }
        if (modal.form.groups) {
          modal.form.groups.forEach(value => {
            formData.append('groups', value);
          });
        }
        if (modal.editFlag) {
          updateApi({
            user_id: modal.form.id
          },formData)
            .then((res) => {
              hideModal();
              getUserList();
            })
            .catch((err) => {
              console.log(err);
              message.warn(err.msg || "操作失败")
            });
        } else {
          createApi(formData)
            .then((res) => {
              hideModal();
              getUserList();
            })
            .catch((err) => {
              console.log(err);
              message.warn(err.msg || "操作失败")
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
