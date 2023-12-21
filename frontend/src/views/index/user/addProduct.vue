<template>
  <div class="content-list">
    <a-spin :spinning="loading">
    <div class="list-title" v-if="!modify">发布商品</div>
    <div class="list-title" v-else>修改商品</div>

      <div class="list-content">
      <div class="edit-view">
        <div class="item flex-view">
          <div class="label">商品名称</div>
          <div class="right-box">
            <input type="text" v-model="tData.form.name" placeholder="请输入商品名" maxlength="40" class="input-dom">
            <p class="tip">支持中英文，长度不能超过 40 个字符</p>
          </div>
        </div>
        <div class="item flex-view">
          <div class="label">售价</div>
          <div class="right-box">
            <a-input-number
                v-model:value="tData.form.price"
                :controls="false"
                :min="0"
                :max="9999999.99"
                :precision="2"
                prefix="￥"
                placeholder="请输入预估售价"
                style="width: 400px"/>
          </div>
        </div>

        <div class="flex-view">
          <div class="item">
          <div class="label">商品状态</div>
          </div>
          <div class="right-box" style="margin-top: 20px">
            <a-radio-group v-model:value="tData.form.status" button-style="solid">
              <a-radio-button value="A">全新</a-radio-button>
              <a-radio-button value="B">几乎全新</a-radio-button>
              <a-radio-button value="C">轻微使用痕迹</a-radio-button>
              <a-radio-button value="D">明显使用痕迹</a-radio-button>
              <a-radio-button value="E">有一定问题</a-radio-button>
            </a-radio-group>
          </div>
        </div>
        <div class="flex-view">
          <div class="item">
            <div class="label">可选校区</div>
          </div>
          <div class="right-box" style="margin-top: 20px">
            <a-radio-group v-model:value="tData.form.addr" button-style="solid">
              <a-radio-button value="1">学院路校区</a-radio-button>
              <a-radio-button value="2">沙河校区</a-radio-button>
              <a-radio-button value="3">两校区均可</a-radio-button>
            </a-radio-group>
          </div>
        </div>
        <div class="flex-view" v-if="props.modify">
          <div class="item">
            <div class="label">上架状态</div>
          </div>
          <div class="right-box" style="margin-top: 20px">
            <a-radio-group v-model:value="tData.form.off_shelve" button-style="solid">
              <a-radio-button value="0">商品上架</a-radio-button>
              <a-radio-button value="1">商品下架</a-radio-button>
            </a-radio-group>
          </div>
        </div>
        <div class="flex-view" v-if="props.modify">
          <div class="item">
            <div class="label">售出状态</div>
          </div>
          <div class="right-box" style="margin-top: 20px">
            <a-radio-group v-model:value="tData.form.is_sold" button-style="solid">
              <a-radio-button value="0">未售出</a-radio-button>
              <a-radio-button value="1">已售出</a-radio-button>
            </a-radio-group>
          </div>
        </div>
        <div class="flex-view">
          <div class="item">
            <div class="label">商品分类</div>
          </div>
          <div class="right-box" style="margin-top: 20px">
            <a-select
                v-model:value="tData.form.classification_1"
                style="width: 120px"
                :options="appStore.classificationTree"
                :field-names="{ label: 'label', value: 'id' }"
                placeholder="一级分类"
            ></a-select>
            <a-select
                v-model:value="tData.form.classification_2"
                style="width: 120px; margin-left: 20px"
                :options="option2"
                :field-names="{ label: 'label', value: 'id' }"
                placeholder="二级分类"
            ></a-select>
          </div>
        </div>
        <div class="item flex-view">
          <div class="label">商品简介</div>
          <div class="right-box">
          <textarea v-model="tData.form.description" placeholder="请输入简介" maxlength="200" class="intro">
          </textarea>
            <p class="tip">限制200字以内</p>
          </div>
        </div>
        <div class="item flex-view">
          <div class="label">商品介绍视频</div>
          <div v-if="modify">暂不支持修改商品视频</div> <!-- TODO: 增加修改商品视频、图片的功能 -->
          <div class="right-box avatar-box flex-view" v-else>
            <div class="change-tips flex-view">
              <a-upload
                  name="file"
                  accept="video/*"
                  :file-list="videoList"
                  :multiple="false"
                  :max-count="1"
                  :before-upload="beforeUploadVideo"
                  @remove="removeVideo"
              >
                <label>点击上传视频</label>
              </a-upload>
              <p class="tip">视频大小需小于 114514 MB</p>
            </div>
          </div>
        </div>
        <div class="item flex-view">
          <div class="label">商品描述图片</div>
          <div v-if="modify">暂不支持修改商品图片</div>
          <div class="right-box avatar-box flex-view" v-else>
            <div class="change-tips flex-view">
              <a-upload
                  name="file"
                  accept="image/*"
                  :multiple="true"
                  :max-count="9"
                  :file-list="imageList"
                  :before-upload="beforeUploadImage"
                  @remove="removeImage"
              >
                <label>点击上传图片</label>
              </a-upload>
              <p class="tip">图片格式支持 GIF、PNG、JPEG，尺寸不小于 200 PX，小于 4 MB</p>
            </div>
          </div>
        </div>
        <button v-if="!modify" class="save mg" @click="submit()" :loading="loading">发布商品</button>
        <button v-else class="save mg" @click="submit()" :loading="loading">修改商品</button>
      </div>
    </div>
    </a-spin>
  </div>
</template>

<script setup>
import {message} from "ant-design-vue";
import {
  userDetailApi,
  userUpdateApi,
  userPasswordApi,
  userDeleteApi
} from '/@/api/index/user'
import {BASE_URL, USER_AVATAR} from "/@/store/constants";
import {useAppStore, useUserStore} from "/@/store";
import AvatarIcon from '/@/assets/images/avatar.jpg'
import {openNotification} from "/@/utils/notice";
import {addProduct, getProductDetail, updateProduct} from "/@/api/index/product";
// console.log("visit id=", useRoute().query.id.trim())
const props = defineProps(['modify', 'mid']);
const emits = defineEmits(['close'])

const router = useRouter();
const userStore = useUserStore();
const appStore = useAppStore();

const confirmLoading = ref(false);
const open = ref(false);
const showDelete = ref(false)
const isFirst = ref(true);

let loading = ref(false)
const imageList = ref([]);
const videoList = ref([]);

let tData = reactive({
  form:{
    name: undefined,
    price: undefined,
    merchant: userStore.user_id,
    status: undefined,
    addr: undefined,
    is_sold: '0',
    off_shelve: '0',
    classification_1: undefined,
    classification_2: undefined,
    description: undefined,
  }
})
const password = reactive({})
let option2 = computed(() => {
  for (let i = 0; i < appStore.classificationTree.length; i++) {
    if (tData.form.classification_1 === appStore.classificationTree[i].id) {
      return appStore.classificationTree[i].children;
    }
  }
  return null;
});

watch(option2, val => {
  console.log(val)
  if (props.modify && isFirst.value) {
    isFirst.value = false;
  } else {
    tData.form.classification_2 = val[0].id;
  }
});

onMounted(() => {
  /* 判断当前浏览的用户是谁，无 query 默认跳自己，query 不是自己会转到该用户的公开界面 */
  if (useRoute().query.id) {
    if (useRoute().query.id.trim() !== String(userStore.user_id)) {
      router.push({name: 'wishThingView', query: {id: useRoute().query.id.trim()}}); /* TODO: router.go(-1) 时有 bug，回不到上一页 */
    }
  } else {
    router.push({name: 'userInfoEditView', query: {id: userStore.user_id}});
  }
  appStore.setViewId(userStore.user_id);
  // getUserInfo()
  if (props.modify) {
    getProductDetail({product_id: props.mid}).then(res => {
      console.log("get old data:", res.data);
      refillData(res.data);
    }).catch(err => {
      openNotification({
        type: 'error',
        message: 'Oops',
        description: '获取商品信息失败！'
      })
    });
  }
})

const beforeUploadImage = (file) => {
  const fileName = new Date().getTime().toString() + '.' + file.type.substring(6);
  const copyFile = new File([file], fileName);
  imageList.value = [...(imageList.value || []), copyFile];
  return false
}

const removeImage = (file) => {
  console.log(imageList.value);
  const index = imageList.value.indexOf(file);
  const newFileList = imageList.value.slice();
  newFileList.splice(index, 1);
  imageList.value = newFileList;
  console.log(imageList.value)
};

const beforeUploadVideo = (file) => {
  // 改文件名
  const fileName = new Date().getTime().toString() + '.' + file.type.substring(6)
  const copyFile = new File([file], fileName)
  console.log(copyFile)
  videoList.value = [...(videoList.value || []), copyFile];
  return false
}

const removeVideo = () => {
  videoList.value = []
  return true;
}

const getUserInfo = () => {
  loading.value = true
  let userId = userStore.user_id
  userDetailApi({user_id: userId}).then(res => {
    tData.form = res.data
    console.log(tData.form)
    if (tData.form.avatar) {
      userStore.user_avatar = tData.form.avatar
      tData.form.avatar = BASE_URL  + tData.form.avatar
      appStore.view_user_avatar = tData.form.avatar
      localStorage.setItem(USER_AVATAR, userStore.user_avatar)
    }
    loading.value = false
  }).catch(err => {
    console.log(err)
    loading.value = false
  })
}
const submit = () => {
  let submitForm = new FormData();
  console.log(tData.form)
  if (!tData.form.name) {
    openNotification({
      type: 'error',
      message: 'Oops',
      description: '商品名称为必填项！'
    })
    return;
  } else if (!tData.form.price) {
    openNotification({
      type: 'error',
      message: 'Oops',
      description: '商品价格为必填项！'
    })
    return;
  } else if (!tData.form.addr) {
    openNotification({
      type: 'error',
      message: 'Oops',
      description: '商品交易校区为必填项！'
    })
    return;
  } else if (!tData.form.classification_1) {
    openNotification({
      type: 'error',
      message: 'Oops',
      description: '商品一级分类为必填项！'
    })
    return;
  } else if (!tData.form.classification_2) {
    openNotification({
      type: 'error',
      message: 'Oops',
      description: '商品二级分类为必填项！'
    })
    return;
  }
  for (const key in tData.form) {
    if (tData.form[key] !== undefined) {
      console.log(key)
      if (key === "is_sold" || key==="off_shelve") {
        console.log((tData.form[key] === '1') ? 'true' : 'false')
        submitForm.append(key, (tData.form[key] === '1') ? 'true' : 'false');
      } else {
        submitForm.append(key, tData.form[key]);
      }
    }
  }
  loading.value= true;
  imageList.value.forEach(file => { submitForm.append('images', file); })
  videoList.value.forEach(file => { submitForm.append('video', file); })
  console.log(submitForm)
  if (!props.modify) {
    addProduct(submitForm).then(res => {
      loading.value = false;
      if (res.code === 0) {
        openNotification({
          type: 'success',
          message: '成功上传商品！',
          description: '您成功上传了商品 ' + tData.form.name
        })
        router.push({name: 'usercenter', query: {id: userStore.user_id }})
      } else {
        openNotification({
          type: 'error',
          message: 'Oops!',
          description: '商品创建失败！',
        })
      }
    }).catch(err => {
      loading.value = false;
      console.log(err)
      openNotification({
        type: 'error',
        message: 'Oops!',
        description: err.response.data.detail,
      })
    })
  } else {
    updateProduct({product_id: props.mid}, submitForm).then(res => {
      loading.value = false;
      if (res.code === 0) {
        openNotification({
          type: 'success',
          message: '您修改了商品信息',
          description: '更新商品信息成功！'
        })
        emits('close');
      }
    }).catch(err => {
      loading.value = false;
      console.log(err);
      openNotification({
        type: 'error',
        message: 'Oops!',
        description: '修改商品信息失败！'
      })

    });
  }
  //loading.value = false;
}

const refillData = (data) => {
  tData.form.name = data.name;
  tData.form.price = Number(data.price);
  switch (data.status) {
    case "全新": tData.form.status = "A"; break;
    case "几乎全新": tData.form.status = "B"; break;
    case "轻微使用痕迹": tData.form.status = "C"; break;
    case "明显使用痕迹": tData.form.status = "D"; break;
    case "有一定问题": tData.form.status = "E"; break;
  }
  switch (data.addr) {
    case "学院路校区": tData.form.addr = '1'; break;
    case "沙河校区": tData.form.addr = '2'; break;
    case "两校区均可": tData.form.addr = '3'; break;
  }
  tData.form.is_sold = data.is_sold ? '1' : '0';
  tData.form.off_shelve = data.off_shelve ? '1' : '0';
  tData.form.classification_1 = data.classification_1;
  tData.form.classification_2 = data.classification_2;
  tData.form.description = data.description;
}

const modifyPassword = () => {
  if (!(password.old) || !(password.new1) || !(password.new2)) {
    openNotification({
      type: 'error',
      message: '修改密码失败',
      description: '请输入字段！'
    })
  } else if (password.new1 !== password.new2) {
    openNotification({
      type: 'error',
      message: '修改密码失败',
      description: '两次输入的密码不一致！'
    })
  } else {
    userPasswordApi({user_id: userStore.user_id}, {old_password: password.old, new_password1: password.new1, new_password2: password.new2}).then(res => {
      console.log(res)
      openNotification({
        type: 'success',
        message: '修改密码成功！',
        description: res.msg
      });
      userStore.setPassword(password.new1);
        }
    ).catch(err => {
      console.log(err)
      let loger = '';
      if (err.response.data.data.old_password) {
        loger = err.response.data.data.old_password[0];
      } else if (err.response.data.data.new_password1) {
        loger = err.response.data.data.new_password1[0];
      } else if (err.response.data.data.new_password2) {
        loger = err.response.data.data.new_password2[0];
        console.log(loger)
      } else {
        loger = err.response.data.detail;
      }
      openNotification({
        type: 'error',
        message: '修改密码失败',
        description: loger
      });
    })
  }
}
</script>

<style scoped lang="less">
input, textarea {
  border-style: none;
  outline: none;
  margin: 0;
  padding: 0;
}

.flex-view {
  display: -webkit-box;
  display: -ms-flexbox;
  display: flex;
}

.content-list {
  -webkit-box-flex: 1;
  -ms-flex: 1;
  flex: 1;

  .list-title {
    color: #152844;
    font-weight: 600;
    font-size: 18px;
    line-height: 48px;
    height: 48px;
    margin-bottom: 4px;
    border-bottom: 1px solid #cedce4;
  }

  .edit-view {
    .item {
      -webkit-box-align: center;
      -ms-flex-align: center;
      align-items: center;
      margin: 24px 0;

      .label {
        width: 100px;
        color: #152844;
        font-weight: 600;
        font-size: 14px;
      }

      .right-box {
        -webkit-box-flex: 1;
        -ms-flex: 1;
        flex: 1;
      }

      .avatar {
        width: 64px;
        height: 64px;
        border-radius: 50%;
        margin-right: 16px;
      }

      .change-tips {
        -webkit-box-align: center;
        -ms-flex-align: center;
        align-items: center;
        -ms-flex-wrap: wrap;
        flex-wrap: wrap;
      }

      label {
        color: #4684e2;
        font-size: 14px;
        line-height: 22px;
        height: 22px;
        cursor: pointer;
        width: 100px;
        display: block;
      }

      .tip {
        color: #6f6f6f;
        font-size: 14px;
        height: 22px;
        line-height: 22px;
        margin: 0;
        width: 100%;
      }

      .right-box {
        -webkit-box-flex: 1;
        -ms-flex: 1;
        flex: 1;
      }

      .input-dom {
        width: 400px;
      }

      .input-dom {
        background: #f8fafb;
        border-radius: 4px;
        height: 40px;
        line-height: 40px;
        font-size: 14px;
        color: #152844;
        padding: 0 12px;
      }

      .tip {
        font-size: 12px;
        line-height: 16px;
        color: #6f6f6f;
        height: 16px;
        margin-top: 4px;
      }

      .intro {
        resize: none;
        background: #f8fafb;
        width: 80%;
        min-height: 120px;
        padding: 8px 12px;
        line-height: 22px;
        font-size: 14px;
        color: #152844;
      }
    }

    .save {
      background: #4684e2;
      border-radius: 32px;
      width: 96px;
      height: 32px;
      line-height: 32px;
      font-size: 14px;
      color: #fff;
      border: none;
      outline: none;
      cursor: pointer;
    }

    .mg {
      margin-left: 100px;
    }
  }
}

</style>
