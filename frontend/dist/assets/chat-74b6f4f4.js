import{W as ee,X as te,a4 as ae,Y as oe,d as ne,r as k,a as F,A as le,D as ie,b as d,o as C,n as S,g as m,f as a,e as n,j as p,C as se,i as l,q as re,I as de,c as ce,M as h,p as me,k as pe}from"./index-6b603672.js";import{e as fe}from"./exportCsv-f7ca4da5.js";import{F as ue}from"./FileImageOutlined-12518b84.js";import{_ as _e}from"./_plugin-vue_export-helper-c27b6911.js";const ge=async c=>ee({url:"/myapp/admin/chat/list",params:c,data:{},headers:{}}),he=async c=>te({url:"/myapp/admin/chat/create",params:{},data:c,headers:{"Content-Type":"multipart/form-data;charset=utf-8"}}),B=async c=>ae({url:"/myapp/admin/chat/delete",params:c,headers:{}}),ve=async(c,f)=>oe({url:"/myapp/admin/chat/update",params:c,data:f,headers:{"Content-Type":"multipart/form-data;charset=utf-8"}}),N=c=>(me("data-v-330f191f"),c=c(),pe(),c),ye={class:"page-view"},ke={class:"table-operations"},xe={key:0},we=["onClick"],Ce=N(()=>m("a",{href:"#"},"删除",-1)),be={style:{"padding-right":"16px","max-height":"480px","overflow-x":"hidden","overflow-y":"auto"}},Ue={class:"ant-upload-drag-icon"},Ie=["src"],Fe=N(()=>m("p",{class:"ant-upload-text"}," 请选择要上传的封面图片 ",-1)),Se=ne({__name:"chat",setup(c){const f=k([]),L=k([]),T=k(!1),V=F([{title:"序号",dataIndex:"id",key:"id",align:"center"},{title:"商品名称",dataIndex:"product_name",key:"product_name",align:"center"},{title:"发送者",dataIndex:"sender_name",key:"sender_name",align:"center"},{title:"接收者",dataIndex:"recipient_name",key:"recipient_name",align:"center"},{title:"评论内容",dataIndex:"content",key:"content",align:"center"},{title:"创建时间",dataIndex:"create_time",key:"create_time",align:"center"},{title:"是否已读",dataIndex:"is_read",key:"is_read",align:"center"},{title:"内容",dataIndex:"create_time",key:"create_time",align:"center"},{title:"操作",dataIndex:"action",key:"operation",align:"center",fixed:"right",width:140}]),s=F({list:[],loading:!1,currentAdminUserName:"",keyword:"",selectedRowKeys:[],pageSize:10,page:1}),e=F({visile:!1,editFlag:!1,title:"",form:{id:void 0,image:void 0,imageFile:void 0,imageUrl:"",imageHeight:0,imageWidth:0,product:void 0,link:void 0,is_read:void 0,recipient:void 0,sender:void 0,content:""},rules:{link:[{required:!0,message:"请输入",trigger:"change"}]}}),b=k();le(()=>{v()});const v=()=>{s.loading=!0,ge({keyword:s.keyword}).then(o=>{s.loading=!1,console.log(o),o.data.forEach((t,i)=>{t.index=i+1,t.is_read=t.is_read?"1":"0",t.image&&(t.image=ie+t.image,console.log(t.image))}),s.list=o.data}).catch(o=>{s.loading=!1,console.log(o)})},W=o=>{const t=new Date().getTime().toString()+"."+o.type.substring(6),i=new File([o],t);console.log(i);const x=new FileReader;return x.onload=w=>{const u=new Image;u.onload=()=>{e.form.imageUrl=String(w.target.result),console.log(e.form.imageUrl);const I=u.width,y=u.height;e.form.imageWidth=I,e.form.imageHeight=y},u.src=w.target.result},x.readAsDataURL(i),e.form.imageFile=i,!1},$=()=>{fe(s.list,"私聊信息.csv")},E=k({onChange:(o,t)=>{console.log(`selectedRowKeys: ${o}`,"selectedRows: ",t),s.selectedRowKeys=o}}),H=o=>{console.log("delete",o),B({ids:o.id}).then(t=>{v()}).catch(t=>{h.error(t.msg||"操作失败")})},R=()=>{var o;(o=b.value)==null||o.resetFields(),f.value=[],L.value=[]},M=o=>{R(),e.visile=!0,e.editFlag=!0,e.title="编辑";for(const i in e.form)e.form[i]=void 0;for(const i in o)o[i]&&(e.form[i]=o[i]);e.form.imageUrl=e.form.image,console.log(e.form.imageUrl);const t=new Image;t.onload=()=>{e.form.imageWidth=t.width,e.form.imageHeight=t.height},t.src=e.form.imageUrl,e.form.image=void 0},A=()=>{var o;(o=b.value)==null||o.validate().then(()=>{const t=new FormData;e.form.recipient&&t.append("product",e.form.recipient),e.form.imageFile&&t.append("image",e.form.imageFile),e.form.content&&t.append("content",e.form.content),e.form.sender&&t.append("sender",e.form.sender),e.form.recipient&&t.append("recipient",e.form.recipient),e.form.is_read&&t.append("is_read",e.form.is_read==="1"?"true":"false"),e.form.product&&t.append("product",e.form.product),e.editFlag?ve({chat_id:e.form.id},t).then(i=>{U(),v()}).catch(i=>{console.log(i),h.error(i.msg||"操作失败")}):he(t).then(i=>{U(),v()}).catch(i=>{console.log(i),h.error(i.msg||"操作失败")})}).catch(t=>{console.log("不能为空")})},D=()=>{U()},O=()=>{R(),e.visile=!0,e.editFlag=!1,e.title="新增";for(const o in e.form)e.form[o]=void 0;e.form.image=void 0},j=()=>{if(console.log(s.selectedRowKeys),s.selectedRowKeys.length<=0){console.log("hello"),h.warn("请勾选删除项");return}B({ids:s.selectedRowKeys.join(",")}).then(o=>{h.success("删除成功"),s.selectedRowKeys=[],v()}).catch(o=>{h.error(o.msg||"操作失败")})},U=()=>{e.visile=!1};return(o,t)=>{const i=d("a-button"),x=d("a-space"),w=d("a-divider"),u=d("a-popconfirm"),I=d("a-table"),y=d("a-input"),_=d("a-form-item"),g=d("a-col"),q=d("a-textarea"),X=d("a-upload-dragger"),z=d("a-select-option"),Y=d("a-select"),G=d("a-row"),J=d("a-form"),P=d("a-modal");return C(),S("div",null,[m("div",ye,[m("div",ke,[a(x,null,{default:n(()=>[a(i,{type:"primary",onClick:$},{default:n(()=>[p("导出 CSV")]),_:1}),a(i,{type:"primary",onClick:O},{default:n(()=>[p("新增")]),_:1}),a(i,{onClick:j},{default:n(()=>[p("批量删除")]),_:1})]),_:1})]),a(I,{size:"middle",rowKey:"id",loading:l(s).loading,columns:l(V),"data-source":l(s).list,scroll:{x:"max-content"},"row-selection":l(E),pagination:{size:"default",current:l(s).page,pageSize:l(s).pageSize,onChange:r=>l(s).page=r,showSizeChanger:!1,showTotal:r=>`共${r}条数据`}},{bodyCell:n(({text:r,record:K,index:Re,column:Q})=>[Q.key==="operation"?(C(),S("span",xe,[m("a",{onClick:Z=>M(K)},"编辑",8,we),a(w,{type:"vertical"}),a(u,{title:"确定删除?","ok-text":"是","cancel-text":"否",onConfirm:Z=>H(K)},{default:n(()=>[Ce]),_:2},1032,["onConfirm"])])):se("",!0)]),_:1},8,["loading","columns","data-source","row-selection","pagination"])]),m("div",null,[a(P,{visible:l(e).visile,forceRender:!0,title:l(e).title,width:"880px","ok-text":"确认","cancel-text":"取消",onCancel:D,onOk:A},{footer:n(()=>[a(i,{key:"back",onClick:D},{default:n(()=>[p("取消")]),_:1}),a(i,{key:"submit",type:"primary",loading:l(T),onClick:A},{default:n(()=>[p("确认")]),_:1},8,["loading"])]),default:n(()=>[m("div",be,[a(J,{ref_key:"myform",ref:b,"label-col":{style:{width:"80px"}},model:l(e).form,rules:l(e).rules},{default:n(()=>[a(G,{gutter:24},{default:n(()=>[a(g,{span:"12"},{default:n(()=>[a(_,{label:"商品 id",name:"product_id"},{default:n(()=>[a(y,{placeholder:"请输入",value:l(e).form.product,"onUpdate:value":t[0]||(t[0]=r=>l(e).form.product=r)},null,8,["value"])]),_:1})]),_:1}),a(g,{span:"12"},{default:n(()=>[a(_,{label:"发送用户 id",name:"receiver_id"},{default:n(()=>[a(y,{placeholder:"请输入",value:l(e).form.sender,"onUpdate:value":t[1]||(t[1]=r=>l(e).form.sender=r)},null,8,["value"])]),_:1})]),_:1}),a(g,{span:"12"},{default:n(()=>[a(_,{label:"接收用户 id",name:"product_id"},{default:n(()=>[a(y,{placeholder:"请输入",value:l(e).form.recipient,"onUpdate:value":t[2]||(t[2]=r=>l(e).form.recipient=r)},null,8,["value"])]),_:1})]),_:1}),a(g,{span:"24"},{default:n(()=>[a(_,{label:"内容"},{default:n(()=>[a(q,{placeholder:"请输入",value:l(e).form.content,"onUpdate:value":t[3]||(t[3]=r=>l(e).form.content=r)},null,8,["value"])]),_:1})]),_:1}),a(g,{span:"24"},{default:n(()=>[a(_,{label:"图片"},{default:n(()=>[a(X,{name:"file",accept:"image/*",multiple:!1,"before-upload":W,"max-count":1,"file-list":l(f),"onUpdate:file-list":t[4]||(t[4]=r=>re(f)?f.value=r:null)},{default:n(()=>[m("p",Ue,[l(e).form.imageUrl?(C(),S("img",{key:0,src:l(e).form.imageUrl,style:de({width:`${160*l(e).form.imageWidth/l(e).form.imageHeight}px`,height:"160px"})},null,12,Ie)):(C(),ce(l(ue),{key:1}))]),Fe]),_:1},8,["file-list"])]),_:1})]),_:1}),a(g,{span:"8"},{default:n(()=>[a(_,{label:"已读",name:"status"},{default:n(()=>[a(Y,{placeholder:"请选择",allowClear:"",value:l(e).form.is_read,"onUpdate:value":t[5]||(t[5]=r=>l(e).form.is_read=r)},{default:n(()=>[a(z,{key:"0",value:"0"},{default:n(()=>[p("是")]),_:1}),a(z,{key:"1",value:"1"},{default:n(()=>[p("否")]),_:1})]),_:1},8,["value"])]),_:1})]),_:1})]),_:1})]),_:1},8,["model","rules"])])]),_:1},8,["visible","title"])])])}}});const Be=_e(Se,[["__scopeId","data-v-330f191f"]]);export{Be as default};
