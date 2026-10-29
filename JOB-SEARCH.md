# Find a Job: A Practical Guide

> The missing half of the plan: how to get interviews, keep a search running without burning out, and
> evaluate an offer without getting hurt. It assumes you are working through [the study plan](README.md)
> or its [minimal path](MINIMAL-PATH.md). It cannot promise an offer.
> 简体中文: [JOB-SEARCH-cn.md](translations/JOB-SEARCH-cn.md)

## Who this is for

- General software engineering roles — backend, infrastructure, platform, data, mobile, ML-adjacent —
  at startups, mid-size companies, and large tech companies.
- People with 0–5 years of professional experience: career changers, bootcamp graduates applying for
  a first role, and people returning after a break who can already write working code.

Not a frontend/full-stack specialization guide; see the [scope note](MINIMAL-PATH.md#scope-note).

## Before you apply

Fix the artifacts first; a weak resume burns applications you cannot send again for six months.

### Resume

- **One page** under about ten years of experience; two pages only where local convention expects it.
- **Impact bullets, not duties.** "Cut p99 latency from 800 ms to 120 ms with a cache layer" beats
  "Responsible for backend performance". Use a real number when you have one.
- **Lead with the strongest item**, and **mirror the posting's vocabulary** — "PostgreSQL", not
  "Postgres". **No photo, birth date, or full address** unless local custom demands it.
- Start with [Update Your Resume](README.md#update-your-resume) and the
  [Tech Interview Handbook resume guide](https://www.techinterviewhandbook.org/resume/).

### GitHub and portfolio

- Pin two or three repositories you can explain; each needs a description, run steps, a screenshot,
  tests that run, and no employer code or credentials in the history. Archive abandoned coursework.
- One deployed project with a live URL beats ten tutorial clones; if you have nothing public, build
  one small end-to-end project — see [The Daily Plan](README.md#the-daily-plan).

### LinkedIn

- Headline: role + stack + location, e.g. "Backend engineer — Go, Postgres, Kubernetes". Fill in
  current role, education, and skills; recruiters search fields, not prose. "Open to work" for
  recruiters is usually enough; set location honestly if you need sponsorship.

### A tracking spreadsheet

One row per application, updated the same day. Minimum columns:

| Column | Why it exists |
|---|---|
| Role, company, level | Identify the process later |
| Posting URL | Re-read requirements before a screen |
| Source (career page, referral, recruiter) | Learn which channel works |
| Date applied | Measure response time and follow-up |
| Stage (applied, screen, onsite, offer, rejected) | See the real pipeline |
| Next action and date | Never let a process go silent |

Referrals are the highest-yield channel; see [Referral strategy](#referral-strategy). Keep a list of
20–30 people you could ask without embarrassment.

## Where to apply

- **Company career pages.** The default channel: apply on the company's own ATS (Greenhouse, Lever,
  Workday, Ashby) — it is the source of truth, and aggregators lag by days. Prefer recent postings.
- **LinkedIn.** Use [LinkedIn jobs](https://www.linkedin.com/jobs/) to find postings and the recruiter
  who owns them, then apply on the career page. "Easy Apply" is fine for volume, but lowest signal.
- **Hacker News "Who is Hiring".** A monthly thread on the first business day: browse the
  [whoishiring threads](https://news.ycombinator.com/submitted?id=whoishiring) or search with
  [HN search](https://hn.algolia.com/?q=who+is+hiring). Reply by email with the exact role, your
  location and visa status, and one concrete thing you built.
- **Wellfound and YC Work at a Startup.** [Wellfound](https://wellfound.com/) (ex-AngelList Talent)
  lists startup roles with salary and equity ranges;
  [YC Work at a Startup](https://www.workatastartup.com/) uses one profile across many YC companies.
- **levels.fyi for compensation research.** [levels.fyi](https://www.levels.fyi/) shows levels, bands,
  equity, and offers by company and location; use it to sanity-check "market rate". Data is
  self-reported, so treat outliers as outliers.
- **Recruiting agencies.** Pros: unposted roles, process knowledge, and a recruiter who negotiates
  for you, paid by the employer. Cons: paid on placement, they rarely work with candidates under
  2–3 years, and duplicate submissions cause conflicts. Never pay a fee.

## Referral strategy

### How to ask

- Ask one specific person about one specific role, not "any jobs at your company". Make it easy:
  link, resume, two sentences on fit.
- Ask for a referral, not a job — they fill in a form; they are not hiring you. Give them an out.
- Follow up once after 5–7 business days, then let it go. Thank them after they submit.

### A short template

```text
Subject: Referral for <role> at <company>?

Hi <name>,

I saw <company> is hiring a <role> (<link>). I have <X years> of <work>,
most recently <one concrete result>. I think I'd fit because <one reason>.

Would you be comfortable referring me? I can send my resume and a short blurb.
No pressure if the team is not hiring or you would rather not.

Thanks, <your name>
```

### What not to do

- Do not ask a stranger to "get you a job" in one line with no context.
- Do not ask for a referral to a role you are clearly unqualified for; do not exaggerate; do not go
  silent afterwards — they will be asked how they know you.

## Application strategy

- **10–20 quality applications per week**, not a hundred — quality means the resume matches the role.
- **Tailor resume keywords** per posting: reorder bullets, mirror the required stack, cut the rest.
- **Apply within 48 hours** of a posting going live; response rates fall after the first few days.
- **Track every stage** in the spreadsheet. Follow up once after 5–7 business days if you have a
  human contact; do not chase an ATS.
- **Rotate channels** — career page, referral, recruiter, HN, community. **Avoid spray-and-pray**:
  mass-applying inside one company, or to roles you do not match, gets you filtered and remembered.
- Applications take 3–5 hours a week; they are not a replacement for [the plan](MINIMAL-PATH.md).

## Interview pipeline

Typical for general SWE roles. Startups compress or reorder stages.

- **Recruiter screen (20–30 min).** Motivation, timeline, location and visa, salary expectations, and
  a background check. Have a one-sentence "why this company" and a range, not a number.
- **Technical screen (45–60 min).** One or two coding problems in a shared editor; sometimes a short
  take-home. Expect [the same material](MINIMAL-PATH.md#the-8-week-schedule) you are already studying.
- **Onsite loop (3–5 rounds).** Usually two coding, one behavioral, and one design or domain round.
  Do not book two full-day loops on consecutive days; ask for the structure in advance.
- **Behavioral round.** STAR (situation, task, action, result), 60–90 seconds, one story per question.
  Prepare conflict, failure, ambiguity, and "why us". See
  [Be thinking of for when the interview comes](README.md#be-thinking-of-for-when-the-interview-comes)
  and [Have questions for the interviewer](README.md#have-questions-for-the-interviewer).
- **System design (if senior).** Expected at 4+ years or for architecture ownership; start early with
  [System Design, Scalability, Data Handling](README.md#system-design-scalability-data-handling).
- **Timelines.** First reply 1–3 weeks; screen to onsite 1–2 weeks; onsite to offer 3–10 days. Whole
  process 4–8 weeks at a large company, 1–3 at a startup. Keep 5–10 active processes and ask for
  offer deadlines in writing.

## Offer and negotiation basics

- **Research first.** Use [levels.fyi](https://www.levels.fyi/) and your network for the band, then
  negotiate base, bonus, equity, sign-on, level, and start date.
- **One respectful negotiation is normal.** Recruiters expect it. State the number you want, with a
  reason (market data, competing offer, scope), then let them respond.
- **A competing offer is leverage only if it is real.** Never fabricate one; a discovered bluff ends
  the process. **Get the final offer in writing** before you resign or decline anything.
- **Prefer level over base** where bands are rigid — a level bump compounds. **Equity is not cash**:
  discount it, check the strike price and vesting, and ask about refresh policy.
- **Deadlines can often be extended once.** Ask politely; do not invent a deadline to create urgency.

## International and visa notes

- **Ask early.** "Do you sponsor work visas?" belongs in the recruiter screen. "No sponsorship" is
  often buried in the fine print; if it matters, ask directly.
- **Timing is long.** A US H-1B needs a March registration and usually an October start (cap-exempt
  employers differ). UK and Canada timelines are shorter but still measured in months.
- **Country caveats.** Some roles require citizenship or clearance; some countries prefer local hires;
  some remote roles are tied to a payroll entity's country. Use primary sources, not forums:
  [USCIS](https://www.uscis.gov/working-in-the-united-states),
  [UK Skilled Worker visa](https://www.gov.uk/skilled-worker-visa),
  [Canada immigration](https://www.canada.ca/en/immigration-refugees-citizenship.html).
- **Do not overpromise yourself.** If a company cannot sponsor, that interview is practice, not a
  pipeline. This is not legal advice; for a real case, talk to an immigration lawyer.

## Red flags and scams

- **Long unpaid take-homes.** Two to four hours is normal; a multi-day feature is free labor.
- **Crypto payments**, "training fees", "equipment fees", or requests for ID or bank details before
  a written offer. Employers pay you, not the other way around.
- **Interviews by chat only**, an offer without a technical conversation, or "sign today" urgency.
- **A vague company:** no website, no employees on LinkedIn, a free email domain, a PO box, or a
  recruiter who will not name the company. Verify `@company.com`, not `@company-careers.example`.

## A 30-day job-search plan

Assumes 8–12 hours a week on the search, alongside study. Adjust the volume, keep the order.

### Week 1 — Artifacts and targets

- Rewrite the resume to one page; get two reviews. Clean GitHub and fix LinkedIn.
- Build the spreadsheet, a target list of 30–40 companies, and 20–30 potential referrers.

### Week 2 — First wave

- Send 10–15 applications, at least half through referrals, and ask five to eight referrers.
- Book two mock interviews or timed sets with peers; keep the study plan running.

### Week 3 — Volume and interviews

- Send 10–20 more applications, tailoring the resume each time.
- Follow up on everything older than a week, do two more mocks, and write the behavioral stories
  down; log every rejection and fumbled question.

### Week 4 — Convert and review

- Push screens to onsites; ask for the loop structure, and note which channel produced the reply.
- With an offer, start negotiation research; without one, send the next ten and review the month's
  response, interview, and offer rates. Change one variable, not five.

### Weekly checklist

- [ ] 10–20 tailored applications sent
- [ ] 5 referral asks sent, one follow-up each
- [ ] 2 mock interviews or timed sets
- [ ] Every active process updated in the tracker
- [ ] Follow-ups sent for anything older than 7 days
- [ ] One concrete improvement to resume, GitHub, or portfolio; study plan still on schedule

## Further reading

- [The Minimal Path](MINIMAL-PATH.md) — the schedule this guide assumes.
- [Update Your Resume](README.md#update-your-resume) — resume guidance in this repo.
- [Interview Process & General Interview Prep](README.md#interview-process--general-interview-prep)
- [Once You've Got The Job](README.md#once-youve-got-the-job) — what to do after the offer.
- [Tech Interview Handbook](https://www.techinterviewhandbook.org/resume/) and its
  [behavioral interview guide](https://www.techinterviewhandbook.org/behavioral-interview/).
- Corrections welcome: [CONTRIBUTING.md](CONTRIBUTING.md).
