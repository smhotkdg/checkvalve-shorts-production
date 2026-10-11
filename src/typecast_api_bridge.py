"""Typecast API bridge. Secrets are read from the local environment only.
Default voice is Piljae (Korean). --voice-name selects another original voice by its English name (e.g. the English narrator)."""
import argparse,json,os,sys,urllib.request,urllib.error
from pathlib import Path
BASE="https://api.typecast.ai"
def api_key():
    key=os.environ.get("TYPECAST_API_KEY","").strip()
    if not key and sys.platform=="win32":
        import winreg
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER,"Environment") as reg:
                key=str(winreg.QueryValueEx(reg,"TYPECAST_API_KEY")[0]).strip()
        except OSError: pass
    if not key:
        raise RuntimeError("API_KEY_NOT_CONFIGURED")
    return key
class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,*args): return None
def request(path,key,payload=None):
    raw=None if payload is None else json.dumps(payload,ensure_ascii=False).encode("utf-8")
    req=urllib.request.Request(BASE+path,data=raw,headers={"X-API-KEY":key,"Content-Type":"application/json"})
    try:
        with urllib.request.build_opener(NoRedirect).open(req,timeout=120) as response:
            return response.read()
    except urllib.error.HTTPError as exc:
        raise RuntimeError("TYPECAST_HTTP_"+str(exc.code)) from None
    except urllib.error.URLError:
        raise RuntimeError("TYPECAST_NETWORK_ERROR; submission may be unknown; do not retry a generation automatically") from None
def resolve_piljae(voices):
    matches=[v for v in voices if isinstance(v.get("voice_name"),dict) and v["voice_name"].get("kor")=="필재" and v.get("voice_type")=="original"]
    if len(matches)!=1:
        raise RuntimeError("PILJAE_API_VOICE_NOT_UNAMBIGUOUS:"+str(len(matches)))
    voice=matches[0]
    supported={m["version"] for m in voice.get("models",[])}
    if "ssfm-v30" not in supported:
        raise RuntimeError("PILJAE_SSFM_V30_NOT_AVAILABLE:"+",".join(sorted(supported)))
    return voice
def resolve_by_name(voices,name):
    matches=[v for v in voices if isinstance(v.get("voice_name"),dict) and v["voice_name"].get("eng")==name and v.get("voice_type")=="original"]
    if len(matches)!=1:
        raise RuntimeError("VOICE_NOT_UNAMBIGUOUS:"+name+":"+str(len(matches)))
    voice=matches[0]
    supported={m["version"] for m in voice.get("models",[])}
    if "ssfm-v30" not in supported:
        raise RuntimeError("VOICE_SSFM_V30_NOT_AVAILABLE:"+name)
    return voice
def list_candidates(voices,gender,use_case):
    for v in voices:
        if v.get("voice_type")!="original" or (gender and v.get("gender")!=gender): continue
        if use_case and use_case not in v.get("use_cases",[]): continue
        if "ssfm-v30" not in {m["version"] for m in v.get("models",[])}: continue
        print(json.dumps({"voice_id":v["voice_id"],"name":v["voice_name"].get("eng"),"age":v.get("age"),"use_cases":v.get("use_cases"),"preview_url":v.get("preview_url")},ensure_ascii=False))
def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--generate",action="store_true")
    parser.add_argument("--script",type=Path)
    parser.add_argument("--out",type=Path,default=Path(__file__).parent/"piljae.wav")
    parser.add_argument("--voice-name",default="",help="English name of an original voice; default is Piljae")
    parser.add_argument("--language",default="",help="ISO 639-3 code sent to the API, e.g. eng; omitted = auto")
    parser.add_argument("--list",action="store_true",help="list original ssfm-v30 voices (filters: --gender, --use-case); no generation")
    parser.add_argument("--gender",default="")
    parser.add_argument("--use-case",default="")
    args=parser.parse_args()
    key=api_key()
    voices=json.loads(request("/v3/voices",key))
    if args.list:
        list_candidates(voices,args.gender,args.use_case); return
    voice=resolve_by_name(voices,args.voice_name) if args.voice_name else resolve_piljae(voices)
    status="authenticated_voice_verified" if args.voice_name else "authenticated_piljae_verified"
    print(json.dumps({"status":status,"voice_id":voice["voice_id"],"voice_name":voice["voice_name"],"models":voice["models"],"preview_url":voice.get("preview_url")},ensure_ascii=False))
    if not args.generate: return
    if args.script is None: raise RuntimeError("SCRIPT_REQUIRED")
    script=args.script.read_text(encoding="utf-8-sig").strip()
    if not script or len(script)>1500: raise RuntimeError("SCRIPT_OUTSIDE_50_SECOND_PROJECT_SCOPE")
    if args.out.exists(): raise RuntimeError("OUTPUT_EXISTS; choose a new output")
    payload={"model":"ssfm-v30","voice_id":voice["voice_id"],"text":script,"output":{"audio_format":"wav","audio_tempo":1.0}}
    if args.language: payload["language"]=args.language
    data=request("/v1/text-to-speech",key,payload)
    if not data.startswith(b"RIFF") or data[8:12]!=b"WAVE":
        raise RuntimeError("INVALID_WAV_RESPONSE")
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_bytes(data)
    print(json.dumps({"status":"audio_saved","characters":len(script),"bytes":len(data),"output":str(args.out.resolve())}))
if __name__=="__main__":
    try: main()
    except RuntimeError as error:
        print(str(error),file=sys.stderr); sys.exit(2)
