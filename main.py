import os
import glob
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors

def process_all_data():
    # Process NMR data
    nmr_files = glob.glob("data/raw/nmr/*_peaks.csv")
    nmr_data = []
    for file in nmr_files:
        cid = os.path.basename(file).split('_')[0]
        df = pd.read_csv(file)
        nmr_data.append({
            'cid': cid,
            'nmr_peaks': df.to_dict(orient='records')
        })
    
    # Process IR data
    ir_files = glob.glob("data/raw/ir/*.csv")
    ir_data = []
    for file in ir_files:
        compound_name = os.path.basename(file).split('_ir')[0]
        df = pd.read_csv(file)
        ir_data.append({
            'compound': compound_name,
            'ir_spectrum': df.to_dict(orient='records')
        })
    
    # Create unified dataset
    combined = []
    for nmr in nmr_data:
        # Find matching IR data
        match = next((ir for ir in ir_data if ir['compound'] in nmr['cid']), None)
        if match:
            combined.append({**nmr, **match})
    
    # Add molecular properties
    for entry in combined:
        try:
            mol = Chem.MolFromSmiles(pcp.Compound.from_cid(entry['cid']).canonical_smiles)
            entry['molecular_weight'] = Descriptors.MolWt(mol)
            entry['formula'] = Chem.rdMolDescriptors.CalcMolFormula(mol)
        except:
            continue
    
    # Save final dataset
    final_df = pd.DataFrame(combined)
    final_df.to_parquet("data/processed/spectral_dataset.parquet", index=False)

if __name__ == "__main__":
    process_all_data()
