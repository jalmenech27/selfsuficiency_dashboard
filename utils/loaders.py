"""
Loaders - Funcions per carregar les dades preprocessades
Compatibilitat amb dades comprimides i sistema original
"""

import pandas as pd
import streamlit as st
import os
from typing import Dict, Optional

# ==========================================
# BLOCS REGIONALS
# ==========================================

REGIONAL_BLOCS = {
    'EU27': [
        'Austria', 'Belgium', 'Bulgaria', 'Croatia', 'Cyprus', 'Czechia',
        'Denmark', 'Estonia', 'Finland', 'France', 'Germany', 'Greece',
        'Hungary', 'Ireland', 'Italy', 'Latvia', 'Lithuania', 'Luxembourg',
        'Malta', 'Netherlands', 'Poland', 'Portugal', 'Romania', 'Slovakia',
        'Slovenia', 'Spain', 'Sweden'
    ],
    'Amèrica Llatina i Carib': [
        'Antigua and Barbuda', 'Argentina', 'Bahamas', 'Barbados', 'Belize',
        'Bolivia (Plurinational State of)', 'Brazil', 'Chile', 'Colombia',
        'Costa Rica', 'Cuba', 'Dominica', 'Dominican Republic', 'Ecuador',
        'El Salvador', 'Grenada', 'Guatemala', 'Guyana', 'Haiti', 'Honduras',
        'Jamaica', 'Mexico', 'Nicaragua', 'Panama', 'Paraguay', 'Peru',
        'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Vincent and the Grenadines',
        'Suriname', 'Trinidad and Tobago', 'Uruguay', 'Venezuela (Bolivarian Republic of)'
    ],
    'Àfrica Subsahariana': [
        'Angola', 'Benin', 'Botswana', 'Burkina Faso', 'Burundi', 'Cabo Verde',
        'Cameroon', 'Central African Republic', 'Chad', 'Comoros', 'Congo',
        "Côte d'Ivoire", 'Democratic Republic of the Congo', 'Djibouti',
        'Equatorial Guinea', 'Eritrea', 'Eswatini', 'Ethiopia', 'Gabon',
        'Gambia', 'Ghana', 'Guinea', 'Guinea-Bissau', 'Kenya', 'Lesotho',
        'Liberia', 'Madagascar', 'Malawi', 'Mali', 'Mauritania', 'Mauritius',
        'Mozambique', 'Namibia', 'Niger', 'Nigeria', 'Rwanda',
        'Sao Tome and Principe', 'Senegal', 'Seychelles', 'Sierra Leone',
        'Somalia', 'South Africa', 'South Sudan', 'Sudan', 'Togo', 'Uganda',
        'United Republic of Tanzania', 'Zambia', 'Zimbabwe'
    ],
    'Nord d\'Àfrica': [
        'Algeria', 'Egypt', 'Libya', 'Morocco', 'Tunisia'
    ],
    'Àsia Oriental i Sud-oriental': [
        'Brunei Darussalam', 'Cambodia', 'China', 'China, Hong Kong SAR',
        'China, Macao SAR', "Democratic People's Republic of Korea", 'Indonesia',
        'Japan', "Lao People's Democratic Republic", 'Malaysia', 'Mongolia',
        'Myanmar', 'Philippines', 'Republic of Korea', 'Singapore', 'Thailand',
        'Timor-Leste', 'Viet Nam'
    ],
    'Àsia Meridional': [
        'Afghanistan', 'Bangladesh', 'Bhutan', 'India', 'Iran (Islamic Republic of)',
        'Maldives', 'Nepal', 'Pakistan', 'Sri Lanka'
    ],
    'Àsia Occidental i Àsia Central': [
        'Armenia', 'Azerbaijan', 'Bahrain', 'Cyprus', 'Georgia', 'Iraq',
        'Israel', 'Jordan', 'Kazakhstan', 'Kuwait', 'Kyrgyzstan', 'Lebanon',
        'Oman', 'Qatar', 'Saudi Arabia', 'State of Palestine', 'Syrian Arab Republic',
        'Tajikistan', 'Turkey', 'Turkmenistan', 'United Arab Emirates',
        'Uzbekistan', 'Yemen'
    ],
    'Amèrica del Nord': [
        'Canada', 'United States of America'
    ],
    'Oceania': [
        'Australia', 'Fiji', 'Kiribati', 'Marshall Islands', 'Micronesia (Federated States of)',
        'Nauru', 'New Zealand', 'Palau', 'Papua New Guinea', 'Samoa', 'Solomon Islands',
        'Tonga', 'Tuvalu', 'Vanuatu'
    ]
}

def prepare_regional_mappings():
    """Prepara mappings de blocs regionals a països"""
    normalized_blocs = {
        bloc_name: [country.lower().strip() for country in country_list]
        for bloc_name, country_list in REGIONAL_BLOCS.items()
    }
    
    country_to_bloc_map = {}
    for bloc_name, countries_in_bloc in normalized_blocs.items():
        for country in countries_in_bloc:
            country_to_bloc_map[country] = bloc_name
            
    return normalized_blocs, country_to_bloc_map

def add_regional_bloc(df):
    """Afegeix bloc regional a un DataFrame"""
    if 'AreaName' not in df.columns:
        return df
    
    _, country_to_bloc_map = prepare_regional_mappings()
    
    df = df.copy()
    df['AreaName_lower'] = df['AreaName'].astype(str).str.lower().str.strip()
    df['BlocRegional'] = df['AreaName_lower'].map(country_to_bloc_map)
    df = df.drop('AreaName_lower', axis=1)
    
    # Afegeix "Altres" per països no assignats
    df['BlocRegional'] = df['BlocRegional'].fillna('Altres')
    
    return df

# ==========================================
# LOADERS PER DADES PREPROCESSADES
# ==========================================

@st.cache_data
def load_ssr_data() -> pd.DataFrame:
    """Carrega dades d'autosuficiència amb informació de gènere"""
    compressed_path = 'data/ssr_women.csv.gz'
    original_path = 'data/fao_QCL.csv'
    
    if os.path.exists(compressed_path):
        df = pd.read_csv(compressed_path, compression='gzip')
        # Afegir blocs regionals si no els té
        if 'BlocRegional' not in df.columns:
            df = add_regional_bloc(df)
        return df
    elif os.path.exists(original_path):
        # Fallback al sistema original (cal implementar la lògica de processament)
        st.warning("Usant dades originals. Per millor rendiment, utilitza dades preprocessades.")
        return load_original_ssr_data()
    else:
        st.error("No s'han trobat dades d'autosuficiència.")
        return pd.DataFrame()

@st.cache_data
def load_footprint_data() -> pd.DataFrame:
    """Carrega dades de petjada alimentària"""
    compressed_path = 'data/food_footprint.csv.gz'
    original_path = 'data/fao_ET.csv'
    
    if os.path.exists(compressed_path):
        df = pd.read_csv(compressed_path, compression='gzip')
        if 'BlocRegional' not in df.columns:
            df = add_regional_bloc(df)
        return df
    elif os.path.exists(original_path):
        st.warning("Usant dades originals per petjada alimentària.")
        return load_original_footprint_data()
    else:
        st.error("No s'han trobat dades de petjada alimentària.")
        return pd.DataFrame()

@st.cache_data
def load_production_data() -> pd.DataFrame:
    """Carrega dades de producció"""
    compressed_path = 'data/production.csv.gz'
    
    if os.path.exists(compressed_path):
        return pd.read_csv(compressed_path, compression='gzip')
    else:
        st.warning("No s'han trobat dades de producció preprocessades.")
        return pd.DataFrame()

@st.cache_data
def load_imports_data() -> pd.DataFrame:
    """Carrega dades d'importacions"""
    compressed_path = 'data/imports.csv.gz'
    
    if os.path.exists(compressed_path):
        return pd.read_csv(compressed_path, compression='gzip')
    else:
        st.warning("No s'han trobat dades d'importacions preprocessades.")
        return pd.DataFrame()

@st.cache_data
def load_exports_data() -> pd.DataFrame:
    """Carrega dades d'exportacions"""
    compressed_path = 'data/exports.csv.gz'
    
    if os.path.exists(compressed_path):
        return pd.read_csv(compressed_path, compression='gzip')
    else:
        st.warning("No s'han trobat dades d'exportacions preprocessades.")
        return pd.DataFrame()

@st.cache_data
def load_lookup_tables() -> tuple:
    """Carrega taules de lookup"""
    area_path = 'data/area_map.csv.gz'
    item_path = 'data/item_map.csv.gz'
    
    area_map = pd.DataFrame()
    item_map = pd.DataFrame()
    
    if os.path.exists(area_path):
        area_map = pd.read_csv(area_path, compression='gzip')
    
    if os.path.exists(item_path):
        item_map = pd.read_csv(item_path, compression='gzip')
    
    return area_map, item_map

# ==========================================
# FUNCIÓ PRINCIPAL PER CARREGAR TOT
# ==========================================

def load_all_data() -> Dict[str, pd.DataFrame]:
    """Carrega totes les dades necessàries per al dashboard"""
    
    data_dict = {
        'ssr': load_ssr_data(),
        'footprint': load_footprint_data(), 
        'production': load_production_data(),
        'imports': load_imports_data(),
        'exports': load_exports_data()
    }
    
    # Carregar lookup tables
    area_map, item_map = load_lookup_tables()
    data_dict['area_map'] = area_map
    data_dict['item_map'] = item_map
    
    return data_dict

# ==========================================
# FALLBACK FUNCTIONS (per compatibilitat)
# ==========================================

def load_original_ssr_data() -> pd.DataFrame:
    """Fallback per carregar i processar dades originals de SSR"""
    # Aquesta funció es pot implementar si es vol mantenir compatibilitat
    # amb el sistema original de descàrrega de dades
    return pd.DataFrame()

def load_original_footprint_data() -> pd.DataFrame:
    """Fallback per carregar i processar dades originals de footprint"""
    return pd.DataFrame()

# ==========================================
# FUNCIONS DE VERIFICACIÓ
# ==========================================

def check_data_availability() -> Dict[str, bool]:
    """Verifica quines dades estan disponibles"""
    availability = {
        'ssr_compressed': os.path.exists('data/ssr_women.csv.gz'),
        'footprint_compressed': os.path.exists('data/food_footprint.csv.gz'),
        'production_compressed': os.path.exists('data/production.csv.gz'),
        'imports_compressed': os.path.exists('data/imports.csv.gz'),
        'exports_compressed': os.path.exists('data/exports.csv.gz'),
        'ssr_original': os.path.exists('data/fao_QCL.csv'),
        'footprint_original': os.path.exists('data/fao_ET.csv'),
    }
    
    return availability

def get_data_info() -> Dict[str, str]:
    """Retorna informació sobre les dades disponibles"""
    availability = check_data_availability()
    
    info = {
        'mode': 'compressed' if availability['ssr_compressed'] else 'original' if availability['ssr_original'] else 'none',
        'files_available': sum(availability.values()),
        'total_files': len(availability)
    }
    
    return info
