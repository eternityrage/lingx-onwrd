"""
Lingexa One Word - Powerful Vocabulary
One word can replace a whole sentence
"""

import os,sys,json,random,asyncio,subprocess,time
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
if sys.platform=="win32": sys.stdout.reconfigure(encoding="utf-8")
load_dotenv()
P=os.getenv("POLLINATIONS_API_KEY", "")
M=os.getenv("AI_MODEL", "gemini-fast")
B=Path(__file__).parent; O=B/"output"; V=O/"video"; H=O/"history"
for d in[O,V,H]: d.mkdir(exist_ok=True)
W=1080; H2=1920; F=30; TV="en-US-GuyNeural"; CN="Lingexa One Word"; WPV=3; HF=H/"all_words.json"; FD=B/"fonts"

def lh():
    if HF.exists():
        try: return json.load(open(HF,"r",encoding="utf-8"))
        except Exception: return {"words":[],"last_updated":None}
    return {"words":[],"last_updated":None}

def sh(d):
    d["last_updated"]=datetime.now().isoformat(); json.dump(d,open(HF,"w",encoding="utf-8"),indent=2,ensure_ascii=False)

def iu(w):
    h=lh(); return w.lower().strip() in[x.lower().strip() for x in h.get("words",[]) if x]

def ah(ws):
    h=lh(); e=[x.lower().strip() for x in h.get("words",[]) if x]
    for w in ws:
        clean = w.lower().strip()
        if clean and clean not in e:
            h["words"].append(clean)
            e.append(clean)
    sh(h)

# Diverse curated vocabulary bank as a 100% reliable fallback
FALLBACK_VOCABULARY = [
    {"word": "ineffable", "part_of_speech": "adjective", "phrase": "too wonderful to be expressed in words", "definition": "too great or extreme to be expressed", "example": "The sunset filled her with ineffable joy.", "tip": "In- (not) + effable (speakable) - cannot speak it."},
    {"word": "serendipity", "part_of_speech": "noun", "phrase": "finding good things without looking", "definition": "fortunate discovery made by chance", "example": "Finding this book was pure serendipity.", "tip": "From Persian fairy tale 'Three Princes of Serendip'."},
    {"word": "ephemeral", "part_of_speech": "adjective", "phrase": "lasting for only a very short time", "definition": "lasting for a very short time", "example": "Cherry blossoms are famously ephemeral.", "tip": "Epi- (upon) + hemera (day) - lasting just a day."},
    {"word": "mellifluous", "part_of_speech": "adjective", "phrase": "sweet and pleasant to hear", "definition": "sweet or musical; pleasant to hear", "example": "She had a rich, mellifluous singing voice.", "tip": "Melli- (honey) + fluous (flowing) - honey-flowing."},
    {"word": "quixotic", "part_of_speech": "adjective", "phrase": "unrealistically idealistic and impractical", "definition": "exceedingly idealistic and unrealistic", "example": "He launched a quixotic quest to fix everything.", "tip": "Inspired by Don Quixote tilting at windmills."},
    {"word": "verisimilitude", "part_of_speech": "noun", "phrase": "the appearance of being true or real", "definition": "the appearance of being real or truthful", "example": "The historical novel lacked verisimilitude.", "tip": "Veri (truth) + similitude (similarity) - like truth."},
    {"word": "alacrity", "part_of_speech": "noun", "phrase": "cheerful and eager readiness to act", "definition": "brisk and cheerful readiness", "example": "She accepted the promotion with joyful alacrity.", "tip": "Think 'alert' and 'active' readiness."},
    {"word": "ebullient", "part_of_speech": "adjective", "phrase": "overflowing with cheerful enthusiasm", "definition": "cheerful, lively, and full of energy", "example": "The crowd was in an ebullient mood tonight.", "tip": "Latin ebullire (to boil over with joy)."},
    {"word": "fastidious", "part_of_speech": "adjective", "phrase": "paying excessive attention to every detail", "definition": "very attentive to accuracy and detail", "example": "He was fastidious about keeping his desk tidy.", "tip": "Think 'fussy' and 'tidy' combined."},
    {"word": "grandiloquent", "part_of_speech": "adjective", "phrase": "using pompous and extravagant language", "definition": "pompous or extravagant in language", "example": "His grandiloquent speech bored the entire audience.", "tip": "Grand (large) + loqui (to speak) - big talk."},
    {"word": "halcyon", "part_of_speech": "adjective", "phrase": "peaceful, idyllic, and deeply happy", "definition": "denoting a period of idyllic calm and peace", "example": "He recalled the halcyon days of his youth.", "tip": "Ancient myth of kingfisher calming storm waters."},
    {"word": "insouciant", "part_of_speech": "adjective", "phrase": "showing a casual lack of worry", "definition": "showing a casual lack of concern; indifferent", "example": "She gave an insouciant shrug and smiled.", "tip": "In- (not) + souci (worry in French) - worry-free."},
    {"word": "juxtapose", "part_of_speech": "verb", "phrase": "place together to highlight contrasts", "definition": "place side by side to compare contrasts", "example": "The artist juxtaposed ancient and modern styles.", "tip": "Juxta (next to) + pose (place) - place beside."},
    {"word": "kaleidoscopic", "part_of_speech": "adjective", "phrase": "continually shifting in patterns and colors", "definition": "constantly changing in pattern or composition", "example": "The city presented a kaleidoscopic array of sights.", "tip": "Like looking through a turning kaleidoscope."},
    {"word": "laconic", "part_of_speech": "adjective", "phrase": "using very few words to explain", "definition": "using very few words to express much", "example": "His laconic reply was simply: 'No.'", "tip": "Spartans of Laconia spoke with extreme brevity."},
    {"word": "munificent", "part_of_speech": "adjective", "phrase": "larger or more generous than usual", "definition": "more generous than is usual or necessary", "example": "A munificent donor funded the entire shelter.", "tip": "Munus (gift) + facere (to make) - gift-maker."},
    {"word": "nefarious", "part_of_speech": "adjective", "phrase": "wicked, criminal, and devoid of morals", "definition": "wicked, villainous, or criminal", "example": "They uncovered a nefarious plot against the city.", "tip": "Latin nefas (crime against divine law)."},
    {"word": "obstreperous", "part_of_speech": "adjective", "phrase": "noisy and difficult to control", "definition": "noisy and difficult to control; unruly", "example": "The obstreperous children refused to sit down.", "tip": "Ob- (against) + strepere (to make noise)."},
    {"word": "panacea", "part_of_speech": "noun", "phrase": "a solution or remedy for all troubles", "definition": "a solution or remedy for all difficulties", "example": "Technology is helpful but not a panacea.", "tip": "Pan (all) + akos (cure) - all-curing remedy."},
    {"word": "querulous", "part_of_speech": "adjective", "phrase": "complaining in a petulant or whining manner", "definition": "complaining in a petulant or whining manner", "example": "She answered with a tired, querulous tone.", "tip": "From Latin queri (to complain like a quarrel)."},
    {"word": "resplendent", "part_of_speech": "adjective", "phrase": "attractive and impressive through richness", "definition": "attractive and impressive through rich brilliance", "example": "She looked resplendent in her velvet gown.", "tip": "Re- + splendere (to shine with splendor)."},
    {"word": "sagacity", "part_of_speech": "noun", "phrase": "the ability to make good judgments", "definition": "the quality of being wise and insightful", "example": "The elder was revered for her quiet sagacity.", "tip": "Think of a 'sage' having true vision."},
    {"word": "taciturn", "part_of_speech": "adjective", "phrase": "reserved and saying very little", "definition": "reserved or uncommunicative in speech", "example": "The detective remained taciturn and watchful.", "tip": "Latin tacere (to be silent) - quiet by nature."},
    {"word": "ubiquitous", "part_of_speech": "adjective", "phrase": "present, appearing, or found everywhere", "definition": "present, appearing, or found everywhere", "example": "Smartphones have become truly ubiquitous.", "tip": "Latin ubique (everywhere) - seen everywhere."},
    {"word": "vacillate", "part_of_speech": "verb", "phrase": "waver between different opinions or actions", "definition": "waver between different opinions or decisions", "example": "He vacillated between accepting or declining.", "tip": "Imagine an unsteady pendulum swinging back and forth."},
    {"word": "winsome", "part_of_speech": "adjective", "phrase": "attractive or appealing in character", "definition": "attractive or appealing in a fresh, charming way", "example": "She won everyone over with a winsome smile.", "tip": "Win + some - naturally wins affection."},
    {"word": "xenial", "part_of_speech": "adjective", "phrase": "warm and hospitable to strangers", "definition": "hospitable to strangers or guests", "example": "They offered a xenial welcome to the traveler.", "tip": "From Greek xenos (guest/stranger) + hospitality."},
    {"word": "yearning", "part_of_speech": "noun", "phrase": "a feeling of intense longing for something", "definition": "a feeling of intense longing for something", "example": "He felt a deep yearning for his homeland.", "tip": "Deep longing that pulls from within."},
    {"word": "zephyr", "part_of_speech": "noun", "phrase": "a gentle, mild, and refreshing breeze", "definition": "a soft, gentle, and mild breeze", "example": "A cool zephyr rustled through the evening leaves.", "tip": "From Zephyros, Greek god of the west wind."},
    {"word": "solipsism", "part_of_speech": "noun", "phrase": "the idea that only one's self exists", "definition": "the philosophical theory that only self exists", "example": "His self-obsession bordered on solipsism.", "tip": "Solus (alone) + ipse (self) - only self is real."},
    {"word": "redolent", "part_of_speech": "adjective", "phrase": "strongly reminiscent or suggestive of something", "definition": "strongly suggestive or evocative of something", "example": "The kitchen was redolent of fresh cinnamon.", "tip": "Re- (again) + olere (to smell) - evokes scent."},
    {"word": "perspicuous", "part_of_speech": "adjective", "phrase": "clearly expressed and easily understood", "definition": "clearly expressed and easily understood; lucid", "example": "Her explanation was admirably perspicuous.", "tip": "Per- (thoroughly) + spicere (to look) - easily seen."},
    {"word": "limerence", "part_of_speech": "noun", "phrase": "an involuntary state of romantic infatuation", "definition": "the state of being obsessively infatuated", "example": "What he thought was love was only limerence.", "tip": "Coined in psychology for all-consuming infatuation."},
    {"word": "chimerical", "part_of_speech": "adjective", "phrase": "wildly fanciful and highly unrealistic", "definition": "existing only as product of unchecked imagination", "example": "Investing all savings was a chimerical scheme.", "tip": "From Chimera, a mythical fire-breathing hybrid monster."},
    {"word": "defenestration", "part_of_speech": "noun", "phrase": "the act of throwing someone out a window", "definition": "the action of throwing someone out of a window", "example": "The historic rebellion began with a defenestration.", "tip": "De- (out of) + fenestra (window in Latin)."},
    {"word": "apocryphal", "part_of_speech": "adjective", "phrase": "widely circulated but of doubtful authenticity", "definition": "of doubtful authenticity, although widely circulated", "example": "The tale of the falling apple is apocryphal.", "tip": "Apo- (away) + kryptein (to hide) - obscure origins."},
    {"word": "lugubrious", "part_of_speech": "adjective", "phrase": "looking or sounding excessively sad and gloomy", "definition": "looking or sounding mournful and dismal", "example": "He wore a lugubrious expression all morning.", "tip": "Latin lugere (to mourn) - gloomy and dismal."}
]

def gd(n=WPV):
    ca=30
    cats=[
        "rare and intense emotional states",
        "character virtues, honor, and inner strength",
        "character flaws, arrogance, and human folly",
        "profound philosophical and existential ideas",
        "brilliant intellectual and academic concepts",
        "vivid sensory, atmospheric, and descriptive words",
        "masterful communication, rhetoric, and debate",
        "bold actions, decisive moves, and transformations",
        "leadership, authority, vision, and governance",
        "artistic brilliance, aesthetics, and creativity",
        "mysterious, ethereal, and enigmatic phenomena",
        "science, cosmic discoveries, and universal laws",
        "nature, wild landscapes, and elemental forces",
        "technology, future paradigms, and invention",
        "time, memory, nostalgia, and impermanence",
        "resilience, perseverance, and grit",
        "social dynamics, charisma, and diplomacy",
        "perception, cognition, and sharp awareness",
        "curiosity, wanderlust, and bold exploration",
        "tranquility, serenity, and mindful presence",
        "contrast, paradox, and subtle duality",
        "elegance, refinement, and sophistication",
        "courage, daring, and heroic feats",
        "ambition, mastery, and relentless pursuit"
    ]
    # Shuffle categories to ensure fresh themes on every single run
    random_cats = cats.copy()
    random.shuffle(random_cats)

    h = lh()
    history_words = [x.lower().strip() for x in h.get("words",[]) if x and x.strip()]
    all_used = set(history_words)
    print(f"[history] Loaded {len(all_used)} previously used words")

    c = []
    for a in range(ca):
        try:
            import requests
            u = "https://gen.pollinations.ai/v1/chat/completions"
            hd = {"Content-Type": "application/json"}
            if P:
                hd["Authorization"] = f"Bearer {P}"

            cat = random_cats[a % len(random_cats)]
            r = n - len(c)
            print(f"[api] Attempt {a+1}: {cat[:50]}... (need {r} more)")

            # Select a fresh mix of recent and sampled past words for the LLM avoid list
            recent_avoid = history_words[-50:]
            sampled_avoid = random.sample(history_words, min(30, len(history_words))) if history_words else []
            avoid_list = list(dict.fromkeys(recent_avoid + sampled_avoid + [x["word"].lower() for x in c]))
            us = ", ".join(avoid_list[-60:]) if avoid_list else "(none)"

            p = f"""Generate 15 powerful, sophisticated single-word English vocabulary words from category: {cat}.

CRITICAL ANTI-REPETITION RULES:
- NEVER repeat or suggest any of these previously used words: {us}
- Do NOT pick basic, common, or cliché words (e.g. happy, sad, angry, tyrant, leader, procrastinate, bibliophile, demagogue, autocrat, maverick).
- Every word must be a powerful, high-level English word that can replace a whole sentence or long phrase.

Return ONLY a valid JSON array of objects.

JSON schema per item:
[
  {{
    "word": "effulgent",
    "part_of_speech": "adjective",
    "phrase": "shining brightly and radiating light",
    "definition": "shining forth brilliantly or radiant",
    "example": "Her effulgent smile lit up the entire hall.",
    "tip": "Latin effulgere - to shine out like sunlight."
  }}
]

REQUIREMENTS:
- 'word': exactly ONE powerful English word (letters only, no spaces or hyphens)
- 'part_of_speech': noun, verb, or adjective
- 'phrase': the longer phrase it replaces (max 7 words)
- 'definition': simple, clear definition (max 10 words)
- 'example': example sentence (max 12 words)
- 'tip': memory trick or word root in ONE short sentence (max 12 words)
Return ONLY the raw JSON array."""

            payload = {
                "model": M or "gemini-fast",
                "messages": [
                    {"role": "system", "content": "You are a master English lexicographer. Return ONLY valid JSON arrays of unique vocabulary."},
                    {"role": "user", "content": p}
                ],
                "temperature": 1.25
            }
            resp = requests.post(u, headers=hd, json=payload, timeout=60)
            resp.raise_for_status()
            ct = resp.json()["choices"][0]["message"]["content"].strip()
            if "```json" in ct:
                ct = ct.split("```json")[1].split("```")[0].strip()
            elif "```" in ct:
                ct = ct.split("```")[1].split("```")[0].strip()
            it = json.loads(ct)
            if not isinstance(it, list):
                raise ValueError("Response is not a list")

            fr = []
            for itm in it:
                raw_w = itm.get("word", "").strip()
                if not raw_w or len(raw_w.split()) > 1:
                    continue
                w_clean = "".join(ch for ch in raw_w.lower() if ch.isalpha())
                if not w_clean or len(w_clean) < 3:
                    continue
                if w_clean in all_used:
                    print(f"  [dedup] Skipping already used word: '{w_clean}'")
                    continue

                itm["word"] = w_clean
                fr.append(itm)
                all_used.add(w_clean)
                if len(c) + len(fr) >= n:
                    break

            c.extend(fr)
            if len(c) >= n:
                chosen = c[:n]
                ah([m["word"] for m in chosen])
                return chosen
        except Exception as e:
            print(f"[api] Attempt {a+1} FAILED: {e}")
            time.sleep(1.5)

    # Robust fallback: use curated bank if API could not fulfill all words
    if len(c) < n:
        print("[fallback] Checking curated vocabulary bank for unused words...")
        shuffled_fallbacks = FALLBACK_VOCABULARY.copy()
        random.shuffle(shuffled_fallbacks)
        for fb in shuffled_fallbacks:
            w_clean = fb["word"].lower().strip()
            if w_clean not in all_used:
                c.append(fb)
                all_used.add(w_clean)
                print(f"  [fallback] Added unused curated word: '{w_clean}'")
                if len(c) >= n:
                    break

    if c:
        chosen = c[:n]
        ah([m["word"] for m in chosen])
        return chosen

    raise RuntimeError("Failed to generate vocabulary even with fallback bank")

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
