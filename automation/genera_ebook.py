# GUIDA-SVILUPPO: genera _data/catalogo.json e le pagine _negozio/ + en/negozio/ dal listino (LISTINO_EBOOK.md sez.3).
# Rilanciabile: sovrascrive catalogo.json e le pagine ebook-*/cat-*. Non tocca gli esempi. Prezzi in centesimi.
import json, os, re, glob
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATS = [  # id, it, en, icona
 ("ai-prompt", "AI e prompt", "AI & Prompts", "\U0001F916"),
 ("creativita", "Creatività", "Creativity", "\U0001F3A8"),
 ("lingue-studio", "Lingue e studio", "Languages & Study", "\U0001F4DA"),
 ("sviluppo-personale", "Sviluppo personale", "Personal Growth", "\U0001F331"),
 ("finanza", "Finanza personale", "Personal Finance", "\U0001F4B6"),
 ("salute", "Salute e benessere", "Health & Wellness", "\U0001F9D8"),
 ("business", "Business", "Business", "\U0001F4BC"),
]
P = [  # cat, it, en, prezzo cent
 (0,"150 prompt ChatGPT per lavorare meglio","150 ChatGPT Prompts to Work Smarter",990),
 (0,"Guadagnare con l'AI: 10 modi concreti","Making Money with AI: 10 Practical Ways",1490),
 (0,"Immagini con l'AI: guida pratica ai prompt","AI Images: A Practical Prompt Guide",1290),
 (1,"Scrivere un libro in 30 giorni","Write a Book in 30 Days",1490),
 (1,"Fotografia con lo smartphone","Smartphone Photography",990),
 (1,"Grafica per non designer","Graphic Design for Non-Designers",1290),
 (2,"Inglese per il lavoro: 300 frasi utili","Business English: 300 Useful Phrases",990),
 (2,"Metodo di studio per esami e concorsi","Study Method for Exams",1290),
 (2,"Imparare una lingua da soli","Learn a Language on Your Own",990),
 (3,"Abitudini: il metodo dei 21 giorni","Habits: The 21-Day Method",990),
 (3,"Produttività senza stress","Stress-Free Productivity",1290),
 (3,"Smart working: organizzare la giornata","Remote Work: Organize Your Day",990),
 (4,"Bilancio familiare in un weekend","Family Budget in One Weekend",990),
 (4,"Investire da zero: ETF spiegati semplici","Investing from Scratch: ETFs Explained",1990),
 (4,"Partita IVA forfettaria: guida pratica","Flat-Rate VAT Number: Practical Guide",1990),
 (5,"Dormire meglio: il metodo passo passo","Sleep Better: Step by Step",990),
 (5,"Allenarsi a casa: programma di 8 settimane","Home Workout: 8-Week Program",1490),
 (5,"Meditazione per chi non ha tempo","Meditation for Busy People",790),
 (6,"Aprire un e-commerce: dalla A alla Z","Start an E-commerce Store: A to Z",2490),
 (6,"Freelance: trovare i primi clienti","Freelancing: Landing Your First Clients",1490),
 (6,"SEO per piccoli siti","SEO for Small Websites",1490),
]
def slug(s):
    s = s.lower().replace("à","a").replace("è","e").replace("é","e").replace("ì","i").replace("ò","o").replace("ù","u")
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", s)).strip("-")[:48]
cats = [{"nome": c[1], "id": c[0], "icona": c[3], "tr": {"en": {"nome": c[2]}}} for c in CATS]
prods, pages = [], []
for cat, it, en, pr in P:
    c = CATS[cat]; pid = "ebook-" + slug(it)
    prods.append({"tipo": "digitale", "id": pid, "nome": it, "categoria": c[0], "prezzo_centesimi": pr,
      "descrizione": "Ebook PDF, download immediato. Argomento: %s." % c[1].lower(),
      "descrizione_completa": "Guida pratica in formato PDF, scritta per essere applicata subito.\nDownload immediato dopo il pagamento.\nIncluso: anteprima gratuita dei primi capitoli.",
      "immagine": "", "icona": c[3], "visibile": True,
      "tr": {"en": {"nome": en, "descrizione": "PDF ebook, instant download. Topic: %s." % c[2].lower(),
        "descrizione_completa": "A practical PDF guide you can apply right away.\nInstant download after payment.\nIncluded: free preview of the first chapters."}}})
    pages.append((pid, it, en))
d = json.load(open(os.path.join(R, "_data", "catalogo.json"), encoding="utf-8"))
d["categorie"], d["prodotti"] = cats, prods
json.dump(d, open(os.path.join(R, "_data", "catalogo.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
json.dump([{"nome": c[0], "slug": c[0]} for c in CATS], open(os.path.join(R, "_data", "shop-categorie.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
for f in glob.glob(os.path.join(R, "_negozio", "ebook-*.md")) + glob.glob(os.path.join(R, "_negozio", "cat-*.md")) + glob.glob(os.path.join(R, "en", "negozio", "ebook-*.md")) + glob.glob(os.path.join(R, "en", "negozio", "categoria", "cat-*.md")):
    os.remove(f)
def w(path, t):
    os.makedirs(os.path.dirname(path), exist_ok=True); open(path, "w", encoding="utf-8", newline="\n").write(t)
for pid, it, en in pages:
    w(os.path.join(R, "_negozio", pid + ".md"), '---\nlayout: negozio-prodotto\ntitle: "%s"\npid: %s\npermalink: /negozio/%s/\ndescription: "%s - ebook PDF."\nref: shop-prod-%s\n---\n' % (it, pid, pid, it, pid))
    w(os.path.join(R, "en", "negozio", pid + ".md"), '---\nlayout: negozio-prodotto\ntitle: "%s"\npid: %s\npermalink: /en/shop/%s/\ndescription: "%s - PDF ebook."\nlang: en\nlocale: en\nref: shop-prod-%s\n---\n' % (en, pid, pid, en, pid))
for c in CATS:
    w(os.path.join(R, "_negozio", "cat-" + c[0] + ".md"), '---\nlayout: negozio-categoria\ntitle: "%s"\ncid: %s\npermalink: /negozio/categoria/%s/\ndescription: "Ebook: %s."\nref: shop-cat-%s\n---\n' % (c[1], c[0], c[0], c[1], c[0]))
    w(os.path.join(R, "en", "negozio", "categoria", "cat-" + c[0] + ".md"), '---\nlayout: negozio-categoria\ntitle: "%s"\ncid: %s\npermalink: /en/shop/category/%s/\ndescription: "Ebooks: %s."\nlang: en\nlocale: en\nref: shop-cat-%s\n---\n' % (c[2], c[0], c[0], c[2], c[0]))
print("ok", len(prods), "prodotti", len(cats), "categorie")
