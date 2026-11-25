#!/usr/bin/env python3
"""허브의 와우 포에버 애드온 페이지(public/addons/)를 만든다.

애드온 버전이나 설명이 바뀌면 아래 ADDONS를 고치고 다시 실행:
    python3 tools/build_addons_pages.py
"""
import html
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "public" / "addons"
REPO = "https://github.com/hyveo/wow-forever-addons"
ISSUES = REPO + "/issues"

# cf_live: CurseForge 검수 통과 후 True로 바꾸면 "검수 중" 표시가 사라진다
ADDONS = [
    {
        "slug": "levelpace",
        "folder": "LevelPace",
        "name": "레벨페이스",
        "en": "LevelPace",
        "version": "1.2.0",
        "cf": "https://www.curseforge.com/wow/addons/levelpace",
        "cf_live": True,
        "summary": "시간당 경험치와 레벨업까지 남은 시간을 작은 바로 보여주는 레벨링 도우미예요. 퀘스트·사냥 경험치 구분, 레벨업 기록까지.",
        "lead": "지금 속도면 언제 레벨업할지 알려주는 레벨링 도우미예요.",
        "card": "levelpace-card.png",
        "shots": [
            ("levelpace-bar.png", "정보 바 — 드래그로 옮기고, 우클릭하면 상세 창이 열려요"),
            ("levelpace-window.png", "상세 창 (/lp) — 세션 통계와 레벨업 기록"),
        ],
        "features": [
            ("레벨업까지 남은 시간", "최근 10분 속도로 계산해서, 쉬었다 와도 금방 다시 맞춰져요."),
            ("퀘스트 vs 사냥", "경험치를 어디서 더 많이 얻는지, 몹을 몇 마리 더 잡으면 되는지 보여줘요."),
            ("레벨업 기록", "레벨마다 걸린 시간이 캐릭터별로 남아요. 로그아웃해도 이어져요."),
            ("10개 언어", "English, 한국어, Deutsch, Español (América Latina), Español (España), Français, Português, Русский, 简体中文, 繁體中文. 애드온 센터에서 고른 언어를 따라가요."),
        ],
        "commands": [("/lp", "상세 창 열기"), ("/lp 바", "바 보이기/숨기기"), ("/lp 잠금", "바 잠금/해제"), ("/lp 초기화", "세션 초기화"), ("/lp 미니맵", "미니맵 버튼 보이기/숨기기")],
    },
    {
        "slug": "centerbar",
        "folder": "CenterBar",
        "name": "센터바",
        "en": "CenterBar",
        "version": "1.7.0",
        "cf": "https://www.curseforge.com/wow/addons/centerbar",
        "cf_live": True,
        "summary": "캐릭터 양옆에 액션 버튼을 최대 18개 놓아 주는 애드온이에요. 시선을 화면 가운데에 둔 채로 기술을 쓸 수 있어요.",
        "lead": "캐릭터 양옆에 액션 버튼을 최대 18개 놓아 주는 애드온이에요.",
        "card": "centerbar-card.png",
        "shots": [("centerbar-card.png", "캐릭터 양옆에 버튼 18개를 놓은 모습")],
        "features": [
            ("슬롯 5개", "슬롯마다 넣은 기술이 따로 저장돼요. 다른 액션바와 섞이지 않고, 특성마다 쓰는 슬롯을 기억해요."),
            ("내 맘대로 배치", "세로 3줄·둥글게 등 배치 5종, 화면 격자에서 버튼을 하나씩 끌어 옮기기, 표시 개수 6/12/18."),
            ("필요할 때만 또렷하게", "투명도를 낮춰 두고 전투 시·대상 선택 시·마우스를 올렸을 때만 또렷하게. 미니맵 버튼, 단축키 18개."),
            ("10개 언어", "English, 한국어, Deutsch, Español (América Latina), Español (España), Français, Português, Русский, 简体中文, 繁體中文. 애드온 센터에서 고른 언어를 따라가고, 설정 창에서 따로 고를 수도 있어요."),
        ],
        "commands": [("/cb", "설정 창 열기"), ("/cb 1 ~ /cb 5", "슬롯 바꾸기"), ("/cb lock", "위치 잠금/해제"), ("/cb reset", "처음으로")],
    },
    {
        "slug": "hyveo-center",
        "folder": "HyveoCenter",
        "name": "hyveo 애드온 센터",
        "en": "hyveo Addon Center",
        "version": "1.1.0",
        "cf": "https://www.curseforge.com/wow/addons/hyveo-addon-center-hyveo",
        "cf_live": True,
        "summary": "레벨페이스와 센터바를 게임 안에서 한 창으로 켜고 끄고, 열고, 자주 쓰는 설정을 바꿔요.",
        "lead": "hyveo 애드온을 게임 안에서 한 창으로 관리해요.",
        "card": "hyveocenter-card.png",
        "shots": [("hyveocenter-card.png", "게임 안 센터 창 (/hv)")],
        "features": [
            ("한눈에 보기", "설치·켜짐 상태와 버전을 한 화면에서 확인해요."),
            ("바로 열기", "/hv lp, /hv cb 처럼 각 애드온 창을 바로 열어요."),
            ("빠른 설정", "레벨페이스 정보 바, 센터바 보이는 때를 바로 바꿔요."),
            ("10개 언어", "English, 한국어, Deutsch, Español (América Latina), Español (España), Français, Português, Русский, 简体中文, 繁體中文. 여기서 고른 언어를 모든 hyveo 애드온이 따라가요."),
        ],
        "commands": [("/hv", "센터 열기"), ("/hv lp", "레벨페이스 창"), ("/hv cb", "센터바 설정 창"), ("/hv help", "명령어 목록")],
    },
]

GA = """<script async src="https://www.googletagmanager.com/gtag/js?id=G-9G9M8R1CRC"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-9G9M8R1CRC');</script>"""

CSS = """
*{box-sizing:border-box}
body{margin:0;background:#0D1117;color:#E6EDF3;font-family:'Noto Sans KR',system-ui,sans-serif;line-height:1.6}
a{color:#58A6FF}a:hover{color:#79C0FF}
.mono{font-family:'JetBrains Mono',ui-monospace,monospace}
header{border-bottom:1px solid rgba(255,255,255,.1)}
.wrap{max-width:1040px;margin:0 auto;padding:0 24px}
.top{display:flex;flex-wrap:wrap;gap:16px;align-items:center;justify-content:space-between;padding:16px 24px}
.brand{font-weight:600;color:#3FB950;text-decoration:none;font-size:15px}
nav{display:flex;gap:24px;font-size:13px}
nav a{color:#9198A1;text-decoration:none}nav a.on{color:#E6EDF3}
main{padding:56px 0 80px;display:flex;flex-direction:column;gap:56px}
h1{margin:0;font-size:clamp(32px,5vw,44px);font-weight:800;letter-spacing:-.5px;line-height:1.2}
h2{margin:0;font-size:20px;font-weight:700}
h3{margin:0;font-size:17px;font-weight:700}
.eyebrow{margin:0;font-size:13px;color:#3FB950}
.lead{margin:0;font-size:17px;color:#9198A1;max-width:640px}
.story{margin:0;font-size:13px;color:#9198A1;font-style:italic}
.btns{display:flex;flex-wrap:wrap;gap:10px}
.btn{display:inline-flex;align-items:center;gap:8px;min-height:44px;padding:0 18px;border-radius:6px;font-weight:600;font-size:15px;text-decoration:none;border:1px solid rgba(255,255,255,.2);color:#E6EDF3;background:transparent}
.btn:hover{color:#fff;border-color:rgba(255,255,255,.4)}
.btn.primary{background:#238636;border-color:#238636;color:#fff}
.btn.primary:hover{background:#2ea043}
.btn.light{background:#E6EDF3;color:#0D1117;border-color:#E6EDF3}
.btn.link{border:0;padding:0 8px;color:#58A6FF}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:16px}
.box{background:#161B22;border:1px solid rgba(255,255,255,.1);border-radius:12px;padding:24px;display:flex;flex-direction:column;gap:14px}
.box.rec{border-color:#3FB950}
.muted{color:#9198A1;font-size:14px;margin:0}
.badge{display:inline-block;font-size:12px;border-radius:999px;padding:1px 9px;border:1px solid rgba(255,255,255,.15);color:#9198A1}
.badge.ver{color:#3FB950;border-color:rgba(63,185,80,.5)}
.badge.wait{color:#E3B341;border-color:rgba(227,179,65,.5)}
.badge.rec{background:#3FB950;color:#0D1117;border-color:#3FB950;font-weight:600}
.badge.dl{color:#0D1117;background:#58A6FF;border-color:#58A6FF;font-weight:700;font-size:13px;padding:2px 10px}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:12px}
.stat{background:#0D1117;border:1px solid rgba(255,255,255,.1);border-radius:10px;padding:14px 16px;display:flex;flex-direction:column;gap:2px}
.stat b{font-size:32px;font-weight:800;line-height:1.2}
.stat .up{color:#3FB950;font-size:13px}
.chart svg{display:block;width:100%;height:auto}
.vt{width:100%;border-collapse:collapse;font-size:14px}
.vt th,.vt td{padding:6px 4px;border-bottom:1px solid rgba(255,255,255,.08);text-align:right}
.vt th:first-child,.vt td:first-child{text-align:left}
.vt td.tR{color:#3FB950;font-weight:700}.vt td.tB{color:#E3B341;font-weight:700}.vt td.tA{color:#F85149;font-weight:700}
.vt th{color:#9198A1;font-weight:500;font-size:12px}
.vt .up{color:#3FB950}
.legend{display:flex;flex-wrap:wrap;gap:14px;font-size:13px;color:#9198A1}
.legend i{display:inline-block;width:10px;height:10px;border-radius:3px;margin-right:6px;vertical-align:middle}
.card{background:#161B22;border:1px solid rgba(255,255,255,.1);border-radius:12px;padding:24px;display:flex;flex-direction:column;gap:16px}
.card .head{display:flex;gap:16px;align-items:center}
.card .head img{width:64px;height:64px;border-radius:12px;flex-shrink:0}
.card .shot{width:100%;aspect-ratio:16/9;object-fit:cover;border-radius:8px;border:1px solid rgba(255,255,255,.08);display:block}
.card .btns{margin-top:auto}.card .btn.cf{flex:1 1 100%;justify-content:center}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:16px}
code{font-family:'JetBrains Mono',ui-monospace,monospace;font-size:13px;background:rgba(255,255,255,.08);padding:1px 6px;border-radius:4px;color:#E6EDF3}
.hero{display:flex;flex-wrap:wrap;gap:32px;align-items:center}
.hero img{width:140px;height:140px;border-radius:24px}
.hero .txt{flex:999 1 420px;min-width:0;display:flex;flex-direction:column;gap:14px}
figure{margin:0;background:#161B22;border:1px solid rgba(255,255,255,.1);border-radius:12px;padding:14px;display:flex;flex-direction:column;gap:10px}
figure img{width:100%;border-radius:8px;display:block}
figcaption{font-size:14px;color:#9198A1}
ol{margin:0;padding-left:22px;display:flex;flex-direction:column;gap:10px;color:#C9D1D9}
.cmds{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:8px;border-top:1px solid rgba(255,255,255,.1);padding-top:16px;font-size:14px}
.cmds span{color:#9198A1}
.note{border:1px dashed rgba(255,255,255,.2);border-radius:12px;padding:20px 24px;display:flex;flex-wrap:wrap;gap:12px;align-items:center;justify-content:space-between}
footer{border-top:1px solid rgba(255,255,255,.1)}
footer .wrap{display:flex;flex-wrap:wrap;gap:12px;justify-content:space-between;padding:24px;font-size:12px;color:#9198A1}
footer a{color:#9198A1}
"""

DL_JS = r"""<script>
(function(){
  var COLORS={"centerbar":"#58A6FF","levelpace":"#A371F7","hyveo-center":"#E3B341"};
  var url=document.currentScript.getAttribute('data-src');
  function n(x){return Number(x||0).toLocaleString('ko-KR');}
  function el(tag,attrs,text){var e=document.createElementNS('http://www.w3.org/2000/svg',tag);for(var k in attrs)e.setAttribute(k,attrs[k]);if(text!=null)e.textContent=text;return e;}
  var TK={"R":"[R]","B":"[B]","A":"[A]"},TN={"R":"정식","B":"베타","A":"알파"};
  Promise.all([fetch(url,{cache:'no-cache'}).then(function(r){return r.json();}),
    fetch(url.replace('downloads.json','files.json'),{cache:'no-cache'}).then(function(r){return r.ok?r.json():{};}).catch(function(){return {};})
  ]).then(function(rs){var d=rs[0],FM=(rs[1]||{}).files||{};
    var h=d.history||[];if(!h.length)return;
    var last=h[h.length-1],prev=h.length>1?h[h.length-2]:null,keys=Object.keys(d.addons||{});
    var today=last.at.slice(0,10),day0=null;for(var q=h.length-1;q>=0;q--){if(h[q].at.slice(0,10)<today){day0=h[q];break;}}
    document.querySelectorAll('[data-dl]').forEach(function(b){var k=b.getAttribute('data-dl');if(last[k]==null)return;b.textContent='다운로드 '+n(last[k]);b.hidden=false;});
    var vlast=null,vprev=null;for(var i=h.length-1;i>=0;i--){if(h[i].versions){if(!vlast)vlast=h[i];else{vprev=h[i];break;}}}
    document.querySelectorAll('[data-dl-versions]').forEach(function(w){
      var k=w.getAttribute('data-dl-versions'),v=vlast&&vlast.versions[k];if(!v)return;
      var t=document.createElement('table');t.className='vt mono';
      var dvr=null;for(var z=h.length-1;z>=0;z--){if(h[z].at.slice(0,10)<today&&h[z].versions){dvr=h[z];break;}}
      var dv=dvr?dvr.versions[k]||{}:null;
      var pv=vprev&&vprev!==dvr?vprev.versions[k]:null;
      var fm=FM[k]||{},hasM=Object.keys(fm).length>0;
      var hr=document.createElement('tr');['버전',hasM?'타입':'',hasM?'업로드':'','다운로드',pv?'변화':'',dv?'오늘':''].forEach(function(x){if(x==='')return;var th=document.createElement('th');th.textContent=x;hr.appendChild(th);});t.appendChild(hr);
      Object.keys(v).forEach(function(ver){var tr=document.createElement('tr');
        var a=document.createElement('td');a.textContent=ver;tr.appendChild(a);
        if(hasM){var m=fm[ver]||{};var ty=document.createElement('td');ty.textContent=TK[m.type]||'';ty.title=TN[m.type]||'';ty.className='t'+(m.type||'');tr.appendChild(ty);
          var up=document.createElement('td');up.textContent=m.uploaded?m.uploaded.slice(2,10).replace(/-/g,'.'):'';tr.appendChild(up);}
        var b=document.createElement('td');b.textContent=n(v[ver]);tr.appendChild(b);
        if(pv){var c=document.createElement('td');var dd=v[ver]-(pv[ver]||0);c.textContent=(dd>0?'+':'')+n(dd);if(dd>0)c.className='up';tr.appendChild(c);}
        if(dv){var c2=document.createElement('td');var dt=v[ver]-(dv[ver]||0);c2.textContent=(dt>0?'+':'')+n(dt);if(dt>0)c2.className='up';tr.appendChild(c2);}
        t.appendChild(tr);});
      var tgt=w.querySelector('.vbody')||w;tgt.textContent='';tgt.appendChild(t);
      var when=w.querySelector('.vwhen');if(when)when.textContent=vlast.at.slice(0,10)+' 기준';
      w.hidden=false;
    });
    var box=document.getElementById('downloads');if(!box)return;box.hidden=false;
    var total=function(r){return keys.reduce(function(s,k){return s+(r[k]||0);},0);};
    var stats=box.querySelector('.stats');stats.textContent='';
    [['total','전체']].concat(keys.map(function(k){return [k,d.addons[k]];})).forEach(function(p){
      var v=p[0]==='total'?total(last):(last[p[0]]||0),pv=prev?(p[0]==='total'?total(prev):(prev[p[0]]||0)):null;
      var c=document.createElement('div');c.className='stat';
      var l=document.createElement('span');l.className='muted';l.textContent=p[1];
      var b=document.createElement('b');b.textContent=n(v);
      c.appendChild(l);c.appendChild(b);
      if(day0){var dv0=p[0]==='total'?total(day0):(day0[p[0]]||0);var td=document.createElement('span');td.className='up mono';td.style.fontWeight='700';td.textContent='오늘 +'+n(v-dv0);c.appendChild(td);}
      if(pv!=null){var u=document.createElement('span');u.className='up mono';u.textContent=(v-pv>=0?'+':'')+n(v-pv)+' 지난 기록 대비';c.appendChild(u);}
      stats.appendChild(c);
    });
    var periods=box.querySelector('.periods');
    if(periods){
      var y=+today.slice(0,4),mo=+today.slice(5,7),dd=+today.slice(8,10);
      var dow=new Date(Date.UTC(y,mo-1,dd)).getUTCDay(),mon=new Date(Date.UTC(y,mo-1,dd-((dow+6)%7))).toISOString().slice(0,10);
      var monthStart=today.slice(0,8)+'01';
      function baseFor(start){for(var q=h.length-1;q>=0;q--){if(h[q].at.slice(0,10)<start)return {r:h[q],partial:false};}return {r:{},partial:true};}
      var rows=[['오늘',baseFor(today)],['이번 주 ('+mon.slice(5).replace('-','/')+'~)',baseFor(mon)],['이번 달 ('+mo+'월)',baseFor(monthStart)]];
      var t=document.createElement('table');t.className='vt mono';
      var hr=document.createElement('tr');['기간','전체'].concat(keys.map(function(k){return d.addons[k];})).forEach(function(x){var th=document.createElement('th');th.textContent=x;hr.appendChild(th);});t.appendChild(hr);
      var note=false;
      rows.forEach(function(rw){var b=rw[1].r;var tr=document.createElement('tr');var a=document.createElement('td');a.textContent=rw[0]+(rw[1].partial?' *':'');if(rw[1].partial)note=true;tr.appendChild(a);
        [total(last)-total(b)].concat(keys.map(function(k){return (last[k]||0)-(b[k]||0);})).forEach(function(v2){var c=document.createElement('td');c.textContent='+'+n(v2);if(v2>0)c.className='up';tr.appendChild(c);});t.appendChild(tr);});
      periods.textContent='';periods.appendChild(t);
      if(note){var nt=document.createElement('p');nt.className='muted';nt.style.fontSize='12px';nt.textContent='* 이 기간 시작 전 기록이 없어 첫 배포부터의 누적으로 계산했어요.';periods.appendChild(nt);}
      periods.hidden=false;
    }
    box.querySelector('.when').textContent=last.at.slice(0,10)+' 기준 · CurseForge 누적 다운로드';
    var wrap=box.querySelector('.chart');
    function draw(){
      wrap.textContent='';var W=Math.max(280,wrap.clientWidth),H=200,P={l:40,r:12,t:12,b:26};
      var max=Math.max(1,d3max());function d3max(){var m=0;h.forEach(function(r){keys.forEach(function(k){m=Math.max(m,r[k]||0);});});return m;}
      var svg=el('svg',{viewBox:'0 0 '+W+' '+H,role:'img','aria-label':'애드온별 누적 다운로드 추이'});
      var x=function(i){return h.length<2?(P.l+(W-P.l-P.r)/2):P.l+i*(W-P.l-P.r)/(h.length-1);};
      var y=function(v){return P.t+(H-P.t-P.b)*(1-v/max);};
      [0,.5,1].forEach(function(f){var v=Math.round(max*f);svg.appendChild(el('line',{x1:P.l,x2:W-P.r,y1:y(v),y2:y(v),stroke:'rgba(255,255,255,.08)'}));svg.appendChild(el('text',{x:P.l-6,y:y(v)+4,'text-anchor':'end','font-size':11,fill:'#9198A1'},n(v)));});
      [0,h.length-1].filter(function(i,j,a){return a.indexOf(i)===j;}).forEach(function(i){svg.appendChild(el('text',{x:x(i),y:H-6,'text-anchor':i===0&&h.length>1?'start':(h.length>1?'end':'middle'),'font-size':11,fill:'#9198A1'},h[i].at.slice(5,10)));});
      keys.forEach(function(k){
        var pts=h.map(function(r,i){return x(i)+','+y(r[k]||0);}).join(' ');
        if(h.length>1)svg.appendChild(el('polyline',{points:pts,fill:'none',stroke:COLORS[k]||'#E6EDF3','stroke-width':2}));
        h.forEach(function(r,i){var c=el('circle',{cx:x(i),cy:y(r[k]||0),r:3,fill:COLORS[k]||'#E6EDF3'});c.appendChild(el('title',{},(d.addons[k]||k)+' '+r.at.slice(0,10)+': '+n(r[k])));svg.appendChild(c);});
      });
      wrap.appendChild(svg);
    }
    draw();window.addEventListener('resize',draw);
    var lg=box.querySelector('.legend');lg.textContent='';keys.forEach(function(k){var s=document.createElement('span');var i=document.createElement('i');i.style.background=COLORS[k]||'#E6EDF3';s.appendChild(i);s.appendChild(document.createTextNode(d.addons[k]));lg.appendChild(s);});
  }).catch(function(){});
})();
</script>"""

DL = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3v12"/><path d="m7 10 5 5 5-5"/><path d="M5 21h14"/></svg>'


def e(s):
    return html.escape(s, quote=True)


def zip_url(a):
    return f"{REPO}/releases/download/{a['folder']}-v{a['version']}/{a['folder']}-{a['version']}.zip"


def page(title, desc, body, depth):
    up = "../" * depth
    out = f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<link rel="icon" href="{up}addons/img/hyveocenter-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
{GA}
<style>{CSS}</style>
</head>
<body>
<header><div class="wrap top">
<a class="brand mono" href="{up}">~/hyveo</a>
<nav class="mono" aria-label="주 메뉴"><a href="{up}">projects</a><a class="on" href="{up}addons/">addons</a></nav>
</div></header>
<div class="wrap"><main>
{body}
</main></div>
<script data-src="{up}addons/downloads.json">__DLJS__</script>
<footer><div class="wrap mono">
<span>© @hyveo · All Rights Reserved</span>
<a href="{ISSUES}">버그 제보는 GitHub Issues로</a>
</div></footer>
</body>
</html>
"""
    js = DL_JS.replace("<script>", f'<script data-src="{up}addons/downloads.json">', 1)
    return out.replace(f'<script data-src="{up}addons/downloads.json">__DLJS__</script>', js)


def cf_button(a):
    return f'<a class="btn primary cf" href="{a["cf"]}">{DL}CurseForge 앱으로 설치</a>'


def wait_badge(a):
    return "" if a["cf_live"] else '<span class="badge wait" title="CurseForge 검수가 끝나면 설치 버튼이 열려요">CurseForge 검수 중</span>'


def index():
    cards = []
    for a in ADDONS:
        cards.append(f"""<article class="card">
<div class="head"><img src="img/{a['slug'].replace('-','')}-icon.png" alt="{e(a['name'])} 아이콘" width="64" height="64">
<div><h3>{e(a['name'])} <span class="mono" style="font-size:12px;color:#9198A1;font-weight:400">{e(a['en'])}</span></h3>
<div style="display:flex;flex-wrap:wrap;gap:6px;margin-top:4px"><span class="badge ver mono">{a['version']}</span><span class="badge dl mono" data-dl="{a['slug']}" hidden></span>{wait_badge(a)}</div></div></div>
<p class="muted" style="color:#C9D1D9;font-size:15px">{e(a['summary'])}</p>
<img class="shot" src="img/{a['card']}" alt="{e(a['name'])} 예시 화면" loading="lazy">
<div class="btns">{cf_button(a)}
<a class="btn" href="{zip_url(a)}">zip 받기</a>
<a class="btn link" href="{a['slug']}/">자세히 보기 →</a></div>
</article>""")
    body = f"""<section style="display:flex;flex-direction:column;gap:16px">
<p class="eyebrow mono">wow-forever-addons</p>
<h1>와우 포에버 애드온</h1>
<p class="lead">와우 포에버에서 바로 쓸 수 있는 애드온을 모아뒀어요. CurseForge 앱에서 버튼 한 번으로 설치하거나, zip을 받아 직접 넣을 수 있어요.</p>
<p class="story">남편용 · Made for my husband, who plays WoW Forever 💛</p>
<div class="btns" style="margin-top:8px">
<a class="btn light" href="{REPO}/issues/new?template=addon-request.md">애드온 요청하기</a>
<a class="btn" href="{REPO}">GitHub 레포</a></div>
</section>

<section id="downloads" class="box" aria-labelledby="dlh" hidden>
<h2 id="dlh">다운로드 현황</h2>
<p class="muted when"></p>
<div class="stats"></div>
<div class="periods" hidden></div>
<div class="chart"></div>
<div class="legend"></div>
<h3 style="margin-top:8px">버전별 다운로드</h3>
<div class="grid">
{''.join(f'<div class="box" data-dl-versions="{a["slug"]}" hidden style="padding:16px;gap:8px"><h3 style="font-size:15px">{e(a["name"])}</h3><div class="vbody"></div></div>' for a in ADDONS)}
</div>
<p class="muted" style="font-size:12px">매일 저녁 CurseForge 기준으로 갱신돼요. zip 직접 다운로드는 포함되지 않아요.</p>
</section>

<section style="display:flex;flex-direction:column;gap:16px" aria-labelledby="ways">
<h2 id="ways">설치 방법은 두 가지예요</h2>
<div class="grid">
<div class="box rec"><div style="display:flex;gap:10px;align-items:center"><span class="badge rec mono">추천</span><h3>CurseForge 앱으로 설치</h3></div>
<p class="muted">CurseForge 앱이 깔려 있으면 [CurseForge 앱으로 설치]를 눌러 페이지에서 Install을 누르면 돼요. 업데이트도 앱이 알아서 챙겨줘요.</p></div>
<div class="box"><h3>zip 받아서 직접 넣기</h3>
<p class="muted">zip을 풀어 나온 폴더를 <code>_forever_\\Interface\\AddOns</code>에 넣고 게임을 완전히 껐다 켜세요.</p></div>
</div></section>

<section style="display:flex;flex-direction:column;gap:16px" aria-labelledby="list">
<h2 id="list">애드온 목록</h2>
<div class="cards">
{chr(10).join(cards)}
</div></section>"""
    return page("와우 포에버 애드온 · hyveo", "레벨페이스, 센터바, hyveo 애드온 센터 — 와우 포에버 애드온 모음", body, 1)


def detail(a):
    icon = f"../img/{a['slug'].replace('-','')}-icon.png"
    shots = "\n".join(
        f'<figure><img src="../img/{f}" alt="{e(c)}" loading="lazy"><figcaption>{e(c)}</figcaption></figure>' for f, c in a["shots"]
    )
    feats = "\n".join(f'<div class="box"><h3 style="font-size:16px">{e(t)}</h3><p class="muted">{e(d)}</p></div>' for t, d in a["features"])
    cmds = "\n".join(f'<div><span class="mono" style="color:#3FB950">{e(c)}</span> <span>{e(d)}</span></div>' for c, d in a["commands"])
    body = f"""<p style="margin:0"><a href="../" style="color:#9198A1;text-decoration:none;font-size:14px">← 애드온 목록</a></p>
<section class="hero">
<img src="{icon}" alt="{e(a['name'])} 아이콘" width="140" height="140">
<div class="txt">
<div style="display:flex;flex-wrap:wrap;gap:8px"><span class="badge ver mono">{a['version']}</span><span class="badge mono">WoW Forever</span><span class="badge dl mono" data-dl="{a['slug']}" hidden></span>{wait_badge(a)}</div>
<h1>{e(a['name'])} <span class="mono" style="font-size:22px;font-weight:400;color:#9198A1">{e(a['en'])}</span></h1>
<p class="lead">{e(a['lead'])} by @hyveo</p>
<div class="btns">{cf_button(a)}
<a class="btn" href="{zip_url(a)}">zip 다운로드</a>
<a class="btn link" href="{REPO}/tree/main/addons/{a['folder']}">GitHub에서 보기</a></div>
</div></section>

<section style="display:flex;flex-direction:column;gap:16px" aria-labelledby="shots">
<h2 id="shots">이렇게 보여요</h2>
<div class="grid" style="align-items:start">{shots}</div>
<p class="muted" style="font-size:12px">예시 화면이에요. 실제 게임 화면과 조금 다를 수 있어요.</p>
</section>

<section style="display:flex;flex-direction:column;gap:16px" aria-labelledby="feat">
<h2 id="feat">할 수 있는 것</h2>
<div class="grid">{feats}</div></section>

<section class="box" data-dl-versions="{a['slug']}" hidden aria-labelledby="vdl">
<h2 id="vdl">버전별 다운로드</h2>
<p class="muted vwhen"></p>
<div class="vbody"></div>
<p class="muted" style="font-size:12px">CurseForge 기준 누적 다운로드예요. zip 직접 다운로드는 포함되지 않아요.</p>
</section>

<section class="box" aria-labelledby="inst">
<h2 id="inst">zip으로 직접 설치하기</h2>
<ol>
<li>[zip 다운로드]로 <code>{a['folder']}-{a['version']}.zip</code>을 받아요.</li>
<li>압축을 풀면 나오는 <code>{a['folder']}</code> 폴더를 <code>World of Warcraft\\_forever_\\Interface\\AddOns\\</code>에 넣어요.</li>
<li>게임을 완전히 껐다 켜요. <span style="color:#9198A1">(/reload로는 새 애드온이 안 읽혀요)</span></li>
</ol>
<div class="cmds">{cmds}</div>
</section>

<section class="note"><p style="margin:0;color:#C9D1D9">오류가 나거나 원하는 기능이 있나요?</p>
<a class="btn" href="{ISSUES}">GitHub에 남기기</a></section>"""
    return page(f"{a['name']} ({a['en']}) · hyveo", a["summary"], body, 2)


def main():
    (OUT).mkdir(parents=True, exist_ok=True)
    (OUT / "index.html").write_text(index(), encoding="utf-8")
    for a in ADDONS:
        d = OUT / a["slug"]
        d.mkdir(exist_ok=True)
        (d / "index.html").write_text(detail(a), encoding="utf-8")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
