#!/usr/bin/env python3
"""
Fix missing university names, countries, and add email placeholders.
Run after every discover batch.
"""

import json
import requests
import time
from dotenv import load_dotenv
import os

load_dotenv(override=True)

API_KEY = os.getenv("SEMANTIC_SCHOLAR_API_KEY")
headers = {
    "User-Agent": "ProfessorOutreachSystem/1.0",
    "x-api-key": API_KEY
}

# Country detection from affiliation text
COUNTRY_KEYWORDS = {
    "USA": ["mit", "stanford", "carnegie mellon", "berkeley", "harvard", "princeton",
            "columbia", "cornell", "nyu", "new york university", "washington", "michigan",
            "ucla", "ucsd", "illinois", "georgia tech", "texas", "penn", "johns hopkins",
            "duke", "wisconsin", "maryland", "brown", "purdue", "minnesota", "ohio state",
            "ucsb", "uci", "rice", "vanderbilt", "colorado", "stony brook", "pittsburgh",
            "rutgers", "penn state", "notre dame", "usc", "northeastern", "boston university",
            "arizona", "virginia", "florida", "michigan state", "indiana", "rochester",
            "buffalo", "suny", "cleveland", "ttic", "riken", "samaya", "center for ai safety",
            "united states", "usa", "u.s."],
    "Germany": ["munich", "tum", "rwth", "karlsruhe", "kit", "freiburg", "tubingen",
                "saarland", "berlin", "heidelberg", "bonn", "hamburg", "darmstadt",
                "erlangen", "stuttgart", "cologne", "gottingen", "munster",
                "ludwig-maximilians", "lmu", "germany", "deutschland"],
    "UK": ["oxford", "cambridge", "imperial", "ucl", "university college london",
           "edinburgh", "manchester", "bristol", "warwick", "glasgow", "birmingham",
           "sheffield", "southampton", "nottingham", "leeds", "king's college",
           "bath", "durham", "st andrews", "united kingdom", "england", "scotland"],
    "Canada": ["toronto", "mcgill", "waterloo", "mila", "ubc", "alberta",
               "simon fraser", "montreal", "ottawa", "york university", "dalhousie",
               "calgary", "queen's", "polytechnique", "canada"],
    "Japan": ["tokyo", "kyoto", "osaka", "titech", "tohoku", "nagoya", "kyushu",
              "hokkaido", "keio", "waseda", "naist", "jaist", "japan"],
    "China": ["tsinghua", "peking", "zhejiang", "shanghai jiao tong", "fudan",
              "ustc", "nanjing", "wuhan", "sun yat-sen", "harbin", "central south",
              "tongji", "beihang", "xi'an jiaotong", "beijing institute", "renmin",
              "jilin", "china"],
    "Singapore": ["national university of singapore", "nus", "ntu", "nanyang",
                  "singapore management", "singapore"],
    "South Korea": ["seoul national", "kaist", "postech", "yonsei", "korea university",
                    "sungkyunkwan", "hanyang", "korea"],
    "Australia": ["australian national", "melbourne", "sydney", "queensland",
                  "monash", "unsw", "new south wales", "adelaide", "western australia",
                  "macquarie", "deakin", "australia"],
    "Switzerland": ["eth zurich", "epfl", "zurich", "basel", "bern", "switzerland"],
    "Netherlands": ["amsterdam", "delft", "eindhoven", "utrecht", "leiden",
                    "radboud", "netherlands"],
    "France": ["inria", "polytechnique", "sorbonne", "paris", "centralesupelec",
               "grenoble", "bordeaux", "france"],
    "Italy": ["politecnico di milano", "politecnico di torino", "sapienza", "bologna",
              "padova", "trento", "italy"],
    "Sweden": ["kth", "chalmers", "lund", "uppsala", "linkoping", "sweden"],
    "Turkey": ["metu", "bilkent", "bogazici", "istanbul technical", "koc university",
               "sabanci", "hacettepe", "turkey"],
    "Hungary": ["budapest university", "eotvos", "debrecen", "pecs", "hungary"],
    "Austria": ["vienna university of technology", "tu wien", "graz", "linz", "austria"],
    "Belgium": ["ku leuven", "ghent", "vrije universiteit brussel", "belgium"],
    "Denmark": ["technical university of denmark", "dtu", "copenhagen", "aarhus", "denmark"],
    "Finland": ["aalto", "helsinki", "oulu", "finland"],
    "Norway": ["ntnu", "oslo", "norway"],
    "Poland": ["warsaw university of technology", "agh", "jagiellonian", "poland"],
    "Czech Republic": ["czech technical", "charles university", "brno", "czech"],
    "Portugal": ["instituto superior tecnico", "porto", "lisbon", "portugal"],
    "Spain": ["upc", "autonoma de madrid", "barcelona", "spain"],
    "Taiwan": ["national taiwan", "tsing hua", "chiao tung", "taiwan"],
    "Hong Kong": ["hong kong university of science", "hkust", "university of hong kong",
                  "chinese university of hong kong", "hong kong polytechnic", "hong kong"],
    "New Zealand": ["auckland", "victoria university of wellington", "new zealand"],
}

def detect_country(aff_text):
    aff_lower = aff_text.lower()
    for country, keywords in COUNTRY_KEYWORDS.items():
        if any(kw in aff_lower for kw in keywords):
            return country
    return "Unknown"

def get_email_pattern(name, affiliation):
    """Generate likely email based on name + institution patterns."""
    parts = name.lower().split()
    if len(parts) < 2:
        return None
    first = parts[0]
    last = parts[-1]
    aff_lower = affiliation.lower()

    # Common patterns by institution
    if "stanford" in aff_lower:
        return f"{first[0]}{last}@stanford.edu or {first}.{last}@stanford.edu"
    if "mit" in aff_lower:
        return f"{first[0]}{last}@mit.edu or {first}.{last}@mit.edu"
    if "carnegie mellon" in aff_lower or "cmu" in aff_lower:
        return f"{first[0]}{last}@cs.cmu.edu or {first}.{last}@andrew.cmu.edu"
    if "oxford" in aff_lower:
        return f"{first}.{last}@cs.ox.ac.uk"
    if "cambridge" in aff_lower:
        return f"{first}.{last}@cl.cam.ac.uk"
    if "edinburgh" in aff_lower:
        return f"{first}.{last}@ed.ac.uk"
    if "ucl" in aff_lower or "university college london" in aff_lower:
        return f"{first}.{last}@ucl.ac.uk"
    if "toronto" in aff_lower:
        return f"{first}.{last}@cs.toronto.edu"
    if "waterloo" in aff_lower:
        return f"{first[0]}{last}@uwaterloo.ca"
    if "tum" in aff_lower or "munich" in aff_lower:
        return f"{first}.{last}@tum.de"
    if "eth" in aff_lower:
        return f"{first}.{last}@ethz.ch"
    if "epfl" in aff_lower:
        return f"{first}.{last}@epfl.ch"
    if "nus" in aff_lower or "national university of singapore" in aff_lower:
        return f"{first}.{last}@comp.nus.edu.sg"
    if "ntu" in aff_lower or "nanyang" in aff_lower:
        return f"{first}.{last}@ntu.edu.sg"
    return None

with open("targets.json") as f:
    data = json.load(f)

profs = data["professors"]
print(f"Fixing {len(profs)} professors...\n")

fixed_count = 0
for i, prof in enumerate(profs, 1):
    author_id = prof.get("authorId") or prof.get("author_id")
    if not author_id:
        continue

    print(f"[{i}/{len(profs)}] {prof['name']}...", end=" ", flush=True)

    try:
        r = requests.get(
            f"https://api.semanticscholar.org/graph/v1/author/{author_id}",
            params={"fields": "name,affiliations,externalIds,homepage"},
            headers=headers,
            timeout=15
        )
        time.sleep(2)

        if r.status_code == 429:
            print("rate limited, waiting 15s...")
            time.sleep(15)
            r = requests.get(
                f"https://api.semanticscholar.org/graph/v1/author/{author_id}",
                params={"fields": "name,affiliations,externalIds,homepage"},
                headers=headers,
                timeout=15
            )
            time.sleep(2)

        if r.status_code != 200:
            print(f"skip ({r.status_code})")
            continue

        author_data = r.json()
        affiliations = author_data.get("affiliations", [])

        if affiliations:
            aff = affiliations[-1]
            uni_name = aff.get("name", "") if isinstance(aff, dict) else str(aff)
            aff_text = " ".join(
                (a.get("name", "") if isinstance(a, dict) else str(a))
                for a in affiliations
            )
            country = detect_country(aff_text)

            prof["university"] = uni_name
            prof["institution"] = uni_name
            prof["affiliations"] = affiliations
            prof["country"] = country

            # Add email pattern hint if no email set
            if not prof.get("email") or "[FILL" in prof.get("email", ""):
                pattern = get_email_pattern(prof["name"], aff_text)
                if pattern:
                    prof["email"] = f"[LOOKUP: {pattern}]"

            print(f"✓ {uni_name} | {country}")
            fixed_count += 1
        else:
            print("no affiliation")

    except Exception as e:
        print(f"error: {e}")

with open("targets.json", "w") as f:
    json.dump(data, f, indent=2)

print(f"\n✓ Fixed {fixed_count} professors")
print("✓ Saved targets.json")
print("\nEmail patterns added — search each professor's faculty page to confirm exact email.")
