import requests
import time
import json
from tqdm import tqdm

# 🔢 List of PubChem Compound IDs to fetch
compound_cids = [2244, 702, 887, 6334]  # Example: Aspirin, Benzene, etc.

# 📁 Where to save the results
output_file = "data/pubchem_spectra.json"
failed_file = "data/failed_compounds.txt"

# 🧪 What spectral types to look for
spectral_keywords = ["NMR", "IR", "Mass Spectrum", "UV"]

# 📦 Final data store
results = []
failed = []

# 🚀 Function to extract spectral data
def extract_spectra_from_sections(sections):
    spectra = []
    for section in sections:
        if "TOCHeading" in section:
            heading = section["TOCHeading"]
            if any(keyword in heading for keyword in spectral_keywords):
                spectra.append({
                    "type": heading,
                    "description": section.get("Description", ""),
                    "information": section.get("Information", [])
                })
        # Recurse through child sections
        if "Sections" in section:
            spectra += extract_spectra_from_sections(section["Sections"])
    return spectra

# 🛠 Main scraping loop
for cid in tqdm(compound_cids):
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/{cid}/JSON"
    try:
        res = requests.get(url, timeout=10)
        if res.status_code != 200:
            raise Exception(f"Status code {res.status_code}")
        data = res.json()
        record = data.get("Record", {})
        sections = record.get("Section", [])
        spectra = extract_spectra_from_sections(sections)
        if spectra:
            results.append({
                "cid": cid,
                "spectra": spectra
            })
        else:
            failed.append(cid)
    except Exception as e:
        failed.append(cid)
        print(f"[!] Failed CID {cid}: {e}")
    time.sleep(0.5)  # ⏱️ Avoid hammering PubChem

# 💾 Save results
with open(output_file, "w") as f:
    json.dump(results, f, indent=2)

with open(failed_file, "w") as f:
    for cid in failed:
        f.write(str(cid) + "\n")

print(f"\n✅ Done. {len(results)} compounds with spectra saved to {output_file}")
print(f"❌ {len(failed)} failed compounds saved to {failed_file}")
