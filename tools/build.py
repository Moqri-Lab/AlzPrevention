"""Build the Alzheimer's prevention site.

Usage, from the repository root:
    python3 tools/build.py

Writes the HTML pages and style.css into the repository root. Shares its
layout with apoe4.science; only the accent colour and content differ.
"""
import pathlib
import re

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE.parent
SITE_URL = "https://alzprevent.org/"
SITE_NAME = "Alzheimer’s Prevention"
DESC = "A community resource on preventing Alzheimer’s disease: risk factors, evidence, prevention trials and data."

# Sibling of apoe4.science: same stylesheet, green accent instead of crimson.
css = (HERE / "apoe4-style.css").read_text()
for old, new in [("#b0234f", "#1f6f54"), ("#f6e3ea", "#e2f1ea"), ("#ec6b93", "#5fcf9f"), ("#3a1a26", "#16302a")]:
    css = css.replace(old, new)

PAGES = [  # (file, nav label, title)
    ("index.html", "Home", SITE_NAME),
    ("risk.html", "Risk factors", "Modifiable risk factors"),
    ("evidence.html", "What works", "Evidence from trials"),
    ("drugs.html", "Drugs", "Drugs"),
    ("trials.html", "Prevention trials", "Drug prevention trials"),
    ("resources.html", "Resources", "Data resources"),
    ("papers.html", "Papers", "Key papers"),
    ("about.html", "About", "About"),
]


def src(url, text):
    return f'<a href="{url}">{text}</a>'


def cite(url):
    return f' <a class="cite" href="{url}" title="Source" aria-label="Source">↗</a>'


def pill(kind, text):
    return f'<span class="pill {kind}">{text}</span>'


def head(label, h1, lede):
    return f"""    <div class="page-head">
      <p class="label">{label}</p>
      <h1>{h1}</h1>
      <p class="lede">{lede}</p>
    </div>"""


def shell(fname, title, body):
    nav = "\n".join(
        f'      <a href="{f}"' + (' aria-current="page"' if f == fname else "") + f">{label}</a>"
        for f, label, _ in PAGES)
    doc_title = SITE_NAME if fname == "index.html" else f"{title} · {SITE_NAME}"
    page_url = SITE_URL + ("" if fname == "index.html" else fname)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{doc_title}</title>
<meta name="description" content="{DESC}">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<meta property="og:title" content="{doc_title}">
<meta property="og:type" content="website">
<meta property="og:url" content="{page_url}">
<link rel="canonical" href="{page_url}">
<meta name="twitter:card" content="summary">
<meta property="og:description" content="{DESC}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Spectral:ital,wght@0,400;0,600;1,400&family=Public+Sans:wght@400;600&family=JetBrains+Mono:wght@400;600&display=swap">
<link rel="stylesheet" href="style.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="wrap">
  <header class="top">
    <a class="mark" href="index.html">alz<span>prevent</span>.org</a>
    <nav aria-label="Pages">
{nav}
    </nav>
  </header>
  <main id="main">
{body}
  </main>
  <footer>
    <span>Maintained by Mahdi Moqri, PhD, in a personal capacity. An educational resource, not medical advice. Sister site: <a href="https://apoe4.science">apoe4.science</a></span>
    <span class="updated">Last reviewed November 2026</span>
  </footer>
</div>
</body>
</html>
"""


def new_tabs(html, own="alzprevent.org"):
    """Open links to other sites in a new tab."""
    def fix(m):
        tag, url = m.group(0), m.group(1)
        if own in url or "target=" in tag:
            return tag
        return tag[:-1] + ' target="_blank" rel="noopener">'
    return re.sub(r'<a\b[^>]*\bhref="(https?://[^"]+)"[^>]*>', fix, html)


def slug(prefix, name):
    return prefix + "-" + re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def link_pair(internal_href, internal_text, external_href, external_text):
    out = '<span class="xlinks">'
    if internal_href:
        out += f'<a class="lnk-int" href="{internal_href}">→ {internal_text}</a>'
    if external_href:
        out += f'<a class="lnk-ext" href="{external_href}">↗ {external_text}</a>'
    return out + "</span>"


def pill_link(res, url):
    return re.sub(r'<span class="pill ([a-z]+)">([^<]*)</span>', lambda m: f'<a class="pill-link" href="{url}" title="Open external record"><span class="pill {m.group(1)}">{m.group(2)} ↗</span></a>', res, count=1)


def table(label, cols, rows, ids=None):
    th = "".join(f"<th>{c}</th>" for c in cols)
    ids = ids or [None] * len(rows)
    trs = "\n".join(
        "            <tr" + (f' id="{i}"' if i else "") + ">" + "".join(f'<td data-label="{c}"><span>{v}</span></td>' for c, v in zip(cols, r)) + "</tr>"
        for r, i in zip(rows, ids))
    return f"""      <div class="alleles" role="region" aria-label="{label}" tabindex="0">
        <table class="data">
          <thead><tr>{th}</tr></thead>
          <tbody>
{trs}
          </tbody>
        </table>
      </div>"""


LANCET = "https://doi.org/10.1016/S0140-6736(24)01296-0"
DISCLAIMER = '      <p class="disclaimer">This site is for education and is not medical advice. Talk with your doctor about your own risk and what is right for you.</p>'

pages = {}

# ---------- Home ----------
cards = [
    ("risk.html", "Risk factors", "The 14 changeable risk factors linked to nearly half of dementia."),
    ("evidence.html", "What works", "What randomized trials and natural experiments show so far."),
    ("trials.html", "Prevention trials", "Drug trials in people with Alzheimer’s changes but no symptoms."),
    ("resources.html", "Resources", "Cohorts and datasets for prevention research."),
    ("https://apoe4.science", "APOE4 carriers", "Sister site for people with two copies of APOE4, the highest-risk common genotype."),
    ("drugs.html", "Drugs", "Medicines tested for prevention, and those with early signals."),
]
pages["index.html"] = f"""    <div class="hero">
      <div>
        <p class="label">A community resource</p>
        <h1 style="margin-top:14px">Nearly half of dementia may be <em>preventable</em> or delayable.</h1>
        <p class="lede">The evidence on preventing Alzheimer’s disease, from everyday risk factors to drug trials in people who have no symptoms yet, with every figure linked to its source.</p>
      </div>
      <div class="geno" aria-label="45 percent">45%<small>Share of dementia linked to 14 modifiable risk factors (<a href="{LANCET}">Lancet Commission 2024</a>)</small></div>
    </div>
    <section>
      <div class="cards">
""" + "\n".join(f'        <a class="card" href="{f}"><h3>{t}</h3><p>{d}</p></a>' for f, t, d in cards) + """
      </div>
    </section>"""

# ---------- Risk factors ----------
risk_rows = [
    ("Early life", "Less education", "Good-quality education for all children; keep learning throughout life"),
    ("Midlife", "Hearing loss", "Get hearing tested; use hearing aids if needed"),
    ("Midlife", "High LDL cholesterol", "Check cholesterol from about age 40 and treat if high"),
    ("Midlife", "Depression", "Seek treatment for depression"),
    ("Midlife", "Traumatic brain injury", "Wear helmets and seatbelts; protect against head injury in sport"),
    ("Midlife", "Physical inactivity", "Stay physically active through life"),
    ("Midlife", "Diabetes", "Prevent and manage diabetes"),
    ("Midlife", "Smoking", "Stop smoking, at any age"),
    ("Midlife", "High blood pressure", "Check blood pressure and treat if high"),
    ("Midlife", "Obesity", "Maintain a healthy weight"),
    ("Midlife", "Excessive alcohol", "Limit alcohol"),
    ("Later life", "Social isolation", "Stay socially connected"),
    ("Later life", "Air pollution", "Reduce exposure to air pollution where possible"),
    ("Later life", "Untreated vision loss", "Get eyes checked; treat vision problems such as cataracts"),
]
pages["risk.html"] = head("Risk factors", "Fourteen risk factors you can change",
    "The 2024 Lancet Commission estimated that about 45% of dementia worldwide is linked to 14 modifiable risk factors across the life course.") + f"""
    <section>
{table("Modifiable risk factors", ["Life stage", "Risk factor", "What can help"], risk_rows)}
      <div class="prose" style="margin-top:24px">
        <p>Two factors were new in 2024: high LDL cholesterol in midlife, estimated to account for about 7% of dementia, and untreated vision loss in later life, about 2%.{cite(LANCET)}</p>
        <p>The suggested actions follow the Commission’s recommendations; they are general advice, not a personal plan.{cite(LANCET)}</p>
        <p>The 45% estimate assumes each factor is causal and could be removed entirely, so it shows the size of the opportunity rather than a promise for any one person.</p>
        <p>Genes matter too. Two copies of APOE4 raise risk far more than any single factor here; see the sister site {src("https://apoe4.science", "apoe4.science")}.</p>
      </div>
{DISCLAIMER}
    </section>"""

# ---------- Evidence ----------
ev_rows = [
    (src("https://doi.org/10.1016/S0140-6736(15)60461-5", "FINGER") + " (Finland)", "Two-year multidomain lifestyle program: diet, exercise, cognitive training, vascular risk management", "1,260 at-risk adults aged 60–77", pill("done", "Benefit") + " Better overall cognition than general health advice over two years; a small but significant effect."),
    (src("https://alz.org/us-pointer/study-results", "U.S. POINTER"), "Two-year structured versus self-guided lifestyle program", "2,111 sedentary adults aged 60–79 at risk", pill("done", "Benefit") + " Both groups improved; the structured program improved global cognition more." + cite("https://practicalneurology.com/news/us-pointer-study-results-a-structured-lifestyle-intervention-improved-cognition-in-older-adults/2475903/")),
    (src("https://doi.org/10.1001/jama.2018.21442", "SPRINT MIND"), "Intensive blood pressure control (systolic under 120) versus standard (under 140)", "Adults with high blood pressure", pill("done", "Partial benefit") + " Fewer cases of mild cognitive impairment (14.6 vs 18.3 per 1,000 person-years); the drop in dementia was not statistically significant. The trial stopped early."),
    (src("https://doi.org/10.1016/S0140-6736(23)01406-X", "ACHIEVE"), "Hearing aids and counselling versus health education", "977 older adults with hearing loss", pill("stop", "No overall benefit") + " No slowing of cognitive decline over three years overall; in a higher-risk subgroup from the ARIC study, decline was about 48% slower." + cite("https://aaic.alz.org/releases_2023/hearing-aids-slow-cognitive-decline.asp")),
    (src("https://www.sciencedaily.com/releases/2025/04/250402122149.htm", "Shingles vaccine, Wales"), "Natural experiment: vaccine eligibility set by date of birth", "Older adults born either side of 2 September 1933", pill("done", "Signal") + " Vaccination reduced new dementia diagnoses by about 3.5 percentage points over seven years (about 20% relative). Older live vaccine; not a randomized trial." + cite("https://www.news-medical.net/news/20250408/Shingles-vaccination-associated-with-reduction-in-probability-of-new-dementia-diagnosis.aspx")),
]
pages["evidence.html"] = head("What works", "Evidence from trials and natural experiments",
    "Randomized trials of lifestyle and medical approaches, and the strongest natural experiments, on preventing cognitive decline and dementia.") + f"""
    <section>
{table("Prevention evidence", ["Study", "Intervention", "Who", "Result"], ev_rows, ids=["ev-finger", "ev-us-pointer", "ev-sprint-mind", "ev-achieve", "ev-shingles"])}
      <p class="note">Benefits so far are on cognitive test scores or milder outcomes; no lifestyle trial has yet shown fewer dementia diagnoses as its main result.</p>
{DISCLAIMER}
    </section>"""

# ---------- Trials ----------
# (name, registry or record URL, drug as named on the Drugs page, who, participants, status-and-result)
TRIALS = [
    ("TRAILBLAZER-ALZ 3", "https://clinicaltrials.gov/study/NCT05026866", "Donanemab", "Cognitively unimpaired adults with Alzheimer’s pathology", "About 3,000 enrolled",
     pill("run", "Fully enrolled") + " Primary completion expected October 2027."),
    ("AHEAD 3-45", "https://clinicaltrials.gov/study/NCT04468659", "Lecanemab", "Adults with amyloid but no symptoms", "About 1,400 enrolled",
     pill("run", "Fully enrolled") + " Primary completion expected December 2028."),
    ("HT-4253", "https://clinicaltrials.gov/study/NCT07399171", "HT-4253", "Biomarker-positive APOE4 carriers in Abu Dhabi", "112 planned",
     pill("recruit", "Recruiting") + " 48-week Phase 2a, started May 2026."),
    ("A4 Study", "https://clinicaltrials.gov/study/NCT02008357", "Solanezumab", "Adults aged 65–85 with amyloid but no symptoms", "1,169 randomized",
     pill("stop", "No benefit") + " Did not slow cognitive decline." + cite("https://doi.org/10.1056/NEJMoa2305032")),
    ("API Colombia", "https://www.businesswire.com/news/home/20220616005106/en/Genentech-Provides-Update-on-Alzheimers-Prevention-Initiative-Study-Evaluating-Crenezumab-in-Autosomal-Dominant-Alzheimers-Disease", "Crenezumab",
     "Members of a Colombian family with an early-onset PSEN1 mutation", "252 enrolled",
     pill("stop", "No significant benefit") + " Numerical trends favoured the drug, none significant (2022)."),
    ("Generation Study 1", "https://clinicaltrials.gov/study/NCT02565511", "Umibecestat", "Cognitively unimpaired APOE4 homozygotes aged 60–75", "478 randomized",
     pill("stop", "Stopped 2019") + " Umibecestat worsened cognition slightly; the program ended."),
]


def drug_link(name, text=None):
    return f'<a href="drugs.html#{slug("drug", name)}">{text or name}</a>'


tr_rows = []
for name, url, drug, who, n, res in TRIALS:
    ext = "Registry" if "clinicaltrials.gov" in url else "Source"
    drug_cell = drug_link(drug) + (" or " + drug_link("CAD106") if name == "Generation Study 1" else "")
    tr_rows.append((f'<span class="dname">{name}</span>' + link_pair(f"drugs.html#{slug('drug', drug)}", "Drug", url, ext),
                    drug_cell, who, n, pill_link(res, url)))
pages["trials.html"] = head("Prevention trials", "Drug trials before symptoms",
    "Trials that treat people who have Alzheimer’s changes, or very high genetic risk, before memory problems begin. Ongoing trials first.") + f"""
    <section>
{table("Prevention drug trials", ["Trial", "Drug", "Who", "Participants", "Status and result"], tr_rows, ids=[slug("trial", t[0]) for t in TRIALS])}
      <p class="note">Status changes often; each status label links to the trial’s external record. To volunteer, search {src("https://clinicaltrials.gov/search?cond=Alzheimer+Disease&term=prevention", "ClinicalTrials.gov")} or use the Alzheimer’s Association’s {src("https://www.alz.org/alzheimers-dementia/research_progress/clinical-trials/trialmatch", "TrialMatch")}.</p>
    </section>"""

# ---------- Drugs ----------
# (name, company, type, internal href, internal label, external href, external label, note)
DRUGS = [
    ("In prevention trials now", [
        ("Donanemab", "Kisunla; Eli Lilly", "Anti-amyloid antibody, IV", "trials.html#trial-trailblazer-alz-3", "Trial", "https://dailymed.nlm.nih.gov/dailymed/search.cfm?query=kisunla", "FDA label",
         "Approved for early symptomatic Alzheimer’s; being tested before symptoms in TRAILBLAZER-ALZ 3."),
        ("Lecanemab", "Leqembi; Eisai and Biogen", "Anti-amyloid antibody, IV or under-the-skin", "trials.html#trial-ahead-3-45", "Trial", "https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=9d1ff786-e577-410a-a273-c4d7d0e4e975", "FDA label",
         "Approved for early symptomatic Alzheimer’s; being tested before symptoms in AHEAD 3-45."),
        ("HT-4253", "Halia Therapeutics", "Oral LRRK2 inhibitor", "trials.html#trial-ht-4253", "Trial", "https://clinicaltrials.gov/study/NCT07399171", "Registry",
         "Investigational; Phase 2a in APOE4 carriers who have no symptoms."),
    ]),
    ("Tested for prevention and failed or stopped", [
        ("Solanezumab", "Eli Lilly", "Anti-amyloid antibody", "trials.html#trial-a4-study", "Trial", "https://doi.org/10.1056/NEJMoa2305032", "Results",
         "No benefit in the A4 Study."),
        ("Crenezumab", "Genentech (Roche)", "Anti-amyloid antibody", "trials.html#trial-api-colombia", "Trial", "https://www.businesswire.com/news/home/20220616005106/en/Genentech-Provides-Update-on-Alzheimers-Prevention-Initiative-Study-Evaluating-Crenezumab-in-Autosomal-Dominant-Alzheimers-Disease", "Results",
         "No significant benefit in a family with early-onset Alzheimer’s."),
        ("Umibecestat", "Novartis and Amgen", "BACE inhibitor", "trials.html#trial-generation-study-1", "Trial", "https://clinicaltrials.gov/study/NCT02565511", "Registry",
         "Stopped in 2019 after mild cognitive worsening."),
        ("CAD106", "Novartis", "Active amyloid vaccine", "trials.html#trial-generation-study-1", "Trial", "https://clinicaltrials.gov/study/NCT02565511", "Registry",
         "Halted in 2019 with the rest of the Generation Program."),
    ]),
    ("Existing medicines with prevention signals", [
        ("Blood-pressure medicines", "Generic", "Lower blood pressure", "evidence.html#ev-sprint-mind", "Evidence", "https://doi.org/10.1001/jama.2018.21442", "Results",
         "Intensive treatment reduced mild cognitive impairment in SPRINT MIND; not approved for dementia prevention."),
        ("Cholesterol-lowering medicines", "Generic", "Lower LDL cholesterol", "risk.html", "Risk factors", LANCET, "Lancet Commission",
         "High midlife LDL cholesterol is linked to about 7% of dementia; trial evidence for prevention is still limited."),
        ("Shingles vaccine", "Older live vaccine (Zostavax)", "Vaccine against herpes zoster", "evidence.html#ev-shingles", "Evidence", "https://www.sciencedaily.com/releases/2025/04/250402122149.htm", "Study",
         "About 20% fewer new dementia diagnoses in a Wales natural experiment; not a randomized trial."),
    ]),
]
body = head("Drugs", "Drugs and prevention",
    "No drug is approved to prevent Alzheimer’s disease. These are the medicines being tested before symptoms, those that failed, and existing medicines with prevention signals.") + "\n    <section>\n"
for g, items in DRUGS:
    rows, ids = [], []
    for name, co, typ, ih, il, eh, el, note in items:
        rows.append((f'<span class="dname">{name}</span><span class="maker">{co}</span>' + link_pair(ih, il, eh, el), typ, note))
        ids.append(slug("drug", name))
    body += f'    <div class="group">\n      <h2>{g}</h2>\n{table(g, ["Drug", "Type", "For prevention"], rows, ids=ids)}\n    </div>\n'
body += DISCLAIMER + "\n    </section>"
pages["drugs.html"] = body

# ---------- Resources ----------
res_rows = [
    (src("https://www.a4studydata.org/", "A4 / LEARN"), "Amyloid PET, MRI, plasma biomarkers and cognition in cognitively unimpaired older adults", "Data use agreement"),
    (src("https://adni.loni.usc.edu/", "ADNI"), "Repeated imaging, fluid biomarkers and cognition from normal ageing to dementia", "Data use agreement"),
    (src("https://naccdata.org/", "NACC"), "Clinical follow-up and neuropathology from US Alzheimer’s Disease Research Centers", "Online request"),
    (src("https://www.ukbiobank.ac.uk/", "UK Biobank"), "About 500,000 adults with lifestyle, genetics, proteomics and linked health records", "Project application"),
    (src("https://www.researchallofus.org/", "All of Us"), "Genomes, health records and wearables in a diverse US cohort", "Registration and training"),
    (src("https://www.alzheimersdata.org/ad-workbench", "AD Workbench"), "Hundreds of datasets with a free secure cloud workspace", "Per-dataset rules"),
]
pages["resources.html"] = head("Resources", "Data for prevention research",
    "Cohorts that follow people before symptoms, or that link risk factors to long-term outcomes.") + f"""
    <section>
{table("Data resources", ["Resource", "What it offers", "Access"], res_rows)}
      <p class="note">For APOE-specific data sources, see {src("https://apoe4.science/resources.html", "apoe4.science Resources")}.</p>
    </section>"""


# ---------- Papers ----------
PAPERS = [
    ("Risk factors", [
        ("Livingston G, et al. Dementia prevention, intervention, and care: 2024 report of the Lancet standing Commission. <i>Lancet</i> 2024.", "The 14 modifiable risk factors and the 45% estimate.", LANCET),
    ]),
    ("Lifestyle and medical trials", [
        ("Ngandu T, et al. A 2 year multidomain intervention of diet, exercise, cognitive training, and vascular risk monitoring versus control to prevent cognitive decline in at-risk elderly people (FINGER): a randomised controlled trial. <i>Lancet</i> 2015.", "First large trial to show a multidomain lifestyle program helps cognition.", "https://doi.org/10.1016/S0140-6736(15)60461-5"),
        ("SPRINT MIND Investigators (Williamson JD, et al.). Effect of intensive vs standard blood pressure control on probable dementia. <i>JAMA</i> 2019.", "Intensive blood pressure control reduced mild cognitive impairment.", "https://doi.org/10.1001/jama.2018.21442"),
        ("Lin FR, et al. Hearing intervention versus health education control to reduce cognitive decline in older adults with hearing loss in the USA (ACHIEVE). <i>Lancet</i> 2023.", "No overall effect; possible benefit in people at higher risk.", "https://doi.org/10.1016/S0140-6736(23)01406-X"),
        ("U.S. POINTER Study Group. Two-year results of the U.S. POINTER lifestyle trial. Published in <i>JAMA</i>, July 2025.", "Both programs improved cognition; the structured one more.", "https://alz.org/us-pointer/study-results"),
        ("Eyting M, et al. A natural experiment on the effect of herpes zoster vaccination on dementia. <i>Nature</i> 2025.", "Shingles vaccination linked to fewer new dementia diagnoses in Wales.", "https://flex.uni-frankfurt.de/?p=3429"),
    ]),
    ("Drug prevention trials", [
        ("Sperling RA, et al. Trial of solanezumab in preclinical Alzheimer’s disease. <i>New England Journal of Medicine</i> 2023.", "The A4 Study: no slowing of decline.", "https://doi.org/10.1056/NEJMoa2305032"),
        ("Donanemab in preclinical Alzheimer’s disease: screening and baseline data from TRAILBLAZER-ALZ 3. 2025.", "Who is enrolled in the largest ongoing prevention trial.", "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12439032/"),
    ]),
]
pages["papers.html"] = head("Papers", "Key papers on prevention", "The studies behind this site, grouped by topic.") + "\n    <section>\n" + "".join(
    f'    <div class="group">\n      <h2>{g}</h2>\n      <ul class="refs">\n' + "".join(f'        <li><a href="{u}">{c}</a><p class="why">{w}</p></li>\n' for c, w, u in items) + "      </ul>\n    </div>\n"
    for g, items in PAPERS) + "    </section>"

# ---------- About ----------
pages["about.html"] = head("About", "About this site",
    "What this resource is, who maintains it, and how information is chosen.") + f"""
    <section>
      <div class="prose">
        <p>This site is maintained by Mahdi Moqri, PhD, in a personal capacity. It is not an official resource of any employer or institution, and it is not medical advice.</p>
        <p>Every figure links to its source, preferring peer-reviewed papers, trial registries and official reports. Trial results are shown as reported, and observational findings are labelled as such.</p>
        <p>It is a sister site to {src("https://apoe4.science", "apoe4.science")}, which focuses on people with two copies of APOE4.</p>
      </div>
    </section>"""

css += """
.geno small{line-height:1.5;max-width:34ch}
:root{--stop:#b0234f}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--stop:#ec6b93}}
:root[data-theme="dark"]{--stop:#ec6b93}
.pill.stop{color:var(--stop)}
.dname{font-weight:600;display:block}
.maker{display:block;font-weight:400;font-size:13px;color:var(--muted);margin-top:2px}
.xlinks{display:flex;flex-wrap:wrap;gap:4px 12px;margin-top:6px;font-size:13px;font-weight:400}
.xlinks a{white-space:nowrap}
a.lnk-int{color:var(--e4);text-decoration:none;border-bottom:1px solid currentColor}
a.lnk-ext{color:var(--muted);text-decoration:underline dotted;text-underline-offset:3px}
a.pill-link{text-decoration:none}
table.data tr[id]{scroll-margin-top:24px}
table.data tr:target td{background:var(--e4-soft)}
"""
OUT.joinpath("style.css").write_text(css)
for fname, label, title in PAGES:
    OUT.joinpath(fname).write_text(new_tabs(shell(fname, title, pages[fname])))
OUT.joinpath(".nojekyll").write_text("")
OUT.joinpath("favicon.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" fill="#1f6f54"/><text x="32" y="45" text-anchor="middle" font-family="Georgia, serif" font-size="38" font-weight="600" fill="#ffffff">A</text></svg>\n')
BASE = SITE_URL
OUT.joinpath("CNAME").write_text("alzprevent.org\n")
OUT.joinpath("robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {BASE}sitemap.xml\n")
OUT.joinpath("sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>{BASE}{'' if f == 'index.html' else f}</loc></url>\n" for f, _, _ in PAGES) + "</urlset>\n")
OUT.joinpath("404.html").write_text(new_tabs(shell("404.html", "Page not found", head("Page not found", "This page doesn’t exist", "It may have moved.") + '\n    <section><div class="prose"><p>Go to the <a href="index.html">home page</a>.</p></div></section>')))
print("built", len(PAGES), "pages")
