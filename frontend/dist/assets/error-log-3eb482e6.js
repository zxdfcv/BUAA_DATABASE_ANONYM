import{b as r}from"./log-59a2d5cf.js";import{d as c,a as l,A as g,r as _,b as p,o as m,n as u,g as f,f as x,i as t}from"./index-6b603672.js";import{_ as y}from"./_plugin-vue_export-helper-c27b6911.js";const h={class:"page-view"},k=c({__name:"error-log",setup(w){const i=l([{title:"序号",dataIndex:"index",key:"index",align:"center"},{title:"请求方式",dataIndex:"method",key:"method",align:"center"},{title:"请求URL",dataIndex:"url",key:"url",align:"center"},{title:"异常信息",dataIndex:"content",key:"content"},{title:"操作IP",dataIndex:"ip",key:"ip",align:"center"},{title:"操作时间",dataIndex:"log_time",key:"log_time",align:"center"}]),e=l({dataList:[],loading:!1,keyword:"",selectedRowKeys:[],pageSize:10,page:1});g(()=>{d()});const d=()=>{e.loading=!0,r({keyword:e.keyword}).then(a=>{e.loading=!1,console.log(a),a.data.forEach((o,n)=>{o.index=n+1}),e.dataList=a.data}).catch(a=>{e.loading=!1,console.log(a)})};return _({onChange:(a,o)=>{console.log(`selectedRowKeys: ${a}`,"selectedRows: ",o),e.selectedRowKeys=a}}),(a,o)=>{const n=p("a-table");return m(),u("div",null,[f("div",h,[x(n,{size:"middle",rowKey:"id",loading:t(e).loading,columns:t(i),"data-source":t(e).dataList,scroll:{x:"max-content"},pagination:{size:"default",current:t(e).page,pageSize:t(e).pageSize,onChange:s=>t(e).page=s,showSizeChanger:!1,showTotal:s=>`共${s}条数据`}},null,8,["loading","columns","data-source","pagination"])])])}}});const z=y(k,[["__scopeId","data-v-4a9746a8"]]);export{z as default};
