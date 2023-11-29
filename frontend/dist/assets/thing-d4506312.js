import{l as o,O as ce,j as fe,I as L,d as ue,a as I,z as k,k as pe,r as c,o as b,b as F,e as p,x as l,E as y,y as me,f as n,F as ge,n as _e,c as j,t as ve,A as q,B as he,m as x,p as ye,g as we}from"./index-68c43909.js";import{l as be}from"./classification-1b474138.js";import{l as xe}from"./tag-7956e621.js";import{F as ke}from"./FileImageOutlined-a57dacfb.js";import{_ as Ce}from"./_plugin-vue_export-helper-c27b6911.js";var Fe={icon:{tag:"svg",attrs:{viewBox:"64 64 896 896",focusable:"false"},children:[{tag:"path",attrs:{d:"M912 302.3L784 376V224c0-35.3-28.7-64-64-64H128c-35.3 0-64 28.7-64 64v576c0 35.3 28.7 64 64 64h592c35.3 0 64-28.7 64-64V648l128 73.7c21.3 12.3 48-3.1 48-27.6V330c0-24.6-26.7-40-48-27.7zM712 792H136V232h576v560zm176-167l-104-59.8V458.9L888 399v226zM208 360h112c4.4 0 8-3.6 8-8v-48c0-4.4-3.6-8-8-8H208c-4.4 0-8 3.6-8 8v48c0 4.4 3.6 8 8 8z"}}]},name:"video-camera",theme:"outlined"};const Oe=Fe;function M(r){for(var f=1;f<arguments.length;f++){var u=arguments[f]!=null?Object(arguments[f]):{},v=Object.keys(u);typeof Object.getOwnPropertySymbols=="function"&&(v=v.concat(Object.getOwnPropertySymbols(u).filter(function(m){return Object.getOwnPropertyDescriptor(u,m).enumerable}))),v.forEach(function(m){Se(r,m,u[m])})}return r}function Se(r,f,u){return f in r?Object.defineProperty(r,f,{value:u,enumerable:!0,configurable:!0,writable:!0}):r[f]=u,r}var R=function(f,u){var v=M({},f,u.attrs);return o(ce,M({},v,{icon:Oe}),null)};R.displayName="VideoCameraOutlined";R.inheritAttrs=!1;const De=R,Ue=async r=>fe({url:"/myapp/admin/thing/list",params:r,data:{},headers:{}}),Ve=async r=>L({url:"/myapp/admin/thing/create",params:{},data:r,timeout:2e4,headers:{"Content-Type":"multipart/form-data;charset=utf-8"}}),Ie=async(r,f)=>L({url:"/myapp/admin/thing/update",params:r,data:f,headers:{"Content-Type":"multipart/form-data;charset=utf-8"}}),K=async r=>L({url:"/myapp/admin/thing/delete",params:r,headers:{}}),z=r=>(ye("data-v-97f0f339"),r=r(),we(),r),Le={class:"page-view"},Re={class:"table-operations"},ze={key:0},Ae=["onClick"],Be=z(()=>p("a",{href:"#"},"删除",-1)),Ee={style:{"padding-right":"16px","max-height":"480px","overflow-x":"hidden","overflow-y":"auto"}},$e={class:"ant-upload-drag-icon"},Ne=["src"],Te=z(()=>p("p",{class:"ant-upload-text"}," 请选择要上传的封面图片 ",-1)),je={class:"ant-upload-drag-icon"},qe=z(()=>p("p",{class:"ant-upload-text"}," 请选择要上传的文件（mp4格式） ",-1)),Me=ue({__name:"thing",setup(r){const f=I([{title:"序号",dataIndex:"id",key:"id",width:60},{title:"菜肴名称",dataIndex:"title",key:"title"},{title:"状态",dataIndex:"status",key:"status",customRender:({text:a,record:t,index:i,column:D})=>a==="0"?"上架":"下架"},{title:"柜台",dataIndex:"classification_title",key:"classification_title"},{title:"简介",dataIndex:"description",key:"description",customRender:({text:a,record:t,index:i,column:D})=>a?a.substring(0,40)+"...":"--",width:600},{title:"操作",dataIndex:"action",key:"operation",align:"center",fixed:"right",width:140}]),u=a=>{const t=new Date().getTime().toString()+"."+a.type.substring(6),i=new File([a],t);return console.log(i),e.form.imageFile=i,!1},v=a=>{const t=new Date().getTime().toString()+"."+a.type.substring(6),i=new File([a],t);return console.log(i),e.form.rawFile=i,!1},m=k([]),C=k([]),h=k(!1),d=I({dataList:[],loading:!1,keyword:"",selectedRowKeys:[],pageSize:10,page:1}),e=I({visile:!1,editFlag:!1,title:"",cData:[],tagData:[{}],form:{id:void 0,title:void 0,classification:void 0,tag:[],repertory:void 0,price:void 0,status:void 0,cover:void 0,coverUrl:void 0,imageFile:void 0,rawFile:void 0},rules:{title:[{required:!0,message:"请输入名称",trigger:"change"}],classification:[{required:!0,message:"请选择柜台",trigger:"change"}],repertory:[{required:!0,message:"请输入库存",trigger:"change"}],price:[{required:!0,message:"请输入定价",trigger:"change"}],status:[{required:!0,message:"请选择状态",trigger:"change"}],canteen:[{required:!0,message:"请输入所在柜台",trigger:"change"}]}}),O=k();pe(()=>{w(),P(),H()});const w=()=>{d.loading=!0,Ue({keyword:d.keyword}).then(a=>{d.loading=!1,console.log(a),a.data.forEach((t,i)=>{t.index=i+1}),d.dataList=a.data}).catch(a=>{d.loading=!1,console.log(a)})},P=()=>{be({}).then(a=>{e.cData=a.data})},H=()=>{xe({}).then(a=>{a.data.forEach((t,i)=>{t.index=i+1}),e.tagData=a.data})},G=a=>{var t;d.keyword=(t=a==null?void 0:a.target)==null?void 0:t.value,console.log(d.keyword)},J=()=>{w()},Q=k({onChange:(a,t)=>{console.log(`selectedRowKeys: ${a}`,"selectedRows: ",t),d.selectedRowKeys=a}}),W=()=>{E(),e.visile=!0,e.editFlag=!1,e.title="新增";for(const a in e.form)e.form[a]=void 0;e.form.cover=void 0},X=a=>{E(),e.visile=!0,e.editFlag=!0,e.title="编辑";for(const t in e.form)e.form[t]=void 0;for(const t in a)a[t]&&(e.form[t]=a[t]);e.form.cover&&(e.form.coverUrl=he+e.form.cover,e.form.cover=void 0)},Y=a=>{console.log("delete",a),K({ids:a.id}).then(t=>{w()}).catch(t=>{x.error(t.msg||"操作失败")})},Z=()=>{if(console.log(d.selectedRowKeys),d.selectedRowKeys.length<=0){console.log("hello"),x.warn("请勾选删除项");return}K({ids:d.selectedRowKeys.join(",")}).then(a=>{x.success("删除成功"),d.selectedRowKeys=[],w()}).catch(a=>{x.error(a.msg||"操作失败")})},A=()=>{var a;(a=O.value)==null||a.validate().then(()=>{const t=new FormData;e.editFlag&&t.append("id",e.form.id),t.append("title",e.form.title),e.form.classification&&t.append("classification",e.form.classification),e.form.tag&&e.form.tag.forEach(function(i){i&&t.append("tag",i)}),e.form.imageFile&&t.append("cover",e.form.imageFile),e.form.rawFile&&t.append("raw",e.form.rawFile),t.append("description",e.form.description||""),t.append("price",e.form.price||""),t.append("canteen",e.form.canteen||""),e.form.repertory>=0&&t.append("repertory",e.form.repertory),e.form.status&&t.append("status",e.form.status),e.editFlag?(h.value=!0,Ie({id:e.form.id},t).then(i=>{h.value=!1,S(),w()}).catch(i=>{h.value=!1,console.log(i),x.error(i.msg||"操作失败")})):(h.value=!0,Ve(t).then(i=>{h.value=!1,S(),w()}).catch(i=>{h.value=!1,console.log(i),x.error(i.msg||"操作失败")}))}).catch(t=>{console.log("不能为空")})},B=()=>{S()},E=()=>{var a;(a=O.value)==null||a.resetFields(),m.value=[],C.value=[]},S=()=>{e.visile=!1};return(a,t)=>{const i=c("a-button"),D=c("a-input-search"),ee=c("a-space"),te=c("a-divider"),ae=c("a-popconfirm"),oe=c("a-table"),$=c("a-input"),g=c("a-form-item"),_=c("a-col"),U=c("a-select"),V=c("a-select-option"),N=c("a-upload-dragger"),le=c("a-textarea"),ne=c("a-row"),ie=c("a-form"),se=c("a-modal");return b(),F("div",null,[p("div",Le,[p("div",Re,[o(ee,null,{default:l(()=>[o(i,{type:"primary",onClick:W},{default:l(()=>[y("新增")]),_:1}),o(i,{onClick:Z},{default:l(()=>[y("批量删除")]),_:1}),o(D,{"addon-before":"名称","enter-button":"",onSearch:J,onChange:G})]),_:1})]),o(oe,{size:"middle",rowKey:"id",loading:n(d).loading,columns:n(f),"data-source":n(d).dataList,scroll:{x:"max-content"},"row-selection":n(Q),pagination:{size:"default",current:n(d).page,pageSize:n(d).pageSize,onChange:s=>n(d).page=s,showSizeChanger:!1,showTotal:s=>`共${s}条数据`}},{bodyCell:l(({text:s,record:T,index:Ke,column:re})=>[re.key==="operation"?(b(),F("span",ze,[p("a",{onClick:de=>X(T)},"编辑",8,Ae),o(te,{type:"vertical"}),o(ae,{title:"确定删除?","ok-text":"是","cancel-text":"否",onConfirm:de=>Y(T)},{default:l(()=>[Be]),_:2},1032,["onConfirm"])])):me("",!0)]),_:1},8,["loading","columns","data-source","row-selection","pagination"])]),p("div",null,[o(se,{visible:n(e).visile,forceRender:!0,title:n(e).title,width:"880px","ok-text":"确认","cancel-text":"取消",onCancel:B,onOk:A},{footer:l(()=>[o(i,{key:"back",onClick:B},{default:l(()=>[y("取消")]),_:1}),o(i,{key:"submit",type:"primary",loading:n(h),onClick:A},{default:l(()=>[y("确认")]),_:1},8,["loading"])]),default:l(()=>[p("div",Ee,[o(ie,{ref_key:"myform",ref:O,"label-col":{style:{width:"80px"}},model:n(e).form,rules:n(e).rules},{default:l(()=>[o(ne,{gutter:24},{default:l(()=>[o(_,{span:"24"},{default:l(()=>[o(g,{label:"菜肴名称",name:"title"},{default:l(()=>[o($,{placeholder:"请输入",value:n(e).form.title,"onUpdate:value":t[0]||(t[0]=s=>n(e).form.title=s)},null,8,["value"])]),_:1})]),_:1}),o(_,{span:"12"},{default:l(()=>[o(g,{label:"柜台",name:"classification"},{default:l(()=>[o(U,{placeholder:"请选择",allowClear:"",options:n(e).cData,"field-names":{label:"title",value:"id"},value:n(e).form.classification,"onUpdate:value":t[1]||(t[1]=s=>n(e).form.classification=s)},null,8,["options","value"])]),_:1})]),_:1}),o(_,{span:"12"},{default:l(()=>[o(g,{label:"标签"},{default:l(()=>[o(U,{mode:"multiple",placeholder:"请选择",allowClear:"",value:n(e).form.tag,"onUpdate:value":t[2]||(t[2]=s=>n(e).form.tag=s)},{default:l(()=>[(b(!0),F(ge,null,_e(n(e).tagData,s=>(b(),j(V,{value:s.id},{default:l(()=>[y(ve(s.title),1)]),_:2},1032,["value"]))),256))]),_:1},8,["value"])]),_:1})]),_:1}),o(_,{span:"12"},{default:l(()=>[o(g,{label:"价格"},{default:l(()=>[o($,{placeholder:"请输入",value:n(e).form.price,"onUpdate:value":t[3]||(t[3]=s=>n(e).form.price=s)},null,8,["value"])]),_:1})]),_:1}),o(_,{span:"24"},{default:l(()=>[o(g,{label:"封面"},{default:l(()=>[o(N,{name:"file",accept:"image/*",multiple:!1,"before-upload":u,"file-list":n(m),"onUpdate:file-list":t[4]||(t[4]=s=>q(m)?m.value=s:null)},{default:l(()=>[p("p",$e,[n(e).form.coverUrl?(b(),F("img",{key:0,src:n(e).form.coverUrl,style:{width:"60px",height:"80px"}},null,8,Ne)):(b(),j(n(ke),{key:1}))]),Te]),_:1},8,["file-list"])]),_:1})]),_:1}),o(_,{span:"24"},{default:l(()=>[o(g,{label:"菜肴文件"},{default:l(()=>[o(N,{name:"file",accept:".mp4",multiple:!1,"before-upload":v,"file-list":n(C),"onUpdate:file-list":t[5]||(t[5]=s=>q(C)?C.value=s:null)},{default:l(()=>[p("p",je,[o(n(De))]),qe]),_:1},8,["file-list"])]),_:1})]),_:1}),o(_,{span:"24"},{default:l(()=>[o(g,{label:"内容简介"},{default:l(()=>[o(le,{placeholder:"请输入",value:n(e).form.description,"onUpdate:value":t[6]||(t[6]=s=>n(e).form.description=s)},null,8,["value"])]),_:1})]),_:1}),o(_,{span:"12"},{default:l(()=>[o(g,{label:"状态",name:"status"},{default:l(()=>[o(U,{placeholder:"请选择",allowClear:"",value:n(e).form.status,"onUpdate:value":t[7]||(t[7]=s=>n(e).form.status=s)},{default:l(()=>[o(V,{key:"0",value:"0"},{default:l(()=>[y("上架")]),_:1}),o(V,{key:"1",value:"1"},{default:l(()=>[y("下架")]),_:1})]),_:1},8,["value"])]),_:1})]),_:1})]),_:1})]),_:1},8,["model","rules"])])]),_:1},8,["visible","title"])])])}}});const We=Ce(Me,[["__scopeId","data-v-97f0f339"]]);export{We as default};
