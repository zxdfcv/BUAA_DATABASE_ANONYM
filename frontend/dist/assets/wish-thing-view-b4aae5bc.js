import{d as x,u as D,a as S,z as B,k as I,B as V,r as v,o as n,b as c,e as t,l as b,x as L,F as E,n as N,t as d,y as h,f as _,c as R,m as A,p as F,g as T,h as U}from"./index-68c43909.js";import{g as $,r as q}from"./canteen-54e19167.js";import{_ as z}from"./_plugin-vue_export-helper-c27b6911.js";const m=l=>(F("data-v-064a698a"),l=l(),T(),l),M={class:"content-list"},j=m(()=>t("div",{class:"list-title"},"食堂收藏",-1)),G=m(()=>t("div",{role:"tablist",class:"list-tabs-view flex-view"},null,-1)),H={class:"list-content"},J={class:"collect-thing-view"},K={class:"thing-list flex-view"},O=["onClick"],P=["onClick"],Q=["src"],W={class:"info-view"},X={class:"thing-name"},Y={key:0,class:"authors"},Z={key:1,class:"translators"},ee=x({__name:"wish-thing-view",setup(l){const g=U(),p=D(),i=S({collectData:[]}),r=B(!1);I(()=>{u()});const f=o=>{let e=g.resolve({name:"detailCanteen",query:{id:o.id}});window.open(e.href,"_blank")},w=o=>{let e=p.user_name;q({username:e,canteenId:o.id}).then(a=>{A.success("移除成功"),u()}).catch(a=>{console.log(a)})},u=()=>{r.value=!0;let o=p.user_name;$({username:o}).then(e=>{e.data.forEach(a=>{a.cover=V+a.cover}),console.log(e.data),i.collectData=e.data,r.value=!1}).catch(e=>{console.log(e.msg),r.value=!1})};return(o,e)=>{const a=v("a-empty"),C=v("a-spin");return n(),c("div",M,[j,G,t("div",H,[t("div",J,[b(C,{spinning:_(r),style:{"min-height":"200px"}},{default:L(()=>[t("div",K,[(n(!0),c(E,null,N(_(i).collectData,(s,k)=>(n(),c("div",{class:"thing-item item-column-3",key:k},[t("div",{class:"remove",onClick:y=>w(s)},"移出",8,O),t("div",{class:"img-view",onClick:y=>f(s)},[t("img",{src:s.cover},null,8,Q)],8,P),t("div",W,[t("h3",X,d(s.title),1),s.author?(n(),c("p",Y,d(s.author)+"（作者)",1)):h("",!0),s.translator?(n(),c("p",Z,d(s.translator)+"（译者）",1)):h("",!0)])]))),128)),!_(i).collectData||_(i).collectData.length<=0?(n(),R(a,{key:0,style:{width:"100%","margin-top":"200px"}})):h("",!0)])]),_:1},8,["spinning"])])])])}}});const oe=z(ee,[["__scopeId","data-v-064a698a"]]);export{oe as default};