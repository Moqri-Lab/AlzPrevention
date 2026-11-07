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
    ("trials.html", "Prevention trials", "Drug prevention trials"),
    ("resources.html", "Resources", "Data resources"),
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
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{doc_title}</title>
<meta name="description" content="{DESC}">
<meta property="og:title" content="{doc_title}">
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
    <a class="mark" href="index.html">alzheimer’s<span>.</span>prevention</a>
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


def table(label, cols, rows):
    th = "".join(f"<th>{c}</th>" for c in cols)
    trs = "\n".join(
        "            <tr>" + "".join(f'<td data-label="{c}"><span>{v}</span></td>' for c, v in zip(cols, r)) + "</tr>"
        for r in rows)
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
    ("about.html", "About", "Who maintains this site and how sources are chosen."),
]
pages["index.html"] = f"""    <div class="hero">
      <div>
        <p class="label">A community resource</p>
        <h1 style="margin-top:14px">Nearly half of dementia may be <em>preventable</em> or delayable.</h1>
        <p class="lede">The evidence on preventing Alzheimer’s disease, from everyday risk factors to drug trials in people who have no symptoms yet, with every figure linked to its source.</p>
      </div>
      <div class="geno" aria-label="45 percent">45%<small>Share of dementia linked to 14 modifiable risk factors (Lancet Commission 2024)</small></div>
    </div>
    <section>
      <div class="cards">
""" + "\n".join(f'        <a class="card" href="{f}"><h3>{t}</h3><p>{d}</p></a>' for f, t, d in cards) + """
      </div>
    </section>"""

# ---------- Risk factors ----------
risk_rows = [
    ("Early life", "Less education"),
    ("Midlife", "Hearing loss"), ("Midlife", "High LDL cholesterol"), ("Midlife", "Depression"),
    ("Midlife", "Traumatic brain injury"), ("Midlife", "Physical inactivity"), ("Midlife", "Diabetes"),
    ("Midlife", "Smoking"), ("Midlife", "High blood pressure"), ("Midlife", "Obesity"),
    ("Midlife", "Excessive alcohol"),
    ("Later life", "Social isolation"), ("Later life", "Air pollution"), ("Later life", "Untreated vision loss"),
]
pages["risk.html"] = head("Risk factors", "Fourteen risk factors you can change",
    "The 2024 Lancet Commission estimated that about 45% of dementia worldwide is linked to 14 modifiable risk factors across the life course.") + f"""
    <section>
{table("Modifiable risk factors", ["Life stage", "Risk factor"], risk_rows)}
      <div class="prose" style="margin-top:24px">
        <p>Two factors were new in 2024: high LDL cholesterol in midlife, estimated to account for about 7% of dementia, and untreated vision loss in later life, about 2%.{cite(LANCET)}</p>
        <p>The 45% estimate assumes each factor is causal and could be removed entirely, so it shows the size of the opportunity rather than a promise for any one person.</p>
        <p>Genes matter too. Two copies of APOE4 raise risk far more than any single factor here; see the sister site {src("https://apoe4.science", "apoe4.science")}.</p>
      </div>
{DISCLAIMER}
    </section>"""

# ---------- Evidence ----------
ev_rows = [
    (src("https://doi.org/10.1016/S0140-6736(15)60461-5", "FINGER") + " (Finland)", "Two-year multidomain lifestyle program: diet, exercise, cognitive training, vascular risk management", "1,260 at-risk adults aged 60–77", pill("done", "Benefit") + " Better overall cognition than general health advice."),
    (src("https://alz.org/us-pointer/study-results", "U.S. POINTER"), "Two-year structured versus self-guided lifestyle program", "2,111 sedentary adults aged 60–79 at risk", pill("done", "Benefit") + " Both groups improved; the structured program improved global cognition more." + cite("https://practicalneurology.com/news/us-pointer-study-results-a-structured-lifestyle-intervention-improved-cognition-in-older-adults/2475903/")),
    (src("https://doi.org/10.1001/jama.2018.21442", "SPRINT MIND"), "Intensive blood pressure control (systolic under 120) versus standard (under 140)", "Adults with high blood pressure", pill("done", "Partial benefit") + " Fewer cases of mild cognitive impairment; the drop in dementia was not statistically significant."),
    (src("https://doi.org/10.1016/S0140-6736(23)01406-X", "ACHIEVE"), "Hearing aids and counselling versus health education", "Older adults with hearing loss", pill("stop", "No overall benefit") + " No slowing of cognitive decline overall; a benefit was seen in a higher-risk subgroup."),
    (src("https://www.sciencedaily.com/releases/2025/04/250402122149.htm", "Shingles vaccine, Wales"), "Natural experiment: vaccine eligibility set by date of birth", "Older adults born either side of 2 September 1933", pill("done", "Signal") + " Vaccination reduced new dementia diagnoses by about 3.5 percentage points over seven years (about 20% relative). Older live vaccine; not a randomized trial." + cite("https://www.news-medical.net/news/20250408/Shingles-vaccination-associated-with-reduction-in-probability-of-new-dementia-diagnosis.aspx")),
]
pages["evidence.html"] = head("What works", "Evidence from trials and natural experiments",
    "Randomized trials of lifestyle and medical approaches, and the strongest natural experiments, on preventing cognitive decline and dementia.") + f"""
    <section>
{table("Prevention evidence", ["Study", "Intervention", "Who", "Result"], ev_rows)}
      <p class="note">Benefits so far are on cognitive test scores or milder outcomes; no lifestyle trial has yet shown fewer dementia diagnoses as its main result.</p>
{DISCLAIMER}
    </section>"""

# ---------- Trials ----------
tr_rows = [
    (src("https://clinicaltrials.gov/study/NCT05026866", "TRAILBLAZER-ALZ 3"), "Donanemab", "About 3,000 cognitively unimpaired adults with Alzheimer’s pathology", pill("run", "Fully enrolled") + " Primary completion expected October 2027."),
    (src("https://clinicaltrials.gov/study/NCT04468659", "AHEAD 3-45"), "Lecanemab", "About 1,400 adults with amyloid but no symptoms", pill("run", "Fully enrolled") + " Primary completion expected December 2028."),
    (src("https://clinicaltrials.gov/study/NCT07399171", "HT-4253"), "Oral LRRK2 inhibitor", "112 biomarker-positive APOE4 carriers in Abu Dhabi", pill("recruit", "Recruiting") + " 48-week Phase 2a, started May 2026."),
    (src("https://clinicaltrials.gov/study/NCT02008357", "A4 Study"), "Solanezumab", "More than 1,100 adults with amyloid but no symptoms", pill("stop", "No benefit") + " Did not slow cognitive decline." + cite("https://doi.org/10.1056/NEJMoa2305032")),
    ("API Colombia", "Crenezumab", "252 members of a Colombian family with an early-onset PSEN1 mutation", pill("stop", "No significant benefit") + " Numerical trends favoured the drug, none significant (2022)." + cite("https://www.businesswire.com/news/home/20220616005106/en/Genentech-Provides-Update-on-Alzheimers-Prevention-Initiative-Study-Evaluating-Crenezumab-in-Autosomal-Dominant-Alzheimers-Disease")),
    (src("https://clinicaltrials.gov/study/NCT02565511", "Generation Study 1"), "Umibecestat or CAD106", "Cognitively unimpaired APOE4 homozygotes aged 60–75", pill("stop", "Stopped 2019") + " Umibecestat worsened cognition slightly; program ended."),
]
pages["trials.html"] = head("Prevention trials", "Drug trials before symptoms",
    "Trials that treat people who have Alzheimer’s changes, or very high genetic risk, before memory problems begin. Ongoing trials first.") + f"""
    <section>
{table("Prevention drug trials", ["Trial", "Drug", "Who", "Status and result"], tr_rows)}
      <p class="note">Status changes often; each trial name links to its ClinicalTrials.gov record. To volunteer, search {src("https://clinicaltrials.gov/search?cond=Alzheimer+Disease&term=prevention", "ClinicalTrials.gov")} or use the Alzheimer’s Association’s {src("https://www.alz.org/alzheimers-dementia/research_progress/clinical-trials/trialmatch", "TrialMatch")}.</p>
    </section>"""

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
"""
OUT.joinpath("style.css").write_text(css)
for fname, label, title in PAGES:
    OUT.joinpath(fname).write_text(shell(fname, title, pages[fname]))
OUT.joinpath(".nojekyll").write_text("")
print("built", len(PAGES), "pages")
