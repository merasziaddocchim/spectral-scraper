import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from tqdm import tqdm

BASE_URL = "https://nmrshiftdb.nmr.uni-koeln.de"
SAVE_PATH = "../data/raw/nmr/"

def fetch_nmr_data():
    os.makedirs(SAVE_PATH, exist_ok=True)
    index_url = f"{BASE_URL}/spectra"
    
    # Fetch compound list
    response = requests.get(index_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    compounds = []
    for row in soup.select('table tr')[1:]:  # Skip header
        cols = row.find_all('td')
        if len(cols) > 1:
            compound_id = cols[0].text.strip()
            name = cols[1].text.strip()
            compounds.append((compound_id, name))
    
    # Fetch NMR data for each compound
    for cid, name in tqdm(compounds[:50]):  # First 50 for testing
        try:
            nmr_url = f"{BASE_URL}/spectrum/{cid}"
            nmr_response = requests.get(nmr_url)
            
            # Save raw data
            with open(f"{SAVE_PATH}{cid}_{name.replace(' ', '_')}.html", 'w') as f:
                f.write(nmr_response.text)
            
            # Extract peaks from HTML
            nmr_soup = BeautifulSoup(nmr_response.text, 'html.parser')
            peak_table = nmr_soup.find('table', {'id': 'peaks'})
            
            peaks = []
            for row in peak_table.find_all('tr')[1:]:
                cols = row.find_all('td')
                if len(cols) >= 3:
                    shift = cols[0].text.strip()
                    intensity = cols[1].text.strip()
                    assignment = cols[2].text.strip()
                    peaks.append([shift, intensity, assignment])
            
            # Save as CSV
            df = pd.DataFrame(peaks, columns=['shift', 'intensity', 'assignment'])
            df.to_csv(f"{SAVE_PATH}{cid}_peaks.csv", index=False)
            
        except Exception as e:
            print(f"Failed {cid}: {str(e)}")
            with open("../data/failed_compounds.txt", "a") as err_file:
                err_file.write(f"NMRShiftDB,{cid}\n")

if __name__ == "__main__":
    fetch_nmr_data()
