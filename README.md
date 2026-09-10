# 🥗 AI-Powered Nutrition Intelligence & Diet Simulator

[![Live Dashboard](https://img.shields.io/badge/Power_BI-Live_Dashboard-F2C811?style=for-the-badge&logo=powerbi)](https://app.powerbi.com/links/bkdBux8Gyz?ctid=48ba00e0-002e-4cb0-b501-07385d34ec34&pbi_source=linkShare&bookmarkGuid=d651f231-c0c8-4dc7-8cf8-e022aaa801f3)

## 📌 Executive Summary (The Business Problem)

In the nutrition and fitness industry, identifying efficient food substitutes is typically a manual process based on human-defined categories (e.g., "Dairy" or "Meat").

This project addresses this issue through an **end-to-end data architecture**. Using **Machine Learning (K-Means Clustering)**, the algorithm grouped over 3,000 foods based purely on nutritional density and macronutrient profiles, revealing genuine biological groupings that are not immediately apparent to the human eye.

The entire process is orchestrated and automated in the cloud, culminating in an **interactive Power BI dashboard** designed to support data-driven dietary decision-making.

## 🏗️ Technical Architecture (The Stack)

1. **Extraction and Data Wrangling:** `Python` (Pandas, NumPy). Cleaned and engineered features like the `Protein_to_Calorie_Ratio` and `Micro_Density_Score`.
2. **Machine Learning (Unsupervised Learning):** `Scikit-Learn` (K-Means, PCA). Compressed 5 nutritional dimensions into a 2D mapping (PCA1, PCA2) for visual topography.
3. **Data Warehouse & Orchestration:** `Google BigQuery` and `GitHub Actions`. Configured a CI/CD automated pipeline to update the cloud database seamlessly.
4. **Visualization and Business Intelligence:** `Power BI` (Advanced DAX, Custom Tooltips, Dark Mode UI).

## 📊 Live Dashboard & Interface

**[👉 Click here to access the interactive Power BI Dashboard 👈](https://app.powerbi.com/links/bkdBux8Gyz?ctid=48ba00e0-002e-4cb0-b501-07385d34ec34&pbi_source=linkShare&bookmarkGuid=d651f231-c0c8-4dc7-8cf8-e022aaa801f3)**

### Page 1: Nutrition Intelligence Engine
A macroscopic view of the nutritional topography, mapping how the AI clustered the food items based on biological similarity rather than human labels. 
![Nutrition Intelligence Dashboard](img1.png)

### Page 2: Dietary Substitution Engine
An operational tool featuring a dynamic macronutrient simulator. Users can input their target serving size (grams), and the DAX engine recalculates nutritional profiles and ranks the most efficient protein sources in real-time.
![Diet Simulator Dashboard](img2.png)

## 🧠 Key Analytical Findings

By applying dimensionality reduction and unsupervised clustering, the model segmented the data into six main groups, highlighting insights such as:

- **Cluster 4 (Pure Fats):** The algorithm identified and perfectly isolated pure oils (e.g., olive oil, lard). Interestingly, the original USDA dataset had incorrectly labeled some of these as "Vegetables," proving the AI's biological accuracy over manual data entry.
- **Cluster 5 (High Caloric Density):** Bacon and pepperoni were grouped alongside nuts and aged cheeses, demonstrating their mathematical and biological similarity (extremely high in fat and calories, low in carbs).
- **Cluster 0 (Protein-Dense):** Revealed the absolute best "superfoods" for muscle building by isolating lean meats with the highest efficiency ratio.

## ⚙️ How the Pipeline (CI/CD) Works

To ensure data integrity and automate cloud synchronization:

- A workflow was implemented in **GitHub Actions** (`.github/workflows/etl_pipeline.yml`).
- The pipeline spins up a virtual environment, executes the `main.py` Python script (handling data cleaning, feature engineering, and KMeans clustering), and securely authenticates with Google Cloud via environment secrets.
- The processed DataFrame is then pushed directly to a **Google BigQuery** table, bypassing standard Sandbox expiration limits and ensuring the Power BI dashboard always connects to a live, persistent cloud source.