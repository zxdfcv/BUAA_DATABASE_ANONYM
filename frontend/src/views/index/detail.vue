<template>
  <div class="home">
    <div class="detail">
      <Header />
      <div class="detail-content">
        <Card style="width:100%">
        <div class="detail-content-top">
          <div style="position: relative;">
            <div class="thing-infos-view">
              <div class="thing-infos">
                <img :src="detailData.cover" width="800" height="500">
                <div class="title">{{ detailData.title }}</div>
                <div class="meta">{{ detailData.pv }}次浏览</div>
                <div class="desc">简介：{{ detailData.description }}</div>
              </div>
              <div class="thing-counts hidden-sm">
                <div class="count-item flex-view pointer" @click="collect()">
                  <div class="count-img">
                    <img :src="RecommendIcon">
                  </div>
                  <div class="count-box flex-view">
                    <div class="count-text-box">
                      <span class="count-title">收藏</span>
                    </div>
                    <div class="count-num-box">
                      <span class="num-text">{{ detailData.collect_count }}</span>
                    </div>
                  </div>
                </div>
                <div class="count-item flex-view pointer" @click="addToWish()">
                  <div class="count-img">
                    <img :src="WantIcon">
                  </div>
                  <div class="count-box flex-view">
                    <div class="count-text-box">
                      <span class="count-title">吃过</span>
                    </div>
                    <div class="count-num-box">
                      <span class="num-text">{{ detailData.wish_count }}</span>
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
                      <img :src="WeixinShareIcon" class="mg-l">
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
                <div style="margin-top: 24px;" v-if="adData">
                  <!--广告区域-->
                  <img style="width: 250px;height: 100px;background-size: cover;object-fit: cover;" src="" />
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="detail-content-bottom">
          <div class="thing-content-view flex-view">
            <div class="main-content">
              <div class="order-view main-tab">
                <span class="tab" :class="selectTabIndex === index ? 'tab-select' : ''" v-for="(item, index) in tabData"
                  :key="index" @click="selectTab(index)">
                  {{ item }}
                </span>
              </div>



              <div class="thing-comment">
                <div class="title">发表新的评论</div>
                <div class="publish flex-view">
                  <img v-if="SelfAvatar(userStore.user_avatar)" :src="BASE_URL + userStore.user_avatar" class="mine-img">
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
                      <img v-if="SelfAvatar(item.user_avatar.avatar)" :src="BASE_URL + item.user_avatar.avatar"
                        class="avator" @click="toggleIsShow(item.id, item.id)">
                      <img v-else :src="AvatarIcon" class="avator" @click="toggleIsShow(item.id, item.id)">
                      <div class="person">
                        <div class="name">{{ item.username }}</div>
                        <div class="time">{{ item.comment_time }}</div>
                      </div>
                      <div class="float-right">
                        <span @click="toggleIsShow(item.id, item.id)">回复</span>
                        <span @click="like(item.id)">点赞</span>
                        <span class="num">{{ item.like_count }}</span>
                      </div>

                    </div>
                    <p class="comment-content">{{ item.content }}</p>
                    <div v-if="item.reply_count > 0">
                      <div class="publish flex-view">
                        <div class="count-text">
                          <span>共有{{ item.reply_count }}条回复，</span>
                          <span class="more-btn-sub" @click="toggleShowReply(item.id)">点击查看</span>
                        </div>
                      </div>
                      <div v-if=showReplies.get(item.id)>
                        <div class="comment-item-sub" v-for="reply in item.replies.data">
                          <div class="flex-item flex-view">
                            <img v-if=SelfAvatar(reply.user_avatar.avatar) :src="BASE_URL + reply.user_avatar.avatar"
                              class="avator" @click="toggleIsShow(item.id, reply.id)">
                            <img v-else :src="AvatarIcon" class="avator" @click="toggleIsShow(item.id, reply.id)">
                            <div class="person">
                              <div class="name">{{ reply.username }}</div>
                              <div class="time">{{ reply.comment_time }}</div>
                            </div>
                            <div class="float-right">
                              <span @click="toggleIsShow(item.id, reply.id)">回复</span>
                              <span @click="like(reply.id)">推荐</span>
                              <span class="num">{{ reply.like_count }}</span>
                            </div>
                          </div>
                          <p class="comment-content-sub">{{ reply.content }}</p>
                        </div>
                      </div>
                    </div>
                    <!-- <button class="float-right send-btn" @click="toggleReplies(item)">回复</button> -->
                    <div v-if="isShow.get(item.id)" class="publish flex-view">
                      <textarea :placeholder="showTarget" class="content-input-sub" v-model="replyText"></textarea>
                      <button class="send-btn-sub" @click="sendReply(item.id)">发送</button>
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

            </div>
            <div class="recommend" style="">
              <div class="title">热门推荐</div>
              <div class="things">
                <div v-for="item in recommendData" :key="item.id" @click="handleDetail(item)"
                  class="thing-item item-column-3"><!---->
                  <div class="img-view">
                    <img :src="item.cover">
                    <!-- <div style="position: absolute; left: 10px; bottom: 10px;">
                    <img :src="PlayIcon" style="width: 30px;height: 30px;">
                  </div> -->
                  </div>
                  <div class="info-view">
                    <h3 class="thing-name">{{ item.title.substring(0, 12) }}</h3>
                    <span style="color: #444; font-size: 11px;height: 11px;">{{ item.create_time.substring(0, 16) }}</span>
                    <br />
                    <span style="color: #444; font-size: 11px;height: 11px;">{{ item.pv }}次浏览</span>
                  </div>
                </div>
              </div>
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
import WeixinShareIcon from '/@/assets/images/weixin-share.svg';
import { message } from "ant-design-vue";
import Header from '/@/views/index/components/header.vue'
import Footer from '/@/views/index/components/footer.vue'
import AddIcon from '/@/assets/images/add.svg';
import WantIcon from '/@/assets/images/want-read-hover.svg';
import RecommendIcon from '/@/assets/images/recommend-hover.svg';
import ShareIcon from '/@/assets/images/share-icon.svg';
import WeiboShareIcon from '/@/assets/images/wb-share.svg';
import AvatarIcon from '/@/assets/images/avatar.jpg';
import PlayIcon from '/@/assets/images/Play.png'

import {
  detailApi as thingDetailApi,
  listApi as listThingList
} from '/@/api/index/thing'
import { listThingCommentsApi, createApi as createCommentApi, likeApi } from '/@/api/index/comment'
import { addWishUserApi } from '/@/api/index/thing'
import { addCollectUserApi } from '/@/api/index/thing'
import { BASE_URL } from "/@/store/constants";
import { useRoute, useRouter } from "vue-router/dist/vue-router";
import { useUserStore } from "/@/store";
import { getFormatTime } from "/@/utils";
import emoji from '/@/assets/emoji'
import { VueElement, reactive } from 'vue'
import { UToast, createObjectURL } from 'undraw-ui'
import { addCollectCounter, detailApi as counterDetailApi } from '/@/api/index/classification'

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
let recommendData = ref([])
let sortIndex = ref(0)
let order = ref('recent') // 默认排序最新

let commentRef = ref()

let replyRef = reactive({})

let video = ref()

let isShow = ref(new Map())

let last1 = ref(-1)
let last2 = ref(-1)

const replyText = ref('')

// const comments = ref(commentData.map(comment => ({ ...comment, showReplies: false})));

let showTarget = ref('')

let showReplies = ref(new Map())

const SelfAvatar = (avatar) => {
  console.log(avatar)
  if (avatar === "null" || avatar === null) {
    return false
  } else {
    return true
  }
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
      showTarget.value = "@" + replyee[0].username + ": "
      console.log(replyee[0])
      console.log(replyee[0].username)
    } else {
      const father = commentData.value.filter(element => element.id == index)
      console.log(father[0])
      const replyee = father[0].replies.data.filter(element => element.id == id)
      showTarget.value = "@" + replyee[0].username + ": "
      console.log(replyee[0])
      console.log(replyee[0].username)
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

onMounted(() => {
  thingId.value = route.query.id.trim()
  getThingDetail()
  getRecommendThing()
  getCommentList()
  for (const idx in commentData.value) {
    isShow.value.set(idx, false)
    showReplies.value.set(idx, false)
  }
  // nextTick(() => {
  //   for (myElementRef in replyRef) {
  //     const myElementRef = myElementRef.value;
  //     if (myElementRef) {
  //       console.log('获取到 ref 引用：', myElementRef);
  //       // 在这里可以处理 ref 引用，比如修改样式、添加事件监听等操作
  //     }
  //   }
  // });
})

const selectTab = (index) => {
  selectTabIndex.value = index
  tabUnderLeft.value = 6 + 54 * index
}

const getThingDetail = () => {
  video = detailData.value.raw == null
  console.log(video)
  thingDetailApi({ id: thingId.value }).then(res => {
    detailData.value = res.data
    detailData.value.cover = BASE_URL + res.data.cover

    detailData.value.raw = BASE_URL + detailData.value.raw
  }).catch(err => {
    message.error('获取详情失败')
  })
}
const addToWish = () => {
  let username = userStore.user_name
  if (username) {
    addWishUserApi({ thingId: thingId.value, username: username }).then(res => {
      message.success(res.msg)
      getThingDetail()
    }).catch(err => {
      console.log('操作失败')
    })
  } else {
    message.warn('请先登录')
  }
}
const collect = () => {
  let username = userStore.user_name
  if (username) {
    console.log(thingId.value)
    addCollectUserApi({ thingId: thingId.value, username: username }).then(res => {
      message.success(res.msg)
      getThingDetail()
    }).catch(err => {
      console.log('收藏菜肴失败')
    })
  } else {
    message.warn('请先登录')
  }
}
const type = 'thing'
const share = () => {
  let text = router.resolve({ name: 'share', query: { type: type, id: thingId.value } })
  console.log(text)
  window.open(text.href, '_blank')
  // let content = '分享一个非常好玩的网站 ' + window.location.href
  // let shareHref = 'http://service.weibo.com/share/share.php?title=' + content
  // window.open(shareHref)
}
const handleOrder = (detailData) => {
  console.log(detailData)
  const userId = userStore.user_id
  router.push({
    name: 'confirm',
    query:
    {
      id: detailData.id,
      title: detailData.title,
      cover: detailData.cover,
      price: detailData.price
    }
  })
}
const getRecommendThing = () => {
  listThingList({ sort: 'recommend' }).then(res => {
    res.data.forEach((item, index) => {
      if (item.cover) {
        item.cover = BASE_URL + item.cover
      }
    })
    console.log(res)
    console.log(detailData)
    recommendData.value = res.data.slice(0, 6)
  }).catch(err => {
    console.log(err)
  })
}
const handleDetail = (item) => {
  // 跳转新页面
  let text = router.resolve({ name: 'detail', query: { id: item.id } })
  window.open(text.href, '_blank')
}
const sendComment = () => {
  console.log(commentRef.value.value)
  let text = commentRef.value.value.trim()
  console.log(text)
  if (text.length <= 0) {
    return
  }
  commentRef.value.value = ''
  let userId = userStore.user_id
  if (userId) {
    createCommentApi({ content: text, thing: thingId.value, user: userId }, {}).then(res => {
      getCommentList()
    }).catch(err => {
      console.log(err)
    })
  } else {
    message.warn('请先登录！')
    router.push({ name: 'login' })
  }
}

const getReply = (parentId) => {
  onMounted(() => {
    if (!replyRef[parentId]) {
      replyRef[parentId] = ref
    }
    return replyRef[parentId]
  })
}

const sendReply = (parentId) => {
  let text = showTarget.value + replyText.value.trim()
  console.log(text)
  if (text.length <= 0) {
    return
  }
  replyText.value = ''
  let userId = userStore.user_id
  if (userId) {
    createCommentApi({ content: text, thing: thingId.value, user: userId }, { parentId: parentId }).then(res => {
      getCommentList()
    }).catch(err => {
      console.log(err)
    })
  } else {
    message.warn('请先登录！')
    router.push({ name: 'login' })
  }
}
const like = (commentId) => {
  likeApi({ commentId: commentId }).then(res => {
    getCommentList()
  }).catch(err => {
    console.log(err)
  })
}
const getCommentList = () => {
  listThingCommentsApi({ thingId: thingId.value, order: order.value })
    .then((res) => {
      const commentDataCopy = [...res.data]; // Make a copy of the original data
      const promises = commentDataCopy.map((item) =>
        // Use map to return an array of promises for fetching replies
        listThingCommentsApi({ parentId: item.id, order: order.value })
      );

      // Wait for all promises to resolve using Promise.all
      return Promise.all(promises)
        .then((repliesData) => {
          // Merge repliesData with the original commentDataCopy
          repliesData.forEach((replies, index) => {
            commentDataCopy[index].replies = replies;
          });

          // Now update commentData.value with the modified data
          commentData.value = commentDataCopy;
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
  background: url("https://s1.ax1x.com/2023/07/30/pPp2re1.jpg") center center no-repeat;
  background-size: 100% 100%;
  position: absolute; //绝对定位
}


.hide {
  display: none;
}

.detail-content {
  display: flex;
  flex-direction: column;
  width: 1100px;
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
  display: flex;
  margin: 89px 0 16px;
  overflow: hidden;

  .thing-infos {
    flex: 1;
    display: flex;
    flex-direction: column;

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
  -ms-flex: 0 0 235px;
  flex: 0 0 235px;
  margin-left: 20px;

  .title {
    font-weight: 600;
    font-size: 18px;
    line-height: 26px;
    color: #152844;
    margin-bottom: 12px;
  }

  .things {
    border-top: 1px solid #cedce4;


    .thing-item {
      min-width: 250px;
      max-width: 250px;
      position: relative;
      flex: 1;
      margin-right: 20px;
      height: fit-content;
      overflow: hidden;
      margin-top: 26px;
      margin-bottom: 36px;
      cursor: pointer;
      box-shadow: 4px 4px 4px rgba(200, 200, 200, 0.3), -4px 4px 4px rgba(200, 200, 200, 0.3);


      .img-view {
        //text-align: center;
        position: relative;
        height: 160px;
        width: 250px;

        img {
          height: 160px;
          width: 250px;
          margin: 0 auto;
          background-size: cover;
          object-fit: cover;
        }
      }

      .info-view {
        //background: #f6f9fb;
        overflow: hidden;
        padding: 16px 16px;

        .thing-name {
          line-height: 32px;
          color: #0F1111;
          font-size: 20px;
        }

        .price {
          color: #ff7b31;
          font-size: 20px;
          line-height: 20px;
          margin-top: 4px;
          overflow: hidden;
          text-overflow: ellipsis;
          white-space: nowrap;
        }

        .translators {
          color: #6f6f6f;
          font-size: 12px;
          line-height: 14px;
          margin-top: 4px;
          overflow: hidden;
          text-overflow: ellipsis;
          white-space: nowrap;
        }
      }
    }

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
