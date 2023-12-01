import{l as Z,d as S,u as ee,c as te}from"./classification-1b474138.js";import{l as oe}from"./canteen-860ad73f.js";import{d as ae,a as b,z as u,k as le,r as c,o as y,b as C,e as d,l as a,x as n,E as w,y as ne,f as l,A as ie,c as se,B as ce,m,p as re,g as de}from"./index-68c43909.js";import{F as fe}from"./FileImageOutlined-a57dacfb.js";import{_ as me}from"./_plugin-vue_export-helper-c27b6911.js";const A=_=>(re("data-v-c4d2c397"),_=_(),de(),_),pe={class:"page-view"},ue={class:"table-operations"},_e={key:0},ge=["onClick"],ve=A(()=>d("a",{href:"#"},"删除",-1)),he={style:{"padding-right":"16px","max-height":"480px","overflow-x":"hidden","overflow-y":"auto"}},ye={class:"ant-upload-drag-icon"},we=["src"],ke=A(()=>d("p",{class:"ant-upload-text"}," 请选择要上传的封面图片 ",-1)),xe=ae({__name:"classification",setup(_){const B=b([{title:"序号",dataIndex:"id",key:"id",width:60},{title:"柜台名称",dataIndex:"title",key:"title"},{title:"食堂",dataIndex:"canteen_title",key:"canteen_title"},{title:"简介",dataIndex:"description",key:"description",customRender:({text:t,record:o,index:i,column:D})=>t?t.substring(0,40)+"...":"--",width:600},{title:"操作",dataIndex:"action",key:"operation",align:"center",fixed:"right",width:140}]),L=t=>{const o=new Date().getTime().toString()+"."+t.type.substring(6),i=new File([t],o);return console.log(i),e.form.imageFile=i,!1},g=u([]),z=u([]),f=u(!1),s=b({userList:[],loading:!1,currentAdminUserName:"",keyword:"",selectedRowKeys:[],pageSize:10,page:1}),e=b({visile:!1,editFlag:!1,bData:[],title:"",form:{id:void 0,title:void 0,canteen:void 0,cover:void 0,coverUrl:void 0,imageFile:void 0},rules:{title:[{required:!0,message:"请输入",trigger:"change"}],cateen:[{required:!0,message:"请选择食堂",trigger:"change"}]}}),k=u();le(()=>{p(),K()});const p=()=>{s.loading=!0,Z({keyword:s.keyword}).then(t=>{s.loading=!1,console.log(t),t.data.forEach((o,i)=>{o.index=i+1}),s.userList=t.data}).catch(t=>{s.loading=!1,console.log(t)})},K=()=>{oe({}).then(t=>{e.bData=t.data})},N=u({onChange:(t,o)=>{console.log(`selectedRowKeys: ${t}`,"selectedRows: ",o),s.selectedRowKeys=t}}),E=()=>{U(),e.visile=!0,e.editFlag=!1,e.title="新增";for(const t in e.form)e.form[t]=void 0;e.form.cover=void 0},$=t=>{U(),e.visile=!0,e.editFlag=!0,e.title="编辑";for(const o in e.form)e.form[o]=void 0;for(const o in t)e.form[o]=t[o];e.form.cover&&(e.form.coverUrl=ce+e.form.cover,e.form.cover=void 0)},V=t=>{console.log("delete",t),S({ids:t.id}).then(o=>{p()}).catch(o=>{m.error(o.msg||"删除失败")})},M=()=>{if(console.log(s.selectedRowKeys),s.selectedRowKeys.length<=0){console.log("hello"),m.warn("请勾选删除项");return}S({ids:s.selectedRowKeys.join(",")}).then(t=>{m.success("删除成功"),s.selectedRowKeys=[],p()}).catch(t=>{m.error(t.msg||"删除失败")})},F=()=>{var t;(t=k.value)==null||t.validate().then(()=>{const o=new FormData;e.editFlag&&o.append("id",e.form.id),o.append("title",e.form.title),e.form.canteen&&o.append("canteen",e.form.canteen),e.form.imageFile&&o.append("cover",e.form.imageFile),o.append("description",e.form.description||""),o.append("canteen",e.form.canteen||""),e.editFlag?(f.value=!0,ee({id:e.form.id},o).then(i=>{f.value=!1,x(),p()}).catch(i=>{f.value=!1,console.log(i),m.error(i.msg||"操作失败")})):(f.value=!0,te(o).then(i=>{f.value=!1,x(),p()}).catch(i=>{f.value=!1,console.log(i),m.error(i.msg||"操作失败")}))}).catch(o=>{console.log("不能为空")})},R=()=>{x()},U=()=>{var t;(t=k.value)==null||t.resetFields(),g.value=[],z.value=[]},x=()=>{e.visile=!1};return(t,o)=>{const i=c("a-button"),D=c("a-space"),O=c("a-divider"),T=c("a-popconfirm"),q=c("a-table"),j=c("a-input"),v=c("a-form-item"),h=c("a-col"),G=c("a-select"),H=c("a-upload-dragger"),J=c("a-textarea"),P=c("a-row"),Q=c("a-form"),W=c("a-modal");return y(),C("div",null,[d("div",pe,[d("div",ue,[a(D,null,{default:n(()=>[a(i,{type:"primary",onClick:E},{default:n(()=>[w("新增")]),_:1}),a(i,{onClick:M},{default:n(()=>[w("批量删除")]),_:1})]),_:1})]),a(q,{size:"middle",rowKey:"id",loading:l(s).loading,columns:l(B),"data-source":l(s).userList,scroll:{x:"max-content"},"row-selection":l(N),pagination:{size:"default",current:l(s).page,pageSize:l(s).pageSize,onChange:r=>l(s).page=r,showSizeChanger:!1,showTotal:r=>`共${r}条数据`}},{bodyCell:n(({text:r,record:I,index:be,column:X})=>[X.key==="operation"?(y(),C("span",_e,[d("a",{onClick:Y=>$(I)},"编辑",8,ge),a(O,{type:"vertical"}),a(T,{title:"确定删除?","ok-text":"是","cancel-text":"否",onConfirm:Y=>V(I)},{default:n(()=>[ve]),_:2},1032,["onConfirm"])])):ne("",!0)]),_:1},8,["loading","columns","data-source","row-selection","pagination"])]),d("div",null,[a(W,{visible:l(e).visile,forceRender:!0,title:l(e).title,width:"880px","ok-text":"确认","cancel-text":"取消",onCancel:R,onOk:F},{footer:n(()=>[a(i,{key:"back",onClick:R},{default:n(()=>[w("取消")]),_:1}),a(i,{key:"submit",type:"primary",loading:l(f),onClick:F},{default:n(()=>[w("确认")]),_:1},8,["loading"])]),default:n(()=>[d("div",he,[a(Q,{ref_key:"myform",ref:k,"label-col":{style:{width:"80px"}},model:l(e).form,rules:l(e).rules},{default:n(()=>[a(P,{gutter:24},{default:n(()=>[a(h,{span:"24"},{default:n(()=>[a(v,{label:"柜台名称",name:"title"},{default:n(()=>[a(j,{placeholder:"请输入",value:l(e).form.title,"onUpdate:value":o[0]||(o[0]=r=>l(e).form.title=r)},null,8,["value"])]),_:1})]),_:1}),a(h,{span:"12"},{default:n(()=>[a(v,{label:"食堂",name:"canteen"},{default:n(()=>[a(G,{placeholder:"请选择",allowClear:"",options:l(e).bData,"field-names":{label:"title",value:"id"},value:l(e).form.canteen,"onUpdate:value":o[1]||(o[1]=r=>l(e).form.canteen=r)},null,8,["options","value"])]),_:1})]),_:1}),a(h,{span:"24"},{default:n(()=>[a(v,{label:"封面"},{default:n(()=>[a(H,{name:"file",accept:"image/*",multiple:!1,"before-upload":L,"file-list":l(g),"onUpdate:file-list":o[2]||(o[2]=r=>ie(g)?g.value=r:null)},{default:n(()=>[d("p",ye,[l(e).form.coverUrl?(y(),C("img",{key:0,src:l(e).form.coverUrl,style:{width:"60px",height:"80px"}},null,8,we)):(y(),se(l(fe),{key:1}))]),ke]),_:1},8,["file-list"])]),_:1})]),_:1}),a(h,{span:"24"},{default:n(()=>[a(v,{label:"内容简介"},{default:n(()=>[a(J,{placeholder:"请输入",value:l(e).form.description,"onUpdate:value":o[3]||(o[3]=r=>l(e).form.description=r)},null,8,["value"])]),_:1})]),_:1})]),_:1})]),_:1},8,["model","rules"])])]),_:1},8,["visible","title"])])])}}});const Ie=me(xe,[["__scopeId","data-v-c4d2c397"]]);export{Ie as default};