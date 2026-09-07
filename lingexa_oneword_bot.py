"""
Lingexa One Word - Powerful Vocabulary
One word can replace a whole sentence
"""

import os,sys,json,random,asyncio,subprocess,time,math
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

FB = [
    "C:/Windows/Fonts/segoeuib.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
]
FR = [
    "C:/Windows/Fonts/segoeui.ttf",
    "C:/Windows/Fonts/arial.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
]
FI = [
    "C:/Windows/Fonts/segoeuii.ttf",
    "C:/Windows/Fonts/ariali.ttf",
    "C:/Windows/Fonts/georgiai.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-Italic.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf"
]

def lf(font_list, sz):
    from PIL import ImageFont
    for fp in font_list:
        try:
            return ImageFont.truetype(fp, sz)
        except Exception:
            continue
    return ImageFont.load_default()


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
    from PIL import Image, ImageDraw
    img = Image.new('RGB', (W, H2), (12, 14, 22))
    d = ImageDraw.Draw(img)
    for y in range(H2):
        ratio = y / H2
        r = int(12 + 12 * math.sin(ratio * math.pi))
        g = int(15 + 15 * math.sin(ratio * math.pi))
        b = int(24 + 32 * math.sin(ratio * math.pi))
        d.line([(0, y), (W, y)], fill=(r, g, b))

    # Glow sphere in upper-middle
    glow = Image.new("RGBA", (W, H2), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    cx, cy = W // 2, 600
    for rad in range(400, 50, -25):
        alpha = int(18 * (1 - rad / 400))
        gd.ellipse([(cx - rad, cy - rad), (cx + rad, cy + rad)], fill=(212, 175, 55, alpha))
    img = Image.alpha_composite(img.convert("RGBA"), glow).convert("RGB")
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

def wt(d, text, font, mw):
    words = str(text).split()
    lines = []
    curr = []
    for wd in words:
        test = ' '.join(curr + [wd])
        bbox = d.textbbox((0, 0), test, font=font)
        if (bbox[2] - bbox[0]) <= mw or not curr:
            curr.append(wd)
        else:
            lines.append(' '.join(curr))
            curr = [wd]
    if curr:
        lines.append(' '.join(curr))
    return lines

def gi(it, bg_img, op):
    from PIL import Image, ImageDraw
    img = bg_img.copy()
    d = ImageDraw.Draw(img)

    MX = 75
    CW = W - MX * 2
    CX = W // 2

    f_brand = lf(FB, 34)
    f_sub = lf(FB, 32)
    f_lbl = lf(FB, 34)
    f_body = lf(FR, 50)
    f_quote = lf(FI, 46)
    f_tip = lf(FR, 44)
    f_foot = lf(FR, 32)

    # 1. Header Brand Pill
    y = 110
    brand_txt = "LINGEXA  •  POWER VOCABULARY"
    bb = d.textbbox((0, 0), brand_txt, font=f_brand)
    bw, bh = bb[2] - bb[0], bb[3] - bb[1]
    px, py = 32, 16
    d.rounded_rectangle([(CX - bw // 2 - px, y), (CX + bw // 2 + px, y + bh + py * 2)], radius=25, fill=(28, 33, 50), outline=(212, 175, 55), width=2)
    d.text((CX, y + bh // 2 + py), brand_txt, fill=(240, 215, 140), font=f_brand, anchor="mm")
    y += bh + py * 2 + 45

    # 2. Hook Card: "STOP SAYING: '<PHRASE>'"
    ph = it.get("phrase", "")
    if ph:
        hook_pill = f"STOP SAYING: \"{ph.upper()}\""
        hook_fs = 36
        f_hook = lf(FB, hook_fs)
        hb = d.textbbox((0, 0), hook_pill, font=f_hook)
        hw = hb[2] - hb[0]
        while hw > CW - 70 and hook_fs > 22:
            hook_fs -= 2
            f_hook = lf(FB, hook_fs)
            hb = d.textbbox((0, 0), hook_pill, font=f_hook)
            hw = hb[2] - hb[0]
        hh = hb[3] - hb[1]
        h_pad = 20
        d.rounded_rectangle([(CX - hw // 2 - 28, y), (CX + hw // 2 + 28, y + hh + h_pad * 2)], radius=16, fill=(45, 20, 30), outline=(220, 80, 90), width=2)
        d.text((CX, y + hh // 2 + h_pad), hook_pill, fill=(255, 190, 195), font=f_hook, anchor="mm")
        y += hh + h_pad * 2 + 35

    # 3. Transition Sub-hook
    trans_txt = "—  USE THIS 1-WORD UPGRADE INSTEAD  —"
    d.text((CX, y), trans_txt, fill=(212, 175, 55), font=lf(FB, 28), anchor="mm")
    y += 50

    # 4. Main Word Hero Card (Glassmorphic)
    word_str = it["word"].upper()
    wf_size = 125
    wf = lf(FB, wf_size)
    ww = d.textbbox((0, 0), word_str, font=wf)[2] - d.textbbox((0, 0), word_str, font=wf)[0]
    while ww > CW - 60 and wf_size > 55:
        wf_size -= 5
        wf = lf(FB, wf_size)
        ww = d.textbbox((0, 0), word_str, font=wf)[2] - d.textbbox((0, 0), word_str, font=wf)[0]

    wh = d.textbbox((0, 0), word_str, font=wf)[3] - d.textbbox((0, 0), word_str, font=wf)[1]
    hero_h = wh + 120
    card_hero = Image.new("RGBA", (CW, hero_h), (25, 30, 48, 220))
    cd = ImageDraw.Draw(card_hero)
    cd.rounded_rectangle([(0, 0), (CW, hero_h)], radius=24, fill=(25, 30, 48, 220), outline=(212, 175, 55), width=3)
    cd.text((CW // 2, hero_h // 2 - 20), word_str, fill=(255, 255, 255), font=wf, anchor="mm")
    pos_val = it.get("part_of_speech") or "vocabulary"
    pos_str = f"•  {pos_val.upper()}  •"
    cd.text((CW // 2, hero_h - 35), pos_str, fill=(212, 175, 55), font=f_sub, anchor="mm")
    img.paste(card_hero.convert("RGB"), (MX, y), card_hero)
    y += hero_h + 40

    # 5. Definition Card
    df = it.get("definition", "")
    lines_def = wt(d, df, f_body, CW - 80)
    while len(lines_def) > 3 and f_body.size > 36:
        f_body = lf(FR, f_body.size - 4)
        lines_def = wt(d, df, f_body, CW - 80)
    lh = d.textbbox((0, 0), "Ag", font=f_body)[3] - d.textbbox((0, 0), "Ag", font=f_body)[1]
    bh1 = 70 + len(lines_def) * int(lh * 1.45) + 25
    c1 = Image.new("RGBA", (CW, bh1), (20, 24, 38, 230))
    c1d = ImageDraw.Draw(c1)
    c1d.rounded_rectangle([(0, 0), (CW, bh1)], radius=18, fill=(20, 24, 38, 230), outline=(50, 60, 90), width=2)
    c1d.text((40, 35), "DEFINITION", fill=(212, 175, 55), font=f_lbl, anchor="lm")
    cy1 = 85
    for line in lines_def:
        c1d.text((40, cy1), line, fill=(245, 245, 250), font=f_body, anchor="lt")
        cy1 += int(lh * 1.45)
    img.paste(c1.convert("RGB"), (MX, y), c1)
    y += bh1 + 35

    # 6. Example Sentence Card
    ex = it.get("example", "")
    ex_quoted = f"\"{ex}\"" if ex and not ex.startswith('"') else (ex or "")
    lines_ex = wt(d, ex_quoted, f_quote, CW - 80)
    while len(lines_ex) > 3 and f_quote.size > 34:
        f_quote = lf(FI, f_quote.size - 4)
        lines_ex = wt(d, ex_quoted, f_quote, CW - 80)
    lh2 = d.textbbox((0, 0), "Ag", font=f_quote)[3] - d.textbbox((0, 0), "Ag", font=f_quote)[1]
    bh2 = 70 + len(lines_ex) * int(lh2 * 1.45) + 25
    c2 = Image.new("RGBA", (CW, bh2), (20, 24, 38, 230))
    c2d = ImageDraw.Draw(c2)
    c2d.rounded_rectangle([(0, 0), (CW, bh2)], radius=18, fill=(20, 24, 38, 230), outline=(50, 60, 90), width=2)
    c2d.text((40, 35), "IN A SENTENCE", fill=(140, 195, 255), font=f_lbl, anchor="lm")
    cy2 = 85
    for line in lines_ex:
        c2d.text((40, cy2), line, fill=(225, 235, 250), font=f_quote, anchor="lt")
        cy2 += int(lh2 * 1.45)
    img.paste(c2.convert("RGB"), (MX, y), c2)
    y += bh2 + 35

    # 7. Memory Trick Card
    tp = it.get("tip", "")
    if tp and y < H2 - 200:
        lines_tip = wt(d, tp, f_tip, CW - 80)
        while len(lines_tip) > 3 and f_tip.size > 30:
            f_tip = lf(FR, f_tip.size - 4)
            lines_tip = wt(d, tp, f_tip, CW - 80)
        lh3 = d.textbbox((0, 0), "Ag", font=f_tip)[3] - d.textbbox((0, 0), "Ag", font=f_tip)[1]
        bh3 = 65 + len(lines_tip) * int(lh3 * 1.45) + 25
        c3 = Image.new("RGBA", (CW, bh3), (35, 30, 20, 230))
        c3d = ImageDraw.Draw(c3)
        c3d.rounded_rectangle([(0, 0), (CW, bh3)], radius=18, fill=(35, 30, 20, 230), outline=(212, 175, 55), width=2)
        c3d.text((40, 32), "MEMORY TRICK", fill=(255, 215, 110), font=f_lbl, anchor="lm")
        cy3 = 78
        for line in lines_tip:
            c3d.text((40, cy3), line, fill=(250, 240, 220), font=f_tip, anchor="lt")
            cy3 += int(lh3 * 1.45)
        img.paste(c3.convert("RGB"), (MX, y), c3)

    # 8. Footer
    d.line([(MX, H2 - 85), (W - MX, H2 - 85)], fill=(50, 60, 90), width=1)
    footer_handle = CN.lower().replace(' ', '')
    d.text((CX, H2 - 45), f"Save & Follow for Daily Power Words  •  @{footer_handle}", fill=(160, 175, 205), font=f_foot, anchor="mm")

    img = img.convert('RGB')
    Path(op).parent.mkdir(parents=True, exist_ok=True)
    img.save(op, quality=96, optimize=True)
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
