import{d as X,a as C,z as I,k as Y,R as Z,r as i,o as c,b as p,e as v,l as t,x as n,E as h,y as _,f as l,c as D,F as ee,n as ae,t as oe,S as K,m as g,T as te,U as le,p as ne,g as se}from"./index-68c43909.js";import{_ as re}from"./_plugin-vue_export-helper-c27b6911.js";const ie=w=>(ne("data-v-8998fc14"),w=w(),se(),w),de={class:"page-view"},ce={class:"table-operations"},me={key:0},ue={key:0},pe={key:1},fe={key:2},_e={key:1},ge=["onClick"],ve=ie(()=>v("a",{href:"#"},"删除",-1)),ke=X({__name:"user",setup(w){const A=C([{title:"序号",dataIndex:"id",key:"id",align:"center"},{title:"用户名",dataIndex:"username",key:"username",align:"center"},{title:"昵称",dataIndex:"nickname",key:"nickname",align:"center"},{title:"角色",dataIndex:"role",key:"role",align:"center"},{title:"状态",dataIndex:"status",key:"status",align:"center",customRender:({text:o,record:a,index:d,column:F})=>o==="0"?"正常":"封号"},{title:"邮箱",dataIndex:"email",key:"email",align:"center"},{title:"手机号",dataIndex:"mobile",key:"mobile",align:"center"},{title:"创建时间",dataIndex:"create_time",key:"create_time",align:"center"},{title:"操作",dataIndex:"action",key:"operation",align:"center",fixed:"right",width:140}]);I([]);const r=C({userList:[],loading:!1,currentAdminUserName:"",keyword:"",selectedRowKeys:[],pageSize:10,page:1}),e=C({visile:!1,editFlag:!1,title:"",roleData:[{id:"1",title:"管理员"},{id:"2",title:"普通用户"},{id:"3",title:"演示账号"}],form:{id:void 0,username:void 0,password:void 0,role:void 0,status:void 0,nickname:void 0,email:void 0,mobile:void 0},rules:{username:[{required:!0,message:"请输入",trigger:"change"}],password:[{required:!0,message:"请输入",trigger:"change"}],role:[{required:!0,message:"请选择",trigger:"change"}],status:[{required:!0,message:"请选择",trigger:"change"}]}}),y=I();Y(()=>{f()});const f=()=>{r.loading=!0,Z({keyword:r.keyword}).then(o=>{r.loading=!1,console.log(o),o.data.forEach((a,d)=>{a.index=d+1}),r.userList=o.data}).catch(o=>{r.loading=!1,console.log(o)})},B=o=>{var a;r.keyword=(a=o==null?void 0:o.target)==null?void 0:a.value,console.log(r.keyword)},L=()=>{f()},N=I({onChange:(o,a)=>{console.log(`selectedRowKeys: ${o}`,"selectedRows: ",a),r.selectedRowKeys=o}}),q=()=>{S(),e.visile=!0,e.editFlag=!1,e.title="新增";for(const o in e.form)e.form[o]=void 0},E=o=>{S(),e.visile=!0,e.editFlag=!0,e.title="编辑";for(const a in e.form)e.form[a]=void 0;for(const a in o)e.form[a]=o[a]},V=o=>{console.log("delete",o),K({ids:o.id}).then(a=>{f()}).catch(a=>{g.warn(a.msg||"操作失败")})},$=()=>{if(console.log(r.selectedRowKeys),r.selectedRowKeys.length<=0){console.log("hello"),g.warn("请勾选删除项");return}K({ids:r.selectedRowKeys.join(",")}).then(o=>{g.success("删除成功"),r.selectedRowKeys=[],f()}).catch(o=>{g.warn(o.msg||"操作失败")})},M=()=>{var o;(o=y.value)==null||o.validate().then(()=>{const a=new FormData;e.form.username&&a.append("username",e.form.username),e.form.password&&a.append("password",e.form.password),e.form.nickname&&a.append("nickname",e.form.nickname),e.form.role&&a.append("role",e.form.role),e.form.status&&a.append("status",e.form.status),e.form.cover&&a.append("cover",e.form.cover),e.form.mobile&&a.append("mobile",e.form.mobile),e.form.email&&a.append("email",e.form.email),e.editFlag?te({id:e.form.id},a).then(d=>{b(),f()}).catch(d=>{console.log(d),g.warn(d.msg||"操作失败")}):le(a).then(d=>{b(),f()}).catch(d=>{console.log(d),g.warn(d.msg||"操作失败")})}).catch(a=>{console.log("不能为空")})},T=()=>{b()},S=()=>{var o;(o=y.value)==null||o.resetFields()},b=()=>{e.visile=!1};return(o,a)=>{const d=i("a-button"),F=i("a-input-search"),O=i("a-space"),j=i("a-divider"),G=i("a-popconfirm"),H=i("a-table"),k=i("a-input"),m=i("a-form-item"),u=i("a-col"),x=i("a-select-option"),R=i("a-select"),J=i("a-row"),P=i("a-form"),Q=i("a-modal");return c(),p("div",null,[v("div",de,[v("div",ce,[t(O,null,{default:n(()=>[t(d,{type:"primary",onClick:q},{default:n(()=>[h("新增")]),_:1}),t(d,{onClick:$},{default:n(()=>[h("批量删除")]),_:1}),t(F,{"addon-before":"用户名","enter-button":"",onSearch:L,onChange:B})]),_:1})]),t(H,{size:"middle",rowKey:"id",loading:l(r).loading,columns:l(A),"data-source":l(r).userList,scroll:{x:"max-content"},"row-selection":l(N),pagination:{size:"default",current:l(r).page,pageSize:l(r).pageSize,onChange:s=>l(r).page=s,showSizeChanger:!1,showTotal:s=>`共${s}条数据`}},{bodyCell:n(({text:s,record:U,index:he,column:z})=>[z.key==="role"?(c(),p("span",me,[s==="1"?(c(),p("span",ue,"管理员")):_("",!0),s==="2"?(c(),p("span",pe,"普通用户")):_("",!0),s==="3"?(c(),p("span",fe,"演示账号")):_("",!0)])):_("",!0),z.key==="operation"?(c(),p("span",_e,[v("a",{onClick:W=>E(U)},"编辑",8,ge),t(j,{type:"vertical"}),t(G,{title:"确定删除?","ok-text":"是","cancel-text":"否",onConfirm:W=>V(U)},{default:n(()=>[ve]),_:2},1032,["onConfirm"])])):_("",!0)]),_:1},8,["loading","columns","data-source","row-selection","pagination"])]),v("div",null,[t(Q,{visible:l(e).visile,forceRender:!0,title:l(e).title,"ok-text":"确认","cancel-text":"取消",onCancel:T,onOk:M},{default:n(()=>[v("div",null,[t(P,{ref_key:"myform",ref:y,"label-col":{style:{width:"80px"}},model:l(e).form,rules:l(e).rules},{default:n(()=>[t(J,{gutter:24},{default:n(()=>[t(u,{span:"24"},{default:n(()=>[t(m,{label:"用户名",name:"username"},{default:n(()=>[t(k,{disabled:l(e).editFlag,placeholder:"请输入",value:l(e).form.username,"onUpdate:value":a[0]||(a[0]=s=>l(e).form.username=s),allowClear:""},null,8,["disabled","value"])]),_:1})]),_:1}),l(e).editFlag?_("",!0):(c(),D(u,{key:0,span:"24"},{default:n(()=>[t(m,{label:"密码",name:"password"},{default:n(()=>[t(k,{placeholder:"请输入",type:"password",value:l(e).form.password,"onUpdate:value":a[1]||(a[1]=s=>l(e).form.password=s),allowClear:""},null,8,["value"])]),_:1})]),_:1})),t(u,{span:"24"},{default:n(()=>[t(m,{label:"昵称",name:"nickname"},{default:n(()=>[t(k,{placeholder:"请输入",value:l(e).form.nickname,"onUpdate:value":a[2]||(a[2]=s=>l(e).form.nickname=s),allowClear:""},null,8,["value"])]),_:1})]),_:1}),t(u,{span:"24"},{default:n(()=>[t(m,{label:"角色",name:"role"},{default:n(()=>[t(R,{placeholder:"请选择",allowClear:"",value:l(e).form.role,"onUpdate:value":a[3]||(a[3]=s=>l(e).form.role=s)},{default:n(()=>[(c(!0),p(ee,null,ae(l(e).roleData,s=>(c(),D(x,{value:s.id},{default:n(()=>[h(oe(s.title),1)]),_:2},1032,["value"]))),256))]),_:1},8,["value"])]),_:1})]),_:1}),t(u,{span:"24"},{default:n(()=>[t(m,{label:"状态",name:"status"},{default:n(()=>[t(R,{placeholder:"请选择",allowClear:"",value:l(e).form.status,"onUpdate:value":a[4]||(a[4]=s=>l(e).form.status=s)},{default:n(()=>[t(x,{key:"0",value:"0"},{default:n(()=>[h("正常")]),_:1}),t(x,{key:"1",value:"1"},{default:n(()=>[h("封号")]),_:1})]),_:1},8,["value"])]),_:1})]),_:1}),t(u,{span:"24"},{default:n(()=>[t(m,{label:"邮箱",name:"email"},{default:n(()=>[t(k,{placeholder:"请输入",value:l(e).form.email,"onUpdate:value":a[5]||(a[5]=s=>l(e).form.email=s),allowClear:""},null,8,["value"])]),_:1})]),_:1}),t(u,{span:"24"},{default:n(()=>[t(m,{label:"手机号",name:"mobile"},{default:n(()=>[t(k,{placeholder:"请输入",value:l(e).form.mobile,"onUpdate:value":a[6]||(a[6]=s=>l(e).form.mobile=s),allowClear:""},null,8,["value"])]),_:1})]),_:1})]),_:1})]),_:1},8,["model","rules"])])]),_:1},8,["visible","title"])])])}}});const be=re(ke,[["__scopeId","data-v-8998fc14"]]);export{be as default};