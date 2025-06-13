import pandas as pd
import numpy as np

# Assegura't que app_ordenada.py existeix al mateix directori
# i conté les definicions de les funcions importades.
from app_ordenada import (
    load_and_process_datasets,
    create_lookup_tables,
    calculate_self_sufficiency_aggregated,
    calculate_food_footprint,
    extract_element_data,
    build_women_agri_share
)

# 1. Defineix els paths als fitxers de dades raw
# Ajusta els noms dels fitxers si són diferents
faostat_file_paths = {
    'df_qcl': 'fao_QCL.csv',
    'df_fbs': 'fao_FBS.csv',
    'df_et': 'fao_ET.csv'
    # Considera afegir 'df_el': 'fao_El.csv' si és utilitzat per alguna funció importada
}
employment_file_path = "Employment by sector (%) .csv" # Nom del fitxer de dades d'ocupació

# Directori de sortida per als fitxers processats
output_dir = 'data/'

print("--- Iniciant script de preprocessament ---")

# 2. Carrega i processa els datasets de FAOSTAT
print("\nProcessant datasets de FAOSTAT...")
datasets = load_and_process_datasets(faostat_file_paths)

# 3. Crea les taules de lookup (mapes d'àrea i ítems)
print("\nCreant taules de lookup...")
if 'df_qcl' in datasets:
    area_map, item_map = create_lookup_tables(datasets['df_qcl'])
    print(f"area_map creada amb {len(area_map)} files.")
    print(f"item_map creada amb {len(item_map)} files.")
else:
    print("ERROR: No s'ha trobat 'df_qcl' als datasets carregats. No es poden crear lookup tables.")
    area_map = pd.DataFrame() # Placeholder
    item_map = pd.DataFrame() # Placeholder

# 4. Calcula els indicadors principals
print("\nCalculant l'indicador de Self-Sufficiency (Autosuficiència)...")
ss_df = calculate_self_sufficiency_aggregated(datasets, area_map)
print(f"Self-Sufficiency (ss_df) calculat amb {len(ss_df)} files.")

print("\nCalculant l'indicador de Food Footprint (Empremta Alimentària CO2)...")
ff_df = calculate_food_footprint(datasets, area_map)
print(f"Food Footprint (ff_df) calculat amb {len(ff_df)} files.")

# 5. Carrega i processa les dades d'ocupació
print("\nProcessant dades d'ocupació (Women in Agriculture)...")
try:
    employment_df = pd.read_csv(employment_file_path)
    print(f"Dades d'ocupació carregades des de '{employment_file_path}' ({len(employment_df)} files).")
except FileNotFoundError:
    print(f"ERROR: El fitxer d'ocupació '{employment_file_path}' no s'ha trobat.")
    employment_df = pd.DataFrame() # Placeholder si el fitxer no existeix

# 6. Calcula la quota de dones en l'agricultura (Women Agri Share)
if not employment_df.empty:
    women_share_df = build_women_agri_share(employment_df)
    print(f"Women Agri Share (women_share_df) calculat amb {len(women_share_df)} files.")
else:
    women_share_df = pd.DataFrame(columns=['AreaCode', 'AreaName', 'Year', 'WomenAgriShare']) # Placeholder

# 7. Fusiona Self-Sufficiency amb Women Agri Share per crear ssr_women_df
print("\nFusionant Self-Sufficiency amb Women Agri Share...")
ssr_women_df = ss_df.copy()
if not women_share_df.empty and 'AreaName' in ssr_women_df.columns and 'AreaName' in women_share_df.columns:
    # Normalitza AreaName per a la fusió, creant una columna temporal
    ssr_women_df['AreaName_lower_merge'] = ssr_women_df['AreaName'].astype(str).str.strip().str.lower()
    women_share_df['AreaName_lower_merge'] = women_share_df['AreaName'].astype(str).str.strip().str.lower()
    
    ssr_women_df = pd.merge(
        ssr_women_df,
        women_share_df[['AreaName_lower_merge', 'Year', 'WomenAgriShare']],
        on=['AreaName_lower_merge', 'Year'],
        how='left'
    )
    ssr_women_df.drop(columns=['AreaName_lower_merge'], inplace=True) # Elimina la columna temporal
    
    if 'WomenAgriShare' not in ssr_women_df.columns:
         ssr_women_df['WomenAgriShare'] = np.nan
    print(f"ssr_women_df creat amb {len(ssr_women_df)} files després de la fusió.")
elif 'WomenAgriShare' not in ssr_women_df.columns: # Si women_share_df estava buit
    ssr_women_df['WomenAgriShare'] = np.nan
    print("ssr_women_df creat (sense dades de WomenAgriShare ja que el DataFrame estava buit o no hi havia coincidències).")


# 8. Extreu dades detallades de Producció, Importacions i Exportacions
print("\nExtraient dades de Producció...")
prod_df = extract_element_data(datasets.get('df_qcl', pd.DataFrame()), 'Production', 'Production', area_map, item_map)
print(f"Dades de Producció (prod_df) extretes amb {len(prod_df)} files.")

print("\nExtraient dades d'Importacions...")
imports_df = extract_element_data(datasets.get('df_fbs', pd.DataFrame()), 'Import Quantity', 'ImportQuantity', area_map, item_map)
print(f"Dades d'Importacions (imports_df) extretes amb {len(imports_df)} files.")

print("\nExtraient dades d'Exportacions...")
exports_df = extract_element_data(datasets.get('df_fbs', pd.DataFrame()), 'Export Quantity', 'ExportQuantity', area_map, item_map)
print(f"Dades d'Exportacions (exports_df) extretes amb {len(exports_df)} files.")

# 9. Desa tots els DataFrames processats en format Parquet
print(f"\nDesant els DataFrames processats a la carpeta '{output_dir}'...")

dataframes_to_save = {
    "ssr_women": ssr_women_df,
    "food_footprint": ff_df,
    "production": prod_df,
    "imports": imports_df,
    "exports": exports_df,
    "area_map": area_map,
    "item_map": item_map,
    "women_agri_share": women_share_df[['AreaCode', 'AreaName', 'Year', 'WomenAgriShare']] if not women_share_df.empty else pd.DataFrame()
}

for name, df_to_save in dataframes_to_save.items():
    if not df_to_save.empty:
        file_path = f'{output_dir}{name}.parquet'
        df_to_save.to_parquet(file_path, compression='snappy', index=False)
        print(f"  ✔️ Desat: {file_path} ({len(df_to_save)} files)")
    else:
        print(f"  ⚠️  Advertència: El DataFrame '{name}' està buit i no s'ha desat.")

print("\n--- Preprocessament completat ---")
print(f"Els fitxers Parquet s'han generat a la carpeta '{output_dir}'.")
print("Recorda afegir els arxius CSV originals (grans) al teu .gitignore.")
