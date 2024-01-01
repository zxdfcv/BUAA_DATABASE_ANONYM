import{d as F,r as m,w as G,H as O,b as a,o,c as l,e as t,h as v,j as c,C as b,n as p,i as r,f as i,g as _,t as C,D as T,q as B,m as w,u as L,l as z,p as J,k as K}from"./index-6b603672.js";import{c as Q,d as W}from"./product-5385049e.js";import{A as X}from"./avatar-4ee3f7af.js";import Y from"./addProduct-a83f796c.js";import{_ as Z}from"./_plugin-vue_export-helper-c27b6911.js";const $="/assets/placeHolder-a39aeb05.svg",ee="/assets/failedHolder-16f82c57.svg",oe=u=>(J("data-v-0e2b09a1"),u=u(),K(),u),te=["src"],se=["src"],ae={style:{height:"90px"}},le={style:{"font-size":"18px","white-space":"nowrap",overflow:"hidden","text-overflow":"ellipsis"}},re={class:"info-view"},ie={key:0,class:"price"},ne=["onClick"],de={style:{color:"#444","font-size":"13px",width:"100px","white-space":"nowrap",overflow:"hidden","text-overflow":"ellipsis","margin-left":"8px"}},ce={key:2,style:{color:"#444","font-size":"11px","margin-left":"50px","margin-top":"-5px"}},pe={key:2,class:"wrap"},ue=oe(()=>_("p",null,"真的要删除这个商品吗，这个操作不可恢复！",-1)),fe=F({__name:"ShopItemCard",props:["shopCard","loading","deletable","editable"],emits:["deleteCollecter"],setup(u,{emit:y}){const e=u,h=m(!1),U=m(!1),n=m(!1),f=m(!1),N=()=>{n.value=!0},H=()=>{f.value=!0},A=()=>{w.push({name:"detail",query:{id:e.shopCard.id}})},D=async()=>{await W({ids:e.shopCard.id}),y("deleteCollecter",e.shopCard.id)},E=()=>{w.push({name:"usercenter",query:{id:e.shopCard.uploaderId}})},V=async()=>{h.value=!0;let d=new FormData;d.append("merchant",L().user_id),Q({product_id:e.shopCard.id},d).then(s=>{s.code===0&&z({type:"success",message:"成功删除商品",description:"成功删除商品！"}),h.value=!1,n.value=!1,y("deleteCollecter",e.shopCard.id)}).catch(s=>{console.log(s),z({type:"error",message:"Oops!",description:s}),h.value=!1,n.value=!1})},j=()=>{f.value=!1,y("deleteCollecter")},q=d=>{d.target.src=ee};return G(O(),(d,s)=>{w.go(0)}),(d,s)=>{const g=a("Button"),x=a("el-tag"),I=a("el-avatar"),M=a("ButtonGroup"),P=a("a-spin"),S=a("a-modal"),R=a("a-card");return o(),l(R,{hoverable:"",style:{cursor:"default"},onClick:A},{cover:t(()=>[e.deletable?(o(),l(g,{key:0,type:"error",shape:"circle",icon:"md-close",style:{position:"absolute",right:"10px",top:"40px",width:"fit-content"},onClick:v(D,["stop"])},{default:t(()=>[c("删除收藏 ")]),_:1},8,["onClick"])):b("",!0),e.shopCard.off_shelve?(o(),l(x,{key:1,type:"warning",class:"mx-1",effect:"dark",style:{position:"absolute",right:"10px",top:"10px",width:"fit-content"}},{default:t(()=>[c(" 已下架 ")]),_:1})):e.shopCard.is_sold?(o(),l(x,{key:2,type:"info",class:"mx-1",effect:"dark",style:{position:"absolute",right:"10px",top:"10px",width:"fit-content"}},{default:t(()=>[c(" 已卖出 ")]),_:1})):(o(),l(x,{key:3,class:"mx-1",effect:"dark",style:{position:"absolute",right:"10px",top:"10px",width:"fit-content"}},{default:t(()=>[c(" 可购买 ")]),_:1})),e.shopCard.url?(o(),p("img",{key:4,alt:"example",src:e.shopCard.url,style:{margin:"0 auto","background-size":"cover","object-fit":"contain",height:"160px"},onError:q},null,40,te)):(o(),p("img",{key:5,alt:"example",src:r($),style:{margin:"0 auto","background-size":"cover","object-fit":"contain",height:"160px"}},null,8,se))]),default:t(()=>[i(P,{spinning:e.loading},{default:t(()=>[_("div",ae,[_("div",le,C(e.shopCard.name),1),_("div",re,[e.shopCard.price!==void 0?(o(),p("h4",ie,C(e.shopCard.price)+" 元",1)):b("",!0),e.editable?(o(),p("div",pe,[i(M,{shape:"circle"},{default:t(()=>[i(g,{type:"primary",style:{"font-size":"12px"},onClick:v(H,["stop"])},{default:t(()=>[c(" 修改信息 ")]),_:1},8,["onClick"]),i(g,{type:"error",style:{"font-size":"12px"},onClick:v(N,["stop"])},{default:t(()=>[c(" 删除商品 ")]),_:1},8,["onClick"])]),_:1})])):(o(),p("div",{key:1,class:"wrap",onClick:v(E,["stop"])},[e.shopCard.avatarUrl===""||e.shopCard.avatarUrl===null||e.shopCard.avatarUrl===void 0?(o(),l(I,{key:1,style:{cursor:"pointer"},src:r(X)},null,8,["src"])):(o(),l(I,{key:0,style:{cursor:"pointer"},size:40,src:r(T)+"/upload/"+e.shopCard.avatarUrl},null,8,["src"])),_("span",de,C(e.shopCard.uploaderName),1),e.shopCard.pv!==void 0?(o(),p("div",ce,C(e.shopCard.pv)+" 次浏览",1)):b("",!0)],8,ne))])])]),_:1},8,["spinning"]),i(S,{closable:!1,visible:r(n),"onUpdate:visible":s[0]||(s[0]=k=>B(n)?n.value=k:null),centered:"",title:"注意！","confirm-loading":r(h),onOk:V},{default:t(()=>[ue]),_:1},8,["visible","confirm-loading"]),i(S,{closable:!1,footer:null,visible:r(f),"onUpdate:visible":s[1]||(s[1]=k=>B(f)?f.value=k:null),centered:"","confirm-loading":r(U),style:{width:"80%"}},{default:t(()=>[i(Y,{modify:!0,mid:e.shopCard.id,onClose:j},null,8,["mid"])]),_:1},8,["visible","confirm-loading"])]),_:1})}}});const ye=Z(fe,[["__scopeId","data-v-0e2b09a1"]]);export{ye as S};
