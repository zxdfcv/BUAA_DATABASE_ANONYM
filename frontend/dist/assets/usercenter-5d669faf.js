import{H as T}from"./header-b5afe422.js";import{F as b}from"./footer-dac38197.js";import{u as H,z as M,s as N,r as v,A as q,S as D,b as p,o as i,n as a,g as s,i as e,D as E,t as P,c as h,e as y,j as C,C as V,T as U,l as R,U as j,p as z,k as L,f as k}from"./index-6b603672.js";import{A as O}from"./avatar-4ee3f7af.js";import{_ as F}from"./_plugin-vue_export-helper-c27b6911.js";import"./logo_b-9bb82155.js";import"./UserOutlined-9a8a0cdc.js";const G="/assets/order-thing-icon-f272a5ca.svg",J="/assets/order-address-icon-a6aec94c.svg",S="/assets/order-point-icon-5cda1200.svg",K="/assets/setting-icon-b7f64d0f.svg",x="/assets/setting-push-icon-24dfdd16.svg";const m=d=>(z("data-v-d63cea14"),d=d(),L(),d),Q={class:"mine-infos-view"},W={class:"info-box flex-view"},X=["src"],Y=["src"],Z={class:"name-box"},ss={class:"nick"},es={class:"age"},os={class:"order-box"},ts={class:"list"},ns=["src"],is={key:0},as={key:1},cs=["src"],rs={key:0},_s={key:1},ls=["src"],ds={key:0},us={key:1},vs={key:0,class:"setting-box"},ps={class:"list"},ms=["src"],ws=m(()=>s("span",null,"发布商品",-1)),fs=["src"],gs=m(()=>s("span",null,"商品收藏",-1)),hs=["src"],ys=m(()=>s("span",null,"我的订单",-1)),ks=["src"],xs=m(()=>s("span",null,"我的评论",-1)),Is=["src"],$s=m(()=>s("span",null,"编辑资料",-1)),Cs={__name:"mine-infos-view",setup(d){const c=H(),t=M(),I=N(),$=v(0);v(0),v(0);const w=v(!1),f=v(0);q(async()=>{$.value=t.view_user_id,await u()});const u=async()=>{(t.view_user_id===null||t.view_user_id===void 0)&&(w.value=!1);const n=await D({user_id:c.user_id});let o=[];for(var _=0;_<n.data.length;_++)o.push(n.data[_].following),n.data[_].following===t.view_user_id&&(f.value=n.data[_].id);console.log(o,o.includes(t.view_user_id)),w.value=o.includes(t.view_user_id)},g=async()=>{c.user_access?U({follower_id:t.view_user_id}).then(async n=>{console.log(n.data),await u()}).catch(n=>{console.log(n)}):R({type:"error",message:"Oops!",description:"你必须先登录才能进行关注操作！"})},A=async()=>{j({ids:f.value}).then(async n=>{console.log(n.data),await u()}).catch(n=>{console.log(n)})},r=n=>{I.push({name:n,query:{id:t.view_user_id}})};return(n,o)=>{const _=p("Button"),B=p("a-space");return i(),a("div",Q,[s("div",W,[e(t).view_user_avatar===null||e(t).view_user_avatar===void 0?(i(),a("img",{key:1,src:e(O),class:"avatar-img"},null,8,Y)):(i(),a("img",{key:0,src:e(E)+e(t).view_user_avatar,class:"avatar-img"},null,8,X)),s("div",Z,[s("h2",ss,P(e(t).view_user_username),1),s("div",es,[e(t).view_user_id!==e(c).user_id?(i(),h(B,{key:0,warp:""},{default:y(()=>[e(c).user_access===void 0||e(c).user_access===null||!e(w)?(i(),h(_,{key:0,onClick:g,style:{width:"90px"}},{default:y(()=>[C("关注 Ta")]),_:1})):(i(),h(_,{key:1,type:"primary",onClick:A,style:{width:"90px"}},{default:y(()=>[C("取消关注")]),_:1}))]),_:1})):V("",!0)])])]),s("div",os,[s("div",ts,[s("div",{class:"mine-item flex-view",onClick:o[0]||(o[0]=l=>r("wishThingView"))},[s("img",{src:e(x)},null,8,ns),e(t).view_user_id===e(c).user_id?(i(),a("span",is,"我的发布")):(i(),a("span",as,"Ta的发布"))]),s("div",{class:"mine-item flex-view",onClick:o[1]||(o[1]=l=>r("myFollow"))},[s("img",{src:e(x)},null,8,cs),e(t).view_user_id===e(c).user_id?(i(),a("span",rs,"我的关注")):(i(),a("span",_s,"Ta的关注"))]),s("div",{class:"mine-item flex-view",onClick:o[2]||(o[2]=l=>r("myFans"))},[s("img",{src:e(x)},null,8,ls),e(t).view_user_id===e(c).user_id?(i(),a("span",ds,"我的粉丝")):(i(),a("span",us,"Ta的粉丝"))])])]),e(t).view_user_id===e(c).user_id?(i(),a("div",vs,[s("div",ps,[s("div",{class:"mine-item flex-view",onClick:o[3]||(o[3]=l=>r("addProduct"))},[s("img",{src:e(S)},null,8,ms),ws]),s("div",{class:"mine-item flex-view",onClick:o[4]||(o[4]=l=>r("scoreView"))},[s("img",{src:e(S)},null,8,fs),gs]),s("div",{class:"mine-item flex-view",onClick:o[5]||(o[5]=l=>r("thingHistory"))},[s("img",{src:e(J)},null,8,hs),ys]),s("div",{class:"mine-item flex-view",onClick:o[6]||(o[6]=l=>r("commentView"))},[s("img",{src:e(G)},null,8,ks),xs]),s("div",{class:"mine-item flex-view",onClick:o[7]||(o[7]=l=>r("userInfoEditView"))},[s("img",{src:e(K),alt:"编辑资料"},null,8,Is),$s])])])):V("",!0)])}}},Vs=F(Cs,[["__scopeId","data-v-d63cea14"]]);const Ss={components:{MineInfosView:Vs,Footer:b,Header:T},data(){return{collapsed:!1}}},Fs={class:"user"},As={class:"user-content"},Bs={class:"user-content-left",style:{"margin-left":"15px","margin-top":"15px"}},Ts={class:"user-content-right"};function bs(d,c,t,I,$,w){const f=p("Header"),u=p("MineInfosView"),g=p("router-view");return i(),a("div",Fs,[k(f),s("div",As,[s("div",Bs,[k(u)]),s("div",Ts,[k(g)])])])}const Us=F(Ss,[["render",bs],["__scopeId","data-v-f5273f74"]]);export{Us as default};
