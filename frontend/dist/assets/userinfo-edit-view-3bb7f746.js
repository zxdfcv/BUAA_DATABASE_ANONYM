import{u as k,z as y,a as I,k as U,J as F,B as V,r as v,o as p,b as _,l as h,x as g,e,f as o,w as c,v as m,h as S,K as B,m as A,p as D,g as E}from"./index-68c43909.js";import{A as N}from"./avatar-4ee3f7af.js";import{_ as C}from"./_plugin-vue_export-helper-c27b6911.js";const i=d=>(D("data-v-8e3fda31"),d=d(),E(),d),G={class:"content-list"},M=i(()=>e("div",{class:"list-title"},"设置",-1)),P={class:"list-content"},J={class:"edit-view"},R={class:"item flex-view"},T=i(()=>e("div",{class:"label"},"头像",-1)),z={class:"right-box avatar-box flex-view"},K=["src"],L=["src"],X={class:"change-tips flex-view"},$=i(()=>e("label",null,"点击更换头像",-1)),j=i(()=>e("p",{class:"tip"},"图片格式支持 GIF、PNG、JPEG，尺寸不小于 200 PX，小于 4 MB",-1)),q={class:"item flex-view"},H=i(()=>e("div",{class:"label"},"昵称",-1)),O={class:"right-box"},Q=i(()=>e("p",{class:"tip"},"支持中英文，长度不能超过 20 个字符",-1)),W={class:"item flex-view"},Y=i(()=>e("div",{class:"label"},"手机号",-1)),Z={class:"right-box"},ee={class:"item flex-view"},se=i(()=>e("div",{class:"label"},"邮箱",-1)),te={class:"right-box"},oe={class:"item flex-view"},ae=i(()=>e("div",{class:"label"},"个人简介",-1)),ie={class:"right-box"},ne=i(()=>e("p",{class:"tip"},"限制200字以内",-1)),le={__name:"userinfo-edit-view",setup(d){S();const f=k();let r=y(!1),s=I({form:{avatar:void 0,avatarFile:void 0,nickname:void 0,email:void 0,mobile:void 0,description:void 0}});U(()=>{u()});const x=a=>{const t=new Date().getTime().toString()+"."+a.type.substring(6),l=new File([a],t);return console.log(l),s.form.avatarFile=l,!1},u=()=>{r.value=!0;let a=f.user_id;F({id:a}).then(t=>{s.form=t.data,s.form.avatar&&(s.form.avatar=V+s.form.avatar),r.value=!1}).catch(t=>{console.log(t),r.value=!1})},b=()=>{let a=new FormData,t=f.user_id;s.form.avatarFile&&a.append("avatar",s.form.avatarFile),s.form.nickname&&a.append("nickname",s.form.nickname),s.form.email&&a.append("email",s.form.email),s.form.mobile&&a.append("mobile",s.form.mobile),s.form.description&&a.append("description",s.form.description),B({id:t},a).then(l=>{A.success("保存成功"),u()}).catch(l=>{console.log(l)})};return(a,t)=>{const l=v("a-upload"),w=v("a-spin");return p(),_("div",G,[M,h(w,{spinning:o(r),style:{"min-height":"200px"}},{default:g(()=>[e("div",P,[e("div",J,[e("div",R,[T,e("div",z,[o(s).form&&o(s).form.avatar?(p(),_("img",{key:0,src:o(s).form.avatar,class:"avatar"},null,8,K)):(p(),_("img",{key:1,src:o(N),class:"avatar"},null,8,L)),e("div",X,[h(l,{name:"file",accept:"image/*",multiple:!1,"before-upload":x},{default:g(()=>[$]),_:1}),j])])]),e("div",q,[H,e("div",O,[c(e("input",{type:"text","onUpdate:modelValue":t[0]||(t[0]=n=>o(s).form.nickname=n),placeholder:"请输入昵称",maxlength:"20",class:"input-dom"},null,512),[[m,o(s).form.nickname]]),Q])]),e("div",W,[Y,e("div",Z,[c(e("input",{type:"text","onUpdate:modelValue":t[1]||(t[1]=n=>o(s).form.mobile=n),placeholder:"请输入邮箱",maxlength:"100",class:"input-dom web-input"},null,512),[[m,o(s).form.mobile]])])]),e("div",ee,[se,e("div",te,[c(e("input",{type:"text","onUpdate:modelValue":t[2]||(t[2]=n=>o(s).form.email=n),placeholder:"请输入邮箱",maxlength:"100",class:"input-dom web-input"},null,512),[[m,o(s).form.email]])])]),e("div",oe,[ae,e("div",ie,[c(e("textarea",{"onUpdate:modelValue":t[3]||(t[3]=n=>o(s).form.description=n),placeholder:"请输入简介",maxlength:"200",class:"intro"},`\r
          `,512),[[m,o(s).form.description]]),ne])]),e("button",{class:"save mg",onClick:t[4]||(t[4]=n=>b())},"保存")])])]),_:1},8,["spinning"])])}}},me=C(le,[["__scopeId","data-v-8e3fda31"]]);export{me as default};