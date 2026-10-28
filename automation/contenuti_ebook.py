# GUIDA-SVILUPPO: sostituisce i testi segnaposto (home, chi siamo, servizi) IT+EN. Rilanciabile. Nessun dato inventato (numeri, recensioni, indirizzi).
import json, os, re
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATS = [("ai-prompt","AI e prompt","AI & Prompts","Prompt pronti e metodi per usare l'AI nel lavoro.","Ready-made prompts and methods to use AI at work."),
 ("creativita","Creatività","Creativity","Scrittura, fotografia e grafica, anche partendo da zero.","Writing, photography and design, even from scratch."),
 ("lingue-studio","Lingue e studio","Languages & Study","Inglese per il lavoro e metodi per studiare meglio.","Business English and better study methods."),
 ("sviluppo-personale","Sviluppo personale","Personal Growth","Abitudini, produttività e organizzazione della giornata.","Habits, productivity and organizing your day."),
 ("finanza","Finanza personale","Personal Finance","Bilancio familiare, ETF e partita IVA forfettaria.","Family budget, ETFs and flat-rate VAT."),
 ("salute","Salute e benessere","Health & Wellness","Sonno, allenamento a casa e meditazione.","Sleep, home workouts and meditation."),
 ("business","Business","Business","E-commerce, freelance e SEO per piccoli siti.","E-commerce, freelancing and SEO for small sites.")]
T = {
 "it": dict(base="__BASEURL__", shop="/negozio/", cat="/negozio/categoria/", srv="/servizi/", con="/contatti/",
  eb="Guide pratiche in PDF", h1="Guide pratiche da leggere in un'ora, <em>da applicare subito.</em>",
  lead="Ebook in italiano su temi concreti: AI al lavoro, finanza personale, produttività, benessere e business. Ogni guida va dritta al punto e dice cosa fare, passo dopo passo.",
  b1="Vai al catalogo", b2="Come funziona", ce="Catalogo", ch="Scegli il tema che ti serve", cl="Sette categorie, ognuna con ebook di ingresso e guide più complete.",
  mc="Come funziona", mh="Dalla scelta alla lettura", steps=[("Scegli","Sfoglia le categorie e leggi la descrizione dell'ebook."),("Acquista","Aggiungi al carrello e completa l'ordine."),("Scarica","Ricevi il PDF e leggilo su telefono, tablet o computer."),("Applica","Ogni guida finisce con cose concrete da fare.")],
  ct="Hai una domanda?", cs="Scrivici prima di acquistare: ti rispondiamo volentieri.", cb="Contattaci", ccat_pre="Vedi gli ebook"),
 "en": dict(base="__BASEURL__", shop="/en/shop/", cat="/en/shop/category/", srv="/en/services/", con="/en/contact/",
  eb="Practical guides in PDF", h1="Practical guides you can read in an hour, <em>and apply today.</em>",
  lead="Ebooks on concrete topics: AI at work, personal finance, productivity, wellness and business. Each guide gets straight to the point and tells you what to do, step by step.",
  b1="Browse the catalog", b2="How it works", ce="Catalog", ch="Pick the topic you need", cl="Seven categories, each with entry-level ebooks and more complete guides.",
  mc="How it works", mh="From choosing to reading", steps=[("Choose","Browse the categories and read the ebook description."),("Buy","Add to cart and complete the order."),("Download","Get the PDF and read it on phone, tablet or computer."),("Apply","Every guide ends with concrete things to do.")],
  ct="Have a question?", cs="Write to us before you buy: we are happy to help.", cb="Contact us", ccat_pre="See the ebooks"),
}
def blocks(l):
    t = T[l]; i = 0 if l == "it" else 1
    cards = "".join('<div class="gc-pl ent-pl"><b>%s</b><p>%s</p><p><a class="gc-link" href="%s%s%s/">%s</a></p></div>' % (c[1+i], c[3+i], t["base"], t["cat"], c[0], t["ccat_pre"]) for c in CATS)
    steps = "".join('<div class="gc-pl"><span class="n">0%d</span><b>%s</b><p>%s</p></div>' % (n+1, s[0], s[1]) for n, s in enumerate(t["steps"]))
    cyc = "".join("<div><b>%s</b><span>%s</span></div>" % s for s in t["steps"])
    return [
     dict(id="hero", nome="Hero", enabled=True, html='<div class="gc"><section class="ent-hero"><div class="gc-wrap gc-hero-in"><div><p class="gc-eyebrow">%s</p><h1 class="gc-h1">%s</h1><p class="gc-lead">%s</p><div class="gc-act"><a class="gc-btn gc-btn-a" href="%s%s">%s</a><a class="gc-btn gc-btn-o" href="%s%s">%s</a></div></div><div class="ent-cycle">%s</div></div></section></div>' % (t["eb"], t["h1"], t["lead"], t["base"], t["shop"], t["b1"], t["base"], t["srv"], t["b2"], cyc)),
     dict(id="categorie", nome=t["ce"], enabled=True, html='<div class="gc"><section class="gc-sec gc-soft" id="categorie"><div class="gc-wrap"><p class="gc-eyebrow">%s</p><h2 class="gc-h2">%s</h2><p class="gc-lead">%s</p><div class="gc-plat ent-4">%s</div></div></section></div>' % (t["ce"], t["ch"], t["cl"], cards)),
     dict(id="metodo", nome=t["mc"], enabled=True, html='<div class="gc"><section class="gc-sec" id="metodo"><div class="gc-wrap"><p class="gc-eyebrow">%s</p><h2 class="gc-h2">%s</h2><div class="gc-plat ent-4">%s</div></div></section></div>' % (t["mc"], t["mh"], steps)),
     dict(id="contatti", nome="Contatti" if l == "it" else "Contact", enabled=True, html='<div class="gc"><section class="gc-sec gc-dark" id="contatti"><div class="gc-wrap"><h2 class="gc-h2">%s</h2><p class="gc-lead">%s</p><a class="gc-btn" href="%s%s">%s</a></div></section></div>' % (t["ct"], t["cs"], t["base"], t["con"], t["cb"]))]
def azienda(l):
    if l == "it":
        a = ("Chi siamo","Guide pratiche, scritte per essere usate","Casa Editrice Ebook pubblica ebook in italiano su temi di tutti i giorni: lavoro, soldi, studio, benessere. Niente teoria inutile: ogni guida spiega come fare una cosa precisa.","Pubblichiamo in PDF, così si legge ovunque e resta tuo. Ogni titolo ha una descrizione chiara di cosa contiene prima dell'acquisto.","Come ci comportiamo",[("Chiarezza","Scriviamo in modo semplice e diciamo subito cosa trovi in ogni ebook."),("Utilità","Ogni guida porta a qualcosa da fare, non solo da leggere."),("Onestà","Niente promesse di guadagni facili: spieghiamo cosa funziona e quanto impegno richiede.")])
    else:
        a = ("About us","Practical guides, written to be used","Casa Editrice Ebook publishes Italian-language ebooks on everyday topics: work, money, study, wellbeing. No useless theory: each guide explains how to do one specific thing.","We publish in PDF, so it reads anywhere and stays yours. Every title has a clear description of its contents before you buy.","How we behave",[("Clarity","We write simply and tell you up front what is in each ebook."),("Usefulness","Every guide leads to something to do, not just to read."),("Honesty","No promises of easy money: we explain what works and how much effort it takes.")])
    p = "".join('<div class="gc-pl"><span class="n">%d</span><b>%s</b><p>%s</p></div>' % (n+1, x[0], x[1]) for n, x in enumerate(a[5]))
    return [dict(id="chi", nome=a[0], enabled=True, html='<div class="gc"><section class="gc-sec" id="chi"><div class="gc-wrap"><p class="gc-eyebrow">%s</p><h2 class="gc-h2">%s</h2><p class="gc-lead">%s</p><p>%s</p></div></section></div>' % (a[0], a[1], a[2], a[3])),
            dict(id="principi", nome="Principi" if l == "it" else "Principles", enabled=True, html='<div class="gc"><section class="gc-sec gc-soft" id="principi"><div class="gc-wrap"><h2 class="gc-h2">%s</h2><div class="gc-plat">%s</div></div></section></div>' % (a[4], p))]
def wj(path, o):
    open(os.path.join(R, path), "w", encoding="utf-8", newline="\n").write(json.dumps(o, ensure_ascii=False, indent=2) + "\n")
wj("_data/blocks_home.json", blocks("it")); wj("_data/i18n/en/blocks_home.json", blocks("en"))
wj("_data/blocks_azienda.json", azienda("it")); wj("_data/i18n/en/blocks_azienda.json", azienda("en"))
def sub(path, pairs):
    f = os.path.join(R, path); s = open(f, encoding="utf-8").read()
    for a, b in pairs:
        s = re.sub(a, lambda m: b, s, flags=re.S)
    open(f, "w", encoding="utf-8", newline="\n").write(s)
sub("_pages/servizi.md", [(r"seo_description:.*?\n", 'seo_description: "Cosa trovi da Casa Editrice Ebook e come funziona l\'acquisto."\n'), (r"---\n\nUna frase.*$", "---\n\nEbook in PDF su temi pratici, in italiano. Ecco cosa trovi e come funziona.\n\n## Ebook\nGuide da 7,90 a 24,90 euro, divise in sette categorie: AI e prompt, creatività, lingue e studio, sviluppo personale, finanza, salute e business.\n\n## Anteprima gratuita e bundle\nPer ogni categoria stiamo preparando un'anteprima gratuita dei primi capitoli e un pacchetto di tre ebook a prezzo ridotto.\n\n## Come funziona l'acquisto\n1. **Scegli** l'ebook dal [catalogo]({{ '/negozio/' | relative_url }}).\n2. **Acquista** dal carrello.\n3. **Leggi** il PDF dove vuoi, su telefono, tablet o computer.\n\n[Contattaci]({{ '/contatti/' | relative_url }}){: .btn .btn--primary}\n")])
sub("en/servizi.md", [(r'description:.*?\n', 'description: "What you get at Casa Editrice Ebook and how buying works."\n'), (r"permalink: /en/services/\n---\n.*$", "permalink: /en/services/\n---\n\nPDF ebooks on practical topics, in Italian. Here is what you get and how it works.\n\n## Ebooks\nGuides from 7.90 to 24.90 euros, in seven categories: AI and prompts, creativity, languages and study, personal growth, finance, health and business.\n\n## Free preview and bundles\nFor each category we are preparing a free preview of the first chapters and a three-ebook bundle at a reduced price.\n\n## How buying works\n1. **Choose** the ebook from the [catalog]({{ '/en/shop/' | relative_url }}).\n2. **Buy** from the cart.\n3. **Read** the PDF anywhere: phone, tablet or computer.\n\n[Contact us]({{ '/en/contact/' | relative_url }}){: .btn .btn--primary}\n")])
sub("_config.yml", [(r'description: "Descrizione breve del sito[^"]*"', 'description: "Ebook in PDF in italiano su AI, finanza personale, produttività, benessere e business: guide pratiche da applicare subito."')])
print("ok")

