import asyncio,json,wave,subprocess,os,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent/'deps'))
import edge_tts
ROOT=Path(__file__).parent
SENTENCES=[
  "펌프가 멈추면 물이 되돌아올 수 있습니다.",
  "역류를 막는 장치가 체크밸브입니다.",
  "스프링식 구조 안에는 마개와 스프링이 있죠.",
  "스프링이 마개를 밀어 통로를 닫고 있습니다.",
  "앞쪽 압력이 충분하면, 마개가 밀려나고 스프링이 압축됩니다.",
  "열린 틈으로 물이 지나갑니다.",
  "앞뒤 압력 차가 줄면, 스프링이 마개를 되밀어 닫습니다.",
  "반대쪽 압력도 마개를 눌러 역류를 막죠.",
  "다만 열리기 시작하는 최소 압력 차가 필요합니다.",
  "전기 없이, 압력과 스프링으로 물의 방향을 제어하는 겁니다."
]
async def main():
    text=" ".join(SENTENCES)
    comm=edge_tts.Communicate(text,"ko-KR-InJoonNeural",rate="+0%",boundary="WordBoundary")
    words=[]
    with (ROOT/'narration.mp3').open('wb') as f:
        async for c in comm.stream():
            if c['type']=='audio': f.write(c['data'])
            elif c['type']=='WordBoundary':
                words.append({'text':c['text'],'start':c['offset']/1e7,'end':(c['offset']+c['duration'])/1e7})
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(ROOT/'narration.mp3'),'-ac','1','-ar','24000',str(ROOT/'narration.wav')],check=True)
    with wave.open(str(ROOT/'narration.wav')) as f: duration=f.getnframes()/f.getframerate()
    data={'voice':'ko-KR-InJoonNeural','duration':duration,'sentences':SENTENCES,'text':text,'words':words}
    (ROOT/'narration.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    (ROOT/'script.json').write_text(json.dumps({'beats':[{'phrase':s} for s in SENTENCES]},ensure_ascii=False),encoding='utf-8')
    print(json.dumps({'duration':duration,'words':len(words),'first':words[:4],'last':words[-4:]},ensure_ascii=False))
asyncio.run(main())
