# Import all the libraries

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import pandas_gbq
import os
import json
from google.oauth2 import service_account
from dotenv import load_dotenv
import warnings
warnings.filterwarnings('ignore')
load_dotenv()


# Dataset Information
DATA_PATH = "data/usda_protein_nutrient_dataset_5000.csv"

df = pd.read_csv(DATA_PATH, sep=",")
print(f"Datos: {df.shape[0]} filas y {df.shape[1]} columnas")


# Dropping useless columns

# Serving_Size: It doesn't have any values.<br>
# FDC_ID: We'll not use the ID of the food.<br>
# Category_Detail: It is the same as the Category column.

print(f"\nCategory values: {df['Category'].unique()}")
print(f"\nCategory details values: {df['Category_Detail'].unique()}")

equals = df['Category'].equals(df['Category_Detail'])
print(f"¿This columns are the same?: {equals}")

df = df.drop(columns=['Serving_Size', 'FDC_ID', 'Category_Detail'])


# A food item cannot contain more than 100 grams of macronutrients per 100-gram serving, nor more than 900 calories.
df['Total_Macros_g'] = df['Protein_g_per_100g'] + df['Fat_g_per_100g'] + df['Carbs_g_per_100g']

df = df[df['Total_Macros_g'] <= 100].copy()
df = df[df['Calories_per_100g'] <= 900].copy()
df.drop(columns=['Total_Macros_g'], inplace=True) # We'll not use this column


# Feature Engineering
df['Protein_to_Calorie_Ratio'] = np.where(df['Calories_per_100g'] > 0,
                                          df['Protein_g_per_100g'] / df['Calories_per_100g'],
                                          0)

# Calories per macro
# Protein & Carbs = 4 kcal/g
# Fat = 9 kcal/g
df['Cal_From_Protein'] = df['Protein_g_per_100g'] * 4
df['Cal_From_Carbs'] = df['Carbs_g_per_100g'] * 4
df['Cal_From_Fat'] = df['Fat_g_per_100g'] * 9

def get_dominant_macro(row):
  macros = {
    'Protein-Dominant': row['Cal_From_Protein'],
    'Carbs-Dominant': row['Cal_From_Carbs'],
    'Fat-Dominant': row['Cal_From_Fat']
	}
  if sum(macros.values()) < 5:
    return 'Micro/Water'
  return max(macros, key=macros.get)

df['Dominant_Macro'] = df.apply(get_dominant_macro, axis=1)

# Clean auxiliar columns
df.drop(columns=['Cal_From_Protein', 'Cal_From_Carbs', 'Cal_From_Fat'], inplace=True)

micronutrients = ['Vitamin_A_RAE', 'Vitamin_C_mg', 'Vitamin_D_µg', 'Vitamin_B12_µg', 
                  'Calcium_mg', 'Iron_mg', 'Magnesium_mg', 'Potassium_mg', 'Zinc_mg']

df['Micro_Density_Score'] = df[micronutrients].apply(lambda x: np.log1p(x)).sum(axis=1)


# Clustering

# 1. Mathematics features

features_for_clustering = [
  'Protein_g_per_100g',
  'Fat_g_per_100g',
  'Carbs_g_per_100g',
  'Calories_per_100g',
  'Micro_Density_Score'
]

X = df[features_for_clustering]

# 2. Data scale (Mean = 0, Variance = 1)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 3. Apply K-Means
kmeans = KMeans(n_clusters=6, random_state=42, n_init=10)

df['Nutritional_Cluster'] = kmeans.fit_predict(X_scaled)

print("\nFood Distribution per Cluster:")
print(df['Nutritional_Cluster'].value_counts())

# 2 principal components
pca = PCA(n_components=2)
components = pca.fit_transform(X_scaled)

df['PCA1'] = components[:, 0]
df['PCA2'] = components[:, 1]

# We need to analyze the average characteristics of each group

cluster_profiles = df.groupby('Nutritional_Cluster')[features_for_clustering].mean()
print("\nAverage profile of each cluster: ")
print(cluster_profiles)

'''
Cluster 0 (Meats and Lean/Medium-Fat Protein)*: Good protein (~15.7g), controlled fat, and the highest micronutrient density in the dataset (19.5). The superfoods for building muscle mass.
Cluster 1 (Fruits and Vegetables / High Volume)*: Very low calories (58 kcal), very low macros. These are water-rich foods that fill you up without adding calories.
Cluster 2 (Grains and Doughs)*: The carbohydrate bomb (61.8g carbs). This group includes pasta, rice, bread, and flour.
Cluster 3 (Dairy and Light Legumes)*: A very balanced profile, low calories (121 kcal), but very high micronutrient density (18.6).
Cluster 4 (Pure Oils)*: 0g protein, 99.93g fat, 0.05g carbohydrates, and ~893 calories. The algorithm perfectly isolated the oils (olive oil, butter, lard). Their micronutrient density is nearly zero.
Cluster 5 (Nuts, Seeds, and Aged Cheeses)*: High protein (16.5g) but very high fat (49.5g) and extremely high calories (527 kcal). These are very dense energy sources.
'''


# 5 food more commun in each cluster
for i in range(6):
    print(f"\n--- Foods in the cluster {i} ---")
    
    print("Principal categorys:")
    print(df[df['Nutritional_Cluster'] == i]['Category'].value_counts().head(3))
    
    print("\nExamples of food:")
    print(df[df['Nutritional_Cluster'] == i]['Food_Item'].head(3).tolist())
    print("-" * 40)


# Name mapping

cluster_names = {
  0: 'Protein-Dense (Meat/Eggs)',
  1: 'Low-Calorie (Fruit/Vegetables)',
  2: 'Carbohydrate-Dominant (Grains/Dough-based)',
  3: 'Light & Balanced (Dairy/Soups)',
  4: 'Pure Fats and Oil',
  5: 'High Caloric Density (Nuts/Seeds)'
}

df['Cluster_Name'] = df['Nutritional_Cluster'].map(cluster_names)

print(df[['Food_Item', 'Category', 'Cluster_Name']].head(10))


# Big Query Connection

credentials_json = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS_JSON")

if credentials_json:
  credentials_dict = json.loads(credentials_json)
  credentials = service_account.Credentials.from_service_account_info(credentials_dict)
else:
  print("file not found")
  credentials = None

project_id = 'proteinfood'
table_id = 'nutrition_analytics.food_data_clustered'
print("Initializing BigQuery charge...")

pandas_gbq.to_gbq(
  dataframe=df,
  destination_table=table_id,
  project_id=project_id,
  if_exists='replace',
  credentials=credentials
)

print(f"{len(df)} files charged correctly in BigQuery")