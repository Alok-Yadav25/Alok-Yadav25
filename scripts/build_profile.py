#!/usr/bin/env python3
"""Build self-contained profile SVGs. Only contribution refresh needs GitHub access."""
import argparse
import datetime as dt
import html
import json
import math
import os
from pathlib import Path
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets' / 'profile'
BG, BORDER, INK, MUTED, MINT = '#0c1110', '#28392f', '#edf5ef', '#a3b7aa', '#a8f0c2'
QUERY = '''query($login:String!) { user(login:$login) { contributionsCollection {
 contributionCalendar { totalContributions weeks { contributionDays { date contributionCount contributionLevel } } }
} } }'''


def esc(value):
    return html.escape(str(value), quote=True)


def text(x, y, value, size=16, color=INK, weight=400, extra=''):
    return f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" font-weight="{weight}" {extra}>{esc(value)}</text>'


def mono(x, y, value, size=12, color=MUTED, extra=''):
    return text(x, y, value, size, color, extra=f'style="font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" {extra}')


def svg(name, width, height, body, title, desc=''):
    ASSETS.mkdir(parents=True, exist_ok=True)
    content = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">{esc(title)}</title><desc id="desc">{esc(desc or title)}</desc>
<defs>
<radialGradient id="glow"><stop stop-color="#477f5c" stop-opacity=".25"/><stop offset="1" stop-color="#0c1110" stop-opacity="0"/></radialGradient>
</defs>
<style>
 text {{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Arial,sans-serif;}}
 .pulse {{animation:pulse 4s ease-in-out infinite;}}
 .rise {{animation:rise 1.8s cubic-bezier(.2,.7,.3,1) both;}}
 .drift {{animation:drift 7s ease-in-out infinite;}}
 .trace {{stroke-dasharray:90 600;animation:trace 7s linear infinite;}}
 @keyframes pulse {{0%,100%{{opacity:.35}}50%{{opacity:1}}}}
 @keyframes rise {{from{{opacity:.7;transform:translateY(14px)}}to{{opacity:1;transform:translateY(0)}}}}
 @keyframes drift {{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-9px)}}}}
 @keyframes trace {{to{{stroke-dashoffset:-690}}}}
 @media(prefers-reduced-motion:reduce){{.pulse,.rise,.drift,.trace{{animation:none;}}}}
</style>
<rect x=".5" y=".5" width="{width-1}" height="{height-1}" rx="22" fill="{BG}" stroke="{BORDER}"/>
{body}
</svg>'''
    (ASSETS / name).write_text(content+'\n')


def cube(x,y,size,height,top,left,right):
    a=[(x,y-height),(x+size,y+size*.5-height),(x,y+size-height),(x-size,y+size*.5-height)]
    l=[a[3],a[2],(x,y+size),(x-size,y+size*.5)]
    r=[a[2],a[1],(x+size,y+size*.5),(x,y+size)]
    points=lambda ps:' '.join(f'{u:.2f},{v:.2f}' for u,v in ps)
    return (f'<polygon points="{points(l)}" fill="{left}"/>'
            f'<polygon points="{points(r)}" fill="{right}"/>'
            f'<polygon points="{points(a)}" fill="{top}" stroke="{BG}" stroke-opacity=".28" stroke-width=".6"/>')


def hero():
    b='<ellipse cx="950" cy="210" rx="300" ry="200" fill="url(#glow)"/>'
    b+='<rect x="36" y="32" width="40" height="40" rx="12" fill="#a8f0c2"/>'
    b+=text(45,59,'AY',18,BG,750)+mono(91,57,'ALOK-YADAV25 / ENGINEERING & DESIGN',12)
    b+='<circle cx="935" cy="51" r="4" fill="#a8f0c2" class="pulse"/>'
    b+=mono(949,55,'OPEN TO OPPORTUNITIES',11,MINT)
    b+=text(42,166,'Alok Yadav',88,INK,650,'letter-spacing="-5"')
    b+=text(45,217,'Intelligence, engineered.',35,MINT,450,'letter-spacing="-1"')
    b+=text(46,264,'AI / ML systems. Thoughtful interfaces.',20,MUTED)
    b+=text(46,295,'Built from the first model to the final interaction.',20,MUTED)
    b+='<g class="drift">'
    for c,r,h in [(0,0,30),(1,0,60),(2,0,26),(0,1,57),(1,1,112),(2,1,56),(0,2,23),(1,2,58),(2,2,28)]:
        b+=cube(934+(c-r)*48,194+(c+r)*25,46,h,'#b8f4ce' if h>80 else '#78b98f','#2a6342','#40835a')
    b+='</g><path d="M792 312 L934 384 L1076 312" fill="none" stroke="#38533f"/>'
    b+=mono(886,370,'BUILD / REFINE',10)
    b+=f'<path d="M44 337 H702" stroke="{BORDER}"/>'
    b+=mono(46,377,'01  APPLIED AI',12,MINT)+mono(248,377,'02  FULL-STACK',12)+mono(455,377,'03  PRODUCT CRAFT',12)
    svg('hero.svg',1200,420,b,'Alok Yadav — Intelligence, engineered.','AI and machine learning systems, full-stack products, and thoughtful interfaces. Open to opportunities.')
    b=mono(28,40,'ALOK-YADAV25 / ENGINEERING & DESIGN',12,MINT)
    b+=text(25,135,'Alok Yadav',76,INK,650,'letter-spacing="-4"')
    b+=text(29,183,'Intelligence, engineered.',32,MINT,450,'letter-spacing="-1"')
    b+=text(30,236,'AI / ML systems.',23,MUTED)
    b+=text(30,270,'Thoughtful interfaces.',23,MUTED)
    b+=mono(30,337,'OPEN TO OPPORTUNITIES',13,MINT)
    b+='<g class="drift">'
    for c,r,h in [(0,0,16),(1,0,33),(2,0,14),(0,1,32),(1,1,62),(2,1,31),(0,2,13),(1,2,32),(2,2,16)]:
        b+=cube(460+(c-r)*25,256+(c+r)*13,24,h,'#b8f4ce' if h>50 else '#78b98f','#2a6342','#40835a')
    b+='</g>'
    svg('hero-mobile.svg',600,375,b,'Alok Yadav — Intelligence, engineered.','AI and ML systems. Thoughtful interfaces. Open to opportunities.')


PROJECTS=[
 ('pulse','01','OBSERVABILITY','Pulse',['Every signal. One clear view.','Website health, performance & visitor analytics.'],'REACT / TYPESCRIPT / FASTAPI','#c7b8ff'),
 ('devpilot','02','AGENTIC AI','DevPilot',['From a reproducible bug to a reviewed patch.','AI-assisted Python debugging with test evidence.'],'PYTHON / LANGGRAPH / GROQ',MINT),
 ('veil','03','PRIVACY ENGINEERING','VEIL',['Privacy, embedded in pixels.','Encrypted payloads inside ordinary images.'],'JAVA / SPRING BOOT / REACT','#cfbbf7'),
 ('codelens','04','DEVELOPER TOOLS','CodeLens',['A second perspective on your code.','Model-assisted reviews & contextual suggestions.'],'PYTORCH / CODEBERT / FASTAPI','#95cfdf'),
]


def project_cards():
    for slug,number,label,title,lines,stack,accent in PROJECTS:
        b=mono(30,39,number+' / '+label,11,accent)+text(542,42,'↗',25,accent)
        b+=text(29,104,title,48,INK,600,'letter-spacing="-2"')
        for i,line in enumerate(lines): b+=text(31,144+i*26,line,17,MUTED)
        b+='<rect x="30" y="199" width="530" height="67" rx="12" fill="#142019"/>'
        if slug=='pulse':
            path='M48 234 H100 L112 224 L125 245 L142 211 L158 253 L174 233 H219 L233 225 L248 241 L265 219 L281 234 H342 L357 228 L371 240 L389 216 L405 247 L423 234 H542'
            b+=f'<path d="{path}" fill="none" stroke="{accent}" stroke-width="2" opacity=".25"/>'
            b+=f'<path class="trace" d="{path}" fill="none" stroke="{accent}" stroke-width="2.5"/>'
        elif slug=='devpilot':
            b+='<path d="M90 221 H490" stroke="#3c5f49"/>'
            for i,s in enumerate(['REPRODUCE','INVESTIGATE','TEST','REVIEW']):
                x=90+i*132
                b+=f'<circle cx="{x}" cy="221" r="5" fill="{accent}" class="pulse" style="animation-delay:{i*.7}s"/>'
                b+=mono(x,249,s,9,MUTED,'text-anchor="middle"')
        elif slug=='veil':
            for i in range(26):
                for j in range(3):
                    opacity=.18+((i*7+j*11)%9)/13
                    b+=f'<rect x="{49+i*19}" y="{211+j*15}" width="10" height="10" rx="2" fill="{accent}" opacity="{opacity:.2f}"/>'
            b+=f'<path d="M299 206 V258" stroke="{accent}" stroke-width="2" class="pulse"/>'
        else:
            b+=mono(52,225,'def review(code):',13,accent)+mono(68,248,'return model.analyze(code)',13,MUTED)
            b+=f'<path d="M401 233 l10 10 20-23" stroke="{accent}" stroke-width="3" fill="none" class="pulse"/>'
            b+=mono(450,239,'INSPECT',11,accent)
        b+=mono(31,301,stack,11,MUTED)
        svg(slug+'.svg',590,326,b,title+' — '+lines[0],' '.join(lines)+' Stack: '+stack)


def toolkit():
    b=mono(35,39,'THE TOOLKIT / FROM IDEA TO INTERFACE',12,MINT)
    groups=[(35,'INTELLIGENCE',['Python · PyTorch · scikit-learn','LLMs · RAG · Computer vision']),
            (435,'PRODUCT',['React · Next.js · TypeScript','Tailwind CSS · Motion']),
            (835,'SYSTEMS',['FastAPI · Spring Boot','PostgreSQL · Docker · Git'])]
    for x,label,lines in groups:
        b+=mono(x,87,label,11)
        for i,line in enumerate(lines): b+=text(x,119+i*27,line,18,INK)
    b+=f'<path d="M401 72 V153 M801 72 V153" stroke="{BORDER}"/>'
    svg('toolkit.svg',1200,180,b,'The toolkit',' | '.join(g+': '+', '.join(lines) for _,g,lines in groups))
    b=mono(28,36,'THE TOOLKIT',13,MINT)
    for i,(_,label,lines) in enumerate(groups):
        y=83+i*107
        b+=mono(28,y,label,12)
        for j,line in enumerate(lines): b+=text(28,y+29+j*27,line,21,INK)
    svg('toolkit-mobile.svg',600,380,b,'The toolkit',' | '.join(g+': '+', '.join(lines) for _,g,lines in groups))


def fetch_calendar(username):
    token=os.environ.get('GH_TOKEN') or os.environ.get('GITHUB_TOKEN')
    if not token: raise SystemExit('Set GH_TOKEN or GITHUB_TOKEN to refresh contribution data.')
    req=urllib.request.Request('https://api.github.com/graphql',
        data=json.dumps({'query':QUERY,'variables':{'login':username}}).encode(),
        headers={'Authorization':f'Bearer {token}','Content-Type':'application/json','User-Agent':'profile-skyline'})
    with urllib.request.urlopen(req,timeout=30) as response: data=json.load(response)
    if data.get('errors'): raise RuntimeError('GitHub GraphQL: '+json.dumps(data['errors']))
    return data['data']['user']['contributionsCollection']['contributionCalendar']


def contribution_skyline(calendar):
    days=[d for w in calendar['weeks'] for d in w['contributionDays']]
    if not days or any(d['contributionCount']<0 for d in days): raise ValueError('Expected dated, nonnegative contribution data')
    ordered=sorted(days,key=lambda d:d['date'])
    counts=[d['contributionCount'] for d in ordered]
    active=sum(n>0 for n in counts)
    peak=max(counts)
    longest=run=0
    for count in counts:
        run=run+1 if count else 0
        longest=max(run,longest)
    end=ordered[-1]['date']
    b=mono(36,42,'THE CONTRIBUTION LANDSCAPE',12,MINT)
    b+=mono(1162,42,'PAST 12 MONTHS',11,MUTED,'text-anchor="end"')
    for x,value,label in [(36,calendar['totalContributions'],'CONTRIBUTIONS'),(334,active,'ACTIVE DAYS'),(632,peak,'BEST DAY'),(930,longest,'LONGEST STREAK / DAYS')]:
        b+=text(x,109,f'{value:,}',44,INK,550,'letter-spacing="-2"')+mono(x,136,label,10)
    b+='<ellipse cx="617" cy="340" rx="530" ry="95" fill="url(#glow)"/>'
    palette={'NONE':('#1c2b22','#132019','#18271e'),'FIRST_QUARTILE':('#467a57','#284832','#345e40'),
             'SECOND_QUARTILE':('#6aaf7f','#326044','#47815a'),'THIRD_QUARTILE':('#97dbad','#47835b','#65a478'),
             'FOURTH_QUARTILE':('#c1f7d2','#609b73','#85c598')}
    for c,week in enumerate(calendar['weeks']):
        for d in week['contributionDays']:
            date=dt.date.fromisoformat(d['date']); r=(date.weekday()+1)%7; count=d['contributionCount']
            height=2 if count==0 else 6+65*math.sqrt(count/max(peak,1))
            x,y=164+c*17-r*15,218+c*2.1+r*8.5
            block=cube(x,y,7.6,height,*palette[d['contributionLevel']])
            b+=f'<g class="rise" style="animation-delay:{c*.015:.3f}s"><title>{esc(d["date"])}: {count} contributions</title>{block}</g>'
    b+=mono(36,431,'REAL ACTIVITY. SMALL STEPS. COMPOUNDING PROGRESS.',11)
    b+=mono(36,468,f'UPDATED {end} / DAILY VIA GITHUB ACTIONS',10)
    b+=mono(916,467,'LESS',10)
    for i,color in enumerate(['#1c2b22','#467a57','#6aaf7f','#97dbad','#c1f7d2']):
        b+=f'<rect x="{958+i*26}" y="455" width="17" height="17" rx="3" fill="{color}"/>'
    b+=mono(1104,467,'MORE',10)
    svg('contributions.svg',1200,496,b,"Alok's 3D contribution landscape",
        f"{calendar['totalContributions']} contributions in the last year, {active} active days, best day {peak}, longest streak {longest} days. Updated {end}. Block heights reflect real daily contributions.")


def footer():
    b=mono(36,42,'HAVE SOMETHING INTERESTING IN MIND?',12,MINT)
    b+=text(34,108,"Let's build what comes next.",45,INK,500,'letter-spacing="-1.5"')
    b+=text(37,154,'AI / ML opportunities · Thoughtful products · Technical collaborations',18,MUTED)
    b+=text(1107,113,'↗',48,MINT)
    svg('connect.svg',1200,190,b,"Let's build what comes next.",'Open to AI and ML opportunities, product work, and technical collaborations. Email ay252003@gmail.com.')


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--calendar-json',type=Path,help='Local GraphQL response or calendar object')
    p.add_argument('--username',default='Alok-Yadav25')
    p.add_argument('--static-only',action='store_true')
    args=p.parse_args()
    hero(); project_cards(); toolkit(); footer()
    if not args.static_only:
        if args.calendar_json:
            calendar=json.loads(args.calendar_json.read_text())
            if 'data' in calendar: calendar=calendar['data']['user']['contributionsCollection']['contributionCalendar']
        else: calendar=fetch_calendar(args.username)
        contribution_skyline(calendar)
    print('Built profile assets in',ASSETS)


if __name__=='__main__': main()
