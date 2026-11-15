# Drop-in updates for the research summary

These replace or extend the matching sections of *B2B Affiliate / Referral Business: Research Summary*. The full summary is not stored in the repository.

## Replace section 0.3 (API facts)

- **Use the async API.** Submit with `POST https://api.cloro.dev/v1/async/task`, body `{"taskType":"CHATGPT","idempotencyKey":"...","payload":{"prompt":"...","country":"DE","include":{"searchQueries":true}}}`. Poll `GET /v1/async/task/{id}` until `task.status` is `COMPLETED` or `FAILED`.
  - A completed task returns the result object **unwrapped**: `response.text`, `response.sources` and so on, with no `result` key.
  - The cost is **7 credits**. A failed task costs nothing.
- **The sync endpoint** (`/v1/monitor/chatgpt`) costs **9 credits** with `searchQueries` and returned frequent 502s on long answers here.
- **Concurrency limit is 1** (`X-Concurrency-Limit: 1`), so send sync calls one at a time.
- **Response fields:**
  - `sources[]`: `{position, label, url, footnote}`
  - `citationPills[]`: `{url, label, domain, type, position}`. These are the sources ChatGPT actually cites inline.
  - `entities[]`, `searchQueries[]`, `mapSearchQueries[]`, `model`
- **Auth in this cloud environment:** the key is saved as a network secret for `api.cloro.dev`, and the proxy injects it into requests. Run the script with `CLORO_API_KEY=proxy-injected`.

## Replace section 13 status

**Status (15 Nov 2026):** wave 1 is done. The 12 ChatGPT prompts ran through the async API for 84 credits. See `ai-act-fanout/FINDINGS.md`.

**Key results:**
- **No fan-out returned** (0 of 12; `model: null`), so the English-vs-local share couldn't be measured on ChatGPT.
- **Informational prompts** are cited almost only from europa.eu pages: digital-strategy, the AI Act Service Desk and EUR-Lex. Most of those pages are in English, even for local-language prompts.
- **"Best tool" prompts** are won by vendors' own comparison pages. ActScope was cited and ranked #1 in DE, FR and NL. No independent comparison site was cited.
- **"Which course" prompts:** DE names KI-Campus, Bitkom Akademie and TÜV; FR names CNIL, FUN MOOC and France Num; NL names no provider at all. That's an open slot.
- **Recommendation:** lead with neutral comparison pages (tools and courses), start with Dutch, and approach ActScope and SetAIComply first.

## Update section 14 (open decisions)

- Wave 2 stays on ChatGPT: EN versions of the prompts plus repeats of the commercial prompts.
- First language: the data points to Dutch.
