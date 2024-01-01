<template>
  <div class="home">
    <div class="detail">
      <Header />
      <div class="detail-content">
        <Card style="width:100%">
        <div class="detail-content-top">
          <div style="position: relative; ">
            <div class="thing-infos-view">
              <div class="thing-infos" >
<!--                <img :src="detailData.cover" width="1000" height="500">-->
                <div>
                  <el-row>
                    <el-col :span="15">
                  <Carousel
                      v-model="value"
                      dots="outside"
                      :radius-dot=false
                      trigger="hover"
                      arrow="hover"
                      style="width: 100%">
                    <CarouselItem v-for="(item, index) in detailData.cover" :key="index"
                    style="height: 600px;">
                      <div :style="{
                        backgroundImage: 'url(' + item + ')',
                        backgroundPosition: 'center center',
                        backgroundRepeat: 'no-repeat',
                        backgroundSize: 'contain',
                        width: '100%',
                        height: '100%'
                      }"></div>
                    </CarouselItem>
                  </Carousel></el-col>
                    <el-col :offset="2" :span="7">
                      <div class="" style="margin: 35px">
                        <div class="count-item flex-view pointer" @click="addCollect()">
                          <div class="count-img">
                            <img :src="Collect_on" v-if="detailData.isCollected === true">
                            <img :src="Collect_off" v-else>
                          </div>
                          <div class="count-box flex-view">
                            <div class="count-text-box">
                              <span class="count-title">收藏</span>
                            </div>
                            <div class="count-num-box" style="margin-right: 35px">
                              <span class="num-text">{{ detailData.collect_count }}</span>
                            </div>
                          </div>
                        </div>
                        <div class="count-item flex-view pointer" @click="raiseChat">
                          <div class="count-img">
                            <img :src="Like_off" >
                          </div>
                          <div class="count-box flex-view">
                            <div class="count-text-box">
                              <span class="count-title">我想要</span> <!-- TODO: 添加按钮跳转到 socket 聊天室 -->
                            </div>
                            <div class="count-num-box" style="margin-right: 35px">
                            </div>
                          </div>
                        </div>
                        <div class="count-item flex-view" @click="share()">
                          <div class="count-img">
                            <img :src="ShareIcon">
                          </div>
                          <div class="count-box flex-view">
                            <div class="count-text-box">
                              <span class="count-title">分享</span>
                            </div>
                            <div class="count-num-box">
                              <span class="num-text"></span>
                              <img :src="WeixinShareIcon" class="mg-l" style="margin-right: 35px">
                            </div>
                          </div>
                          <!-- <div class="count-item flex-view" @click="share()">
                        <div class="count-img">
                          <img :src="ShareIcon">
                        </div>
                        <div class="count-box flex-view">
                          <div class="count-text-box">
                            <span class="count-title">分享</span>
                          </div>
                          <div class="count-num-box">
                            <span class="num-text"></span>
                            <img :src="WeiboShareIcon" class="mg-l">
                          </div>
                        </div> -->
                        </div>
                        <a-card style="margin: 15px; cursor: default;" hoverable>
                          <a-descriptions title="商品信息" :column="1" style="vertical-align: center; font-size: large; overflow-y: auto; max-height: 400px">
                            <a-descriptions-item label="商品名称">
                              <div>{{ detailData.title }}</div>
                            </a-descriptions-item>
                            <a-descriptions-item label="发布者">
                              <a-avatar
                                v-if="!(detailData.avatarUrl === '' || detailData.avatarUrl === null || detailData.avatarUrl === undefined)"
                                style="cursor: pointer"
                                :size="40"
                                :src="BASE_URL + '/upload/' + detailData.avatarUrl"
                                @click="router.push({ name: 'usercenter', query:{id: detailData.uploaderId}})"/>
                              <a-avatar
                                v-else
                                :src="AvatarIcon"
                                style="cursor: pointer" />
                              <a-button type="link" @click="router.push({ name: 'usercenter', query:{id: detailData.uploaderId}})" style="top: -13px; left: -7px">{{ detailData.uploaderName }}</a-button>
                            </a-descriptions-item>

                            <a-descriptions-item label="分类所属">
                              <a-space direction="vertical">
                              <a-space wrap>
                                <a-button type="primary" shape="round" @click="router.push({name: 'search', query: {keyword: detailData.Class1, type:'C_1'}});">{{ detailData.Class1 }}</a-button>
                                <a-button type="primary" shape="round" @click="router.push({name: 'search', query: {keyword: detailData.Class2, type:'C_2'}});">{{ detailData.Class2 }}</a-button>
                              </a-space>
                              <a-space wrap>
                                <a-button type="primary" shape="round" @click="router.push({name: 'search', query: {
                                  keyword: detailData.addr,
                                  type:'addr'}});">{{ detailData.addr }}</a-button>
                                <a-button type="primary" shape="round" @click="router.push({name: 'search', query: {
                                  keyword: detailData.status, type:'status'}});">{{ detailData.status }}</a-button>
                              </a-space>
                              </a-space>
                            </a-descriptions-item>
                            <a-descriptions-item label="浏览量">
                              <div>{{ detailData.pv }}</div>
                            </a-descriptions-item>
                            <a-descriptions-item label="发布时间">
                              <div>{{ detailData.createTime }}</div>
                            </a-descriptions-item>
                            <a-descriptions-item label="商品价格">
                              <div>{{ detailData.price }} 元</div>
                            </a-descriptions-item>
                            <a-descriptions-item label="在售状态" v-if="detailData.is_sold || detailData.off_shelve">
                              <div>
                                <a-button danger shape="round" v-if="detailData.is_sold">已售出</a-button>
                                <a-button shape="round" v-else-if="detailData.off_shelve">已下架</a-button>
                              </div>
                            </a-descriptions-item>

                          </a-descriptions>
                        </a-card>
                        <div style="margin-top: 24px;" v-if="adData">
                          <!--广告区域-->
                          <img style="width: 250px;height: 100px;background-size: cover;object-fit: cover;" src="" />
                        </div>
                      </div>
                    </el-col>
                  </el-row>

                </div>
                <div class="desc">商品简介：</div>
                <div class="desc" style="font-size: 18px">{{ detailData.description }}</div>
              </div>
            </div>
          </div>
        </div>
        <div class="detail-content-bottom">
          <div class="thing-content-view flex-view">
            <div class="main-content">


              <div class="detail-content-bottom">
                <div class="thing-content-view flex-view">
                  <div class="main-content">
                    <div class="order-view main-tab" >
                <span class="tab" :class="selectTabIndex === index ? 'tab-select' : ''" v-for="(item, index) in tabData"
                  :key="index" @click="selectTab(index)">
                  {{ item }}
                </span>
              </div>
                    <div class="thing-comment" >
                      <div class="title">发表新的评论</div>
                      <div class="publish flex-view">
                        <img v-if="userStore.user_avatar !== null && userStore.user_avatar !== undefined && userStore.user_avatar !== ''" :src="BASE_URL + userStore.user_avatar" class="mine-img">
                        <img v-else :src="AvatarIcon" class="mine-img">
                        <textarea placeholder="说点什么..." class="content-input" ref="commentRef"></textarea>
                        <button class="send-btn" @click="sendComment()">发送</button>
                      </div>
                      <div class="tab-view flex-view">
                        <div class="count-text">共有{{ commentData.length }}条评论</div>
                        <div class="tab-box flex-view" v-if="commentData.length > 0">
                          <span :class="sortIndex === 0 ? 'tab-select' : ''" @click="sortCommentList('recent')">最新</span>
                          <div class="line"></div>
                          <span :class="sortIndex === 1 ? 'tab-select' : ''" @click="sortCommentList('hot')">热门</span>
                        </div>
                      </div>
                      <div class="comments-list">
                        <div class="comment-item" v-for="item in commentData">
                          <div class="flex-item flex-view">
                            <img v-if="item.user_avatar !== null && item.user_avatar !== undefined && item.user_avatar !== ''" :src="BASE_URL + '/upload/' + item.user_avatar"
                                 class="avator" @click="pushToTarget(item.user)">
                            <img v-else :src="AvatarIcon" class="avator" @click="pushToTarget(item.user)">
                            <div class="person">
                              <div class="name" @click="pushToTarget(item.user)">{{ item.user_name }}</div>
                              <div class="time">{{ item.create_time }}</div>
                            </div>
                            <div class="float-right">
                              <ButtonGroup>
                                <Button @click="toggleIsShow(item.id, item.id)"  style="width: 80px"><Icon type="md-chatboxes" style="margin-left: -3px"/> 回复&nbsp;&nbsp;&nbsp;</Button>
                                <Button type="primary" v-if="item.liked" @click="dislike(item.id)" style="width: 80px"><Icon type="md-thumbs-up" /> {{ item.likes_count }}</Button>
                                <Button v-else @click="like(item.id)" style="width: 80px"><Icon type="md-thumbs-up" /> {{ item.likes_count }}</Button>
                              </ButtonGroup>
                            </div>

                          </div>
                          <p class="comment-content">{{ item.content }}</p>
                          <div v-if="item.reply_count > 0">
                            <div class="publish flex-view">
                              <div class="count-text" style="text-align: center">
                                <span>共有{{ item.reply_count }}条回复，</span>
                                <span class="more-btn-sub" @click="toggleShowReply(item.id)" v-if="showReplies.get(item.id) !== true"><a>点击查看</a></span>
                                <span class="more-btn-sub" @click="toggleShowReply(item.id)" v-else><a>点击收折</a></span>
                              </div>
                            </div>
                            <div v-if=showReplies.get(item.id)>
                              <div class="comment-item-sub" v-for="reply in item.replies">
                                <div class="flex-item flex-view">
                                  <img v-if="reply.user_avatar !== null && reply.user_avatar !== undefined && reply.user_avatar !== ''" :src="BASE_URL + '/upload/' + reply.user_avatar"
                                       class="avator" @click="toggleIsShow(item.id, reply.id)">
                                  <img v-else :src="AvatarIcon" class="avator" @click="pushToTarget(reply.user)">
                                  <div class="person">
                                    <div class="name" @click="pushToTarget(reply.user)">{{ reply.user_name }}</div>
                                    <div class="time">{{ reply.comment_time }}</div>
                                  </div>
                                  <div class="float-right">
                                    <ButtonGroup>
                                      <Button @click="toggleIsShow(item.id, reply.id)"  style="width: 70px"><Icon type="md-chatboxes" style="font-size: 10px"/> 回复&nbsp;&nbsp;&nbsp;</Button>
                                      <Button type="primary" v-if="reply.liked" @click="dislikeReply(reply.id)" style="width: 70px"><Icon type="md-thumbs-up" /> {{ reply.likes_count }}</Button>
                                      <Button v-else @click="likeReply(reply.id)" style="width: 70px"><Icon type="md-thumbs-up" /> {{ reply.likes_count }}</Button>
                                    </ButtonGroup>
                                    <span class="num">{{ reply.like_count }}</span>
                                  </div>
                                </div>
                                <p class="comment-content-sub">
                                  <a @click="pushToTarget(reply.mentioned_user)">@{{ reply.mentioned_name }}&nbsp;&nbsp;</a>{{ reply.content }}
                                </p>
                              </div>
                            </div>
                          </div>
                          <!-- <button class="float-right send-btn" @click="toggleReplies(item)">回复</button> -->
                          <div v-if="isShow.get(item.id)" class="publish flex-view">
                            <textarea :placeholder="showTarget" class="content-input-sub" v-model="replyText"></textarea>
                            <button class="send-btn-sub" @click="sendReply(item.id, item)">发送</button>
                          </div>
                        </div>
                        <div class="infinite-loading-container">
                          <div class="infinite-status-prompt" style="">
                            <div slot="no-results" class="no-results">
                              <div></div>
                              <p>没有更多了</p>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>


<!-- TODO: 考虑用 a-comment 重写评论部分-->

                  </div></div></div></div>
            <div class="recommend" style="">
              <div class="title">热门推荐</div>
              <ShopItemCard
                  v-for="(item, index) in recommendData.value"
                  :key="index"
                  :shop-card="item"
                  :loading="false"
                  style="margin: 5%;" />
            </div>
          </div>
        </div>
      </Card>
      </div>
      <Footer />
    </div>
  </div>
</template>
<script setup>
import WeixinShareIcon from "/@/assets/images/weixin-share.svg";
import { message } from "ant-design-vue";
import Header from "/@/views/index/components/header.vue";
import Footer from "/@/views/index/components/footer.vue";
import ShareIcon from "/@/assets/images/share-icon.svg";
import AvatarIcon from "/@/assets/images/avatar.jpg";
import Collect_on from "/@/assets/images/collect_on.png";
import Collect_off from "/@/assets/images/collect_off.png";
import Like_off from "/@/assets/images/like_off.png";
import {
  createCommentApi,
  createReplyApi,
  dislikeCommentApi,
  dislikeReplyApi,
  likeCommentApi,
  likeReplyApi,
  queryCommentReplyApi,
  queryLoggedCommentReplyApi,
  queryLoggedProductCommentApi,
  queryProductCommentApi
} from "/@/api/index/comment";
import { BASE_URL } from "/@/store/constants";
import { useRoute, useRouter } from "vue-router/dist/vue-router";
import { useUserStore, useWebSocketStore } from "/@/store";
import { reactive } from "vue";
import { addToCollect, deleteFromCollect, getProductDetail, getProductList } from "/@/api/index/product";
import { openNotification } from "/@/utils/notice";
import { getCollectList } from "/@/api/index/user";
import ShopItemCard from "/@/views/index/components/ShopItemCard.vue";

const router = useRouter()
const route = useRoute()
const userStore = useUserStore();

let adData = ref()

let thingId = ref('')
let detailData = ref({})
let tabUnderLeft = ref(6)
let tabData = ref(['评论'])
let selectTabIndex = ref(0)

let commentData = ref([])
const recommendData = reactive([])
let sortIndex = ref(0)
let order = ref('create_time') // 默认排序最新

let commentRef = ref()

let replyRef = reactive({})

let value = ref(0);

let isShow = ref(new Map())

let last1 = ref(-1)
let last2 = ref(-1)

const replyText = ref('')
const replyId = ref(0)
// const comments = ref(commentData.map(comment => ({ ...comment, showReplies: false})));

let showTarget = ref('')

let showReplies = ref(new Map())

const pushToTarget = (targetId) => {
  console.log(targetId)
  router.push({name: 'usercenter', query: {id: targetId}})
}

const toggleIsShow = (index, id) => {
  if (!isShow.value.has(index)) {
    isShow.value.set(index, false)
  }
  console.log(isShow.value.get(index))
  if (last1.value == index && last2.value != id) {

  } else {
    isShow.value.set(index, !isShow.value.get(index))
  }
  if (isShow.value.get(index)) {
    // replyText.value = commentData.value[id].username
    replyText.value = ''
    if (index == id) {
      const replyee = commentData.value.filter(element => element.id == id)
      showTarget.value = "@" + replyee[0].user_name + ": "
      replyId.value = replyee[0].user;
      console.log(replyee[0])
      console.log(replyee[0].user_name)
    } else {
      const father = commentData.value.filter(element => element.id == index)
      console.log(father[0])
      const replyee = father[0].replies.filter(element => element.id == id)
      showTarget.value = "@" + replyee[0].user_name + ": "
      replyId.value = replyee[0].user;
      console.log(replyee[0])
      console.log(replyee[0].user_name)
    }
    for (const idx in commentData.value) {
      console.log(commentData.value[idx].id)
      if (commentData.value[idx].id != index) {
        isShow.value.set(commentData.value[idx].id, false)
      }
    }
  }
  last1.value = index
  last2.value = id
}

const toggleShowReply = (index) => {
  if (!showReplies.value.has(index)) {
    showReplies.value.set(index, false)
  }
  showReplies.value.set(index, !showReplies.value.get(index))
}

const getPostDetail = async () => {
  await getProductDetail({product_id: thingId.value}).then(async res => {
    console.log(res.data)
    detailData.value['is_sold'] = res.data.is_sold;
    detailData.value['off_shelve'] = res.data.off_shelve;
    detailData.value['id'] = res.data.id;
    detailData.value['cover'] = res.data.images;
    detailData.value['title'] = res.data.name;
    detailData.value['pv'] = res.data.views;
    detailData.value['description'] = res.data.description;
    detailData.value['collect_count'] = res.data.collectors_count;
    detailData.value['wish_count'] = res.data.wants; /* TODO: 缺少是否卖出/下架在前端的展示点 */
    for (var i = 0; i < res.data.images.length; i++) {
      detailData.value['cover'][i] = BASE_URL + detailData.value['cover'][i].image;
    }
    let collecter = [];
    if (userStore.user_access) {
      getCollectList({}).then(res2 => {
        const collect = res2.data;
        if (res2.code === 0) {
          for (var i = 0; i < collect.length; i++) {
            collecter.push(collect[i].id);
          }
        }
        detailData.value['isCollected'] = (userStore.user_access) ? (collecter.includes(Number(res.data.id))) : false;
      })
    } else {
      detailData.value['isCollected'] = false;
    }
    detailData.value['isWanted'] = (userStore.user_access) ? false : false;
    detailData.value['onSale'] = true;
    detailData.value["uploaderId"] = res.data.merchant;
    detailData.value["avatarUrl"] = res.data.merchant_avatar;
    detailData.value["uploaderName"] = res.data.merchant_name;
    detailData.value["Class1"] = res.data.classification_1_name;
    detailData.value["Class2"] = res.data.classification_2_name;
    detailData.value["C_1"] = res.data.classification_1;
    detailData.value["C_2"] = res.data.classification_2;
    detailData.value["createTime"] = res.data.create_time;
    detailData.value['addr'] = res.data.addr;
    detailData.value['status'] = res.data.status;
    detailData.value['price'] = res.data.price;
  }).catch(err => {
    openNotification({
      type: 'error',
      message: 'Oops!',
      description: err.msg
    })
  });
}

const fillData = (list) => {
  var res = [];
  for (var i = 0; i < list.length; i++) {
    var item = list[i];
    var data = {};
    data['name'] = item.name;
    data["id"] = item.id;
    data["price"] = item.price;
    data["url"] = (item.images.length !== 0) ? BASE_URL + item.images[0].image : null; /* TODO: 服务器端可以默认配置一个缺省的图片 url */
    data["avatarUrl"] = item.merchant_avatar; /* TODO: 缺少一个上传者的 avatar_URL */
    data["uploaderId"] = item.merchant;
    data["uploaderName"] = item.merchant_name;
    data["pv"] = item.views;
    data["off_shelve"] = item.off_shelve;
    data["is_sold"] = item.is_sold;
    res.push(data);
  }
  return [res, res.length];
}

const getRecommendPost = async () => {
    getProductList({limit: 5}).then(res => {
      if (res.code === 0) {
        [ recommendData.value, length ] = fillData(res.data.results);
      } else {
        openNotification({
          type: 'error',
          message: 'Oops!',
          description: res.msg
        })
      }
      console.log(recommendData.value)
    }).catch(err => {
      openNotification({
        type: 'error',
        message: 'Oops!',
        description: err.msg
      })
    });
}

onMounted(async () => {
  thingId.value = route.query.id.trim()
  await getPostDetail();
  await getRecommendPost();
  console.log("mounted")
  // getRecommendThing()
  getCommentList()
  for (const idx in commentData.value) {
    isShow.value.set(idx, false)
    showReplies.value.set(idx, false)
  }
})

const selectTab = (index) => {
  selectTabIndex.value = index
  tabUnderLeft.value = 6 + 54 * index
}

const raiseChat = () => {
  if (detailData.value.is_sold || detailData.value.off_shelve) {
    openNotification({
      type: 'error',
      message: 'Oops!',
      description: "当前商品不允许购买！",
    })
    return;
  }
  if (userStore.user_access) {
    /* TODO: addWantedProductApi here userId/name, productId, state(ONLY ADD) */
    detailData.value.isWanted = true;
    router.push({name: 'chatpage'});
    useWebSocketStore().modifySession(detailData.value);
    // getPostDetail();
  } else {
    openNotification({
      type: 'error',
      message: 'Oops!',
      description: "请先登录！",
    })
  }
}

const addCollect = async () => {
  if (userStore.user_access) {
    if (detailData.value.isCollected === true) {
      await deleteFromCollect({ids: detailData.value.id}).catch();
    } else {
      await addToCollect({product_id: detailData.value.id}).catch();
    }
    await getPostDetail().catch();
  } else {
    openNotification({
      type: 'error',
      message: 'Oops!',
      description: "请先登录！",
    })
  }
}

const type = 'thing'
const share = () => {
  let text = router.resolve({ name: 'share', query: { type: type, id: thingId.value } })
  console.log(text)
  window.open(text.href, '_blank')
}

const sendComment = () => {
  console.log(commentRef.value.value)
  let text = commentRef.value.value.trim()
  console.log(text)
  if (text.length <= 0) {
    openNotification({
      type: 'error',
      message: '评论发送失败',
      description: '评论文字不能为空！'
    })
    return;
  }
  commentRef.value.value = ''
  if (userStore.user_access) {
    createCommentApi({ content: text, product: thingId.value, user: String(userStore.user_id) }).then(res => {
      getCommentList()
      if (res.data.code === 0) {
        openNotification({
          type: 'success',
          message: '评论发送成功',
          description: ''
        })
      }
    }).catch(err => {
      console.log(err)
    })
  } else {
    openNotification({
      type: 'error',
      message: '您尚未登陆',
      description: '评论前需要登录！'
    })
    router.push({ name: 'login' })
  }
}

const sendReply = (parentId) => {
  let text = replyText.value.trim()
  if (text.length <= 0) {
    openNotification({
      type: 'error',
      message: '回复发送失败',
      description: '回复的内容不能为空！'
    })
    return
  }
  replyText.value = ''
  let userId = userStore.user_id
  if (userId) {
    console.log(userId, parentId, text)
    createReplyApi({user: String(userId), comment: parentId, content: text, mentioned_user: replyId.value}).then(res => {
      getCommentList()
    }).catch(err => {
      console.log(err)
    })
  } else {
    message.warn('请先登录！')
    router.push({ name: 'login' })
  }
}

const like = async (commentId) => {
  if (userStore.user_access) {
    const res = await likeCommentApi({comment_id: commentId});
    if (res.code === 0) {
      console.log(res)
    }
    getCommentList();
  } else {
    openNotification({
      type: 'error',
      message: '您尚未登陆',
      description: '点赞前需要登录！'
    })
    await router.push({name: 'login'})
  }
}

const likeReply = async (replyId) => {
  if (userStore.user_access) {
    const res = await likeReplyApi({reply_id: replyId});
    if (res.code === 0) {
      console.log(res)
    }
    getCommentList();
  } else {
    openNotification({
      type: 'error',
      message: '您尚未登陆',
      description: '点赞前需要登录！'
    })
    await router.push({name: 'login'})
  }
}

const dislike = async (commentId) => {
  if (userStore.user_access) {
    const res = await dislikeCommentApi({comment_id: commentId});
    if (res.code === 0) {
      console.log(res)
    }
    getCommentList(commentId);
  } else {
    openNotification({
      type: 'error',
      message: '您尚未登陆',
      description: '点赞前需要登录！'
    })
    await router.push({name: 'login'})
  }
}

const dislikeReply = async (replyId) => {
  if (userStore.user_access) {
    const res = await dislikeReplyApi({reply_id: replyId});
    if (res.code === 0) {
      console.log(res)
    }
    getCommentList();
  } else {
    openNotification({
      type: 'error',
      message: '您尚未登陆',
      description: '点赞前需要登录！'
    })
    await router.push({name: 'login'})
  }
}

const getCommentList = () => {
  if (userStore.user_access) {
    queryLoggedProductCommentApi({ product_id: thingId.value, sort: order.value })
      .then((res) => {
        const commentDataCopy = [...res.data]; // Make a copy of the original data
        const promises = commentDataCopy.map((item) =>
          // Use map to return an array of promises for fetching replies
          queryLoggedCommentReplyApi({ comment_id: item.id, sort: order.value })
        );

        // Wait for all promises to resolve using Promise.all
        return Promise.all(promises)
          .then((repliesData) => {
            // Merge repliesData with the original commentDataCopy
            repliesData.forEach((replies, index) => {
              commentDataCopy[index].replies = replies.data;
              // for (let i = 0; i < commentDataCopy[index].replies.length; i++) {
              //   commentDataCopy[index].replies[i]['isLiked'] = !!commentDataCopy[index].replies[i].likes.includes(userStore.user_id);
              // }
            });

            // Now update commentData.value with the modified data
            commentData.value = commentDataCopy;
            // for (let i = 0; i < commentData.value.length; i++) {
            //   commentData.value[i]['isLiked'] = !!commentData.value[i].likes.includes(userStore.user_id);
            // }
            console.log(commentData.value)
          })
          .catch((err) => {
            console.log(err);
          });
      })
      .catch((err) => {
        console.log(err);
      });
  } else {
    queryProductCommentApi({ product_id: thingId.value, sort: order.value })
      .then((res) => {
        const commentDataCopy = [...res.data]; // Make a copy of the original data
        const promises = commentDataCopy.map((item) =>
          // Use map to return an array of promises for fetching replies
          queryCommentReplyApi({ comment_id: item.id, sort: order.value })
        );

        // Wait for all promises to resolve using Promise.all
        return Promise.all(promises)
          .then((repliesData) => {
            // Merge repliesData with the original commentDataCopy
            repliesData.forEach((replies, index) => {
              commentDataCopy[index].replies = replies.data;
              // for (let i = 0; i < commentDataCopy[index].replies.length; i++) {
              //   commentDataCopy[index].replies[i]['isLiked'] = !!commentDataCopy[index].replies[i].likes.includes(userStore.user_id);
              // }
            });

            // Now update commentData.value with the modified data
            commentData.value = commentDataCopy;
            // for (let i = 0; i < commentData.value.length; i++) {
            //   commentData.value[i]['isLiked'] = !!commentData.value[i].likes.includes(userStore.user_id);
            // }
            console.log(commentData.value)
          })
          .catch((err) => {
            console.log(err);
          });
      })
      .catch((err) => {
        console.log(err);
      });
  }
}

const sortCommentList = (sortType) => {
  if (sortType === 'recent') {
    sortIndex.value = 0
  } else {
    sortIndex.value = 1
  }
  order.value = sortType
  getCommentList()
}

</script>

<style scoped lang="less">
.home {
  z-index: 0;
  width: 100%;
  min-height: 100vh;
  background: #dae6f9;
  background-size: 100% 100%;
  position: absolute; //绝对定位
}


.hide {
  display: none;
}

.detail-content {
  display: flex;
  flex-direction: column;
  width: 80%;
  margin: 4px auto;
}

.flex-view {
  display: -webkit-box;
  display: -ms-flexbox;
  display: flex;
}

.hidden-lg {
  display: none !important;
}

.thing-infos-view {
  //display: flex;
  margin: 89px 0 16px;
  overflow: hidden;

  .thing-infos {
    //flex: 1;
    //display: flex;
    //flex-direction: column;

    .title {
      margin-top: 16px;
      font-size: 24px;
      font-weight: 400;
      color: #1e1e1e;
    }

    .meta {
      font-size: 12px;
      color: #1e1e1e;
    }

    .desc {
      width: 800px;
      margin-top: 10px;
      font-size: 14px;
      color: #1e1e1e;
    }
  }

  .mobile-share-box {
    height: 38px;
    background: transparent;
    padding: 0 16px;
    margin: 12px 0;
    font-size: 0;
    -webkit-box-align: center;
    -ms-flex-align: center;
    align-items: center;
    -webkit-box-pack: justify;
    -ms-flex-pack: justify;
    justify-content: space-between;

    .state {
      width: 64px;
      height: 24px;
      line-height: 24px;
      background: rgba(70, 132, 226, .1);
      border-radius: 2px;
      font-weight: 500;
      font-size: 12px;
      color: #4684e2;
      text-align: center;
    }

    .share-img {
      background: #fff;
      width: 38px;
      height: 38px;
      border-radius: 50%;
      text-align: center;

      img {
        position: relative;
        top: 4px;
        width: 24px;
      }
    }
  }

  .thing-img-box {
    -webkit-box-flex: 0;
    -ms-flex: 0 0 235px;
    flex: 0 0 235px;
    margin: 0 40px 0 0;

    img {
      width: 200px;
      height: 186px;
      display: block;
    }
  }

  .thing-info-box {
    text-align: left;
    padding: 0;
    margin: 0;
  }

  .thing-state {
    height: 26px;
    line-height: 26px;

    .state {
      font-weight: 500;
      color: #4684e2;
      background: rgba(70, 132, 226, .1);
      border-radius: 2px;
      padding: 5px 8px;
      margin-right: 16px;
    }

    span {
      font-size: 14px;
      color: #152844;
    }
  }

  .thing-name {
    line-height: 32px;
    margin: 16px 0;
    color: #0F1111 !important;
    font-size: 15px !important;
    font-weight: 400 !important;
    font-style: normal !important;
    text-transform: none !important;
    text-decoration: none !important;
  }

  .translators,
  .authors {
    line-height: 18px;
    font-size: 14px;
    margin: 8px 0;
    -webkit-box-align: start;
    -ms-flex-align: start;
    align-items: flex-start;
    -webkit-box-pack: start;
    -ms-flex-pack: start;
    justify-content: flex-start;

    .name {
      color: #315c9e;
      white-space: normal;
    }
  }

  .tags {
    position: absolute;
    bottom: 20px;
    margin-top: 16px;

    .category-box {
      color: #152844;
      font-size: 14px;

      .title {
        color: #787878;
      }
    }
  }

  .thing-counts {
    -webkit-box-flex: 0;
    -ms-flex: 0 0 235px;
    flex: 0 0 235px;
    margin-left: 20px;
  }

  .pointer {
    cursor: pointer;
  }

  .count-item {
    height: 64px;
    -webkit-box-align: center;
    -ms-flex-align: center;
    align-items: center;
    cursor: pointer;
  }

  .count-img {
    -webkit-box-flex: 0;
    -ms-flex: 0 0 32px;
    flex: 0 0 32px;
    margin-right: 24px;
    font-size: 0;

    img {
      width: 100%;
      display: block;
    }
  }

  .count-box {
    position: relative;
    border-bottom: 1px solid #cedce4;
    -webkit-box-align: center;
    -ms-flex-align: center;
    align-items: center;
    -webkit-box-pack: justify;
    -ms-flex-pack: justify;
    justify-content: space-between;
    -webkit-box-flex: 1;
    -ms-flex: 1;
    flex: 1;
    height: 100%;
  }

  .count-text-box {
    font-size: 0;

    .count-title {
      color: #152844;
      font-weight: 600;
      font-size: 16px;
      line-height: 18px;
      display: block;
      height: 18px;
    }
  }

  .count-text-box {
    font-size: 0;

    .count-title {
      color: #152844;
      font-weight: 600;
      font-size: 16px;
      line-height: 18px;
      display: block;
      height: 18px;
    }
  }

  .count-num-box {
    font-weight: 600;
    font-size: 20px;
    line-height: 24px;
    color: #152844;
  }
}

.buy-btn {
  cursor: pointer;
  display: block;
  background: #4684e2;
  border-radius: 4px;
  text-align: center;
  color: #fff;
  font-size: 14px;
  height: 36px;
  line-height: 36px;
  width: 110px;
  outline: none;
  border: none;
  margin-top: 18px;
}

.buy-btn img {
  width: 12px;
  margin-right: 2px;
  vertical-align: middle;
}

.buy-btn span {
  vertical-align: middle;
}

.buy-way {
  overflow: hidden;

  .title {
    font-weight: 600;
    font-size: 18px;
    height: 26px;
    line-height: 26px;
    color: #152844;
    margin-bottom: 12px;
  }
}

.thing-content-view {
  margin-top: 4px;
  padding-bottom: 50px;
}

.main-content {
  -webkit-box-flex: 1;
  -ms-flex: 1;
  flex: 1;
  padding-right: 16px;

  .text {
    color: #484848;
    font-size: 16px;
    line-height: 26px;
    padding-left: 12px;
    margin: 11px 0;
    white-space: pre-wrap;
  }
}

.main-tab {
  border-bottom: 1px solid #cedce4;
}

.order-view {
  position: relative;
  color: #6c6c6c;
  font-size: 14px;
  line-height: 40px;

  .title {
    margin-right: 8px;
  }

  .tab {
    margin-right: 20px;
    cursor: pointer;
    color: #5f77a6;
    font-size: 16px;
    cursor: pointer;
  }

  .tab-select {
    color: #152844;
    font-weight: 600;
  }

  .tab-underline {
    position: absolute;
    bottom: 0;
    left: 84px;
    width: 16px;
    height: 4px;
    background: #4684e2;
    -webkit-transition: left .3s;
    transition: left .3s;
  }
}

.recommend {
  -webkit-box-flex: 0;
  -ms-flex: 0 0 460px;
  flex: 0 0 460px;
  margin-left: 20px;

  .title {
    font-weight: 600;
    font-size: 18px;
    line-height: 26px;
    color: #152844;
    margin-bottom: 12px;
  }

}

.flex-view {
  display: flex;
}

.thing-comment {
  .title {
    font-weight: 600;
    font-size: 14px;
    line-height: 22px;
    height: 22px;
    color: #152844;
    margin: 24px 0 12px;
  }

  .publish {
    -webkit-box-align: center;
    -ms-flex-align: center;
    align-items: center;

    .mine-img {
      -webkit-box-flex: 0;
      -ms-flex: 0 0 40px;
      flex: 0 0 40px;
      margin-right: 12px;
      border-radius: 50%;
      width: 40px;
      height: 40px;
    }

    .content-input {
      -webkit-box-flex: 1;
      -ms-flex: 1;
      flex: 1;
      background: #f6f9fb;
      border-radius: 4px;
      height: 48px;
      line-height: 16px;
      color: #484848;
      padding: 5px 12px;
      white-space: nowrap;
      outline: none;
      border: 0px;
      resize: none;
      outline: none;
    }

    .content-input-sub {
      -webkit-box-flex: 1;
      -ms-flex: 1;
      flex: 1;
      background: #f6f9fb;
      border-radius: 4px;
      height: 64px;
      line-height: 16px;
      color: #484848;
      padding: 5px 12px;
      white-space: nowrap;
      outline: none;
      border: 0px;
      margin-left: 70px;
      resize: none;
      outline: none;
    }

    .send-btn {
      margin-left: 10px;
      background: #4684e2;
      border-radius: 4px;
      -webkit-box-flex: 0;
      -ms-flex: 0 0 80px;
      flex: 0 0 80px;
      color: #fff;
      font-size: 14px;
      text-align: center;
      height: 48px;
      line-height: 48px;
      outline: none;
      border: 0px;
      cursor: pointer;
    }

    .more-btn-sub {
      color: #63aad4;
      background-color: #fff;
      border: 0px;

    }

    :hover {
      // color: lightblue;
      color: var(--text3);
    }

    .send-btn-sub {
      margin-left: 10px;
      background: #4684e2;
      border-radius: 4px;
      -webkit-box-flex: 0;
      -ms-flex: 0 0 80px;
      flex: 0 0 80px;
      color: #fff;
      font-size: 14px;
      text-align: center;
      height: 64px;
      line-height: 32px;
      outline: none;
      border: 0px;
      cursor: pointer;
    }
  }

  .tab-view {
    -webkit-box-pack: justify;
    -ms-flex-pack: justify;
    justify-content: space-between;
    font-size: 14px;
    -webkit-box-align: center;
    -ms-flex-align: center;
    align-items: center;
    margin: 24px 0;

    .count-text {
      color: #484848;
      float: left;
    }

    .tab-box {
      color: #5f77a6;
      -webkit-box-align: center;
      -ms-flex-align: center;
      align-items: center;

      .tab-select {
        color: #152844;
      }

      span {
        cursor: pointer;
      }
    }

    .line {
      width: 1px;
      height: 12px;
      margin: 0 12px;
      background: #cedce4;
    }
  }

  .tab-view-sub {
    -webkit-box-pack: justify;
    -ms-flex-pack: justify;
    justify-content: space-between;
    font-size: 14px;
    -webkit-box-align: center;
    -ms-flex-align: center;
    align-items: center;
    margin: 8px 50px;

    .count-text {
      color: #484848;
      float: left;
    }

    .count-text-sub {
      color: #484848;
      float: left;
    }


    .tab-box {
      color: #5f77a6;
      -webkit-box-align: center;
      -ms-flex-align: center;
      align-items: center;

      .tab-select {
        color: #152844;
      }

      span {
        cursor: pointer;
      }
    }

    .line {
      width: 1px;
      height: 12px;
      margin: 0 12px;
      background: #cedce4;
    }
  }
}


.comments-list {
  .comment-item {
    .flex-item {
      -webkit-box-align: center;
      -ms-flex-align: center;
      align-items: center;
      padding-top: 16px;

      .avator {
        -webkit-box-flex: 0;
        -ms-flex: 0 0 40px;
        flex: 0 0 40px;
        width: 40px;
        height: 40px;
        margin-right: 12px;
        border-radius: 50%;
        cursor: pointer;
      }

      .person {
        -webkit-box-flex: 1;
        -ms-flex: 1;
        flex: 1;
      }

      .name {
        color: #152844;
        font-weight: 600;
        font-size: 14px;
        line-height: 22px;
        height: 22px;
        cursor: pointer;
      }

      .time {
        color: #5f77a6;
        font-size: 12px;
        line-height: 16px;
        height: 16px;
        margin-top: 2px;
      }

      .float-right {
        color: #4684e2;
        font-size: 14px;
        float: right;

        span {
          margin-left: 19px;
          cursor: pointer;
        }

        .num {
          color: #152844;
          margin-left: 6px;
          cursor: auto;
        }
      }
    }
  }

  .comment-item-sub {
    //统一右移动18px
    // background-color: lightpink;

    .flex-item {
      -webkit-box-align: center;
      -ms-flex-align: center;
      align-items: center;
      padding-top: 12px;

      .avator {
        -webkit-box-flex: 0;
        -ms-flex: 0 0 40px;
        flex: 0 0 24px;
        width: 24px;
        height: 24px;
        margin-right: 12px;
        border-radius: 50%;
        cursor: pointer;
        margin-left: 36px;
      }

      .person {
        -webkit-box-flex: 1;
        -ms-flex: 1;
        flex: 1;
      }

      .name {
        color: #152844;
        font-weight: 600;
        font-size: 14px;
        line-height: 28px;
        height: 22px;
        cursor: pointer;
        //margin-left: 18px;
      }

      .time {
        color: #5f77a6;
        font-size: 12px;
        line-height: 16px;
        height: 16px;
        margin-top: 2px;
        // /margin-left: 18px;
      }

      .float-right {
        color: #4684e2;
        font-size: 14px;
        float: right;

        span {
          margin-left: 19px; //19 + 18px
          cursor: pointer;
        }

        .num {
          color: #152844;
          margin-left: 6px;
          cursor: auto;
        }
      }
    }
  }
}

.comment-content {
  margin-top: 8px;
  color: #484848;
  font-size: 14px;
  line-height: 22px;
  padding-bottom: 16px;
  border-bottom: 1px dashed #cedce4;
  margin-left: 52px;
  overflow: hidden;
  word-break: break-word;
}

.comment-content-sub {
  margin-top: 8px;
  color: #484848;
  font-size: 14px;
  line-height: 22px;
  padding-bottom: 16px;
  border-bottom: 1px dashed #63aad4;
  margin-left: 70px;
  overflow: hidden;
  word-break: break-word;
}

.infinite-loading-container {
  clear: both;
  text-align: center;
}

.a-price-symbol {
  top: -0.5em;
  font-size: 12px;
}

.a-price {
  color: #0F1111;
  font-size: 21px;
}</style>
