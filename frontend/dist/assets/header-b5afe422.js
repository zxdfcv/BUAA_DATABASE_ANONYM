import{f as o,N as re,L as Se,u as ce,O as v,r as x,b as p,o as c,c as k,e as n,i as e,q as E,a3 as Le,a7 as Be,a8 as Pe,j as _,g as u,h as g,n as b,C as P,y as Z,t as L,D as T,m as S,a9 as Re,aa as je,ab as qe,d as Ie,s as He,z as ze,A as Ne,ac as Ue,F as oe,B as Ve}from"./index-6b603672.js";import{l as We}from"./logo_b-9bb82155.js";import{A as K}from"./avatar-4ee3f7af.js";import{_ as ie}from"./_plugin-vue_export-helper-c27b6911.js";import{U as De}from"./UserOutlined-9a8a0cdc.js";var Ee={icon:{tag:"svg",attrs:{viewBox:"64 64 896 896",focusable:"false"},children:[{tag:"path",attrs:{d:"M868 732h-70.3c-4.8 0-9.3 2.1-12.3 5.8-7 8.5-14.5 16.7-22.4 24.5a353.84 353.84 0 01-112.7 75.9A352.8 352.8 0 01512.4 866c-47.9 0-94.3-9.4-137.9-27.8a353.84 353.84 0 01-112.7-75.9 353.28 353.28 0 01-76-112.5C167.3 606.2 158 559.9 158 512s9.4-94.2 27.8-137.8c17.8-42.1 43.4-80 76-112.5s70.5-58.1 112.7-75.9c43.6-18.4 90-27.8 137.9-27.8 47.9 0 94.3 9.3 137.9 27.8 42.2 17.8 80.1 43.4 112.7 75.9 7.9 7.9 15.3 16.1 22.4 24.5 3 3.7 7.6 5.8 12.3 5.8H868c6.3 0 10.2-7 6.7-12.3C798 160.5 663.8 81.6 511.3 82 271.7 82.6 79.6 277.1 82 516.4 84.4 751.9 276.2 942 512.4 942c152.1 0 285.7-78.8 362.3-197.7 3.4-5.3-.4-12.3-6.7-12.3zm88.9-226.3L815 393.7c-5.3-4.2-13-.4-13 6.3v76H488c-4.4 0-8 3.6-8 8v56c0 4.4 3.6 8 8 8h314v76c0 6.7 7.8 10.5 13 6.3l141.9-112a8 8 0 000-12.6z"}}]},name:"logout",theme:"outlined"};const Te=Ee;function se(i){for(var t=1;t<arguments.length;t++){var s=arguments[t]!=null?Object(arguments[t]):{},f=Object.keys(s);typeof Object.getOwnPropertySymbols=="function"&&(f=f.concat(Object.getOwnPropertySymbols(s).filter(function(h){return Object.getOwnPropertyDescriptor(s,h).enumerable}))),f.forEach(function(h){Ke(i,h,s[h])})}return i}function Ke(i,t,s){return t in i?Object.defineProperty(i,t,{value:s,enumerable:!0,configurable:!0,writable:!0}):i[t]=s,i}var ee=function(t,s){var f=se({},t,s.attrs);return o(re,se({},f,{icon:Te}),null)};ee.displayName="LogoutOutlined";ee.inheritAttrs=!1;const Fe=ee;var Ge={icon:{tag:"svg",attrs:{viewBox:"64 64 896 896",focusable:"false"},children:[{tag:"path",attrs:{d:"M880 112H144c-17.7 0-32 14.3-32 32v736c0 17.7 14.3 32 32 32h736c17.7 0 32-14.3 32-32V144c0-17.7-14.3-32-32-32zm-40 464H528V448h312v128zm0 264H184V184h656v200H496c-17.7 0-32 14.3-32 32v192c0 17.7 14.3 32 32 32h344v200zM580 512a40 40 0 1080 0 40 40 0 10-80 0z"}}]},name:"wallet",theme:"outlined"};const Je=Ge;function le(i){for(var t=1;t<arguments.length;t++){var s=arguments[t]!=null?Object(arguments[t]):{},f=Object.keys(s);typeof Object.getOwnPropertySymbols=="function"&&(f=f.concat(Object.getOwnPropertySymbols(s).filter(function(h){return Object.getOwnPropertyDescriptor(s,h).enumerable}))),f.forEach(function(h){Qe(i,h,s[h])})}return i}function Qe(i,t,s){return t in i?Object.defineProperty(i,t,{value:s,enumerable:!0,configurable:!0,writable:!0}):i[t]=s,i}var te=function(t,s){var f=le({},t,s.attrs);return o(re,le({},f,{icon:Je}),null)};te.displayName="WalletOutlined";te.inheritAttrs=!1;const Xe=te,Ye="/assets/search-icon-2c208f60.svg",Ze="/assets/message-icon-b7a386ca.svg";const et={style:{textAlign:"center",marginTop:"12px",marginBottom:"12px",height:"32px",lineHeight:"32px"}},tt={key:1},nt=["onClick"],at={style:{textAlign:"center",marginTop:"12px",marginBottom:"12px",height:"32px",lineHeight:"32px"}},ot={key:1},st=["onClick"],lt={style:{textAlign:"center",marginTop:"12px",marginBottom:"12px",height:"32px",lineHeight:"32px"}},rt={key:1},ct=["onClick"],it={style:{margin:"30px","text-align":"center"}},ut={key:0,style:{"margin-bottom":"10px"}},dt={__name:"NoticeCenter",setup(i){const t=Se(),s=ce(),f=t.new_comment,h=t.new_reply,R=t.new_mention,z=v(()=>{let l=t.chat_list;for(let r=0;r<l.length;r++)if(l[r].is_read===!1&&l[r].sender!==s.user_id)return 1;return 0}),N=v(()=>(console.log(f+h+R),t.new_comment+t.new_reply+t.new_mention+z.value)),j=x("1"),q=x(!1),m=x(!1),y=v(()=>t.comment_list),$=v(()=>t.comment_all_list),U=v(()=>t.reply_list),M=v(()=>t.reply_all_list),I=v(()=>t.mention_list),H=v(()=>t.mention_all_list),d=x("0"),w=x("0"),O=x("0"),ue=v(()=>t.has_more_comment),de=v(()=>t.has_more_all_comment),_e=v(()=>t.has_more_reply),pe=v(()=>t.has_more_all_reply),me=v(()=>t.has_more_mention),ge=v(()=>t.has_more_all_mention),fe=async()=>{m.value=!0,await t.fillComment(d.value),m.value=!1},ye=async()=>{m.value=!0,await t.fillReply(w.value),m.value=!1},he=async()=>{m.value=!0,await t.fillMention(O.value),m.value=!1},ve=async l=>{await Re({ids:l.id}).then(r=>console.log(r)).catch(r=>console.log(r))},ke=async l=>{await je({ids:l.id}).then(r=>console.log(r)).catch(r=>console.log(r)),console.log(l),G(l.product_id)},Ce=async l=>{await qe({ids:l.id}).then(r=>console.log(r)).catch(r=>console.log(r)),G(l.product_id)},xe=async l=>{await ve(l),G(l.product),await t.refreshMessage()},ne=async l=>{S.push({name:"usercenter",query:{id:l.user}}),await t.refreshMessage()},be=async l=>{await ke(l),await t.refreshMessage()},ae=async l=>{await t.refreshMessage(),S.push({name:"usercenter",query:{id:l.user}})},we=async l=>{await Ce(l),await t.refreshMessage()},F=async l=>{await t.refreshMessage(),S.push({name:"usercenter",query:{id:l.user}})},G=l=>{console.log(l),S.push({name:"detail",query:{id:l}})},$e=()=>{S.push({name:"chatpage"})};return(l,r)=>{const A=p("a-avatar"),Me=p("a-badge"),B=p("a-radio-button"),J=p("a-radio-group"),V=p("a-button"),Q=p("a-list-item-meta"),X=p("a-list-item"),Y=p("a-list"),W=p("el-scrollbar"),D=p("a-tab-pane"),Oe=p("a-tabs"),Ae=p("el-popover");return c(),k(Ae,{width:450,height:600,trigger:"click","popper-style":"box-shadow: rgb(14 18 22 / 35%) 0px 10px 38px -10px, rgb(14 18 22 / 20%) 0px 10px 20px -15px; padding: 20px;"},{reference:n(()=>[o(Me,{count:e(N)},{default:n(()=>[o(A,{src:e(Ze),style:{height:"25px"}},null,8,["src"])]),_:1},8,["count"])]),default:n(()=>[o(Oe,{activeKey:e(j),"onUpdate:activeKey":r[3]||(r[3]=a=>E(j)?j.value=a:null),size:"large",centered:""},{renderTabBar:n(({DefaultTabBar:a,...C})=>[(c(),k(Le(a),Be(Pe(C)),null,16))]),default:n(()=>[o(D,{key:"1",tab:"评论我的",style:{height:"450px"}},{default:n(()=>[o(J,{value:e(d),"onUpdate:value":r[0]||(r[0]=a=>E(d)?d.value=a:null),"button-style":"solid",style:{display:"flex","justify-content":"flex-end"}},{default:n(()=>[o(B,{value:"0"},{default:n(()=>[_("未读")]),_:1}),o(B,{value:"1"},{default:n(()=>[_("全部")]),_:1})]),_:1},8,["value"]),o(W,{style:{height:"400px","margin-top":"5px"}},{default:n(()=>[o(Y,{loading:e(q),"data-source":e(d)==="0"?e(y):e($)},{loadMore:n(()=>[u("div",et,[(e(d)==="0"?e(ue):e(de))?(c(),k(V,{key:0,onClick:g(fe,["stop"])},{default:n(()=>[_("loading more")]),_:1},8,["onClick"])):(e(d)==="0"?e(y).length!==0:e($).length!==0)?(c(),b("div",tt,"到底啦 ~")):P("",!0)])]),renderItem:n(({item:a})=>[o(X,{class:Z(a.is_read?"back_read":"back_unread"),onClick:g(C=>xe(a),["stop"]),style:{"margin-right":"15px","margin-left":"10px",cursor:"pointer"}},{default:n(()=>[o(Q,{description:a.create_time},{title:n(()=>[u("a",{onClick:g(C=>ne(a),["stop"])},"评论者："+L(a.user_name),9,nt)]),avatar:n(()=>[a.user_avatar===""||a.user_avatar===null||a.user_avatar===void 0?(c(),k(A,{key:1,onClick:g(C=>e(S).push({name:"usercenter",query:{id:a.user}}),["stop"]),src:e(K)},null,8,["onClick","src"])):(c(),k(A,{key:0,onClick:g(C=>ne(a),["stop"]),src:e(T)+"/upload/"+a.user_avatar},null,8,["onClick","src"]))]),_:2},1032,["description"]),_(" "+L("您的商品 "+a.product_name+" 有新的评论啦，快来看看吧！"),1)]),_:2},1032,["class","onClick"])]),_:1},8,["loading","data-source"])]),_:1})]),_:1}),o(D,{key:"2",tab:"回复我的",style:{height:"450px"}},{default:n(()=>[o(J,{value:e(w),"onUpdate:value":r[1]||(r[1]=a=>E(w)?w.value=a:null),"button-style":"solid",style:{display:"flex","justify-content":"flex-end"}},{default:n(()=>[o(B,{value:"0"},{default:n(()=>[_("未读")]),_:1}),o(B,{value:"1"},{default:n(()=>[_("全部")]),_:1})]),_:1},8,["value"]),o(W,{style:{height:"400px","margin-top":"5px"}},{default:n(()=>[o(Y,{loading:e(q),"data-source":e(w)==="0"?e(U):e(M)},{loadMore:n(()=>[u("div",at,[(e(w)==="0"?e(_e):e(pe))?(c(),k(V,{key:0,onClick:g(ye,["stop"])},{default:n(()=>[_("loading more")]),_:1},8,["onClick"])):(e(w)==="0"?e(U).length!==0:e(M).length!==0)?(c(),b("div",ot,"到底啦 ~")):P("",!0)])]),renderItem:n(({item:a})=>[o(X,{class:Z(a.is_read?"back_read":"back_unread"),onClick:g(C=>be(a),["stop"]),style:{"margin-right":"15px","margin-left":"10px",cursor:"pointer"}},{default:n(()=>[o(Q,{description:a.create_time},{title:n(()=>[u("a",{onClick:g(C=>ae(a),["stop"])},"回复者："+L(a.user_name),9,st)]),avatar:n(()=>[a.user_avatar===""||a.user_avatar===null||a.user_avatar===void 0?(c(),k(A,{key:1,onClick:g(C=>e(S).push({name:"usercenter",query:{id:a.user}}),["stop"]),src:e(K)},null,8,["onClick","src"])):(c(),k(A,{key:0,onClick:g(C=>ae(a),["stop"]),src:e(T)+"/upload/"+a.user_avatar},null,8,["onClick","src"]))]),_:2},1032,["description"]),_(" "+L("您在商品 "+a.product_name+" 的评论有新的回复啦，快来看看吧！"),1)]),_:2},1032,["class","onClick"])]),_:1},8,["loading","data-source"])]),_:1})]),_:1}),o(D,{key:"3",tab:"@我",style:{height:"450px"}},{default:n(()=>[o(J,{value:e(O),"onUpdate:value":r[2]||(r[2]=a=>E(O)?O.value=a:null),"button-style":"solid",style:{display:"flex","justify-content":"flex-end"}},{default:n(()=>[o(B,{value:"0"},{default:n(()=>[_("未读")]),_:1}),o(B,{value:"1"},{default:n(()=>[_("全部")]),_:1})]),_:1},8,["value"]),o(W,{style:{height:"400px","margin-top":"5px"}},{default:n(()=>[o(Y,{loading:e(q),"data-source":e(O)==="0"?e(I):e(H)},{loadMore:n(()=>[u("div",lt,[(e(O)==="0"?e(me):e(ge))?(c(),k(V,{key:0,onClick:g(he,["stop"])},{default:n(()=>[_("loading more")]),_:1},8,["onClick"])):(e(O)==="0"?e(I).length!==0:e(H).length!==0)?(c(),b("div",rt,"到底啦 ~")):P("",!0)])]),renderItem:n(({item:a})=>[o(X,{class:Z(a.comment_read?"back_read":"back_unread"),onClick:g(C=>we(a),["stop"]),style:{"margin-right":"15px","margin-left":"10px",cursor:"pointer"}},{default:n(()=>[o(Q,{description:a.create_time},{title:n(()=>[u("a",{onClick:g(C=>F(a),["stop"])},"回复者："+L(a.user_name),9,ct)]),avatar:n(()=>[a.user_avatar===""||a.user_avatar===null||a.user_avatar===void 0?(c(),k(A,{key:1,onClick:g(C=>F(a),["stop"]),src:e(K)},null,8,["onClick","src"])):(c(),k(A,{key:0,onClick:g(C=>F(a),["stop"]),src:e(T)+"/upload/"+a.user_avatar},null,8,["onClick","src"]))]),_:2},1032,["description"]),_(" "+L("有人在商品 "+a.product_name+" 的评论区@你，快来看看吧！"),1)]),_:2},1032,["class","onClick"])]),_:1},8,["loading","data-source"])]),_:1})]),_:1}),o(D,{key:"4",tab:"私聊消息",style:{height:"400px"}},{default:n(()=>[o(W,null,{default:n(()=>[u("div",it,[e(z)===1?(c(),b("div",ut,"你有新的私聊消息哦，快来聊天室看看吧！")):P("",!0),o(V,{type:"primary",onClick:g($e,["stop"])},{default:n(()=>[_("前往聊天室")]),_:1},8,["onClick"])])]),_:1})]),_:1})]),_:1},8,["activeKey"])]),_:1})}}},_t=ie(dt,[["__scopeId","data-v-8843aad4"]]),pt={class:"main-bar-view"},mt={class:"logo"},gt=["src"],ft={class:"search-entry"},yt=["src"],ht=["onKeyup"],vt=["onClick"],kt={class:"right-view",style:{"margin-right":"30px"}},Ct=["src"],xt=["src"],bt={key:2,class:"right-icon"},wt=Ie({__name:"header",setup(i){const t=He(),s=ce(),f=ze(),h=x();x(!1),x(!1),x([]),x(!1);let R=["hello","world"];const z=m=>!(m==="null"||m===null||m===void 0);Ne(async()=>{R=await f.getC1(),console.log(R)});const N=()=>{const m=h.value.value;m!==""&&t.push({name:"search",query:{keyword:m}})},j=()=>{t.push({name:"login"})},q=()=>{s.logout().then(m=>{t.push({name:"portal"})})};return(m,y)=>{const $=p("Button"),U=p("Icon"),M=p("a-menu-item"),I=p("a-menu"),H=p("a-dropdown");return c(),b("div",pt,[u("div",mt,[u("img",{src:e(We),class:"search-icon",onClick:y[0]||(y[0]=d=>m.$router.push({name:"portal"}))},null,8,gt)]),u("div",ft,[u("img",{src:e(Ye),class:"search-icon"},null,8,yt),u("input",{placeholder:"今天想搜些什么？",ref_key:"keywordRef",ref:h,onKeyup:Ue(N,["enter"])},null,40,ht)]),o($,{type:"primary",shape:"circle",icon:"ios-search",style:{"margin-left":"15px"},onClick:N},{default:n(()=>[_("搜索")]),_:1}),o(H,{trigger:"click"},{overlay:n(()=>[o(I,null,{default:n(()=>[(c(!0),b(oe,null,Ve(e(R),d=>(c(),k(M,null,{default:n(()=>[u("a",{onClick:w=>{e(t).push({name:"search",query:{keyword:d,type:"C_1"}})}},L(d),9,vt)]),_:2},1024))),256))]),_:1})]),default:n(()=>[o($,{type:"default",style:{"margin-left":"15px"}},{default:n(()=>[_(" 全部分类 "),o(U,{type:"ios-arrow-down"})]),_:1})]),_:1}),u("div",kt,[e(s).user_access?(c(),b(oe,{key:0},[e(s).is_admin?(c(),k($,{key:0,type:"primary",onClick:y[1]||(y[1]=d=>e(t).push({name:"admin"}))},{default:n(()=>[_("后台入口")]),_:1})):P("",!0),o(H,null,{overlay:n(()=>[o(I,{style:{width:"120px"}},{default:n(()=>[o(M,null,{icon:n(()=>[o(e(Xe))]),default:n(()=>[u("a",{onClick:y[3]||(y[3]=d=>e(t).push({name:"addProduct",query:{id:e(s).user_id}}))},"我要发布")]),_:1}),o(M,null,{icon:n(()=>[o(e(De))]),default:n(()=>[u("a",{onClick:y[4]||(y[4]=d=>e(t).push({name:"userInfoEditView",query:{id:e(s).user_id}}))},"账号设置")]),_:1}),o(M,null,{icon:n(()=>[o(e(Fe))]),default:n(()=>[u("a",{onClick:y[5]||(y[5]=d=>q())},"退出登录")]),_:1})]),_:1})]),default:n(()=>[u("a",{class:"ant-dropdown-link",onClick:y[2]||(y[2]=d=>d.preventDefault())},[z(e(s).user_avatar)?(c(),b("img",{key:0,src:e(T)+e(s).user_avatar,class:"self-img"},null,8,Ct)):(c(),b("img",{key:1,src:e(K),class:"self-img"},null,8,xt))])]),_:1})],64)):(c(),k($,{key:1,type:"primary",shape:"circle",icon:"md-log-in",onClick:j},{default:n(()=>[_("登录")]),_:1})),e(s).user_access?(c(),b("div",bt,[o(_t)])):P("",!0)])])}}});const Lt=ie(wt,[["__scopeId","data-v-8e79a55a"]]);export{Lt as H};
