import json,math,subprocess,sys,wave
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np
R=Path(__file__).parent
DATA=json.loads((R/'narration.json').read_text(encoding='utf-8'))
W,H,FPS,DURATION=540,960,24,50
FONT=R/'fonts/NotoSansCJKkr-Bold.otf'
NAVY='#081626'; PANEL='#11263A'; GRID='#142B40'; WHITE='#F1F4ED'; MUTED='#8EA6B8'; CYAN='#4CE0D2'; GOLD='#FFD469'; CORAL='#F58A7B'
FONTS={s:ImageFont.truetype(str(FONT),s) for s in [14,16,18,20,22,25,28,32,36,44,51]}
def text(d,xy,s,size=20,color=WHITE,anchor=None):
    d.text(xy,s,font=FONTS[size],fill=color,anchor=anchor)
def center(d,y,s,size=20,color=WHITE):
    text(d,(W/2,y),s,size,color,'mt')
def smooth(x):
    x=max(0,min(1,x)); return x*x*(3-2*x)
def lerp(a,b,t): return a+(b-a)*t
def arrow(d,x,y,dx,length=26,color=GOLD):
    x2=x+dx*length; d.line((x,y,x2,y),fill=color,width=5)
    d.polygon([(x2,y),(x2-dx*10,y-6),(x2-dx*10,y+6)],fill=color)
def path_point(points,u):
    lengths=[math.dist(points[i],points[i+1]) for i in range(len(points)-1)]
    total=sum(lengths); target=(u%1)*total
    for i,l in enumerate(lengths):
        if target<=l:
            a=target/l; return lerp(points[i][0],points[i+1][0],a),lerp(points[i][1],points[i+1][1],a)
        target-=l
    return points[-1]
def marker(key):
    return next(w['start'] for w in DATA['words'] if w['text'].startswith(key))
TIMES=[0,marker('스프링식'),marker('앞쪽'),marker('앞뒤'),marker('다만'),marker('전기')]
ENDS=TIMES[1:]+[DURATION]
TITLES=['펌프가 멈추면?','마개와 스프링','압력 차가 충분하면','압력 차가 줄어들면','열리기 시작하는 조건','압력으로 움직이는 장치']
BASE=Image.new('RGB',(W,H),NAVY)
bd=ImageDraw.Draw(BASE)
for x in range(0,W,30): bd.line((x,220,x,H),fill=GRID,width=1)
for y in range(220,H,30): bd.line((0,y,W,y),fill=GRID,width=1)
bd.rounded_rectangle((24,315,516,632),radius=28,fill=PANEL,outline='#243E52',width=2)
def frame(t):
    im=BASE.copy(); d=ImageDraw.Draw(im)
    stage=max(i for i,start in enumerate(TIMES) if t>=start)
    q=t-TIMES[stage]
    p=q/max(0.01,ENDS[stage]-TIMES[stage])
    text(d,(34,32),'생활 속 공학',16,CYAN)
    text(d,(505,32),'50초 원리 설명',14,MUTED,'rt')
    text(d,(34,73),'물은 보내고',51,WHITE)
    text(d,(34,133),'역류는 막는다',51,GOLD)
    d.line((34,206,506,206),fill='#294459',width=2)
    text(d,(35,228),f'{stage+1:02d} / 06',14,CYAN)
    text(d,(504,228),'스프링식 체크밸브',14,MUTED,'rt')
    center(d,263,TITLES[stage],28)
    opening=0.; forward=False; reverse=False
    if stage==0: reverse=True
    elif stage==1: pass
    elif stage==2: opening=smooth(q/2.2); forward=True
    elif stage==3: opening=1-smooth(q/2.0); reverse=q>2.2
    elif stage==4:
        opening=smooth((q-2.5)/1.8); forward=True
    elif stage==5:
        cycle=(q%5)/5
        opening=smooth(cycle/.25) if cycle<.5 else 1-smooth((cycle-.5)/.25)
        forward=cycle<.5; reverse=cycle>=.75
    closed=opening<.05
    pop=199+65*opening
    # Cutaway housing: a wide chamber allows flow AROUND the poppet and spring.
    d.rounded_rectangle((43,419,497,501),radius=9,fill='#172F43',outline='#AEBFC7',width=4)
    d.rounded_rectangle((125,365,431,555),radius=34,fill='#172F43',outline='#AEBFC7',width=5)
    # Restore pipe bore at both chamber connections.
    d.rectangle((47,426,130,494),fill='#172F43')
    d.rectangle((426,426,493,494),fill='#172F43')
    d.line((43,419,125,419),fill='#AEBFC7',width=4); d.line((43,501,125,501),fill='#AEBFC7',width=4)
    d.line((430,419,497,419),fill='#AEBFC7',width=4); d.line((430,501,497,501),fill='#AEBFC7',width=4)
    # Fixed annular seat: central opening y=435..485.
    d.rectangle((183,371,199,435),fill='#92A9B5')
    d.rectangle((183,485,199,549),fill='#92A9B5')
    d.line((199,435,199,485),fill=CORAL,width=2)
    # Flow path never crosses the poppet, stem or coil.
    if opening>.25 and forward:
        gapx=(199+pop)/2
        path=[(48,460),(166,460),(200,460),(gapx,404),(pop+27,402),(340,414),(408,410),(445,460),(493,460)]
        # Use particles in the upper bypass only.
        d.line(path,fill='#225860',width=3,joint='curve')
        for k in range(15):
            x,y=path_point(path,(t*.22+k/15)%1)
            d.ellipse((x-3,y-3,x+3,y+3),fill=CYAN)
        for x in (70,110,466): arrow(d,x,460,1,19,CYAN)
    elif forward:
        for k in range(7):
            x=48+((t*50+k*19)%133)
            d.ellipse((x-3,458,x+3,464),fill=CYAN)
        arrow(d,88,460,1,34,CYAN)
    elif reverse:
        path=[(491,460),(443,460),(410,401),(285,401),(pop+18,423)]
        for k in range(13):
            x,y=path_point(path,(t*.18+k/13)%1)
            d.ellipse((x-3,y-3,x+3,y+3),fill=CYAN)
        arrow(d,485,460,-1,29,CORAL)
    # Axial stem, moving poppet and spring, with invariant fixed retainer.
    d.line((pop+15,460,398,460),fill='#758D9F',width=5)
    start=pop+31; end=395
    pts=[]
    for n in range(181):
        z=n/180; pts.append((lerp(start,end,z),460+16*math.sin(z*math.pi*12)))
    d.line(pts,fill=GOLD,width=4)
    d.line((399,414,399,506),fill='#9FB2BF',width=7)
    d.rounded_rectangle((pop,415,pop+16,505),radius=7,fill=WHITE,outline='#BDCFD5',width=2)
    d.line((pop+7,424,pop+7,497),fill='#ACBEC8',width=2)
    # Identify solid parts outside the mechanism.
    text(d,(69,388),'입구',16,MUTED)
    text(d,(462,388),'출구',16,MUTED,'rt')
    badge='열림' if opening>.05 else '닫힘'
    color=CYAN if opening>.05 else CORAL
    d.rounded_rectangle((217,574,323,608),radius=17,fill=color)
    center(d,581,badge,18,NAVY)
    if stage==1:
        text(d,(145,338),'밸브 시트',14,MUTED)
        d.line((184,355,191,373),fill=MUTED,width=1)
        text(d,(188,530),'마개',14,WHITE)
        text(d,(308,530),'스프링',14,GOLD)
    else:
        text(d,(39,655),'앞쪽 압력',16,MUTED)
        text(d,(501,655),'뒤쪽 압력 + 스프링',16,MUTED,'rt')
        left=(.42+.44*opening) if forward else .20
        right=.42 if forward else .85
        d.rounded_rectangle((39,685,245,700),radius=7,fill='#203C50')
        d.rounded_rectangle((295,685,501,700),radius=7,fill='#203C50')
        d.rounded_rectangle((39,685,39+206*left,700),radius=7,fill=CYAN)
        d.rounded_rectangle((295,685,295+206*right,700),radius=7,fill=GOLD)
        center(d,677,'↔',20,MUTED)
    notes=[
        ('역류가 생길 수 있는 순간','작은 밸브가 돌아오는 길을 막습니다'),
        ('스프링이 마개를 시트 쪽으로','밀어서 통로를 닫습니다'),
        ('압력 차가 스프링 힘을 이기면','틈이 열리고 물이 지나갑니다'),
        ('스프링이 닫고, 역압도 닫힘을 돕습니다','물은 마개를 통과하지 않습니다'),
        ('최소 개방 압력 차','열리기 시작하는 조건이 필요합니다'),
        ('압력 차로 열고 · 스프링으로 닫고','물의 흐름 방향을 제어합니다')
    ]
    center(d,730,notes[stage][0],20,WHITE)
    center(d,763,notes[stage][1],14,MUTED)
    # Keep y=810..875 clear for speech captions.
    text(d,(35,898),'원리 이해를 위한 개념도',14,MUTED)
    text(d,(505,898),'CHECK VALVE',14,CYAN,'rt')
    d.rounded_rectangle((35,930,505,934),radius=2,fill='#274253')
    if t>0: d.rounded_rectangle((35,930,35+470*t/DURATION,934),radius=2,fill=CYAN)
    return im
def main():
    if '--preview' in sys.argv:
        for idx,t in enumerate([2,12,22,29,37,47]):
            frame(t).resize((810,1440),Image.Resampling.LANCZOS).save(R/f'preview{idx}.jpg',quality=83)
        print(json.dumps({'scene_starts':TIMES,'audio_seconds':DATA['duration']},ensure_ascii=False))
        return
    if DATA['duration']>48.5: raise RuntimeError('Narration exceeds safe window')
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','pipe:0','-i',str(R/'narration.wav'),'-vf','scale=1080:1920:flags=lanczos','-af','apad,loudnorm=I=-16:TP=-1.5:LRA=11','-t',str(DURATION),'-c:v','libx264','-preset','fast','-crf','19','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-ar','48000','-movflags','+faststart',str(R/'final_clean.mp4')]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    for n in range(int(DURATION*FPS)):
        proc.stdin.write(frame(n/FPS).tobytes())
        if n%240==0: print(f'RENDER_SECONDS={n/FPS:.0f}',flush=True)
    proc.stdin.close()
    if proc.wait()!=0: raise RuntimeError('Render failed')
    print('CLEAN_MASTER_READY',flush=True)
if __name__=='__main__': main()
