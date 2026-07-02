"""
Lingexa One Word - Upload Script
"""
import os,sys,json
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()
ud=Path(__file__).parent/"upload"
if ud.exists() and str(ud) not in sys.path: sys.path.insert(0,str(ud))
CN="Lingexa One Word"
def gl():
    vd=Path("output/video")
    if not vd.exists(): return None
    rs=list(vd.glob("*/final_reel.mp4"))
    if not rs: return None
    lt=max(rs,key=lambda p:p.stat().st_mtime)
    mf=lt.parent/"metadata.json"; meta={}
    if mf.exists():
        with open(mf,"r",encoding="utf-8") as f: meta=json.load(f)
    ws=meta.get("words",[])
    return {"video_path":str(lt),"metadata":meta,"words":ws,"word":ws[0].get("word","Word") if ws else "Word"}
def gc(data,platform="facebook"):
    ws=data.get("words",[])
    if not ws: return f"Powerful words with {CN}! #LingexaOneWord"
    lines=[f"📖 One Word That Replaces a Whole Sentence! with {CN}", f""]
    for i,w in enumerate(ws,1):
        wd=w.get("word",""); ph=w.get("phrase",""); df=w.get("definition",""); ex=w.get("example","")
        lines.append(f"{i}. {wd.upper()}")
        lines.append(f"   Instead of: \"{ph}\"")
        lines.append(f"   Meaning: {df}")
        lines.append(f"   Example: {ex}")
        lines.append(f"")
    lines.extend([f"💡 Save this to grow your vocabulary!", f"🔔 Follow {CN}!", f"", f"#LingexaOneWord #Vocabulary #LearnEnglish #PowerWords #WordPower #ESL #SAT #GRE #EnglishVocabulary"])
    return "\n".join(lines)
def main():
    d=gl()
    if not d: print("No reel!"); sys.exit(1)
    print(gc(d,"facebook")[:500])
if __name__=="__main__": main()
