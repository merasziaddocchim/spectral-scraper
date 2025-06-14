import pubchempy as pcp
import pandas as pd
import os
from tqdm import tqdm

SAVE_PATH = "../data/raw/uvvis/"
COMPOUND_CIDS = [2244, 702, 887, 6334]  # Ethanol, Acetone, Methanol, Isopropanol

def fetch_pubchem_uvvis():
    os.makedirs(SAVE_PATH, exist_ok=True)
    
    for cid in tqdm(COMPOUND_CIDS):
        try:
            # Fetch compound data
            compound = pcp.Compound.from_cid(cid)
            
            # Extract UV-Vis spectra
            spectra = compound.spectra
            uv_spectra = [s for s in spectra if s.get('spectrum_type') == 'UV-Visible']
            
            if not uv_spectra:
                continue
                
            # Process best spectrum
            best_spectrum = max(uv_spectra, key=lambda x: len(x['points']))
            points = best_spectrum['points']
            
            # Save data
            df = pd.DataFrame(points, columns=['wavelength', 'absorbance'])
            df.to_csv(f"{SAVE_PATH}{compound.iupac_name.replace(' ', '_')}_uv.csv", index=False)
            
        except Exception as e:
            print(f"Failed CID {cid}: {str(e)}")
            with open("../data/failed_compounds.txt", "a") as err_file:
                err_file.write(f"PubChem,{cid}\n")

if __name__ == "__main__":
    fetch_pubchem_uvvis()
