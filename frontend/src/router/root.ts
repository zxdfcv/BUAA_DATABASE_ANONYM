// 路由表
const constantRouterMap = [
  // ************* 前台路由 **************
  {
    path: '/',
    redirect: '/index'
  },
  {
    path: '/index',
    name: 'index',
    redirect: '/portal',
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('/@/views/index/login.vue')
  },
  {
    path: '/portal',
    name: 'portal',
    component: () => import('/@/views/index/portal.vue')
  },
  {
    path: '/share',
    name: 'share',
    component: () => import('/@/views/index/share.vue')
  },
  {
    path: '/detail',
    name: 'detail',
    component: () => import('/@/views/index/detail.vue')
  },
  {
    path: '/purchase',
    name: 'purchase',
    component: () => import('/@/views/index/purchase.vue')
  },
  {
    path: '/search',
    name: 'search',
    component: () => import('/@/views/index/search.vue')
  },
  {
    path: '/chatpage',
    name: 'chatpage',
    component: () => import('/@/views/index/chat.vue')
  },
  {
    path: '/welcome',
    name: 'welcome',
    component: () => import('/@/views/index/welcome.vue')
  },
  {
    path: '/usercenter',
    name: 'usercenter',
    redirect: '/usercenter/wishThingView',
    component: () => import('/@/views/index/usercenter.vue'),
    children: [
      {
        path: 'wishThingView',
        name: 'wishThingView',
        component: () => import('/@/views/index/user/wish-thing-view.vue')
      },
      {
        path: 'thingHistory',
        name: 'thingHistory',
        component: () => import('/@/views/index/user/thingHistory.vue')
      },
      {
        path: 'userInfoEditView',
        name: 'userInfoEditView',
        component: () => import('/@/views/index/user/userinfo-edit-view.vue')
      },
      {
        path: 'scoreView',
        name: 'scoreView',
        component: () => import('/src/views/index/user/ItemCollection.vue')
      },
      {
        path: 'commentView',
        name: 'commentView',
        component: () => import('/@/views/index/user/comment-view.vue')
      },
      {
        path: 'myFollow',
        name: 'myFollow',
        component: () => import('/@/views/index/user/MyFollow.vue')
      },
      {
        path: 'myFans',
        name: 'myFans',
        component: () => import('/@/views/index/user/MyFans.vue')
      },
      {
        path: 'addProduct',
        name: 'addProduct',
        component: () => import('/@/views/index/user/addProduct.vue')
      },
    ]
  },
  {
    path: '/createProductView',
    name: 'createProductView',
    component: () => import('/@/views/index/createProductView.vue')
  },
  {
    path: '/adminLogin',
    name: 'adminLogin',
    component: () => import('/@/views/admin/admin-login.vue'),
  },
  {
    path: '/admin',
    name: 'admin',
    redirect: '/admin/product',
    component: () => import('/@/views/admin/main.vue'),
    children: [
      { path: 'overview', name: 'overview', component: () => import('/@/views/admin/overview.vue') },
      { path: 'product', name: 'product', component: () => import('/@/views/admin/product.vue') },
      { path: 'comment', name: 'comment', component: () => import('/@/views/admin/comment.vue') },
      { path: 'reply', name: 'reply', component: () => import('/@/views/admin/reply.vue') },
      { path: 'chat', name: 'chat', component: () => import('/@/views/admin/chat.vue') },
      { path: 'user', name: 'user', component: () => import('/@/views/admin/user.vue') },
      { path: 'classification1', name: 'classification1', component: () => import('/@/views/admin/classification1.vue') },
      { path: 'classification2', name: 'classification2', component: () => import('/@/views/admin/classification2.vue') },
      { path: 'tag', name: 'tag', component: () => import('/@/views/admin/tag.vue') },
      { path: 'notice', name: 'notice', component: () => import('/@/views/admin/notice.vue') },
      { path: 'loginLog', name: 'loginLog', component: () => import('/@/views/admin/login-log.vue') },
      { path: 'opLog', name: 'opLog', component: () => import('/@/views/admin/op-log.vue') },
      { path: 'errorLog', name: 'errorLog', component: () => import('/@/views/admin/error-log.vue') },
      { path: 'sysInfo', name: 'sysInfo', component: () => import('/@/views/admin/sys-info.vue') },
      { path: 'permission', name: 'permission', component: () => import('/@/views/admin/permission.vue') },
      { path: 'order', name: 'order', component: () => import('/@/views/admin/order.vue') }
    ]
  },
  {
    path: '/:catchAll(.*)',
    name: '404',
    component: () => import('/@/views/admin/404.vue')
  }
];

export default constantRouterMap;
