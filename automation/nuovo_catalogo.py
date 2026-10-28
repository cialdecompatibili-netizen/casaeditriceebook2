# GUIDA-SVILUPPO: genera il catalogo per reparti (12 reparti, ognuno con 8 sottocategorie), IT + EN. Rilanciabile.
# Cancella tutte le pagine _negozio/cat-*, _negozio/ebook-*, en/negozio/categoria/cat-*, en/negozio/ebook-* e le riscrive.
# Scrive: _data/catalogo.json (categorie, prodotti = []), _data/shop-categorie.json, _data/shop_nav.yml (+ i18n/en), home (blocco categorie).
# Aggiungere un reparto o una sottocategoria = modificare DEPTS qui sotto e rilanciare. Nessun prodotto: si aggiungono dall'admin.
import json, os, re, glob, unicodedata
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def slug(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

def clean(s):
    for a, b in (("attivita'", "attivit\u00e0"), ("Attualita'", "Attualit\u00e0"), ("produttivita'", "produttivit\u00e0"), ("Contabilita'", "Contabilit\u00e0"), ("spiritualita'", "spiritualit\u00e0")):
        s = s.replace(a, b)
    return s

# (icona, it, en, descrizione it, descrizione en, [(sotto it, sotto en), ...])
DEPTS = [
 ("\U0001F575", "Gialli, thriller e noir", "Crime, Thrillers & Noir", "Indagini, suspense e storie che non si lasciano posare.", "Investigations, suspense and stories you cannot put down.",
  [("Gialli classici", "Classic Mysteries"), ("Polizieschi e procedurali", "Police Procedurals"), ("Thriller psicologici", "Psychological Thrillers"), ("Noir e hard-boiled", "Noir & Hard-Boiled"),
   ("Legal thriller", "Legal Thrillers"), ("Spy story e intrigo internazionale", "Spy & International Intrigue"), ("True crime e cold case", "True Crime & Cold Cases"), ("Giallo leggero", "Cozy Mysteries")]),
 ("\u2764", "Romance e storie d'amore", "Romance & Love Stories", "Dalla commedia romantica al grande amore in costume.", "From romantic comedy to sweeping historical love.",
  [("Romance contemporaneo", "Contemporary Romance"), ("Romance storico", "Historical Romance"), ("New adult", "New Adult"), ("Paranormal romance", "Paranormal Romance"),
   ("Suspense romantica", "Romantic Suspense"), ("Commedia romantica", "Romantic Comedy"), ("Romance LGBTQ+", "LGBTQ+ Romance"), ("Seconde occasioni", "Second Chances")]),
 ("\U0001F409", "Fantasy e fantascienza", "Fantasy & Science Fiction", "Mondi inventati, futuri possibili e brividi dall'ignoto.", "Invented worlds, possible futures and chills from the unknown.",
  [("Epic fantasy", "Epic Fantasy"), ("Urban fantasy", "Urban Fantasy"), ("Dark fantasy", "Dark Fantasy"), ("Fantascienza spaziale", "Space Science Fiction"),
   ("Distopia e post-apocalittico", "Dystopian & Post-Apocalyptic"), ("Cyberpunk e steampunk", "Cyberpunk & Steampunk"), ("Viaggi nel tempo", "Time Travel"), ("Horror e soprannaturale", "Horror & Supernatural")]),
 ("\U0001F4D6", "Narrativa e classici", "Fiction & Classics", "I grandi romanzi di ieri e le voci di oggi.", "The great novels of yesterday and the voices of today.",
  [("Classici della letteratura", "Literary Classics"), ("Narrativa contemporanea", "Contemporary Fiction"), ("Romanzi di formazione", "Coming-of-Age Novels"), ("Narrativa storica", "Historical Fiction"),
   ("Racconti e antologie", "Short Stories & Anthologies"), ("Poesia", "Poetry"), ("Teatro", "Theatre & Plays"), ("Umorismo e satira", "Humor & Satire")]),
 ("\U0001F4A5", "Fumetti, manga e graphic novel", "Comics, Manga & Graphic Novels", "Storie a vignette per ogni gusto ed et\u00e0.", "Panel-by-panel stories for every taste and age.",
  [("Manga shonen e seinen", "Shonen & Seinen Manga"), ("Manga shojo e josei", "Shojo & Josei Manga"), ("Supereroi", "Superheroes"), ("Graphic novel d'autore", "Auteur Graphic Novels"),
   ("Fumetti italiani", "Italian Comics"), ("Fumetti autobiografici", "Autobiographical Comics"), ("Fumetti per ragazzi", "Comics for Young Readers"), ("Strisce e vignette", "Strips & Cartoons")]),
 ("\U0001F9F8", "Bambini e ragazzi", "Kids & Young Readers", "Letture per crescere, giocare e immaginare.", "Reads to grow, play and imagine.",
  [("Albi illustrati", "Picture Books"), ("Prime letture", "First Readers"), ("Avventura per ragazzi", "Adventure for Young Readers"), ("Fiabe e favole", "Fairy Tales & Fables"),
   ("Scienza e natura per ragazzi", "Science & Nature for Kids"), ("Giochi e attivita'", "Games & Activities"), ("Young adult", "Young Adult"), ("Libri per la scuola", "School Books")]),
 ("\U0001F464", "Biografie e memorie", "Biographies & Memoirs", "Vite vere raccontate da chi le ha vissute o studiate.", "True lives told by those who lived or studied them.",
  [("Artisti e creativi", "Artists & Creatives"), ("Imprenditori e leader", "Entrepreneurs & Leaders"), ("Sportivi", "Athletes"), ("Musicisti e protagonisti dello spettacolo", "Musicians & Performers"),
   ("Scienziati e pensatori", "Scientists & Thinkers"), ("Protagonisti della storia", "Figures of History"), ("Autobiografie e memorie", "Autobiographies & Memoirs"), ("Diari e lettere", "Diaries & Letters")]),
 ("\U0001F3DB", "Storia, politica e societ\u00e0", "History, Politics & Society", "Per capire il passato e leggere il presente.", "To understand the past and read the present.",
  [("Storia antica e medievale", "Ancient & Medieval History"), ("Storia moderna", "Modern History"), ("Storia contemporanea", "Contemporary History"), ("Guerre e conflitti", "Wars & Conflicts"),
   ("Politica e istituzioni", "Politics & Institutions"), ("Sociologia e cultura", "Sociology & Culture"), ("Filosofia", "Philosophy"), ("Attualita' e inchieste", "Current Affairs & Investigations")]),
 ("\U0001F4C8", "Economia, lavoro e finanza", "Business, Work & Finance", "Soldi, carriera e impresa spiegati con concretezza.", "Money, career and business explained plainly.",
  [("Finanza personale", "Personal Finance"), ("Investimenti e borsa", "Investing & Markets"), ("Startup e imprenditoria", "Startups & Entrepreneurship"), ("Management e leadership", "Management & Leadership"),
   ("Marketing e vendite", "Marketing & Sales"), ("Carriera e ricerca del lavoro", "Career & Job Search"), ("Contabilita' e fisco", "Accounting & Taxes"), ("Economia e mercati", "Economics")]),
 ("\U0001F331", "Crescita personale e benessere", "Self-Improvement & Wellbeing", "Mente, abitudini e relazioni: stare meglio ogni giorno.", "Mind, habits and relationships: feeling better every day.",
  [("Motivazione e successo", "Motivation & Success"), ("Abitudini e produttivita'", "Habits & Productivity"), ("Gestione dello stress", "Stress Management"), ("Psicologia", "Psychology"),
   ("Relazioni e famiglia", "Relationships & Family"), ("Meditazione e mindfulness", "Meditation & Mindfulness"), ("Alimentazione e salute", "Nutrition & Health"), ("Sonno e riposo", "Sleep & Rest")]),
 ("\U0001F52C", "Tecnologia, scienza e natura", "Technology, Science & Nature", "Dal codice alle stelle: curiosit\u00e0 e competenze.", "From code to the stars: curiosity and skills.",
  [("Informatica e programmazione", "Computing & Programming"), ("Intelligenza artificiale", "Artificial Intelligence"), ("Web e social media", "Web & Social Media"), ("Divulgazione scientifica", "Popular Science"),
   ("Matematica e fisica", "Mathematics & Physics"), ("Astronomia e spazio", "Astronomy & Space"), ("Natura e animali", "Nature & Animals"), ("Ambiente e clima", "Environment & Climate")]),
 ("\U0001F3A8", "Vita, hobby e tempo libero", "Lifestyle, Hobbies & Leisure", "Cucina, viaggi, arte e passioni per il tempo libero.", "Cooking, travel, art and passions for your free time.",
  [("Cucina e vini", "Cooking & Wine"), ("Casa, giardino e fai da te", "Home, Garden & DIY"), ("Viaggi e guide", "Travel & Guides"), ("Arte e fotografia", "Art & Photography"),
   ("Musica, cinema e spettacolo", "Music, Film & Performance"), ("Sport e outdoor", "Sports & Outdoors"), ("Religione e spiritualita'", "Religion & Spirituality"), ("Lingue e studio", "Languages & Study")]),
]

cats, fcat = [], []
for ic, it, en, dit, den, subs in DEPTS:
    it = clean(it); did = slug(it)
    cats.append(dict(nome=it, id=did, icona=ic, tr=dict(en=dict(nome=en))))
    fcat.append((did, it, en, slug(en), None))
    for sit, sen in subs:
        sit = clean(sit); sid = did + "-" + slug(sit)
        cats.append(dict(nome=sit, id=sid, icona="", genitore=did, tr=dict(en=dict(nome=sen))))
        fcat.append((sid, sit, sen, slug(en) + "-" + slug(sen), did))

# 1) cancella le vecchie pagine shop (categorie e prodotti)
for pat in ("_negozio/cat-*.md", "_negozio/ebook-*.md", "en/negozio/categoria/cat-*.md", "en/negozio/ebook-*.md"):
    for f in glob.glob(os.path.join(R, pat)):
        os.remove(f)

def w(path, txt):
    p = os.path.join(R, path); os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8", newline="\n").write(txt)

# 2) pagine categoria IT + EN (le sottocategorie vuote restano noindex finche' non hanno prodotti)
for cid, it, en, enslug, par in fcat:
    ni = "noindex: true\n" if par else ""
    w("_negozio/cat-%s.md" % cid, '---\nlayout: negozio-categoria\ntitle: "%s"\ncid: %s\npermalink: /negozio/categoria/%s/\ndescription: "Ebook: %s."\nref: shop-cat-%s\n%s---\n' % (it, cid, cid, it, cid, ni))
    w("en/negozio/categoria/cat-%s.md" % cid, '---\nlayout: negozio-categoria\ntitle: "%s"\ncid: %s\npermalink: /en/shop/category/%s/\ndescription: "Ebooks: %s."\nlang: en\nlocale: en\nref: shop-cat-%s\ntr: tradotto\n%s---\n' % (en, cid, enslug, en, cid, ni))

# 3) dati: nessun prodotto
d = json.load(open(os.path.join(R, "_data/catalogo.json"), encoding="utf-8"))
d["categorie"] = cats; d["prodotti"] = []
w("_data/catalogo.json", json.dumps(d, ensure_ascii=False, indent=2) + "\n")
w("_data/shop-categorie.json", json.dumps([dict(nome=c[0], slug=c[0]) for c in fcat], ensure_ascii=False, indent=2) + "\n")

# 4) menu Shop: tendina con i dodici reparti
def nav(lang):
    out = ["# Voci del dropdown Shop nella navbar (reparti). Generato da automation/nuovo_catalogo.py", "", "categories:"]
    for ic, it, en, dit, den, subs in DEPTS:
        it = clean(it)
        out.append('  - title: "%s"' % (it if lang == "it" else en))
        out.append("    url: %s" % (("/negozio/categoria/%s/" % slug(it)) if lang == "it" else ("/en/shop/category/%s/" % slug(en))))
    return "\n".join(out) + "\n\nfeatured: []\n"
w("_data/shop_nav.yml", nav("it")); w("_data/i18n/en/shop_nav.yml", nav("en"))

# 5) home: schede reparto + titolo e testo di apertura
TX = dict(
 it=("Il tuo prossimo ebook <em>lo trovi qui.</em>", "Dodici reparti, dai gialli ai romanzi d'amore, dalla fantascienza alla finanza personale. Scegli il genere, trova il titolo, scaricalo e leggilo dove vuoi.", "Catalogo", "Scegli il tuo reparto", "Dodici reparti, ognuno con le sue sottocategorie.", "Vedi gli ebook", "/negozio/categoria/"),
 en=("Your next ebook <em>is waiting here.</em>", "Twelve departments, from crime to romance, from science fiction to personal finance. Pick a genre, find a title, download it and read it anywhere.", "Catalog", "Choose your department", "Twelve departments, each with its own subcategories.", "See the ebooks", "/en/shop/category/"))
def home(lang):
    f = "_data/blocks_home.json" if lang == "it" else "_data/i18n/en/blocks_home.json"
    b = json.load(open(os.path.join(R, f), encoding="utf-8")); T = TX[lang]
    cards = "".join('<div class="gc-pl ent-pl"><b>%s</b><p>%s</p><p><a class="gc-link" href="__BASEURL__%s%s/">%s</a></p></div>' % (
        clean(x[1]) if lang == "it" else x[2], x[3] if lang == "it" else x[4], T[6], slug(clean(x[1])) if lang == "it" else slug(x[2]), T[5]) for x in DEPTS)
    for blk in b:
        if blk["id"] == "categorie":
            blk["html"] = '<div class="gc"><section class="gc-sec gc-soft" id="categorie"><div class="gc-wrap"><p class="gc-eyebrow">%s</p><h2 class="gc-h2">%s</h2><p class="gc-lead">%s</p><div class="gc-plat ent-4">%s</div></div></section></div>' % (T[2], T[3], T[4], cards)
        if blk["id"] == "hero":
            blk["html"] = re.sub(r'(<h1 class="gc-h1">).*?(</h1>)', lambda m: m.group(1) + T[0] + m.group(2), blk["html"], flags=re.S)
            blk["html"] = re.sub(r'(<p class="gc-lead">).*?(</p>)', lambda m: m.group(1) + T[1] + m.group(2), blk["html"], count=1, flags=re.S)
    w(f, json.dumps(b, ensure_ascii=False, indent=2) + "\n")
home("it"); home("en")
print("reparti:", len(DEPTS), "categorie totali:", len(cats), "prodotti: 0")
