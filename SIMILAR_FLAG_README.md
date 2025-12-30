# Similar Flag

Flags molecular compounds (SMILES) by finding similar patented compounds in PubChem.

## Install

```bash
pip install pandas requests
```

## Usage

```bash
python similar_flag.py -i input.txt -o output.csv -t 95
```

### Arguments

- `-i, --input` (required): Input file with SMILES strings (one per line)
- `-o, --output` (default: `patent_results.csv`): Output CSV file
- `-t, --threshold` (default: `95`): Similarity threshold (0-100)

## Examples

```bash
# Basic
python similar_flag.py -i molecules.txt

# Custom output
python similar_flag.py -i molecules.txt -o results.csv

# Lower threshold (wider search)
python similar_flag.py -i molecules.txt -t 85
```

## Input Format

One SMILES per line. Comments and empty lines are skipped:

```
CCO
c1ccccc1O
# Comment line
CC(C)Cc1ccc(cc1)C
```

## Output Format

CSV with columns:

- `input_smile`: Input SMILES string
- `is_patented`: True if similar patented compound found
- `patent_cid`: PubChem ID of matched patent compound
- `similar_smile_patent`: Canonical SMILES of patent match

## How It Works

1. Searches PubChem for 2D-similar compounds
2. Checks results for patent information
3. Returns first patented match
4. Includes 0.2s delays between requests
