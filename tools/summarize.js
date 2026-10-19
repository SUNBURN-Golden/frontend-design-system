const fs=require('fs');
const files=process.argv.slice(2);
for(const f of files){let j;try{j=JSON.parse(fs.readFileSync(f))}catch(e){console.log(f,'parse err');continue}
 console.log('=== '+f);
 for(const[k,v]of Object.entries(j)){
  if(v.error){console.log(k,'ERR',v.error);continue}
  const t=x=>x?[x.fs,x.lh,x.ls,x.fw,(x.ff||'').split(',')[0].replace(/"/g,'')].join('/'):'-';
  console.log(k,'| h1',t(v.h1),'| p',t(v.p),'cpl',v.cpl&&v.cpl.width+'px','| body',v.body&&v.body.fs,'| hdr',v.hdrH,v.blur?('blur '+v.blur.bf+' '+v.blur.bg):'noblur','| rad',JSON.stringify((v.radius||[]).slice(0,4)),'| shadow',(v.shadow||[]).length?(v.shadow[0][0].slice(0,60)+' x'+v.shadow[0][1]):'none','| trans',JSON.stringify((v.trans||[]).slice(0,2)),'| sizes',(v.sizes||[]).slice(0,6).map(x=>x[0]).join(','),'| small',v.smallTargets,'| bg',v.bodyBg,'| scrollW',v.scrollW);
 }}
