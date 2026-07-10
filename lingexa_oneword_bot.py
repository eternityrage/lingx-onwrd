"""
Lingexa One Word - Powerful Vocabulary
One word can replace a whole sentence
"""

import os,sys,json,random,asyncio,subprocess
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
if sys.platform=="win32": sys.stdout.reconfigure(encoding="utf-8")
load_dotenv()
P=os.getenv("POLLINATIONS_API_KEY"); M=os.getenv("AI_MODEL")
if not M: raise ValueError("AI_MODEL not set!")
B=Path(__file__).parent; O=B/"output"; V=O/"video"; H=O/"history"
for d in[O,V,H]: d.mkdir(exist_ok=True)
W=1080; H2=1920; F=30; TV="en-US-GuyNeural"; CN="Lingexa One Word"; WPV=3; HF=H/"all_words.json"; FD=B/"fonts"

def lh():
    if HF.exists(): return json.load(open(HF,"r",encoding="utf-8"))
    return {"words":[],"last_updated":None}
def sh(d):
    d["last_updated"]=datetime.now().isoformat(); json.dump(d,open(HF,"w",encoding="utf-8"),indent=2,ensure_ascii=False)
def iu(w):
    h=lh(); return w.lower().strip() in[x.lower().strip() for x in h.get("words",[])]
def ah(ws):
    h=lh(); e=[x.lower().strip() for x in h.get("words",[])]
    for w in ws:
        if w.lower().strip() not in e: h["words"].append(w.lower().strip()); e.append(w.lower().strip())
    sh(h)

def gd(n=WPV):
    ca=20; cats=[
        "people and roles",
        "actions and behaviors",
        "emotions and states",
        "character traits",
        "intellectual and academic concepts",
        "descriptive and sensory words",
        "negative qualities and flaws",
        "positive qualities and virtues",
        "nature and environment",
        "technology and innovation",
        "food and cooking",
        "travel and adventure",
        "art and creativity",
        "science and discovery",
        "business and finance",
        "health and wellness",
        "music and sound",
        "sports and competition",
        "relationships and communication",
        "philosophy and wisdom",
        "weather and seasons",
        "animals and nature",
        "architecture and design",
        "fashion and style",
    ]
    c=[]
    for a in range(ca):
        try:
            import requests
            u="https://gen.pollinations.ai/v1/chat/completions"
            hd={"Authorization":f"Bearer {P}","Content-Type":"application/json"}
            cat=cats[a%len(cats)]; r=n-len(c); print(f"[api] Attempt {a+1}: {cat[:50]}... (need {r} more)")
            h=lh(); ua=set(h.get("words",[])[-50:]); ua.update([x["word"].lower() for x in c]); us=", ".join(list(ua)[-30:]) if ua else "(none)"
            p=f"""Generate 15 powerful single-word vocabulary words from: {cat}

NEVER repeat: {us}
Each word should replace a LONG PHRASE. The word should be POWERFUL and USEFUL.

Return ONLY JSON array.

Format per item:
[{{"word":"bibliophile","phrase":"a person who loves books","definition":"a person who collects or loves books","example":"She is a true bibliophile with thousands of books.","tip":"Biblio = book, phile = lover. Think 'library' + 'philosophy'."}}]

REQUIREMENTS:
- 'word': one powerful word
- 'phrase': the longer phrase it replaces (max 8 words)
- 'definition': simple definition (max 10 words)
- 'example': example sentence (max 10 words)
- 'tip': memory trick in ONE short sentence
Return ONLY the JSON array.""" 
            payload={"model":M,"messages":[{"role":"system","content":"Return ONLY valid JSON arrays."},{"role":"user","content":p}],"temperature":1.3}
            resp=requests.post(u,headers=hd,json=payload,timeout=60); resp.raise_for_status()
            ct=resp.json()["choices"][0]["message"]["content"].strip()
            if "```json" in ct: ct=ct.split("```json")[1].split("```")[0].strip()
            elif "```" in ct: ct=ct.split("```")[1].split("```")[0].strip()
            it=json.loads(ct)
            if not isinstance(it,list): raise ValueError("Not a list")
            fr=[]
            for itm in it:
                w=itm.get("word","").strip()
                if not w: continue
                if len(w.split())>1: continue
                if w.lower() in ua: continue
                fr.append(itm); ua.add(w.lower())
                if len(c)+len(fr)>=n: break
            c.extend(fr)
            if len(c)>=n: ah([m["word"] for m in c[:n]]); return c[:n]
        except Exception as e: print(f"[api] Attempt {a+1} FAILED: {e}")
    if c: ah([m["word"] for m in c]); return c
    raise RuntimeError("API failed")

def bg():
    from PIL import Image,ImageDraw
    img=Image.new('RGB',(W,H2)); d=ImageDraw.Draw(img)
    for y in range(H2):
        r=y/H2
        if r<0.5: rgb=(252,250,248)
        else: rgb=(int(252+(248-252)*(r-0.5)*2),int(250+(246-250)*(r-0.5)*2),int(248+(244-248)*(r-0.5)*2))
        d.rectangle([(0,y),(W,y+1)],fill=rgb)
    return img

async def ga(t,v,p):
    try: import edge_tts; await edge_tts.Communicate(t,v).save(p); return True
    except: return False
async def gar(t,v,p,r=3):
    for a in range(1,r+1):
        ok=await ga(t,v,p)
        if ok and Path(p).exists() and Path(p).stat().st_size>100: return True
        await asyncio.sleep(2*a)
    return False
def gad(f):
    if not Path(f).exists(): return 2.0
    r=subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","default=noprint_wrappers=1:nokey=1",f],capture_output=True,text=True)
    try: return float(r.stdout.strip())
    except: return 2.0

def ga2(items,od):
    od=Path(od); od.mkdir(parents=True,exist_ok=True)
    af=[]; tot=0.0
    for i,it in enumerate(items):
        w=it["word"]; p=it.get("phrase",""); d=it.get("definition",""); e=it.get("example",""); t=it.get("tip","")
        tx=f"Stop saying: {p}. Instead say: {w}. {w} means {d}. For example: {e}. Tip: {t}"
        fp=od/f"w_{i}.mp3"
        ok=asyncio.run(gar(tx,TV,str(fp)))
        if not ok: subprocess.run(["ffmpeg","-y","-f","lavfi","-i","anullsrc=r=24000:cl=mono","-t","5",str(fp)],capture_output=True)
        du=gad(str(fp)); af.append({"file":str(fp),"duration":du}); tot+=du+0.3
    print(f"[audio] {len(af)} words, {tot:.1f}s")
    return af,tot

def cfa(af,of):
    od=Path(of).parent; parts=[]
    for i,a in enumerate(af):
        p=od/f"pd_{i}.mp3"
        subprocess.run(["ffmpeg","-y","-i",str(a["file"]),"-af","apad=pad_dur=0.3","-ar","24000","-ac","1","-c:a","libmp3lame",str(p)],capture_output=True)
        parts.append(p)
    cl=od/"cl.txt"
    with open(cl,"w") as f:
        for p in parts: f.write(f"file '{str(p.resolve()).replace(chr(92),chr(47))}'\n")
    subprocess.run(["ffmpeg","-y","-f","concat","-safe","0","-i",str(cl),"-c:a","libmp3lame",str(of)],capture_output=True)
    for p in parts:
        if p.exists(): p.unlink()
    if cl.exists(): cl.unlink()
    return Path(of).exists() and Path(of).stat().st_size>100

def wt(d,text,font,mw):
    w=text.split(); l=[]; c=[]
    for wd in w:
        t=' '.join(c+[wd])
        if d.textbbox((0,0),t,font=font)[2]<=mw or not c: c.append(wd)
        else: l.append(' '.join(c)); c=[wd]
    if c: l.append(' '.join(c))
    return l

def gi(it,bg,op):
    from PIL import Image,ImageDraw,ImageFont
    img=bg.copy().convert('RGBA'); d=ImageDraw.Draw(img)
    MX=90; CX=W//2; CW=W-MX*2
    FB=["/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf","/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf","C:/Windows/Fonts/arialbd.ttf","C:/Windows/Fonts/segoeuib.ttf"]
    FR=["/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf","/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf","C:/Windows/Fonts/arial.ttf","C:/Windows/Fonts/segoeui.ttf"]
    def lf(p,sz):
        for pp in p:
            try: f=ImageFont.truetype(pp,sz); return f
            except: continue
        return ImageFont.load_default()
    fh=lf(FB,65); fw=lf(FB,130); fb=lf(FB,36); fp=lf(FB,55)
    fdl=lf(FB,42); fd=lf(FR,60); fel=lf(FB,42); fe=lf(FR,50)
    ftl=lf(FB,40); ft=lf(FR,44); ff=lf(FB,42)

    w=it["word"].upper(); ph=it.get("phrase",""); df=it.get("definition",""); ex=it.get("example",""); tp=it.get("tip","")
    H=(45,35,65); W2=(25,20,45); L=(80,65,105); DB=(65,50,95); EB=(95,80,125); F2=(45,35,65)

    d.rectangle([(0,0),(W,90)],fill=H)
    d.text((CX,45),CN.upper(),fill=(255,255,255),font=fh,anchor="mm")

    y=260
    mww=CW; wfs=130; wf=lf(FB,wfs); ww=d.textbbox((0,0),w,font=wf)[2]
    while ww>mww and wfs>40: wfs-=5; wf=lf(FB,wfs); ww=d.textbbox((0,0),w,font=wf)[2]
    wh=d.textbbox((0,0),"Ay",font=wf)[3]-d.textbbox((0,0),"Ay",font=wf)[1]
    d.text((CX,y+wh//2),w,fill=W2,font=wf,anchor="mm",stroke_width=max(1,wfs//40),stroke_fill=(220,215,220))
    y+=wh+50

    if ph:
        pt=ph.upper(); pfs=36; pf=lf(FB,pfs); pw=d.textbbox((0,0),pt,font=pf)[2]
        while pw>CW-40 and pfs>20: pfs-=2; pf=lf(FB,pfs); pw=d.textbbox((0,0),pt,font=pf)[2]
        pb=d.textbbox((0,0),pt,font=pf); pw=pb[2]-pb[0]; ph2=pb[3]-pb[1]
        d.rounded_rectangle([(CX-pw//2-12,y),(CX+pw//2+12,y+ph2+18)],radius=10,fill=(90,70,130))
        d.text((CX,y+ph2//2+9),pt,fill=(255,255,255),font=pf,anchor="mm")
        y+=ph2+60

    pt2="VOCABULARY"
    pb2=d.textbbox((0,0),pt2,font=fp); pw2=pb2[2]-pb2[0]; ph3=pb2[3]-pb2[1]
    d.rounded_rectangle([(CX-pw2//2-22,y),(CX+pw2//2+22,y+ph3+22)],radius=12,fill=(75,55,115))
    d.text((CX,y+ph3//2+11),pt2,fill=(255,245,140),font=fp,anchor="mm")
    y+=ph3+70

    d.text((MX,y),"MEANING",fill=L,font=fdl,anchor="lm"); y+=60
    dl=wt(d,df,fd,CW-70)
    while len(dl)>2 and fd.size>36: fd=lf(FR,fd.size-4); dl=wt(d,df,fd,CW-70)
    lh=d.textbbox((0,0),"A",font=fd)[3]-d.textbbox((0,0),"A",font=fd)[1]
    ls=int(lh*1.5); th=(len(dl)-1)*ls+lh; pd=45; bh=th+pd*2
    box=Image.new('RGBA',(CW,bh),DB+(255,)); bd=ImageDraw.Draw(box)
    bd.rounded_rectangle([(0,0),(CW,bh)],radius=18,fill=DB+(255,))
    for i,line in enumerate(dl): bd.text((CW//2,pd+(i*ls)+lh//2),line,fill=(255,255,255),font=fd,anchor="mm")
    img.paste(box,(MX,y),box); y+=bh+65

    d.text((MX,y),"EXAMPLE",fill=L,font=fel,anchor="lm"); y+=60
    el=wt(d,ex,fe,CW-70)
    while len(el)>2 and fe.size>30: fe=lf(FR,fe.size-4); el=wt(d,ex,fe,CW-70)
    elh=d.textbbox((0,0),"A",font=fe)[3]-d.textbbox((0,0),"A",font=fe)[1]
    els=int(elh*1.5); eth=(len(el)-1)*els+elh; epd=40; ebh=eth+epd*2
    ebox=Image.new('RGBA',(CW,ebh),EB+(220,)); ed=ImageDraw.Draw(ebox)
    ed.rounded_rectangle([(0,0),(CW,ebh)],radius=15,fill=EB+(220,))
    for i,line in enumerate(el): ed.text((CW//2,epd+(i*els)+elh//2),line,fill=(255,255,255),font=fe,anchor="mm")
    img.paste(ebox,(MX,y),ebox); y+=ebh+65

    if tp and y<H2-180:
        d.text((MX,y),"TIP",fill=(110,75,55),font=ftl,anchor="lm"); y+=55
        tl=wt(d,tp,ft,CW-70)
        while len(tl)>2 and ft.size>28: ft=lf(FR,ft.size-4); tl=wt(d,tp,ft,CW-70)
        tlh=d.textbbox((0,0),"A",font=ft)[3]-d.textbbox((0,0),"A",font=ft)[1]
        tls=int(tlh*1.5); tth=(len(tl)-1)*tls+tlh; tpd=35; tbh=tth+tpd*2
        tbox=Image.new('RGBA',(CW,tbh),(255,210,160,200)); td=ImageDraw.Draw(tbox)
        td.rounded_rectangle([(0,0),(CW,tbh)],radius=14,fill=(255,210,160,200))
        for i,line in enumerate(tl): td.text((CW//2,tpd+(i*tls)+tlh//2),line,fill=(70,45,25),font=ft,anchor="mm")
        img.paste(tbox,(MX,y),tbox)

    d.rectangle([(0,H2-65),(W,H2)],fill=F2)
    d.text((CX,H2-32),f"Power words daily  |  {CN}",fill=(210,200,220),font=ff,anchor="mm")
    img=img.convert('RGB')
    Path(op).parent.mkdir(parents=True,exist_ok=True); img.save(op,quality=96,optimize=True)
    print(f"[image] {Path(op).name}")
    return op

def cv(imgs,afs,of):
    print(f"[video] {len(imgs)} images...")
    clips=[]
    for i,(ip,ai) in enumerate(zip(imgs,afs)):
        tc=Path(of).parent/f"c_{i}.mp4"; d=ai["duration"]
        subprocess.run(["ffmpeg","-y","-loop","1","-i",str(ip),"-i",str(ai["file"]),"-vf",f"scale={W}:{H2}:force_original_aspect_ratio=decrease,pad={W}:{H2}:(ow-iw)/2:(oh-ih)/2,fps={F}","-c:v","libx264","-preset","medium","-pix_fmt","yuv420p","-c:a","aac","-b:a","128k","-t",f"{d}","-shortest",str(tc)],capture_output=True)
        ad=gad(str(tc)); print(f"  Clip {i+1}: {ad:.1f}s"); clips.append(tc)
    if not clips: return False
    cf=Path(of).parent/"cl.txt"
    with open(cf,"w") as f:
        for c in clips: f.write(f"file '{str(c.resolve()).replace(chr(92),chr(47))}'\n")
    subprocess.run(["ffmpeg","-y","-f","concat","-safe","0","-i",str(cf),"-c","copy",str(of)],capture_output=True)
    for c in clips:
        if c.exists(): c.unlink()
    if cf.exists(): cf.unlink()
    print(f"[video] {Path(of).name}")
    return True

def gr():
    print(f"\n{'='*80}\n  {CN.upper()}\n{'='*80}\n")
    ts=datetime.now().strftime("%Y%m%d_%H%M%S"); rd=V/f"words_{ts}"; rd.mkdir()
    print("[1/3] Generating powerful words...")
    its=gd(WPV)
    for i,m in enumerate(its,1): print(f"  {i}. {m['word']}  ({m.get('phrase','')})")
    print("\n[2/3] Generating images...")
    b=bg(); imgs=[]
    for i,m in enumerate(its): ip=rd/f"w_{i}.jpg"; gi(m,b,str(ip)); imgs.append(str(ip))
    print("\n[3/3] Generating audio & video...")
    af,td=ga2(its,str(rd)); fa=rd/"narration.mp3"; cfa(af,str(fa))
    ov=rd/"final_reel.mp4"; cv(imgs,af,str(ov))
    meta={"channel":CN,"words":its,"timestamp":ts,"video":str(ov),"duration":td}
    with open(rd/"metadata.json","w") as f: json.dump(meta,f,indent=2)
    print(f"\n{'='*80}\n  COMPLETE! {td:.1f}s\n{'='*80}\n"); return meta

if __name__=="__main__":
    print(f"\n{'='*80}\n  {CN.upper()}\n{'='*80}\n"); gr()
