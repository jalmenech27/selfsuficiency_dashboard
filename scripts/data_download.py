#!/usr/bin/env python3
"""
Script per descarregar dades de FAOSTAT per al projecte d'Autosuficiència Alimentària
Author: Jordi Almiñana Domènech (UOC Visualització de Dades)
Data: juny 2025

Aquest script descarrega automàticament les dades necessàries des de FAOSTAT
i altres fonts de dades per al dashboard d'autosuficiència alimentària.
"""

import os
import sys
import requests
import pandas as pd
from pathlib import Path
import zipfile
import time
from urllib.parse import urljoin

# Configuració
DATA_DIR = Path("data")
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

# Crear directoris si no existeixen
DATA_DIR.mkdir(exist_ok=True)
RAW_DATA_DIR.mkdir(exist_ok=True)
PROCESSED_DATA_DIR.mkdir(exist_ok=True)

# URLs de descàrrega de FAOSTAT (cal actualitzar amb les URLs reals)
FAOSTAT_URLS = {
    'production': {
        'url': 'https://www.fao.org/faostat/en/#data/QCL',
        'filename': 'fao_QCL.csv',
        'description': 'Crops and livestock products (Production data)'
    },
    'food_balance': {
        'url': 'https://www.fao.org/faostat/en/#data/FBS',
        'filename': 'fao_FBS.csv',
        'description': 'Food Balance Sheets (Import/Export/Supply data)'
    },
    'trade': {
        'url': 'https://www.fao.org/faostat/en/#data/TM',
        'filename': 'fao_TM.csv',
        'description': 'Detailed trade matrix'
    },
    'emissions': {
        'url': 'https://www.fao.org/faostat/en/#data/ET',
        'filename': 'fao_ET.csv',
        'description': 'Emissions - Agriculture (CO2 footprint data)'
    }
}

# URLs adicionals per dades d'ocupació i gènere
OTHER_DATA_SOURCES = {
    'employment': {
        'url': 'https://data.worldbank.org/indicator/SL.AGR.EMPL.FE.ZS',
        'filename': 'Employment by sector (%) .csv',
        'description': 'World Bank - Employment in agriculture, female (% of female employment)'
    }
}

def download_file(url: str, filename: str, description: str = "") -> bool:
    """
    Descarrega un fitxer des d'una URL.
    
    Args:
        url: URL del fitxer a descarregar
        filename: Nom del fitxer de destinació
        description: Descripció del dataset
    
    Returns:
        bool: True si la descàrrega ha estat exitosa
    """
    filepath = RAW_DATA_DIR / filename
    
    if filepath.exists():
        print(f"✓ {filename} ja existeix. Ometent descàrrega.")
        return True
    
    print(f"📥 Descarregant {description or filename}...")
    print(f"   URL: {url}")
    
    try:
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0
        
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    
                    if total_size > 0:
                        progress = (downloaded / total_size) * 100
                        print(f"\r   Progrés: {progress:.1f}%", end='', flush=True)
        
        print(f"\n✅ Descarregat: {filename} ({downloaded / (1024*1024):.1f} MB)")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error descarregant {filename}: {e}")
        if filepath.exists():
            filepath.unlink()  # Eliminar fitxer parcial
        return False

def download_faostat_data():
    """
    Descarrega tots els datasets de FAOSTAT necessaris.
    
    Nota: FAOSTAT requereix descàrrega manual o ús de la seva API.
    Aquest és un placeholder per a futures implementacions.
    """
    print("🌾 === DESCÀRREGA DE DADES FAOSTAT ===")
    print("\n⚠️  NOTA IMPORTANT:")
    print("   Les dades de FAOSTAT requereixen descàrrega manual des del lloc web oficial.")
    print("   Si us plau, visiteu els següents enllaços i descarregueu els fitxers CSV:")
    print()
    
    for key, data in FAOSTAT_URLS.items():
        print(f"📊 {data['description']}")
        print(f"   URL: {data['url']}")
        print(f"   Desar com: {RAW_DATA_DIR / data['filename']}")
        print()
    
    print("📝 Instruccions de descàrrega:")
    print("1. Aneu a cada URL")
    print("2. Seleccioneu tots els països i anys disponibles")
    print("3. Descarregueu com a CSV")
    print("4. Deseu els fitxers al directori data/raw/")
    print()

def download_world_bank_data():
    """
    Intenta descarregar dades del World Bank.
    """
    print("🏦 === DESCÀRREGA DE DADES WORLD BANK ===")
    
    # Exemple d'URL directa del World Bank (pot requerir ajustaments)
    wb_url = "https://api.worldbank.org/v2/en/indicator/SL.AGR.EMPL.FE.ZS?downloadformat=csv"
    
    try:
        success = download_file(
            wb_url,
            "Employment by sector (%) .csv",
            "World Bank - Employment in agriculture, female"
        )
        if not success:
            print("⚠️  Descàrrega automàtica fallida. Descàrrega manual necessària:")
            print("   https://data.worldbank.org/indicator/SL.AGR.EMPL.FE.ZS")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("⚠️  Si us plau, descarregueu manualment des de:")
        print("   https://data.worldbank.org/indicator/SL.AGR.EMPL.FE.ZS")

def check_data_availability():
    """
    Comprova quines dades estan disponibles localment.
    """
    print("\n📋 === ESTAT DE LES DADES ===")
    
    all_files = list(FAOSTAT_URLS.values()) + list(OTHER_DATA_SOURCES.values())
    
    available = 0
    total = len(all_files)
    
    for data in all_files:
        filepath = RAW_DATA_DIR / data['filename']
        if filepath.exists():
            size = filepath.stat().st_size / (1024*1024)  # MB
            print(f"✅ {data['filename']} ({size:.1f} MB)")
            available += 1
        else:
            print(f"❌ {data['filename']} (No disponible)")
    
    print(f"\n📊 Resum: {available}/{total} fitxers disponibles")
    
    if available == total:
        print("🎉 Totes les dades estan disponibles!")
        return True
    else:
        print("⚠️  Falten alguns fitxers de dades.")
        return False

def create_sample_data():
    """
    Crea dades de mostra per provar el dashboard sense les dades reals.
    """
    print("\n🧪 === CREANT DADES DE MOSTRA ===")
    
    # Crear dades de mostra mínimes
    sample_data = {
        'ssr_sample.csv': pd.DataFrame({
            'AreaCode': [1, 2, 3],
            'AreaName': ['Spain', 'France', 'Italy'],
            'Year': [2020, 2020, 2020],
            'SelfSufficiency': [0.85, 0.92, 0.78],
            'WomenAgriShare': [25.5, 28.3, 22.1]
        }),
        'production_sample.csv': pd.DataFrame({
            'AreaCode': [1, 2, 3],
            'AreaName': ['Spain', 'France', 'Italy'],
            'Year': [2020, 2020, 2020],
            'Production': [1000000, 1200000, 900000]
        })
    }
    
    for filename, df in sample_data.items():
        filepath = RAW_DATA_DIR / filename
        df.to_csv(filepath, index=False)
        print(f"✅ Creat: {filename}")
    
    print("✨ Dades de mostra creades per a proves!")

def main():
    """Funció principal del script."""
    print("🚀 === SCRIPT DE DESCÀRREGA DE DADES ===")
    print(f"📁 Directori de dades: {DATA_DIR.absolute()}")
    print()
    
    # Comprovar estat actual
    check_data_availability()
    
    # Intentar descarregar dades
    print("\n" + "="*50)
    download_faostat_data()
    
    print("\n" + "="*50)
    download_world_bank_data()
    
    # Comprovar estat final
    print("\n" + "="*50)
    all_available = check_data_availability()
    
    if not all_available:
        print("\n🧪 Voleu crear dades de mostra per a proves? (y/n): ", end="")
        response = input().lower().strip()
        if response in ['y', 'yes', 'sí', 's']:
            create_sample_data()
    
    print("\n✨ Script completat!")
    print("\n📝 Propers passos:")
    print("1. Executeu 'python scripts/preprocess_data.py' per processar les dades")
    print("2. Executeu 'streamlit run app.py' per llançar el dashboard")
    
    # Crear un fitxer .gitignore si no existeix
    gitignore_path = Path(".gitignore")
    if not gitignore_path.exists():
        gitignore_content = """
# Dades raw (grans fitxers CSV)
data/raw/*.csv
data/raw/*.zip

# Fitxers de sistema
.DS_Store
Thumbs.db
