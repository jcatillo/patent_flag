import argparse
import time
from pathlib import Path
from typing import List, Tuple, Optional, Dict, Any

import pandas as pd
import requests
from rdkit import Chem, DataStructs
from rdkit.Chem import AllChem

PUBCHEM_PUG_REST = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"
PUBCHEM_PUG_VIEW = "https://pubchem.ncbi.nlm.nih.gov/rest/pug_view"

from rdkit import Chem, DataStructs
from rdkit.Chem import rdFingerprintGenerator

def get_rdkit_similarity(s1: str, s2: str) -> float:
    print(f"Smiles 1: {s1}, Smiles 2: {s2}")

    if not s1 or not s2:
        return 0.0
    
    m1, m2 = Chem.MolFromSmiles(s1), Chem.MolFromSmiles(s2)
    if not m1 or not m2: 
        return 0.0

    # Initialize the Morgan Generator
    # Radius 2 corresponds to ECFP4
    gen = rdFingerprintGenerator.GetMorganGenerator(radius=2, fpSize=2048)

    # Generate Fingerprints as Bit Vectors
    fp1 = gen.GetFingerprint(m1)
    fp2 = gen.GetFingerprint(m2)

    similarity = float(DataStructs.TanimotoSimilarity(fp1, fp2))
    print(f"  RDKit Tanimoto Similarity: {similarity:.4f}")

    return similarity

def _collect_toc_headings(section: Dict[str, Any]) -> List[str]:
    """Recursively crawls PUG-View sections to find all TOCHeadings."""
    out = []
    if toc := section.get("TOCHeading"):
        out.append(toc)
    for sub in section.get("Section", []):
        if isinstance(sub, dict):
            out.extend(_collect_toc_headings(sub))
    return out

def check_patent_in_toc(session: requests.Session, cid: int) -> bool:
    """Queries PUG-View index to check if 'patent' appears in any TOC heading."""
    url = f"{PUBCHEM_PUG_VIEW}/index/compound/{cid}/JSON"
    try:
        r = session.get(url, timeout=10)
        if r.status_code != 200: 
            return False
        
        sections = r.json().get("Record", {}).get("Section", [])
        headings = []
        for sec in sections:
            headings.extend(_collect_toc_headings(sec))  # recursively collect all headings

        print(f"  TOC Headings for CID  {cid}: {headings}")  # shows all headings
        # Check if any heading contains the word "patent"
        return any("patents" in h.lower() for h in headings)
    except:
        return False


def get_canonical_smiles(session: requests.Session, cid: int) -> Optional[str]:
    """Retrieves the standardized SMILES for a given CID."""
    url = f"{PUBCHEM_PUG_REST}/compound/cid/{cid}/property/CanonicalSMILES/JSON"
    try:
        r = session.get(url, timeout=10)
        return r.json()['PropertyTable']['Properties'][0]['ConnectivitySMILES']
    except:
        return None

def process_molecules(input_path: str, output_path: str, threshold: int):
    p = Path(input_path)
    if not p.exists():
        print(f"Error: {input_path} not found.")
        return

    # Parse SMILES and names (assumes: SMILES [Name])
    lines = [l.strip() for l in p.read_text().splitlines() if l.strip() and not l.startswith(('#', '//'))]
    session = requests.Session()
    results = []

    for line in lines:
        parts = line.split()
        input_smi = parts[0]
        
        
        # 1. Similarity Search (Threshold-based)
        search_url = f"{PUBCHEM_PUG_REST}/compound/fastsimilarity_2d/smiles/cids/JSON"
        try:
            r = session.post(search_url, data={'smiles': input_smi, 'Threshold': threshold, 'MaxRecords': 50}, timeout=15)
            cids = r.json().get('IdentifierList', {}).get('CID', [])
        except:
            cids = []

        is_patented = False
        patented_smi = "None"
        found_cid = None

        # 2. Check each CID for Patent TOC headings
        for cid in cids:
            cid_to_smile = get_canonical_smiles(session, cid)

            score = get_rdkit_similarity(input_smi, cid_to_smile)


            if score * 100 < 80:
                continue 

            if check_patent_in_toc(session, cid):
                found_cid = cid
                is_patented = True
                patented_smi = get_canonical_smiles(session, cid)
                break
            time.sleep(0.2) 

        # 3. Final RDKit Score
        
        results.append({
            "input_smile": input_smi,
            "is_patented": is_patented,
            "patent_cid": found_cid,
            "similar_smile_patent": patented_smi,
            "exact_tanimoto": round(score, 4)
        })

    pd.DataFrame(results).to_csv(output_path, index=False)
    print(f"Results successfully saved to {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Synthesized PubChem Patent TOC Checker")
    parser.add_argument("-i", "--input", required=True, help="Input .txt file (SMILES [Name])")
    parser.add_argument("-o", "--output", default="patent_results.csv", help="Output .csv file")
    parser.add_argument("-t", "--threshold", type=int, default=85, help="Tanimoto threshold (0-100)")
    
    args = parser.parse_args()
    process_molecules(args.input, args.output, args.threshold)