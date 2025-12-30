# Patent Flag - Molecular Patent Analysis Toolkit

A comprehensive Python toolkit for analyzing molecular compounds against patent databases using PubChem APIs. Combines scaffold extraction, similarity searching, and substructure matching to identify patented and novel compounds.

## Overview

This project provides an integrated pipeline to:

1. **Extract scaffolds** from molecular SMILES strings
2. **Search for similar** patented compounds (2D similarity)
3. **Search for substructure** matches in patents
4. **Visualize results** with patent analysis graphs
5. **Interpret findings** for drug discovery and IP strategy

---

## Project Structure

```
patent_flag/
├── scaffold.py                      # Extract Bemis-Murcko scaffolds
├── similar_flag.py                  # Find patented similar compounds
├── substructure_flag.py             # Find patented substructure matches
├── generate_patent_graph.py         # Generate analysis visualizations
│
├── exact/                           # Original SMILES files
│   ├── all_single_exact.txt
│   ├── antifungal_smiles.txt
│   ├── canonical_gen_mol.txt
│   └── screening_top10_broad_spectrum.txt
│
├── scaffold/                        # Generated scaffold files
│   ├── all_single_scaffold.txt
│   ├── antifungal_smiles_scaffold.txt
│   ├── canonical_gen_mol_scaffold.txt
│   └── screening_top10_broad_spectrum_scaffold.txt
│
├── similarity/                      # Similarity search results
│   ├── all_single_exact_flag.csv
│   ├── all_single_scaffold_flag.csv
│   ├── antifungal_smiles_flag.csv
│   ├── antifungal_smiles_scaffold_flag.csv
│   ├── canonical_gen_mol_flag.csv
│   ├── canonical_gen_mol_scaffold_flag.csv
│   ├── screening_top10_broad_spectrum_flag.csv
│   └── screening_top10_broad_spectrum_scaffold_flag.csv
│
├── substructure/                    # Substructure search results
│   └── *.csv
│
├── similarity_analysis.png          # Visualization output
├── substructure_analysis.png        # Visualization output
│
└── README.md, *.md                  # Documentation files
```

---

## Installation

### Requirements

- Python 3.7+
- Dependencies: pandas, requests, rdkit, matplotlib

### Setup

```bash
# Install dependencies
pip install pandas requests rdkit matplotlib
```

---

## Quick Start

### 1. Extract Scaffolds

Convert exact SMILES to Bemis-Murcko scaffolds:

```bash
python scaffold.py -i exact/molecules.txt -o scaffold/molecules_scaffold.txt
```

### 2. Search for Similar Patented Compounds

Find 2D-similar compounds in PubChem patents:

```bash
python similar_flag.py -i exact/molecules.txt -o similarity/results.csv -t 95
```

### 3. Search for Substructure Patents

Find compounds containing your molecule as substructure:

```bash
python substructure_flag.py -i exact/molecules.txt -o substructure/results.csv
```

### 4. Generate Analysis Graphs

Create visualization of patent status:

```bash
python generate_patent_graph.py
```

Outputs: `similarity_analysis.png`, `substructure_analysis.png`

---

## Scripts Reference

### scaffold.py

**Purpose**: Extract chemical scaffolds from SMILES strings

```bash
python scaffold.py -i input.txt -o output.txt
```

| Argument       | Type | Required | Default | Description                   |
| -------------- | ---- | -------- | ------- | ----------------------------- |
| `-i, --input`  | str  | Yes      | -       | Input TXT file with SMILES    |
| `-o, --output` | str  | Yes      | -       | Output TXT file for scaffolds |

**How it works**: Uses RDKit's Bemis-Murcko algorithm to extract core structure

**See**: [SCAFFOLD_README.md](SCAFFOLD_README.md)

---

### similar_flag.py

**Purpose**: Find 2D-similar compounds in PubChem and flag if patented

```bash
python similar_flag.py -i input.txt -o output.csv -t 95
```

| Argument          | Type | Required | Default            | Description                  |
| ----------------- | ---- | -------- | ------------------ | ---------------------------- |
| `-i, --input`     | str  | Yes      | -                  | Input TXT file with SMILES   |
| `-o, --output`    | str  | No       | patent_results.csv | Output CSV file              |
| `-t, --threshold` | int  | No       | 95                 | Similarity threshold (0-100) |

**Output Columns**:

- `input_smile`: Original SMILES
- `is_patented`: Patent found (True/False)

**See**: [SIMILAR_FLAG_README.md](SIMILAR_FLAG_README.md)

---

### substructure_flag.py

**Purpose**: Find compounds with input as substructure, flag if patented

```bash
python substructure_flag.py -i input.txt -o output.csv
```

| Argument       | Type | Required | Default                  | Description                |
| -------------- | ---- | -------- | ------------------------ | -------------------------- |
| `-i, --input`  | str  | Yes      | -                        | Input TXT file with SMILES |
| `-o, --output` | str  | No       | substructure_results.csv | Output CSV file            |

**Output Columns**:

- `input_smile`: Original SMILES
- `is_patented`: Patent found (True/False)

**See**: [SUBSTRUCTURE_FLAG_README.md](SUBSTRUCTURE_FLAG_README.md)

---

### generate_patent_graph.py

**Purpose**: Analyze results and create visualization

```bash
python generate_patent_graph.py
```

**Generates**:

- `similarity_analysis.png` - Similarity search patent breakdown
- `substructure_analysis.png` - Substructure search patent breakdown
- Console summary with statistics

**See**: [GRAPH_INTERPRETATION.md](GRAPH_INTERPRETATION.md)

---

## Complete Workflow Example

### Step 1: Prepare Input

```bash
# Place SMILES file in exact/ folder
# Format: One SMILES per line
```

### Step 2: Generate Scaffolds

```bash
python scaffold.py -i exact/antifungal_smiles.txt \
                   -o scaffold/antifungal_smiles_scaffold.txt
```

### Step 3: Run Similarity Search

```bash
python similar_flag.py -i exact/antifungal_smiles.txt \
                       -o similarity/antifungal_exact.csv -t 95

python similar_flag.py -i scaffold/antifungal_smiles_scaffold.txt \
                       -o similarity/antifungal_scaffold.csv -t 90
```

### Step 4: Run Substructure Search

```bash
python substructure_flag.py -i exact/antifungal_smiles.txt \
                            -o substructure/antifungal_exact.csv

python substructure_flag.py -i scaffold/antifungal_smiles_scaffold.txt \
                            -o substructure/antifungal_scaffold.csv
```

### Step 5: Generate Analysis

```bash
python generate_patent_graph.py
```

---

## Output Format

### CSV Results

All flag scripts output CSV files with:

- **input_smile**: Input SMILES string
- **is_patented**: Boolean (True = patent found, False = no patent)

### Visualization

Two PNG graphs:

- **Left chart**: Absolute counts
- **Right chart**: Percentage breakdown

---

## Key Findings from Default Data

| Dataset            | Similarity Patent Rate | Substructure Patent Rate | Status               |
| ------------------ | ---------------------- | ------------------------ | -------------------- |
| All Single (Exact) | 92.3%                  | 45.7%                    | Highly patented      |
| Top 10 (Exact)     | 0%                     | 0%                       | **Novel candidates** |
| Antifungal         | 50-64%                 | 31-42%                   | Mixed protection     |
| Canonical          | 60-72%                 | 52.5%                    | Moderate coverage    |

---

## Interpretation Guide

**Key Insights**:

- **High similarity patent rate (>70%)**: Exact molecules heavily patented
- **Lower substructure rate**: More structural diversity available
- **0% in both searches**: Strongly unpatented (development opportunity)
- **Difference between searches**: Patent protection specific to exact molecules, not scaffolds

**For IP Strategy**:

- Explore compounds with low similarity but potential substructure hits
- Modify high-similarity patented compounds via scaffold changes
- Prioritize compounds with 0% in both searches

**See**: [GRAPH_INTERPRETATION.md](GRAPH_INTERPRETATION.md)

---

## API Rate Limiting

- PubChem REST API limits requests
- Built-in delays: 0.2s between requests
- Substructure polling: 2s intervals, max 15 attempts
- Recommended batch processing for large datasets

---

## Troubleshooting

| Issue              | Solution                                                        |
| ------------------ | --------------------------------------------------------------- |
| Connection timeout | PubChem may be down; retry later                                |
| No results found   | SMILES may be invalid; check format                             |
| Slow processing    | Reduce threshold or use smaller batches                         |
| Empty output       | Verify input file format (one SMILES per line)                  |
| Import errors      | Install missing dependencies: `pip install -r requirements.txt` |

---

## File Descriptions

| File                          | Purpose                           |
| ----------------------------- | --------------------------------- |
| `README.md`                   | This file - project overview      |
| `SCAFFOLD_README.md`          | Scaffold extraction documentation |
| `SIMILAR_FLAG_README.md`      | Similarity search documentation   |
| `SUBSTRUCTURE_FLAG_README.md` | Substructure search documentation |
| `GRAPH_INTERPRETATION.md`     | Analysis visualization guide      |

---

## Data Flow Diagram

```
Input SMILES (exact/)
    ↓
    ├─→ Scaffold Extraction (scaffold.py) → scaffold/
    │       ↓
    │   Scaffold SMILES (scaffold/)
    │
    ├─→ Similarity Search (similar_flag.py)
    │   ├─→ Exact SMILES → similarity/*exact*_flag.csv
    │   └─→ Scaffold SMILES → similarity/*scaffold*_flag.csv
    │
    ├─→ Substructure Search (substructure_flag.py)
    │   ├─→ Exact SMILES → substructure/*exact*_flag.csv
    │   └─→ Scaffold SMILES → substructure/*scaffold*_flag.csv
    │
    └─→ Analysis (generate_patent_graph.py)
        ├─→ similarity_analysis.png
        └─→ substructure_analysis.png
```

---

## Performance Notes

**Typical Runtime**:

- Small batch (10 compounds): 5-10 minutes
- Medium batch (100 compounds): 30-60 minutes
- Large batch (1000+ compounds): 4-6 hours

**Factors affecting speed**:

- Number of input molecules
- Similarity threshold (lower = more compounds to check)
- PubChem API availability
- Network latency

---

## License & References

**PubChem API**:

- [REST API Docs](https://pubchem.ncbi.nlm.nih.gov/docs/PUG-REST)
- [PUG View Docs](https://pubchem.ncbi.nlm.nih.gov/docs/PUG-View)

**RDKit**:

- [Bemis-Murcko Scaffolds](https://www.rdkit.org/docs/source/rdkit.Chem.Scaffolds.html)

---

## Quick Links

- 📊 [Interpretation Guide](GRAPH_INTERPRETATION.md)
- 🧬 [Scaffold Tool](SCAFFOLD_README.md)
- 🔍 [Similarity Search](SIMILAR_FLAG_README.md)
- 🏗️ [Substructure Search](SUBSTRUCTURE_FLAG_README.md)

---

**Last Updated**: December 2025
