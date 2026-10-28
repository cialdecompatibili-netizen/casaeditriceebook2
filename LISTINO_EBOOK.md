# LISTINO EBOOK - casaeditriceebook

Studio del 26/10/2026. Fonti: dataset Gumroad locale (420 ebook, `trend\analisi_ebook.py`), ricerche web su KDP/Kindle 2026. Prezzi in euro, pensati per il pubblico italiano.

## 1. Cosa dicono i dati

Gumroad (recensioni = proxy delle vendite, per prodotto):

| Tema | Ebook | Recensioni/prodotto | Prezzo mediano |
|---|---|---|---|
| AI e prompt | 27 | 128 | 29 |
| Creativita (arte, design, foto, scrittura) | 68 | 65 | 20 |
| Lingue e studio | 34 | 42 | 19 |
| Sviluppo personale | 30 | 30 | 20 |
| Finanza personale | 34 | 26 | 25 |
| Salute e benessere | 36 | 15 | 20 |
| Business e marketing | 22 | 8 | 29 |

Dal web (KDP 2026): non-fiction piu affidabile = business, finanza, produttivita, salute in micro-nicchie con domanda reale; in crescita sonno, genitorialita, benessere, cane/educazione; romance/romantasy e il genere che vende di piu ma richiede serie lunghe (per ora fuori).

Prezzi: i gratuiti (0-5) fanno 90 recensioni medie contro 13-18 delle altre fasce, quindi vanno bene come esca. Da 5 a 50 euro la resa e simile, il prezzo non frena.

Scartati: seduzione, steroidi, trading con Discord. Vendono ma non adatti a un brand editoriale.

## 2. Scala prezzi

- Assaggio gratuito: primi capitoli in PDF, per ogni categoria
- Ingresso: 4,90 - 9,90
- Principale: 14,90 - 24,90
- Bundle di categoria (3 ebook): 29 - 39

## 3. Listino (ordine = priorita di inserimento)

| # | Categoria | Titolo | Prezzo |
|---|---|---|---|
| 1 | AI e prompt | 150 prompt ChatGPT per lavorare meglio | 9,90 |
| 2 | AI e prompt | Guadagnare con l'AI: 10 modi concreti | 14,90 |
| 3 | AI e prompt | Immagini con l'AI: guida pratica ai prompt | 12,90 |
| 4 | Creativita | Scrivere un libro in 30 giorni | 14,90 |
| 5 | Creativita | Fotografia con lo smartphone | 9,90 |
| 6 | Creativita | Grafica per non designer | 12,90 |
| 7 | Lingue e studio | Inglese per il lavoro: 300 frasi utili | 9,90 |
| 8 | Lingue e studio | Metodo di studio per esami e concorsi | 12,90 |
| 9 | Lingue e studio | Imparare una lingua da soli | 9,90 |
| 10 | Sviluppo personale | Abitudini: il metodo dei 21 giorni | 9,90 |
| 11 | Sviluppo personale | Produttivita senza stress | 12,90 |
| 12 | Sviluppo personale | Smart working: organizzare la giornata | 9,90 |
| 13 | Finanza personale | Bilancio familiare in un weekend | 9,90 |
| 14 | Finanza personale | Investire da zero: ETF spiegati semplici | 19,90 |
| 15 | Finanza personale | Partita IVA forfettaria: guida pratica | 19,90 |
| 16 | Salute e benessere | Dormire meglio: il metodo passo passo | 9,90 |
| 17 | Salute e benessere | Allenarsi a casa: programma di 8 settimane | 14,90 |
| 18 | Salute e benessere | Meditazione per chi non ha tempo | 7,90 |
| 19 | Business | Aprire un e-commerce: dalla A alla Z | 24,90 |
| 20 | Business | Freelance: trovare i primi clienti | 14,90 |
| 21 | Business | SEO per piccoli siti | 14,90 |

Contenuto, titoli esatti e dati di partenza: rivedere dopo la prova di mercato (sez. 5).

## 4. Da inserire nel sito (casaeditriceebook)

- [ ] 7 categorie in `_data/catalogo.json` in ordine di profitto, con traduzione EN
- [ ] Prodotti 1-21 come `tipo: digitale`, con descrizione breve e completa
- [ ] Anteprima gratuita per categoria (lead magnet)
- [ ] Bundle di categoria (3 ebook a prezzo scontato)
- [ ] Copertine per ogni ebook (generaimmagini)
- [ ] Sostituire testi segnaposto home, servizi, chi siamo
- [ ] Contatti, email, WhatsApp
- [ ] Riuso del pattern scheda corso gia fatto su `corsi` (niente quantita, bottone "Acquista")

## 5. Prova di mercato (cosa va davvero)

Strumento: `Desktop\trend` (Reddit/HN/GitHub come sensori precoci, Google Trends per conferma, Gumroad/Etsy come arrivo). Aggiungere in `keywords_digitale.txt`: ebook prompt chatgpt, ebook finanza personale, ebook produttivita, ebook sonno, ebook partita iva, ebook inglese lavoro.
Regola: dopo 30 giorni tenere i primi 5 per visite/ordini, rimpiazzare gli ultimi.

## 6. Note

- Dataset Gumroad e in inglese: validare i titoli italiani con ricerche su Google Trends Italia e Amazon.it prima di scrivere.
- Il dataset ha bias verso nicchie web/AI/giochi. Per finanza, salute e studio pesano di piu le ricerche web.
