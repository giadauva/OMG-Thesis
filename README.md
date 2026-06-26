> **BSc Business Analytics · University of Amsterdam**  
# Company: Online Marketing Group 
> A data-driven decision support system for predicting and improving email engagement.

## Project overview

This repository contains the artifacts produced in collaboration with Online Marketing Group (OMG) as part of the UvA Business Analytics bachelor's thesis. The project applies Design Science Research (DSR) and CRISP-DM to build an email engagement scoring system to support a human marketer in deciding *who* to target, *what content* to send and *when* to send it.

Each group member contributes an individual model component. The shared foundation (data preprocessing, EDA, feature engineering) lives in the group notebook and is used by all components.

---

## Structure

```
OMG-Thesis/
│
├── data/                                    # Raw and processed datasets (gitignored — NDA)
│   ├── Dataset 1 UVA .csv                   # User-level subscriber data
│   ├── DATSET 2 UVA lijst mailings.xlsx     # Mailing metadata (subject lines, preheaders)
│   ├── Data device, browsers, emailclient.xlsx #
│   ├── UVA Robin .xlsx                      # Dataset containg send times and dates
│   ├── df_model_with_ids.csv                # Preprocessed modelling ready dataset
│   └── mailing_dates.csv                    # Send dates for date-based robustness check in the adaptive learning component
│
├── Thesis_OMG_analysis.ipynb      # Shared group notebook: preprocessing & EDA
├── Adaptive_learning.ipynb        # Giada: adaptive batch retraining framework
│
│   [Groupmates will add their notebooks]
│
└── README.md
```

> **Note on data:** All datasets are subject to an NDA with OMG and are not tracked in this repository. Contact the project team or OMG directly for data access queries.

---

## Shared notebook — `Thesis_OMG_analysis.ipynb`

The group notebook establishes the shared data foundation used across all individual components. It covers:

- **Data handling and cleaning** — merging the subscriber dataset (Dataset 1) with mailing metadata (Dataset 2); standardising Dutch column names; handling missing values in gender, birth date, and postcode fields
- **Feature engineering** — parsing structured mailing/open/click ID strings into binary engagement flags; computing user-level open and click rates; deriving age from birth date; exploding multi-valued interest fields
- **Campaign analysis** — overall open and click rates; subject line effectiveness; four-quadrant engagement segmentation (high/low open × high/low click)
- **User analysis** — engagement distribution across users; demographic breakdowns by gender and age group; interest-level engagement patterns
- **Model preparation** — producing `df_model_with_ids.csv`, the shared model-ready dataset with `user_id`, `mailing_id`, `open`, `click`, and engineered features used by all individual notebooks
- **Shared modelling** — naive baseline (per-user historical mean open rate) and logistic regression model trained on the full feature dataset; these serve as the shared performance benchmarks against which all individual components are evaluated

---

## Individual components

### Giada — Adaptive batch retraining (`Adaptive_learning.ipynb`)

**Research question:** *How does the predictive performance of email engagement scoring models evolve as new campaign observations are incrementally added, and to what extent does periodic batch retraining outperform a static baseline?*

This notebook implements and evaluates an adaptive retraining framework for logistic regression models predicting email open and click rates.

**Methodology:**
- Mailings are ordered chronologically by `mailing_id` (and separately by `send_date` for robustness checks) and split into sequential batches
- Three model types are evaluated at each batch step: (1) a **naive baseline** (per-user historical mean), (2) a **static logistic regression** trained once on the first batch and never updated, and (3) an **adaptive logistic regression** retrained on all data seen so far (expanding window) or the most recent *k* batches (sliding window, `window_size=3`)
- Primary metric: AUC-ROC; secondary: MAE and PR-AUC
- Statistical comparison via Wilcoxon signed-rank test across batch steps
- Sensitivity analysis across batch granularities: `n_batches ∈ {5, 10, 15, 20}`
- Robustness check: date-based chronological split (168 mailings / 711,747 rows) to validate ID-based findings

**Key results (primary setup, `n_batches=10`):**
- *Open prediction:* adaptive vs. static difference not statistically significant (Wilcoxon *p* = 0.641); static model marginally ahead on mean AUC across all batch sizes
- *Click prediction:* adaptive AUC significantly outperforms static (Wilcoxon *p* = 0.023); adaptive wins at every batch size tested; static collapses at `n=20` (mean AUC ≈ 0.700) due to severe class imbalance (~0.1% positive class) and limited initial training data
- The retraining benefit is **target-dependent**: recommended for click prediction, not clearly beneficial for open prediction

**Key results (optimal setup, `n_batches=20`):**
- *Open prediction:* adaptive vs. static remains non-significant (Wilcoxon *p* = 0.5277); mean AUC 0.8091 (adaptive) vs. 0.8149 (static); adaptive wins in 13 of 19 batches on AUC
- *Click prediction:* adaptive AUC significantly outperforms static (Wilcoxon *p* = 0.0002); mean adaptive AUC = 0.9291 vs. static = 0.7000; adaptive wins in 18 of 19 batches — note that there is severe class imbalance in the target variable (0.1% positive rate)


## Setup

### Prerequisites

- Python 3.9+
- Jupyter Notebook or JupyterLab

### Installation

```bash
git clone https://github.com/giadauva/OMG-Thesis.git
cd OMG-Thesis
pip install -r requirements.txt
```

### Core dependencies

```
pandas
numpy
scikit-learn
scipy
matplotlib
seaborn
openpyxl
```

### Data setup

Place the following files in a `data/` directory at the repository root (not tracked — see NDA note above):

| File | Description |
| `Dataset 1 UVA .csv`               | Subscriber-level data (semicolon-delimited) |
| `DATSET 2 UVA lijst mailings.xlsx` | Mailing metadata |
| `df_model_with_ids.csv`            | Preprocessed model-ready dataset (output of group notebook) |
| `mailing_dates.csv`                | Mailing send dates (used for date-based robustness checks) |
| Data device, browsers, emailclient.xlsx |
│ UVA Robin .xlsx                    | Dataset containg send times and dates

---

## Research context

**Framework:** Design Science Research (DSR) with three cycles (rigour, relevance, design) and CRISP-DM  
**Artefact type:** Decision support system, engagement probability scores reviewed by a human marketer before action, not a fully automated pipeline  
**Dataset:** ~1,011,197 user–mailing pairings after preprocessing  
**Targets:** Binary open (`1` = opened, `0` = not opened) and binary click (`1` = clicked, `0` = not clicked)  
**Thesis supervisors:** Yunming Hui

---

## Authors

| Name | Component | Contact |

| Giada Frontini | Adaptive batch retraining | [GitHub](https://github.com/giadauva) |
| Loreta Lasmane | Component | *(to be added)* |
| Trang Nguyen   | Component | *(to be added)* |
| Hien Nguyen    | Component | *(to be added)* |
| Maia Villar    | Component | *(to be added)* |


