"""
Explore ChatGPT query fan-out for EU AI Act prompts via the Cloro API.

Usage:
    python cloro_fanout.py --smoke     # 1 prompt, prints response schema
    python cloro_fanout.py             # full 12-prompt study (~84 credits)

Auth: Authorization: Bearer $CLORO_API_KEY. In the cloud session the proxy
injects the real key for api.cloro.dev, so a dummy value is fine there.
Writes fanout_results.json and fanout_summary.csv in the current directory.
"""
import csv
import json
import os
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor

import requests

API_URL = "https://api.cloro.dev/v1/monitor/chatgpt"
KEY = os.environ.get("CLORO_API_KEY", "sk_proxy_injected")

PROMPTS = [
    # (id, language, country, prompt)
    ("chatbot", "de", "DE", "Muss mein Website-Chatbot nach dem EU AI Act angeben, dass er eine KI ist?"),
    ("chatbot", "fr", "FR", "Mon chatbot de site web doit-il indiquer qu'il est une IA selon l'AI Act européen ?"),
    ("chatbot", "nl", "NL", "Moet mijn websitechatbot volgens de EU AI Act vermelden dat het AI is?"),
    ("sme_duties", "de", "DE", "Was verlangt der EU AI Act von einem Unternehmen mit 50 Mitarbeitern, das ChatGPT nutzt?"),
    ("sme_duties", "fr", "FR", "Qu'exige l'AI Act européen d'une entreprise de 50 salariés qui utilise ChatGPT ?"),
    ("sme_duties", "nl", "NL", "Wat vereist de EU AI Act van een bedrijf met 50 medewerkers dat ChatGPT gebruikt?"),
    ("best_tool", "de", "DE", "Was ist das beste Tool zur Einhaltung des EU AI Act für KMU?"),
    ("best_tool", "fr", "FR", "Quel est le meilleur outil de conformité à l'AI Act pour les PME ?"),
    ("best_tool", "nl", "NL", "Wat is de beste EU AI Act compliance tool voor het mkb?"),
    ("literacy", "de", "DE", "Ist eine KI-Kompetenz-Schulung nach dem AI Act Pflicht, und welchen Kurs sollten wir nutzen?"),
    ("literacy", "fr", "FR", "La formation à la maîtrise de l'IA est-elle obligatoire selon l'AI Act, et quelle formation choisir ?"),
    ("literacy", "nl", "NL", "Is AI-geletterdheidstraining verplicht onder de AI Act, en welke cursus moeten we gebruiken?"),
]

PROMPTS_ES_IT = [
    ("chatbot", "es", "ES", "¿Mi chatbot web tiene que indicar que es una IA según la Ley de IA de la UE (AI Act)?"),
    ("chatbot", "it", "IT", "Il chatbot del mio sito web deve dichiarare di essere un'IA secondo l'AI Act europeo?"),
    ("sme_duties", "es", "ES", "¿Qué exige la Ley de IA de la UE a una empresa de 50 empleados que usa ChatGPT?"),
    ("sme_duties", "it", "IT", "Cosa richiede l'AI Act europeo a un'azienda con 50 dipendenti che usa ChatGPT?"),
    ("best_tool", "es", "ES", "¿Cuál es la mejor herramienta de cumplimiento de la Ley de IA de la UE para pymes?"),
    ("best_tool", "it", "IT", "Qual è il miglior strumento di conformità all'AI Act per le PMI?"),
    ("literacy", "es", "ES", "¿Es obligatoria la formación en alfabetización en IA según la Ley de IA, y qué curso deberíamos hacer?"),
    ("literacy", "it", "IT", "La formazione sull'alfabetizzazione in materia di IA è obbligatoria secondo l'AI Act, e quale corso dovremmo seguire?"),
]

EN_WORDS = {"the", "and", "for", "ai", "act", "eu", "best", "tool", "tools", "compliance", "requirements",
            "chatbot", "disclosure", "sme", "smes", "training", "literacy", "what", "how", "is", "of", "to",
            "in", "under", "company", "companies", "course", "courses", "mandatory", "obligations", "using",
            "employees", "transparency", "article", "software", "small", "business", "businesses"}
LOCAL_HINTS = {
    "de": {"der", "die", "das", "und", "für", "pflicht", "ki", "verordnung", "unternehmen", "kmu", "mitarbeiter", "schulung", "kennzeichnungspflicht"},
    "fr": {"le", "la", "les", "des", "pour", "et", "ia", "entreprise", "pme", "formation", "obligatoire", "conformité", "obligation"},
    "nl": {"de", "het", "en", "voor", "verplicht", "bedrijf", "mkb", "cursus", "geletterdheid", "medewerkers", "wat"},
}


def guess_lang(q: str, local: str) -> str:
    words = re.findall(r"[a-zA-ZÀ-ÿ]+", q.lower())
    if not words:
        return "?"
    en = sum(w in EN_WORDS for w in words)
    loc = sum(w in LOCAL_HINTS.get(local, set()) for w in words)
    if re.search(r"[äöüßéèêàçëï]", q.lower()):
        loc += 1
    return "en" if en > loc else local


def query_text(q):
    if isinstance(q, str):
        return q
    if isinstance(q, dict):
        return q.get("query") or q.get("text") or json.dumps(q, ensure_ascii=False)
    return str(q)


def domain_of(url: str) -> str:
    return re.sub(r"^https?://(www\.)?", "", url or "").split("/")[0].lower()


def run(item, attempts=4):
    pid, lang, country, prompt = item
    data = {}
    for i in range(attempts):
        try:
            r = requests.post(
                API_URL,
                headers={"Authorization": f"Bearer {KEY}"},
                json={"prompt": prompt, "country": country, "include": {"searchQueries": True}},
                timeout=320,
            )
            try:
                data = r.json()
            except ValueError:
                data = {"error": f"HTTP {r.status_code}", "body": r.text[:500]}
            data["_http_status"] = r.status_code
            data["_credits_charged"] = r.headers.get("X-Credits-Charged")
            data["_credits_remaining"] = r.headers.get("X-Credits-Remaining")
            if r.status_code < 500 and r.status_code != 429:
                break
        except Exception as e:  # noqa: BLE001
            data = {"error": str(e)}
        wait = 15 * (2 ** i)
        print(f"  retry {pid}/{lang} after {wait}s ({data.get('_http_status') or data.get('error')})", flush=True)
        time.sleep(wait)
    print(f"done {pid}/{lang}: HTTP {data.get('_http_status')} credits left {data.get('_credits_remaining')}", flush=True)
    return {"id": pid, "lang": lang, "country": country, "prompt": prompt, "response": data}


ASYNC_URL = "https://api.cloro.dev/v1/async/task"


def _req(method, url, **kw):
    for i in range(6):
        try:
            r = requests.request(method, url, headers={"Authorization": f"Bearer {KEY}"}, timeout=60, **kw)
            if r.status_code < 500 and r.status_code != 429:
                return r
            print(f"  {method} {r.status_code}, retrying", flush=True)
        except requests.RequestException as e:
            print(f"  {method} error {e}, retrying", flush=True)
        time.sleep(10 * (i + 1))
    return r


def run_async(items, wave="w1", poll=15, max_wait=1800):
    """Submit all prompts as async tasks (7 credits each), then poll until done."""
    tasks = {}
    for pid, lang, country, prompt in items:
        key = f"aiact-{wave}-{pid}-{lang}-{country}"
        body = {"taskType": "CHATGPT", "idempotencyKey": key,
                "payload": {"prompt": prompt, "country": country, "include": {"searchQueries": True}}}
        r = _req("POST", ASYNC_URL, json=body)
        d = r.json()
        tid = (d.get("task") or {}).get("id") or ((d.get("error") or {}).get("details") or {}).get("taskId")
        print(f"submitted {pid}/{lang}: HTTP {r.status_code} task={tid}", flush=True)
        tasks[(pid, lang, country, prompt)] = tid
    out, start = {}, time.time()
    while len(out) < len(tasks) and time.time() - start < max_wait:
        time.sleep(poll)
        for item, tid in tasks.items():
            if item in out or not tid:
                continue
            d = _req("GET", f"{ASYNC_URL}/{tid}").json()
            st = (d.get("task") or {}).get("status")
            if st in ("COMPLETED", "FAILED"):
                resp = d.get("response") or {}
                resp = dict(resp)
                if st == "COMPLETED" and "result" not in resp:  # async returns the result object unwrapped
                    resp = {"success": True, "result": resp}
                resp.setdefault("success", st == "COMPLETED")
                resp["_task_status"] = st
                resp["_credits_charged"] = (d.get("credits") or {}).get("creditsCharged")
                out[item] = resp
                print(f"done {item[0]}/{item[1]}: {st} credits={resp['_credits_charged']}", flush=True)
    results = []
    for item, tid in tasks.items():
        resp = out.get(item) or {"error": "not finished or not submitted", "_task_id": tid}
        results.append({"id": item[0], "lang": item[1], "country": item[2], "prompt": item[3], "response": resp})
    return results


def describe(obj, prefix="", depth=0):
    if depth > 3:
        return
    if isinstance(obj, dict):
        for k, v in obj.items():
            t = type(v).__name__ + (f"[{len(v)}]" if isinstance(v, (list, str)) else "")
            print(f"{prefix}{k}: {t}")
            describe(v, prefix + "  ", depth + 1)
    elif isinstance(obj, list) and obj:
        describe(obj[0], prefix + "  [0].", depth + 1)


def write_outputs(results, json_path="fanout_results.json", csv_path="fanout_summary.csv"):
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["prompt_id", "lang", "fanout_query", "query_lang_guess", "cited_domains"])
        for res in results:
            result = (res["response"] or {}).get("result", {}) or {}
            queries = [query_text(q) for q in (result.get("searchQueries") or [])]
            sources = result.get("sources") or []
            domains = sorted({domain_of(s.get("url") or s.get("link", "")) for s in sources if isinstance(s, dict)} - {""})
            if not queries:
                w.writerow([res["id"], res["lang"], "(no fan-out returned)", "", "; ".join(domains)])
            for q in queries:
                w.writerow([res["id"], res["lang"], q, guess_lang(q, res["lang"]), "; ".join(domains)])
            err = res["response"].get("error") if isinstance(res["response"], dict) else None
            print(f"[{res['lang']}] {res['id']}: {len(queries)} fan-out, {len(domains)} domains"
                  + (f"  ERROR: {err}" if err else ""))


def main():
    if "--smoke" in sys.argv:
        res = run(PROMPTS[0])
        with open("smoke_result.json", "w", encoding="utf-8") as f:
            json.dump(res, f, ensure_ascii=False, indent=2)
        print("HTTP", res["response"].get("_http_status"))
        describe(res["response"])
        return
    if "--async" in sys.argv:
        if "--es-it" in sys.argv:
            results = run_async(PROMPTS_ES_IT, wave="w1esit")
            write_outputs(results, "fanout_results_es_it.json", "fanout_summary_es_it.csv")
            return
        results = run_async(PROMPTS)
        write_outputs(results)
        print("Saved fanout_results.json and fanout_summary.csv")
        return
    if "--retry-failed" in sys.argv:
        results = json.load(open("fanout_results.json", encoding="utf-8"))
        for i, res in enumerate(results):
            if not (res["response"] or {}).get("success"):
                results[i] = run((res["id"], res["lang"], res["country"], res["prompt"]), attempts=6)
        write_outputs(results)
        print("Saved fanout_results.json and fanout_summary.csv")
        return
    with ThreadPoolExecutor(max_workers=1) as pool:
        results = list(pool.map(run, PROMPTS))
    write_outputs(results)
    print("Saved fanout_results.json and fanout_summary.csv")


if __name__ == "__main__":
    main()
