 <template>
	<div class="detail">
	  <Header/>
		<div class="thing-infos-view">
			<div class="thing-infos">
			<div class="desc">保存二维码，方便下次登录网站</div>
			<qrcode-vue class="desc" :value="value" :size="size" :foreground="color" level="H"/>
		</div>
	  </div>
  
	  <Footer/>
	</div>
  </template>
  <script setup>
  import {message} from "ant-design-vue";
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
  import {listThingCommentsApi, createApi as createCommentApi, likeApi} from '/@/api/index/comment'
  import {addWishUserApi} from '/@/api/index/thing'
  import {addCollectUserApi} from '/@/api/index/thing'
  import {BASE_URL} from "/@/store/constants";
  import {useRoute, useRouter} from "vue-router/dist/vue-router";
  import {useUserStore} from "/@/store";
  import {getFormatTime} from "/@/utils";
  import emoji from '/@/assets/emoji'
  import { VueElement, reactive } from 'vue'
  import { UToast, createObjectURL } from 'undraw-ui'
  import { convertLegacyProps } from "ant-design-vue/es/button/buttonTypes";
  import {addCollectCanteen, detailApi as canteenDetailApi} from '/@/api/index/canteen'
  import {addCollectCounter, detailApi as counterDetailApi} from '/@/api/index/classification'
  
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
  
//   const SelfAvatar = (avatar) => {
// 	console.log(avatar)
// 	if (avatar === "null" || avatar===null) {
// 	  return false
// 	} else {
// 	  return true
// 	}
//   }
//   const toggleIsShow = (index, id) => {
// 	if (!isShow.value.has(index)) {
// 	  isShow.value.set(index, false)
// 	}
// 	console.log(isShow.value.get(index))
// 	if (last1.value == index && last2.value != id) {
  
// 	} else {
// 	  isShow.value.set(index, !isShow.value.get(index))
// 	}
// 	if (isShow.value.get(index)) {
// 	  // replyText.value = commentData.value[id].username
// 	  replyText.value = ''
// 	  if (index == id) {
// 		const replyee = commentData.value.filter(element=> element.id == id)
// 		showTarget.value = "@" + replyee[0].username + ": "
// 		console.log(replyee[0])
// 		console.log(replyee[0].username)
// 	  } else {
// 		const father = commentData.value.filter(element=> element.id == index)
// 		console.log(father[0])
// 		const replyee = father[0].replies.data.filter(element=> element.id == id)
// 		showTarget.value = "@" + replyee[0].username + ": "
// 		console.log(replyee[0])
// 		console.log(replyee[0].username)
// 	  }
// 	  for (const idx in commentData.value) {
// 		console.log(commentData.value[idx].id)
// 		if (commentData.value[idx].id != index) {
// 		  isShow.value.set(commentData.value[idx].id, false)
// 		}
// 	  }
// 	}
// 	last1.value = index
// 	last2.value = id
//   }
  
//   const toggleShowReply = (index) => {
// 	if (!showReplies.value.has(index)) {
// 	  showReplies.value.set(index, false)
// 	}
// 	showReplies.value.set(index, !showReplies.value.get(index))
//   }
  
//   onMounted(() => {
// 	thingId.value = route.query.id.trim()
// 	//getThingDetail()
// 	//getRecommendThing()
// 	getCommentList()
// 	for (const idx in commentData.value) {
// 	  isShow.value.set(idx, false)
// 	  showReplies.value.set(idx, false)
// 	}
// 	// nextTick(() => {
// 	//   for (myElementRef in replyRef) {
// 	//     const myElementRef = myElementRef.value;
// 	//     if (myElementRef) {
// 	//       console.log('获取到 ref 引用：', myElementRef);
// 	//       // 在这里可以处理 ref 引用，比如修改样式、添加事件监听等操作
// 	//     }
// 	//   }
// 	// });
//   })
  
//   const selectTab = (index) => {
// 	selectTabIndex.value = index
// 	tabUnderLeft.value = 6 + 54 * index
//   }
  
//   const getThingDetail = () => {
// 	video = detailData.value.raw == null
// 	console.log(video)
// 	thingDetailApi({id: thingId.value}).then(res => {
// 	  detailData.value = res.data
// 	  detailData.value.cover = BASE_URL + res.data.cover
  
// 	  detailData.value.raw = BASE_URL + detailData.value.raw
// 	}).catch(err => {
// 	  message.error('获取详情失败')
// 	})
//   }
//   const addToWish = () => {
// 	let username = userStore.user_name
// 	if (username) {
// 	  addWishUserApi({thingId: thingId.value, username: username}).then(res => {
// 		message.success(res.msg)
// 		getThingDetail()
// 	  }).catch(err => {
// 		console.log('操作失败')
// 	  })
// 	} else {
// 	  message.warn('请先登录')
// 	}
//   }
//   const collect = () => {
// 	let username = userStore.user_name
// 	if (username) {
// 	  console.log(thingId.value)
// 	  addCollectUserApi({thingId: thingId.value, username: username}).then(res => {
// 		message.success(res.msg)
// 		getThingDetail()
// 	  }).catch(err => {
// 		console.log('收藏菜肴失败')
// 	  })
// 	} else {
// 	  message.warn('请先登录')
// 	}
//   }
//   const type = 'thing'
//   const share = () => {
// 	let text = router.resolve({name: 'share', query: {type: type, id: thingId.value}})
// 	console.log(text)
// 	window.open(text.href, '_blank')
// 	// let content = '分享一个非常好玩的网站 ' + window.location.href
// 	// let shareHref = 'http://service.weibo.com/share/share.php?title=' + content
// 	// window.open(shareHref)
//   }
//   const handleOrder = (detailData) => {
// 	console.log(detailData)
// 	const userId = userStore.user_id
// 	router.push({
// 	  name: 'confirm',
// 	  query:
// 		  {
// 			id: detailData.id,
// 			title: detailData.title,
// 			cover: detailData.cover,
// 			price: detailData.price
// 		  }
// 	})
//   }
//   const getRecommendThing = () => {
// 	listThingList({sort: 'recommend'}).then(res => {
// 	  res.data.forEach((item, index) => {
// 		if (item.cover) {
// 		  item.cover = BASE_URL + item.cover
// 		}
// 	  })
// 	  console.log(res)
// 	  console.log(detailData)
// 	  recommendData.value = res.data.slice(0, 6)
// 	}).catch(err => {
// 	  console.log(err)
// 	})
//   }
//   const handleDetail = (item) => {
// 	// 跳转新页面
// 	let text = router.resolve({name: 'detail', query: {id: item.id}})
// 	window.open(text.href, '_blank')
//   }
//   const sendComment = () => {
// 	console.log(commentRef.value.value)
// 	let text = commentRef.value.value.trim()
// 	console.log(text)
// 	if (text.length <= 0) {
// 	  return
// 	}
// 	commentRef.value.value = ''
// 	let userId = userStore.user_id
// 	if (userId) {
// 	  createCommentApi({content: text, thing: thingId.value, user: userId}, {}).then(res => {
// 		getCommentList()
// 	  }).catch(err => {
// 		console.log(err)
// 	  })
// 	} else {
// 	  message.warn('请先登录！')
// 	  router.push({name: 'login'})
// 	}
//   }
  
//   const getReply = (parentId) => {
// 	onMounted(() => {
// 	if (!replyRef[parentId]) {
// 		replyRef[parentId] = ref
// 	}
// 	return replyRef[parentId]
// 	})
//   }
  
//   const sendReply = (parentId) => {
// 	let text = showTarget.value + replyText.value.trim()
// 	console.log(text)
// 	if (text.length <= 0) {
// 	  return
// 	}
// 	replyText.value = ''
// 	let userId = userStore.user_id
// 	if (userId) {
// 	  createCommentApi({content: text, thing: thingId.value, user: userId}, {parentId: parentId}).then(res => {
// 		getCommentList()
// 	  }).catch(err => {
// 		  console.log(err)
// 	  })
// 	} else {
// 	  message.warn('请先登录！')
// 	  router.push({name: 'login'})
// 	}
//   }
//   const like = (commentId) => {
// 	likeApi({commentId: commentId}).then(res => {
// 	  getCommentList()
// 	}).catch(err => {
// 	  console.log(err)
// 	})
//   }
//   const getCommentList = () => {
// 	listThingCommentsApi({ thingId: thingId.value, order: order.value })
// 	.then((res) => {
// 	  const commentDataCopy = [...res.data]; // Make a copy of the original data
// 	  const promises = commentDataCopy.map((item) =>
// 		// Use map to return an array of promises for fetching replies
// 		listThingCommentsApi({ parentId: item.id, order: order.value })
// 	  );
  
// 	  // Wait for all promises to resolve using Promise.all
// 	  return Promise.all(promises)
// 		.then((repliesData) => {
// 		  // Merge repliesData with the original commentDataCopy
// 		  repliesData.forEach((replies, index) => {
// 			commentDataCopy[index].replies = replies;
// 		  });
  
// 		  // Now update commentData.value with the modified data
// 		  commentData.value = commentDataCopy;
// 		  console.log(commentData.value)
// 		})
// 		.catch((err) => {
// 		  console.log(err);
// 		});
// 	})
// 	.catch((err) => {
// 	  console.log(err);
// 	});
//   }
//   const sortCommentList = (sortType) => {
// 	if (sortType === 'recent') {
// 	  sortIndex.value = 0
// 	} else {
// 	  sortIndex.value = 1
// 	}
// 	order.value = sortType
// 	getCommentList()
//   }
  
import { ref } from 'vue'
import QrcodeVue from 'qrcode.vue'
// import {useRoute} from "vue-router/dist/vue-router";
// const route = useRoute()
let content = window.location.href.slice(0,window.location.href.indexOf('index')) + "index/"
if (route.query.type=='thing') {
    content += 'detail' + '?id=' + route.query.id
} else if (route.query.type=='counter') {
    content += 'detailCounter' + '?id=' + route.query.id
} else {
    content += 'detailCanteen' + '?id=' + route.query.id
}
console.log(content)
const value = ref(content)
const position = ref('middle')
const size = ref(300)
const color = ref('#000000')

  </script>
  <style scoped lang="less">
  
  
  .thing-infos-view {
	display: flex;
	margin: 89px auto;
	position: relative;
	display: flex;
  	justify-content: center; /* 水平居中 */
  	align-items: center; /* 垂直居中 */
	//overflow: hidden;
  
	.thing-infos {
		flex:0;
		display: flex;
		flex-direction: column;
  
	  	display: -webkit-box;
		display: -ms-flexbox;
		display: flex;
		-webkit-box-align: center;
		-ms-flex-align: center;
		align-items: center;
		//overflow: hidden;
		//margin: 24px auto 16px;
		-webkit-box-pack: center;
		-ms-flex-pack: center;
		justify-content: center;
  
	  .desc {
		font-size: 14px;
		color: #1e1e1e;
	  }
	}
  
	// .mobile-share-box {
	//   height: 38px;
	//   background: transparent;
	//   padding: 0 16px;
	//   margin: 12px 0;
	//   font-size: 0;
	//   -webkit-box-align: center;
	//   -ms-flex-align: center;
	//   align-items: center;
	//   -webkit-box-pack: justify;
	//   -ms-flex-pack: justify;
	//   justify-content: space-between;
  
	//   .state {
	// 	width: 64px;
	// 	height: 24px;
	// 	line-height: 24px;
	// 	background: rgba(70, 132, 226, .1);
	// 	border-radius: 2px;
	// 	font-weight: 500;
	// 	font-size: 12px;
	// 	color: #4684e2;
	// 	text-align: center;
	//   }
  
	//   .share-img {
	// 	background: #fff;
	// 	width: 38px;
	// 	height: 38px;
	// 	border-radius: 50%;
	// 	text-align: center;
  
	// 	img {
	// 	  position: relative;
	// 	  top: 4px;
	// 	  width: 24px;
	// 	}
	//   }
	}
  
	
  </style>
  