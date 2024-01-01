function l(n,o){const c="\uFEFF",r=Object.keys(n[0]).join(",")+`
`,s=n.map(u=>Object.values(u).map(t=>Array.isArray(t)||typeof t=="string"&&t.includes(",")?`"${t}"`.replace(/,/g," "):t).join(",")).join(`
`),d=c+r+s,i=new Blob([d],{type:"text/csv;charset=utf-8;"}),e=document.createElement("a"),a=URL.createObjectURL(i);e.href=a,e.setAttribute("download",o||"exported_data.csv"),document.body.appendChild(e),e.click(),document.body.removeChild(e)}export{l as e};
