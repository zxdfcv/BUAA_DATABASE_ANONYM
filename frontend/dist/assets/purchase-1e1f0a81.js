import{H as R}from"./header-808b5fed.js";import{p as q,c as z,a as G,g as J}from"./order-39da16d5.js";import{H as K,r as f,u as M,A as Q,D as W,l as y,b as h,o as i,c as m,e as r,f as d,g as D,i as a,n as S,B as X,F as Z,j as c,t as p,C as _,m as P}from"./index-6d07a472.js";import{a as $}from"./product-eb9e53e1.js";import{_ as Y}from"./_plugin-vue_export-helper-c27b6911.js";import"./logo_b-9bb82155.js";import"./avatar-4ee3f7af.js";import"./UserOutlined-056eb93f.js";function ee(N,b){if(N!=null){var l=parseInt(N),o=new Date(l),u=o.getFullYear(),s=o.getMonth()+1<10?"0"+(o.getMonth()+1):o.getMonth()+1,t=o.getDate()<10?"0"+o.getDate():o.getDate();if(b){var w=o.getHours()<10?"0"+o.getHours():o.getHours(),x=o.getMinutes()<10?"0"+o.getMinutes():o.getMinutes(),O=o.getSeconds()<10?"0"+o.getSeconds():o.getSeconds();return u+"-"+s+"-"+t+" "+w+":"+x+":"+O}else return u+"-"+s+"-"+t}else return""}const te={style:{top:"20px"}},ae={class:"steps-content"},oe={key:0},le={key:1,style:{"padding-top":"5%"}},re={key:2,style:{"padding-top":"15%"}},se={class:"steps-action"},ne={__name:"purchase",setup(N){const b=K(),l=f(0);M();const o=f(0),u=f(0),s=f(!1);let t=f({});const w=f(""),x=f(!1);Q(()=>{o.value=b.query.product.trim(),b.query.order_number!==null&&b.query.order_number!==void 0?(u.value=b.query.order_number.trim(),l.value=1,B()):O()});const O=async()=>{await $({product_id:o.value}).then(async e=>{console.log(e),t.value.id=e.data.id,t.value.addr=e.data.addr,t.value.cover=e.data.images,t.value.title=e.data.name,t.value.pv=e.data.views,t.value.description=e.data.description,t.value.collect_count=e.data.collectors_count,t.value.wish_count=e.data.wants;for(var n=0;n<e.data.images.length;n++)t.value.cover[n]=W+t.value.cover[n].image;t.value.onSale=!0,t.value.uploaderId=e.data.merchant,t.value.avatarUrl=e.data.merchant_avatar,t.value.uploaderName=e.data.merchant_name,t.value.Class1=e.data.classification_1_name,t.value.Class2=e.data.classification_2_name,t.value.C_1=e.data.classification_1,t.value.C_2=e.data.classification_2,t.value.createTime=e.data.create_time,t.value.price=e.data.price,x.value=!0}).catch(e=>{console.log(e),y({type:"error",message:"Oops!",description:e.msg})})},F=()=>{if(u.value!==0){l.value++;return}s.value=!0,w.value=ee(Date.now(),!0),z({product:o.value}).then(e=>{console.log(e.data),e.code===0&&(l.value++,u.value=e.data.order_number,y({type:"success",message:"订单创建成功"}),q({order_number:u.value}).then(n=>{n.code===0&&(console.log(n.data),window.open(n.data.支付url,"_blank")),s.value=!1}).catch(n=>{console.log(n),y({type:"error",message:"支付跳转失败",description:"网络问题，请点击按钮重试"}),s.value=!1}))}).catch(e=>{console.log(e),y({type:"error",message:"订单创建失败",description:"商品已被购买或不可购哦"}),s.value=!1})},B=()=>{s.value=!0,console.log(u.value),q({order_number:u.value}).then(e=>{e.code===0&&(console.log(e.data),window.open(e.data.支付url,"_blank")),s.value=!1}).catch(e=>{console.log(e),y({type:"error",message:"支付跳转失败",description:"网络问题，请点击按钮重试"}),s.value=!1})},I=()=>{G({order_number:u.value}).then(e=>{e.code===0&&y({type:"success",message:"订单取消成功"}),P.go(-1)}).catch(e=>{y({type:"error",message:"网络错误！"})})},T=()=>{s.value=!0,J({user_type:"receiver"}).then(e=>{if(e.code===0){let n=e.data;console.log(n);let v=[];for(let k=0;k<n.length;k++)if(n[k].order_number===u.value){v=n[k];break}v.length!==0&&v.status==="1"&&(console.log(v.status),l.value++)}s.value=!1}).catch(e=>{console.log(e),s.value=!1})},V=()=>{const e=M();P.push({name:"usercenter",query:{id:e.user_id}})},L=()=>{l.value--},A=[{title:"订单确认"},{title:"订单支付"},{title:"支付完成"}];return A.map(e=>({key:e.title,title:e.title})),(e,n)=>{const v=h("a-col"),k=h("a-step"),U=h("a-steps"),g=h("a-descriptions-item"),j=h("a-descriptions"),C=h("a-button"),E=h("a-row");return i(),m(E,{justify:"center"},{default:r(()=>[d(v,{span:24,style:{height:"60px"}},{default:r(()=>[d(R)]),_:1}),d(v,{span:10,style:{"padding-top":"20px"}},{default:r(()=>[D("div",te,[d(U,{current:a(l),style:{"padding-top":"60px"}},{default:r(()=>[(i(),S(Z,null,X(A,H=>d(k,{key:H.title,title:H.title},null,8,["title"])),64))]),_:1},8,["current"]),D("div",ae,[a(l)===0||a(l)===1?(i(),S("div",oe,[a(x)?(i(),m(j,{key:0,title:"订单商品详情",bordered:"",column:1},{default:r(()=>[d(g,{label:"商品名"},{default:r(()=>[c(p(a(t).title),1)]),_:1}),d(g,{label:"可提货地点"},{default:r(()=>[c(p(a(t).addr),1)]),_:1}),d(g,{label:"所属分类"},{default:r(()=>[c(p(a(t).Class1)+" 、"+p(a(t).Class2),1)]),_:1}),d(g,{label:"发布者"},{default:r(()=>[c(p(a(t).uploaderName),1)]),_:1}),d(g,{label:"发布时间"},{default:r(()=>[c(p(a(t).createTime),1)]),_:1}),d(g,{label:"订单金额"},{default:r(()=>[c(p(a(t).price)+" 元",1)]),_:1}),a(l)===1?(i(),m(g,{key:0,label:"订单提交时间"},{default:r(()=>[c(p(a(w)),1)]),_:1})):_("",!0)]),_:1})):_("",!0)])):_("",!0),a(l)===1?(i(),S("div",le,[c("请在跳转后页面完成支付后点击“我已完成支付”按钮 "),D("div",null,[d(C,{type:"primary",style:{margin:"15px"},onClick:B,loading:a(s)},{default:r(()=>[c("跳转到支付界面")]),_:1},8,["loading"])])])):_("",!0),a(l)===2?(i(),S("div",re,"您的订单已经支付完毕！")):_("",!0)]),D("div",se,[a(l)===0?(i(),m(C,{key:0,type:"primary",onClick:F,loading:a(s)},{default:r(()=>[c(p(a(u)===0?"确认提交订单":"继续提交订单"),1)]),_:1},8,["loading"])):_("",!0),a(l)===1?(i(),m(C,{key:1,onClick:L},{default:r(()=>[c("返回查看订单信息")]),_:1})):_("",!0),a(l)===1?(i(),m(C,{key:2,danger:"",style:{"margin-left":"8px"},onClick:I},{default:r(()=>[c("取消订单")]),_:1})):_("",!0),a(l)===1?(i(),m(C,{key:3,type:"primary",style:{"margin-left":"8px"},onClick:T,loading:a(s)},{default:r(()=>[c(p(a(s)===!1?"我已完成支付":"正在更新订单信息"),1)]),_:1},8,["loading"])):_("",!0),a(l)===A.length-1?(i(),m(C,{key:4,type:"primary",onClick:V},{default:r(()=>[c("返回个人中心")]),_:1})):_("",!0)])])]),_:1})]),_:1})}}},ge=Y(ne,[["__scopeId","data-v-9b2afc5c"]]);export{ge as default};
