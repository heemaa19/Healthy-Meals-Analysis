# Healthy Meals – Interactive Dashboard (EN)

This folder includes a **Streamlit** dashboard for the cleaned meals dataset.

## 📁 Files
- `healthy_meals_dashboard_app.py` – Streamlit app
- `healthy_eating_dataset_clean.csv` – cleaned dataset (ensure it exists alongside the app)
- `requirements.txt` – dependencies to run the app

## ▶️ Run locally
```bash
# 1) Create venv (optional)
python3 -m venv .venv && source .venv/bin/activate

# 2) Install dependencies
pip install -r requirements.txt

# 3) Launch the app
streamlit run healthy_meals_dashboard_app.py
```
The app will open at `http://localhost:8501`.

## ☁️ Deploy on Streamlit Cloud
1. Push these files to a public GitHub repo.
2. On https://streamlit.io/cloud, create a new app pointing to `healthy_meals_dashboard_app.py`.
3. Set Python version and add `requirements.txt`.

## Notes
- The app auto-detects filters (Cuisine, Diet Type, Cooking Method) if columns exist.
- KPIs: **Rows (filtered)**, **Avg Calories**, **Healthy Share**, **Avg Health Score**.
- Charts: **Calories Distribution**, **Avg Health Score by Cuisine (Top N)**, **Healthy Ratio by Diet**, **Calories vs Health Score**.
- A trained model `.joblib` is optional; the app will show a note if it is present.