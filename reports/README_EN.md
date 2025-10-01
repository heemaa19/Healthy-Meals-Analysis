
# Healthy Meals – Exploratory Data Analysis (EDA)

This repository contains a compact, portfolio-ready EDA of a synthetic meals/nutrition dataset. It includes:

- **Data cleaning** with plausibility checks (macro-based kcal vs. declared kcal, extreme sodium, critical fields).
- **Feature engineering** (kcal/100g, macro shares, simple composite **Health Score** 0–100).
- **Key visuals** (calories distribution, boxplot by diet type, average Health Score by cuisine, healthy-share by diet, correlations).
- **Deliverables**: cleaned CSV, an English Word report, and a concise PPTX deck.

## Health Score (0–100)
Components (equal weights by default):
- Calories in the 200–800 kcal range (closer is better)
- Lower sodium (≤ 1,500 mg) and lower sugar (≤ 25 g)
- Higher fiber (5–15 g range)
- Macro balance (Protein 20–35% kcal, Carbs 40–55%, Fat 20–35%)

> **Note**: This score is a comparative index for this dataset, not medical advice.

## Files
- `healthy_eating_dataset_clean.csv` – cleaned dataset
- `Healthy_Meals_Analysis_Report_EN.docx` – English report with tables and charts
- `Healthy_Meals_Analysis_Deck_EN.pptx` – short presentation deck

## Reproduce locally
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install pandas matplotlib python-docx python-pptx
python eda_script.py  # (if you separate the logic into a script)
```

## Next steps
- Optional modeling: classify `is_healthy` or predict `rating`.
- Add an interactive dashboard (e.g., Power BI / Streamlit).

