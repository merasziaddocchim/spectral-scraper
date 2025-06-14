import requests
from pyjcamp import jcamp_read
import pandas as pd
import os
import time
from tqdm import tqdm

SAVE_PATH = "../data/raw/ir/"
COMPOUNDS = ["methanol", "ethanol", "acetone", "benzene", "toluene", 
             "acetic acid", "water", "cyclohexane", "diethyl ether"]

def fetch_nist_ir_data():
    os.makedirs(SAVE_PATH, exist_ok=True)
    base_url = "https://webbook.nist.gov/cgi/cbook.cgi"
    
    for compound in tqdm(COMPOUNDS):
        try:
            # Search for compound
            params = {'Name': compound, 'Units': 'SI'}
            search_response = requests.get(base_url, params=params)
            
            # Extract first result ID
            soup = BeautifulSoup(search_response.text, 'html.parser')
            result_link = soup.find('a', string='IR Spectrum')
            if not result_link: 
                continue
                
            # Fetch JCAMP-DX data
            jcamp_url = result_link['href'].replace('#', '')
            jcamp_response = requests.get(f"https://webbook.nist.gov{jcamp_url}")
            
            # Parse with pyjcamp
            jcamp_data = jcamp_read(jcamp_response.text)
            
            # Save data
            df = pd.DataFrame({
                'wavenumber': jcamp_data['x'],
                'transmittance': jcamp_data['y']
            })
            df.to_csv(f"{SAVE_PATH}{compound.replace(' ', '_')}_ir.csv", index=False)
            
            time.sleep(2)  # Be polite to NIST servers
            
        except Exception as e:
            print(f"Failed {compound}: {str(e)}")
            with open("../data/failed_compounds.txt", "a") as err_file:
                err_file.write(f"NIST,{compound}\n")

if __name__ == "__main__":
    fetch_nist_ir_data()
