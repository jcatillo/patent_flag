# Patent Flag - Molecular Patent Analysis

Python toolkit for screening compounds against PubChem patents using scaffold extraction, similarity search, and substructure matching.

## Table of Contents

- [Quick Start](#quick-start)
- [Installation](#installation)
- [Scripts](#scripts)
- [Usage Examples](#usage-examples)
- [Output Format](#output-format)
- [File Structure](#file-structure)

---

## Quick Start

```bash
# 1. Extract scaffolds
python scaffold.py -i exact/molecules.txt -o scaffold/molecules.txt

# 2. Search similar compounds for patents
python similar_flag.py -i exact/molecules.txt -o similarity/results.csv -t 95

# 3. Search substructure matches for patents
python substructure_flag.py -i exact/molecules.txt -o substructure/results.csv
```

---

## Installation

```bash
pip install pandas requests rdkit matplotlib
```

---

## Scripts

| Script                 | Purpose                            | Command                                                  |
| ---------------------- | ---------------------------------- | -------------------------------------------------------- |
| `scaffold.py`          | Extract Bemis-Murcko scaffolds     | `python scaffold.py -i INPUT -o OUTPUT`                  |
| `similar_flag.py`      | Find 2D-similar patented compounds | `python similar_flag.py -i INPUT -o OUTPUT -t THRESHOLD` |
| `substructure_flag.py` | Find substructure-matching patents | `python substructure_flag.py -i INPUT -o OUTPUT`         |

---

## Usage Examples

### Scaffold Extraction

```bash
python scaffold.py -i exact/antifungal.txt -o scaffold/antifungal.txt
```

### Similarity Search

```bash
# High threshold (strict matching)
python similar_flag.py -i exact/molecules.txt -o similarity/exact.csv -t 95

# Lower threshold (broader search)
python similar_flag.py -i exact/molecules.txt -o similarity/broad.csv -t 85
```

### Substructure Search

```bash
python substructure_flag.py -i exact/molecules.txt -o substructure/results.csv
```

---

## Output Format

All CSV outputs contain:

- `input_smile`: Original SMILES string
- `is_patented`: True/False (patent found)

Example:

```csv
input_smile,is_patented
CCO,True
c1ccccc1O,False
```

---

## File Structure

```
patent_flag/
├── scaffold.py                          # Main scripts
├── similar_flag.py
├── substructure_flag.py
│
├── exact/                               # Input SMILES files
│   ├── antifungal_smiles.txt
│   ├── canonical_gen_mol.txt
│   └── screening_top10_broad_spectrum.txt
│
├── scaffold/                            # Generated scaffolds
│   ├── antifungal_smiles_scaffold.txt
│   └── ...
│
└── similarity/                          # Results CSVs
    ├── antifungal_smiles_flag.csv
    └── ...
```

---

## Key Arguments

**scaffold.py**

- `-i, --input` (required): Input TXT file
- `-o, --output` (required): Output TXT file

**similar_flag.py**

- `-i, --input` (required): Input TXT file
- `-o, --output` (default: `patent_results.csv`): Output CSV
- `-t, --threshold` (default: `95`): Similarity threshold 0-100

**substructure_flag.py**

- `-i, --input` (required): Input TXT file
- `-o, --output` (default: `substructure_results.csv`): Output CSV

---

## Input Format

One SMILES per line:

```
CCO
c1ccccc1O
CC(C)Cc1ccc(cc1)C(C)C(O)=O
```

---

## Performance

- 10 compounds: 5-10 min
- 100 compounds: 30-60 min
- 1000+ compounds: 4-6 hours

Depends on: compound count, threshold, API speed, network

---

## Notes

- Respects PubChem API rate limits (0.2s delays)
- Substructure search uses async polling (2s intervals)
- Empty lines or comments skipped automatically

---

## Documentation

- [SCAFFOLD_README.md](SCAFFOLD_README.md) - Scaffold tool details
- [SIMILAR_FLAG_README.md](SIMILAR_FLAG_README.md) - Similarity search details
- [SUBSTRUCTURE_FLAG_README.md](SUBSTRUCTURE_FLAG_README.md) - Substructure search details
- [GRAPH_INTERPRETATION.md](GRAPH_INTERPRETATION.md) - Analysis guide

---

**Last Updated**: December 2025
