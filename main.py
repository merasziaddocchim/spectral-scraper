from scrapers.pubchem_scraper import scrape_nmr_from_pubchem, scrape_ir_from_pubchem, scrape_uv_from_pubchem
import pandas as pd

cids = [2244, 1983, 3672]  # Add more later
nmr_all, ir_all, uv_all = [], [], []

for cid in cids:
    print(f"🔍 Scraping CID: {cid}")
    try:
        nmr, _ = scrape_nmr_from_pubchem(cid)
        ir, _ = scrape_ir_from_pubchem(cid)
        uv, _ = scrape_uv_from_pubchem(cid)

        nmr_all.extend(nmr)
        ir_all.extend(ir)
        uv_all.extend(uv)
    except Exception as e:
        print(f"⚠️ Error with CID {cid}: {e}")

# Save to CSV
pd.DataFrame(nmr_all).to_csv("data/nmr.csv", index=False)
pd.DataFrame(ir_all).to_csv("data/ir.csv", index=False)
pd.DataFrame(uv_all).to_csv("data/uv_vis.csv", index=False)
print("✅ Scraping complete. All data saved.")
