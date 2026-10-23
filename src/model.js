export const uid = () => crypto.randomUUID();
export function initialState() {
  return {version:1, strategies:[{id:uid(),name:'추세 눌림목 · 샘플',sample:true,thresholds:{'A+':90,A:80,B:70},items:[
    {id:uid(),label:'상위 시간대의 추세와 진입 방향이 일치한다',weight:25,required:true},
    {id:uid(),label:'진입 전 손절 가격과 리스크를 정했다',weight:20,required:true},
    {id:uid(),label:'주요 지지·저항 구간에서 반응이 확인된다',weight:20,required:false},
    {id:uid(),label:'거래량이 셋업을 뒷받침한다',weight:15,required:false},
    {id:uid(),label:'계획한 손익비가 2R 이상이다',weight:10,required:false},
    {id:uid(),label:'충동이 아닌 사전 계획에 따른 진입이다',weight:10,required:false}
  ]}],records:[]};
}
export function evaluate(strategy, checked) {
  const total=strategy.items.reduce((s,i)=>s+i.weight,0);
  const earned=strategy.items.reduce((s,i)=>s+(checked.includes(i.id)?i.weight:0),0);
  const score=total?earned/total*100:0;
  const missing=strategy.items.filter(i=>!checked.includes(i.id));
  const blocked=missing.some(i=>i.required);
  const grade=blocked||!total?'PASS':score>=strategy.thresholds['A+']?'A+':score>=strategy.thresholds.A?'A':score>=strategy.thresholds.B?'B':'PASS';
  return {score,earned,total,missing,blocked,grade};
}
export function statistics(records) {
  return ['A+','A','B','PASS'].map(grade=>{
    const all=records.filter(r=>r.grade===grade), closed=all.filter(r=>r.status==='closed');
    return {grade,total:all.length,count:closed.length,skipped:all.filter(r=>r.status==='skipped').length,winRate:closed.length?closed.filter(r=>r.result>0).length/closed.length*100:null,average:closed.length?closed.reduce((s,r)=>s+r.result,0)/closed.length:null};
  });
}
export function validateState(s) {
  const obj=x=>x&&typeof x==='object'&&!Array.isArray(x);
  const str=x=>typeof x==='string';
  const id=x=>str(x)&&/^[a-zA-Z0-9_-]{1,100}$/.test(x);
  const num=x=>typeof x==='number'&&Number.isFinite(x);
  const unique=a=>new Set(a.map(x=>x.id)).size===a.length;
  if(!obj(s)||s.version!==1||!Array.isArray(s.strategies)||!s.strategies.length||!Array.isArray(s.records))throw Error('지원하지 않는 백업 형식입니다.');
  if(!unique(s.strategies)||!unique(s.records))throw Error('중복된 ID가 있습니다.');
  for(const p of s.strategies){
    const t=p.thresholds;
    if(!id(p.id)||!str(p.name)||!p.name.trim()||!obj(t)||![t['A+'],t.A,t.B].every(v=>num(v)&&v>0&&v<=100)||!(t['A+']>t.A&&t.A>t.B)||!Array.isArray(p.items)||!p.items.length||!unique(p.items))throw Error('매매법 또는 등급 기준이 올바르지 않습니다.');
    for(const i of p.items)if(!id(i.id)||!str(i.label)||!i.label.trim()||!num(i.weight)||i.weight<0||typeof i.required!=='boolean')throw Error('체크리스트 항목이 올바르지 않습니다.');
    if(!p.items.some(i=>i.weight>0))throw Error('배점 합계는 0보다 커야 합니다.');
  }
  for(const r of s.records)if(!id(r.id)||!str(r.createdAt)||!Number.isFinite(Date.parse(r.createdAt))||!str(r.symbol)||!str(r.strategyName)||!str(r.note)||!['long','short'].includes(r.direction)||!['A+','A','B','PASS'].includes(r.grade)||!num(r.score)||r.score<0||r.score>100||!['pending','closed','skipped'].includes(r.status)||(r.status==='closed'?!num(r.result):r.result!==null)||!Array.isArray(r.conditions)||r.conditions.some(c=>!obj(c)||!str(c.label)||typeof c.checked!=='boolean'||typeof c.required!=='boolean'||!num(c.weight)||c.weight<0))throw Error('평가 기록이 올바르지 않습니다.');
  return s;
}
