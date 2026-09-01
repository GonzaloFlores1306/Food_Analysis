# Nutritional Data Pipeline & ML Clustering

## Executive Summary (The Business Problem)

In the nutrition and fitness industry, identifying efficient food substitutes is typically a manual process based on human-defined categories (e.g., "Dairy" or "Meat").

This project addresses this issue through an **end-to-end** data architecture. Using **Machine Learning (K-Means Clustering)**, the algorithm grouped over 3,000 foods based purely on nutritional density and macronutrient profiles, revealing genuine biological groupings that are not immediately apparent to the human eye.

The entire process is orchestrated and automated in the cloud, culminating in an **interactive Power BI dashboard** designed to support decision-making.

## Technical Architecture (The Stack)

1. **Extraction and Cleaning (Data Wrangling):** `Python` (Pandas, NumPy)
2. **Machine Learning (Unsupervised Learning):** `Scikit-Learn` (K-Means, PCA)
3. **Data Warehouse & Orchestration:** `Google BigQuery` and `GitHub Actions` (Automated CI/CD)
4. **Visualization and Business Intelligence:** `Power BI` (Direct Query, Advanced DAX)

## Key Analytical Findings

By applying dimensionality reduction and unsupervised clustering, the model segmented the data into six main groups, highlighting insights such as:

- **Cluster 4 (Pure Fats):** The algorithm identified and isolated oils, even though the original dataset (USDA) had incorrectly labeled them as "Vegetables."
- **Cluster 5 (High Caloric Density):** Bacon and pepperoni were grouped alongside nuts and seeds, demonstrating their biological similarity (high in fat and calories, low in carbs).

## How the Pipeline (CI/CD) Works

To ensure data integrity and keep the data up to date:

- A workflow was implemented in **GitHub Actions** (`etl_pipeline.yml`) that spins up a virtual environment, runs the Machine Learning model, and automatically pushes data to the **Google BigQuery** table every month, bypassing the Sandbox's temporary expiration restriction.

## Dashboard Preview
