import argparse
from rdkit import Chem
from rdkit.Chem.Scaffolds import MurckoScaffold

def extract_scaffolds(input_txt, output_txt):
    with open(input_txt, 'r') as f:
        smiles_list = [line.strip() for line in f.readlines()]

    lead_compounds = []

    for i, smi in enumerate(smiles_list):
        try:
            mol = Chem.MolFromSmiles(smi)
            if mol is None:
                lead_compounds.append("None")
                continue

            scaffold = MurckoScaffold.GetScaffoldForMol(mol)
            scaffold_smi = Chem.MolToSmiles(scaffold) if scaffold else "None"
            lead_compounds.append(scaffold_smi)

        except Exception:
            print(f"Row {i} failed")
            lead_compounds.append("None")

    with open(output_txt, 'w') as f:
        for scaffold_smi in lead_compounds:
            f.write(scaffold_smi + "\n")

def main():
    parser = argparse.ArgumentParser(
        description="Generate Murcko scaffolds from exact SMILES"
    )
    parser.add_argument("-i", "--input", required=True, help="Input TXT file")
    parser.add_argument("-o", "--output", required=True, help="Output TXT file")

    args = parser.parse_args()

    extract_scaffolds(
        input_txt=args.input,
        output_txt=args.output
    )

if __name__ == "__main__":
    main()
