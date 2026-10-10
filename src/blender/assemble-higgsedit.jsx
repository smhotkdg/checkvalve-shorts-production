// Native Higgsedit assembly. Inputs are rendered Blender footage, a completed
// Higgsfield intro, and the exact continuous Typecast Piljae narration.
import path from 'node:path';

export default async ({ project }) => {
  const root = path.resolve(process.env.HYBRID_ASSET_DIR || '.');
  const p = await project({dir: path.join(root,'edit'), size:'1080x1920',fps:24,background:'#081626'});
  const hook = await p.add(path.join(root,'hook.mp4'));
  const body = await p.add(path.join(root,'blender-body.mp4'));
  const voice = await p.add(path.join(root,'piljae.wav'));
  const font = await p.add(path.join(root,'NotoSansCJKkr-Bold.otf'));
  // Composed video is picture-only, so generated source audio is never mixed.
  p.compose(<media x={0} y={0} file={hook} width={1080} height={1920} fit="contain" />, {at:0,dur:8,name:'Introduction'});
  p.compose(<media x={0} y={0} file={body} width={1080} height={1920} fit="contain" />, {at:8,dur:42,name:'Blender mechanism'});
  p.cut(voice,{from:0,dur:44.6,at:0});
  const phases = [
    [0,8,'펌프가 멈추면\n물이 되돌아온다?','역류를 막는 작은 장치'],
    [8,15.65,'체크밸브의 내부','밸브 시트, 마개, 스프링'],
    [15.65,27.65,'압력 차가 충분하면','마개가 움직이고, 스프링은 압축'],
    [27.65,36.63,'압력이 줄면 닫힌다','스프링과 역압이 닫힘을 돕습니다'],
    [36.63,40.51,'열리기 시작하는 조건','최소 개방 압력 차'],
    [40.51,50,'압력으로 열고\n스프링으로 닫고','물의 흐름 방향을 제어합니다']
  ];
  for (const [start,end,title,detail] of phases) {
    p.compose(<frame width={1080} height={1920} layout="none">
      <text x={95} y={195} width={890} height={220} typography={{fontAssetId:font.id,script:'Hang',language:'ko',direction:'ltr'}} fontSize={76} color="#F1F4ED" align="center" lineHeight={1.25}>{title}</text>
      <text x={95} y={465} width={890} height={80} typography={{fontAssetId:font.id,script:'Hang',language:'ko',direction:'ltr'}} fontSize={36} color="#FFD469" align="center">{detail}</text>
      <text x={120} y={1370} width={840} height={70} typography={{fontAssetId:font.id,script:'Hang',language:'ko',direction:'ltr'}} fontSize={27} color="#8EA6B8" align="center">스프링식 구조를 설명하는 개념도</text>
    </frame>, {at:start,dur:end-start,name:`Explanation ${start}`});
  }
  p.compose(<frame width={1080} height={1920} layout="none">
    <text x={365} y={760} width={110} height={65} typography={{fontAssetId:font.id,script:'Hang',language:'ko',direction:'ltr'}} fontSize={30} color="#B9C9D3" align="center">시트</text>
    <text x={385} y={1055} width={130} height={65} typography={{fontAssetId:font.id,script:'Hang',language:'ko',direction:'ltr'}} fontSize={30} color="#F1F4ED" align="center">마개</text>
    <text x={575} y={760} width={180} height={65} typography={{fontAssetId:font.id,script:'Hang',language:'ko',direction:'ltr'}} fontSize={30} color="#FFD469" align="center">스프링</text>
  </frame>,{at:8,dur:7.65,name:'Part labels'});
  await p.frame(20,path.join(root,'edit-open.png'));
  await p.frame(2,path.join(root,'edit-intro.png'));
  if (process.env.HYBRID_PREVIEW_ONLY !== '1') {
    await p.render(path.join(root,'clean-master.mp4'),{depth:8,bitrate:4000000,accel:'auto'});
  }
};
