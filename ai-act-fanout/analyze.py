"""Analyze fanout_results.json -> findings.json + printed summary."""
import json
import re
import sys
from collections import Counter, defaultdict

path = sys.argv[1] if len(sys.argv) > 1 else "fanout_results.json"
results = json.load(open(path, encoding="utf-8"))

CATS = [
    ("eu_gov", r"(europa\.eu|eur-lex|ec\.europa)"),
    ("national_gov_regulator", r"(bundesnetzagentur|bsi\.bund|\.gouv\.fr|cnil\.fr|government\.nl|rijksoverheid|autoriteitpersoonsgegevens|rdi\.nl|bmwk|bund\.de|ondernemersplein|kvk\.nl|bpifrance)"),
    ("chamber_assoc", r"(ihk|dihk|bitkom|cci\.fr|cpme|medef|nlai|vno-ncw|mkb\.nl|handwerk|vdma|eco\.de)"),
    ("law_firm", r"(law|legal|kanzlei|avocat|advocaten|rechtsanwalt|heuking|taylorwessing|bird|osborne|cms|noerr|gleiss|hoganlovells|dlapiper|whitecase|lexology|fieldfisher|activemind|dr-datenschutz|datenschutz)"),
    ("standards_cert", r"(iso\.org|tuv|tüv|dekra|bsigroup|afnor|nen\.nl|din\.de)"),
    ("training", r"(academy|akademie|course|kurs|formation|training|udemy|coursera|linkedin\.com/learning|founderz|appliedai|ml6|opleiding)"),
    ("vendor_tool", r"(onetrust|vanta|secureframe|credo|modulos|matproof|validaitor|simpleact|setaicomply|holistic|trail|saidot|fairly|enzai|legiscope|drata|usercentrics|2b-advice|dataguard|heydata|caralegal|proliance)"),
    ("comparison_review", r"(capterra|g2\.com|getapp|trustradius|softwareadvice|omr\.com|appvizer|comparatif|vergleich)"),
    ("media_wiki_social", r"(wikipedia|linkedin|reddit|medium|youtube|heise|t3n|lesechos|lemonde|nos\.nl|fd\.nl|handelsblatt|computerwoche|zdnet|forbes|golem|frandroid|emerce|techzine)"),
    ("ai_act_info_site", r"(artificialintelligenceact|ai-act|aiact|ki-verordnung|euaiact)"),
]


def cat(domain):
    for name, rx in CATS:
        if re.search(rx, domain):
            return name
    return "other"


def dom(u):
    return re.sub(r"^https?://(www\.)?", "", u or "").split("/")[0].lower()


rows = []
dom_count = Counter()
cited_count = Counter()
cat_by_prompt = defaultdict(Counter)
fanout = []
for r in results:
    resp = r["response"] or {}
    res = resp.get("result") or {}
    sources = [s for s in (res.get("sources") or []) if isinstance(s, dict)]
    pills = [p for p in (res.get("citationPills") or []) if isinstance(p, dict)]
    sdoms = [dom(s.get("url")) for s in sources]
    pdoms = {p.get("domain") or dom(p.get("url")) for p in pills}
    for d in set(sdoms):
        dom_count[d] += 1
        cat_by_prompt[r["id"]][cat(d)] += 1
    for d in pdoms:
        cited_count[d] += 1
    qs = res.get("searchQueries") or []
    for q in qs:
        fanout.append((r["id"], r["lang"], q if isinstance(q, str) else json.dumps(q, ensure_ascii=False)))
    rows.append({
        "id": r["id"], "lang": r["lang"], "http": resp.get("_http_status"), "ok": bool(resp.get("success")),
        "n_sources": len(sources), "n_cited_domains": len(pdoms), "n_fanout": len(qs),
        "entities": [e.get("name") if isinstance(e, dict) else e for e in (res.get("entities") or [])],
        "domains": sorted(set(sdoms)),
        "text_len": len(res.get("text") or ""),
    })

findings = {
    "per_prompt": rows,
    "top_domains": [(d, n, cat(d)) for d, n in dom_count.most_common(40)],
    "top_cited_inline": cited_count.most_common(25),
    "category_by_prompt_type": {k: dict(v) for k, v in cat_by_prompt.items()},
    "category_totals": dict(Counter(cat(d) for d in dom_count.elements())),
    "fanout_queries": fanout,
}
json.dump(findings, open("findings.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)

for row in rows:
    print(f"{row['id']:11} {row['lang']} http={row['http']} src={row['n_sources']:2} cited={row['n_cited_domains']:2} "
          f"fanout={row['n_fanout']} entities={row['entities'][:6]}")
print("\nTOP DOMAINS (prompts citing):")
for d, n, c in findings["top_domains"]:
    print(f"  {n:2}  {d:45} {c}")
print("\nCATEGORY TOTALS:", findings["category_totals"])
print("\nBY PROMPT TYPE:")
for k, v in findings["category_by_prompt_type"].items():
    print(" ", k, v)
print("\nFAN-OUT:", len(fanout))
for f in fanout:
    print("  ", f)
