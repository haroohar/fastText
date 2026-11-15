# EU AI Act: what ChatGPT cites (wave 1)

*Run on 15 Nov 2026 through the Cloro async API, ChatGPT engine, with `include.searchQueries`. 12 prompts (4 questions × DE/FR/NL, sent from DE/FR/NL). 84 credits. Raw data: `fanout_results.json`, `fanout_summary.csv`, `findings.json`. A single run per prompt, so treat this as directional, not statistical. Not legal advice.*

## TL;DR

1. **No fan-out came back: 0 of 12.** Every response had `searchQueries: []` and `model: null`. This is the "newer ChatGPT models may not expose it" case. So the English-vs-local search share **can't be measured on ChatGPT through Cloro right now.** The cited sources (below) are the usable signal instead.
2. **Informational questions are a lock for EU sources.** For "chatbot disclosure" and "50-person company duties", **every inline citation went to europa.eu**: digital-strategy.ec.europa.eu, the AI Act Service Desk, or EUR-Lex. The only national exceptions were Bundesnetzagentur (DE) and CNIL (FR). No law firm, chamber or vendor was cited. Writing another explainer won't win these answers.
3. **Local-language prompts get answered from English pages.** Most cited URLs are `/en/` pages from the Commission, even for the German, French and Dutch prompts. The answers themselves are fluent and in the local language. ChatGPT translates the English sources.
4. **Commercial questions are won by vendors' own comparison pages.** For "best AI Act tool for SMEs", the cited sources are vendor-written "best software 2026" lists:
   - **ActScope** (`actscope.eu`, "Best EU AI Act Compliance Software for SMEs (2026)") was cited in **all three languages**, and ChatGPT ranked it #1 in all three.
   - DE: Legalithm ("Compliance Software Tools Compared"), Compaia, SetAIComply.
   - FR: Transparia ("Comparatif 2026 des logiciels de conformité AI Act"), Kertos ("lequel choisir ?").
   - NL: unadhi.com, praxikon.com. These are weak, thin sources: **the Dutch slot is the most open.**
   - **No independent comparison or review site (G2, Capterra, a neutral publisher) was cited anywhere.** That is exactly the gap the business plan wants to fill.
5. **The training question splits by country.**
   - DE names real providers: **KI-Campus, Bitkom Akademie, TÜV (kurse.tuv.com, akademie.tuv.com)**. These are referral-partner candidates, but they also compete for the citation.
   - FR names free public offerings: CNIL, FUN MOOC, France Num.
   - NL names **no provider at all**. The answer ends by asking the user which kind of organisation they are, and offers to build "a shortlist of three Dutch-language courses". **That's a clear unfilled slot.**

## Who was cited (inline citation pills)

| Prompt | DE | FR | NL |
|---|---|---|---|
| chatbot disclosure | EC digital-strategy, EUR-Lex, Bundesnetzagentur | EC digital-strategy, AI Act Service Desk | EC digital-strategy, EUR-Lex |
| 50-person company duties | EUR-Lex, EC, Service Desk | EC, EUR-Lex, CNIL, Service Desk | EC, Service Desk, EUR-Lex, Council |
| best tool for SMEs | **actscope.eu, legalithm.com, compaia.eu, setaicomply.com**, EC | **actscope.eu, transparia.fr, kertos.io**, Service Desk | **actscope.eu, unadhi.com, praxikon.com** |
| literacy course | EC, **ki-campus.org, bitkom-akademie.de, kurse.tuv.com** | EC, EUR-Lex, Service Desk | EC, EUR-Lex |

**Brands ChatGPT recommended in "best tool" answers:**
- DE: ActScope, SetAIComply, Compaia, Legalithm, Credo AI
- FR: ActScope, SetAIComply, TransparIA, Dastra, Witik
- NL: ActScope, SetAIComply, AI-Act-Kompass, Veritome, Complipath

The NL answer quoted prices taken from "published comparisons": ActScope €39/mo, SetAIComply €39/mo, AI-Act-Kompass €9.99/mo, Veritome €79/mo, Complipath about $499/mo. A comparison page with up-to-date prices is evidently what gets cited.

## Terms the answers use (page targets)

There was no fan-out, so these come from the answer texts:
- **DE:** KI-Kompetenz, Schulung, Hochrisiko, Transparenzpflicht, Kennzeichnungspflicht, KMU, KI-Verordnung, Anbieter/Betreiber
- **FR:** formation (17× in one answer), maîtrise de l'IA, haut risque, PME, obligation de transparence, déployeur/fournisseur
- **NL:** AI-geletterdheid, mkb, transparantieverplichting, hoog risico, aanbieder, AI-verordening

## What this means for the plan

- **Don't compete on "what does the law say".** The EU pages win those answers. Use explainers only as supporting pages that link into the commercial ones.
- **Compete on "which tool / which course / which consultant".** Today ChatGPT fills those slots with vendors' self-promotional lists. A neutral, up-to-date comparison page per language is the most citable asset. It needs prices, a feature matrix, "best for" segments, and a last-updated date.
- **Start with Dutch.** It's the thinnest market (weak sources, and no course named at all), and KVK data says Dutch SMEs are the least informed.
- **Relationship angle:** ActScope and SetAIComply show up in every language. They are the obvious first vendors to approach for referral deals, and also the benchmark to beat in the rankings.

## Recommended first pages (content plan v1)

Each one in DE / FR / NL, plus an EN twin:

1. Best EU AI Act compliance tools for SMEs (2026): comparison with prices *(commercial, top priority)*
2. AI literacy (Article 4) training: course comparison by country, price and format *(commercial, NL first)*
3. ActScope vs SetAIComply vs Veritome *(commercial, "X vs Y")*
4. AI Act tools under €50/month for small businesses *(commercial)*
5. Chatbot and voice-agent disclosure: copy-paste texts plus a tool list *(bridge page to the voice-agent niche)*
6. AI Act checklist for a 50-person company, with a checker → recommended tools *(bridge page)*
7. ISO 42001 certification for SMEs: cost and providers by country *(commercial)*
8. AI Act consultants for SMEs by country *(lead-gen)*
9. What counts as high-risk (Annex III) in HR tools, plus which tools help *(bridge page)*
10. AI register / AI inventory templates and tools *(commercial)*

## Caveats and method notes

- One sample per prompt, and answers vary from run to run. Repeat 3× before you trust any ranking.
- The Cloro **sync** endpoint returned frequent 502s on the longer answers from this environment. The **async** API (`--async`) worked first time and costs 7 credits instead of 9. There were about 221 credits left after this run.
- The domain categories in `analyze.py` are regex heuristics. Many small AI Act vendors fall into "other"; the table above was classified by hand.

## Next step (wave 2)

Stay on ChatGPT:
- Run EN versions of the 4 questions from DE/FR/NL. This shows whether English prompts cite different (non-EU, commercial) sources.
- Repeat the commercial prompts ("best tool", "which course") to check whether ActScope's lead and the empty Dutch slot are stable.
- Re-check `searchQueries` from time to time in case Cloro starts returning fan-out again.

---

# Addendum: Spain and Italy (15 Nov 2026)

*8 more prompts (the same 4 questions in ES and IT, sent from ES/IT), Cloro async, 56 credits. Data: `fanout_results_es_it.json`, `fanout_summary_es_it.csv`. Again no fan-out returned.*

| Prompt | ES (inline cited) | IT (inline cited) |
|---|---|---|
| chatbot disclosure | EC digital-strategy, EUR-Lex | EUR-Lex, EC, Service Desk |
| 50-person company duties | EC, EUR-Lex, Council, **aepd.es** | EC, Service Desk, EUR-Lex |
| best tool for SMEs | **actscope.eu, toolradar.com, unadhi.com**, EC | **actscope.eu, setaicomply.com, veritome.eu, legalithm.com, aicomplibot.eu, expertinsights.com, flintbrief.com, toolradar.com, unadhi.com, praxikon.com**, EC |
| literacy course | EC, **boe.es, aesia.digital.gob.es**, EUR-Lex | EC, EUR-Lex, Service Desk |

- **Same pattern as DE/FR/NL.** EU sources win the questions about the law. Spain adds its national authorities (AEPD, BOE, AESIA).
- **ActScope is #1 again in both countries**, at €39/mo. ES recommends ActScope, SetAIComply, Complipath and Modulos; IT recommends ActScope, SetAIComply, Veritome and Legalithm. **No Spanish- or Italian-language comparison site was cited.** The sources are English-language vendor and directory pages (toolradar, expertinsights).
- **The training question is fully open in both.** Neither answer names a single course or provider. Like the NL answer, both end by asking about the type of organisation, and IT offers "un corso concreto, possibilmente in italiano e con attestato". **ES and IT are the same open slot as NL.**

**Updated language priority:** NL, IT and ES all have an empty "which course" slot and thin "best tool" sources. DE is the most contested, since established providers are already cited.

# Affiliate check: the cited German training providers

| Provider | What it is | Affiliate program? |
|---|---|---|
| **KI-Campus** (ki-campus.org) | Free learning platform funded by the BMBF (German federal research ministry), with CC BY-SA courses | **No.** It's free and non-commercial, so there's nothing to earn. It's useful as a free option on comparison pages, and it competes for the citation. |
| **Bitkom Akademie** | Paid seminars and certificate courses from the Bitkom industry association, including "KI-Kompetenzschulungen" | **None found.** No public program. You'd have to negotiate a referral or reseller deal directly (B2B in-house training is the valuable part). |
| **TÜV** (TÜV Rheinland Akademie, TÜV Austria, TÜV SÜD/NORD) | Paid courses and certificates | **No commission program.** TÜV Rheinland and TÜV Austria "partner programs" are licensing deals for training organisations that want to run TÜV-accredited courses, not referral commissions. |

**Implication:** the training slot doesn't monetise through public affiliate links. The options are:
1. negotiated referral deals with paid providers (Bitkom Akademie, TÜV, private trainers);
2. course marketplaces that have affiliate programs (to verify);
3. selling or reselling your own course or partner bundle in the empty NL/IT/ES slots.
