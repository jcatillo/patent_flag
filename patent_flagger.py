import argparse
import time
from pathlib import Path
from typing import List, Tuple, Optional, Dict, Any

import pandas as pd
import requests

PUBCHEM_PUG_REST = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"
PUBCHEM_PUG_VIEW = "https://pubchem.ncbi.nlm.nih.gov/rest/pug_view"

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
    """Queries PUG-View index to check if 'patents' appears in any TOC heading."""
    url = f"{PUBCHEM_PUG_VIEW}/index/compound/{cid}/JSON"
    try:
        r = session.get(url, timeout=10)
        if r.status_code != 200: 
            return False
        
        sections = r.json().get("Record", {}).get("Section", [])
        headings = []
        for sec in sections:
            headings.extend(_collect_toc_headings(sec))

        print(f"  TOC Headings for CID {cid}: {headings}")
        return any("patents" in h.lower() for h in headings)
    except:
        return False

def get_canonical_smiles(session: requests.Session, cid: int) -> Optional[str]:
    """Retrieves the standardized SMILES for a given CID."""
    url = f"{PUBCHEM_PUG_REST}/compound/cid/{cid}/property/CanonicalSMILES/JSON"
    try:
        r = session.get(url, timeout=10)

        returned_smile =  r.json()['PropertyTable']['Properties'][0]['ConnectivitySMILES']

        print(f"Canonical SMILES for CID {cid}: {returned_smile}")
        return returned_smile
    except:
        return None

def process_molecules(input_path: str, output_path: str, threshold: int):
    p = Path(input_path)
    if not p.exists():
        print(f"Error: {input_path} not found.")
        return

    lines = [l.strip() for l in p.read_text().splitlines() if l.strip() and not l.startswith(('#', '//'))]
    session = requests.Session()
    results = []

    for line in lines:
        parts = line.split()
        input_smi = parts[0]
        
        # 1. PubChem Similarity Search
        search_url = f"{PUBCHEM_PUG_REST}/compound/fastsimilarity_2d/smiles/cids/JSON"
        try:
            r = session.post(search_url, data={'smiles': input_smi, 'Threshold': threshold, 'MaxRecords': 50}, timeout=15)
            cids = r.json().get('IdentifierList', {}).get('CID', [])
        except:
            cids = []

        is_patented = False
        patented_smi = "None"
        found_cid = None

        print(f"Processing SMILES NO. {lines.index(line) + 1}: {input_smi}")

        # 2. Check each CID for Patent TOC headings
        for cid in cids:
            if check_patent_in_toc(session, cid):
                found_cid = cid
                is_patented = True
                patented_smi = get_canonical_smiles(session, cid)
                break
            time.sleep(0.1) 

        results.append({
            "input_smile": input_smi,
            "is_patented": is_patented,
            "patent_cid": found_cid,
            "similar_smile_patent": patented_smi
        })

    pd.DataFrame(results).to_csv(output_path, index=False)
    print(f"Results successfully saved to {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Synthesized PubChem Patent TOC Checker")
    parser.add_argument("-i", "--input", required=True, help="Input .txt file (SMILES [Name])")
    parser.add_argument("-o", "--output", default="patent_results.csv", help="Output .csv file")
    parser.add_argument("-t", "--threshold", type=int, default=95, help="PubChem Tanimoto threshold (0-100)")
    
    args = parser.parse_args()
    process_molecules(args.input, args.output, args.threshold)