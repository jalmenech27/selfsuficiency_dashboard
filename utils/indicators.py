"""
Indicators - Funcions per calcular indicadors i mètriques
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple

def calculate_correlations(df1: pd.DataFrame, df2: pd.DataFrame, 
                         col1: str, col2: str, merge_on: str = 'AreaName') -> Dict:
    """Calcula correlacions entre dues variables de diferents DataFrames"""
    
    merged = pd.merge(df1, df2, on=merge_on, how='inner')
    merged_clean = merged.dropna(subset=[col1, col2])
    
    if len(merged_clean) < 5:
        return {'correlation': np.nan, 'p_value': np.nan, 'n_samples': 0}
    
    correlation = merged_clean[col1].corr(merged_clean[col2])
      # Càlcul simplificat del p-value (aproximació)
    n = len(merged_clean)
    if abs(correlation) >= 0.999:  # Evitar divisió per zero
        p_value = 0.0
    else:
        try:
            from scipy import stats
            t_stat = correlation * np.sqrt((n - 2) / (1 - correlation**2))
            p_value = 2 * (1 - stats.norm.cdf(abs(t_stat)))
        except ImportError:
            # Fallback si scipy no està disponible
            p_value = np.nan
    
    return {
        'correlation': correlation,
        'p_value': p_value,
        'n_samples': n,
        'strength': interpret_correlation_strength(correlation)
    }

def interpret_correlation_strength(correlation: float) -> str:
    """Interpreta la força d'una correlació"""
    abs_corr = abs(correlation)
    
    if abs_corr >= 0.7:
        return 'Forta'
    elif abs_corr >= 0.5:
        return 'Moderada'
    elif abs_corr >= 0.3:
        return 'Feble'
    else:
        return 'Molt feble'

def calculate_yearly_growth(df: pd.DataFrame, value_col: str, 
                          group_cols: List[str] = ['AreaName']) -> pd.DataFrame:
    """Calcula el creixement anual per grups"""
    
    def growth_rate(series):
        if len(series) < 2:
            return np.nan
        return ((series.iloc[-1] / series.iloc[0]) ** (1 / (len(series) - 1)) - 1) * 100
    
    growth_data = df.groupby(group_cols)[value_col].apply(growth_rate).reset_index()
    growth_data.columns = group_cols + ['growth_rate']
    
    return growth_data

def calculate_regional_averages(df: pd.DataFrame, value_cols: List[str], 
                              regional_col: str = 'BlocRegional') -> pd.DataFrame:
    """Calcula mitjanes per blocs regionals"""
    
    if regional_col not in df.columns:
        return pd.DataFrame()
    
    regional_stats = df.groupby(regional_col)[value_cols].agg(['mean', 'std', 'count']).round(3)
    
    # Aplanar les columnes multinivell
    regional_stats.columns = [f'{col}_{stat}' for col, stat in regional_stats.columns]
    regional_stats = regional_stats.reset_index()
    
    return regional_stats

def identify_outliers(df: pd.DataFrame, value_col: str, method: str = 'iqr') -> pd.DataFrame:
    """Identifica valors atípics en un DataFrame"""
    
    df_clean = df.dropna(subset=[value_col])
    
    if method == 'iqr':
        Q1 = df_clean[value_col].quantile(0.25)
        Q3 = df_clean[value_col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outliers = df_clean[(df_clean[value_col] < lower_bound) | 
                           (df_clean[value_col] > upper_bound)]
        
    elif method == 'zscore':
        z_scores = np.abs((df_clean[value_col] - df_clean[value_col].mean()) / df_clean[value_col].std())
        outliers = df_clean[z_scores > 3]
    
    return outliers

def calculate_sustainability_index(ssr_data: pd.DataFrame, 
                                 footprint_data: pd.DataFrame,
                                 year: int = 2020) -> pd.DataFrame:
    """Calcula un índex de sostenibilitat combinant SSR i petjada de carboni"""
    
    # Filtrar per any
    ssr_year = ssr_data[ssr_data['Year'] == year]
    footprint_year = footprint_data[footprint_data['Year'] == year]
    
    # Merge datasets
    merged = pd.merge(
        ssr_year[['AreaName', 'SelfSufficiency']],
        footprint_year[['AreaName', 'FoodFootprintCO2']],
        on='AreaName',
        how='inner'
    )
    
    if merged.empty:
        return pd.DataFrame()
    
    # Normalitzar valors (0-1)
    merged['SSR_normalized'] = (merged['SelfSufficiency'] - merged['SelfSufficiency'].min()) / \
                              (merged['SelfSufficiency'].max() - merged['SelfSufficiency'].min())
    
    # Per footprint, valors més baixos són millors, així que invertim
    merged['Footprint_normalized'] = 1 - ((merged['FoodFootprintCO2'] - merged['FoodFootprintCO2'].min()) / \
                                          (merged['FoodFootprintCO2'].max() - merged['FoodFootprintCO2'].min()))
    
    # Índex de sostenibilitat (mitjana ponderada)
    merged['SustainabilityIndex'] = (0.6 * merged['SSR_normalized'] + 
                                   0.4 * merged['Footprint_normalized']) * 100
    
    return merged[['AreaName', 'SustainabilityIndex']].sort_values('SustainabilityIndex', ascending=False)

def calculate_trade_balance(imports_data: pd.DataFrame, 
                          exports_data: pd.DataFrame, 
                          year: int = 2020) -> pd.DataFrame:
    """Calcula el balanç comercial per país"""
    
    imports_year = imports_data[imports_data['Year'] == year]
    exports_year = exports_data[exports_data['Year'] == year]
    
    imports_agg = imports_year.groupby('AreaName')['ImportQuantity'].sum()
    exports_agg = exports_year.groupby('AreaName')['ExportQuantity'].sum()
    
    balance_df = pd.DataFrame({
        'AreaName': imports_agg.index.union(exports_agg.index),
        'TotalImports': imports_agg.reindex(imports_agg.index.union(exports_agg.index), fill_value=0),
        'TotalExports': exports_agg.reindex(imports_agg.index.union(exports_agg.index), fill_value=0)
    }).reset_index(drop=True)
    
    balance_df['TradeBalance'] = balance_df['TotalExports'] - balance_df['TotalImports']
    balance_df['TradeRatio'] = np.where(balance_df['TotalImports'] > 0,
                                       balance_df['TotalExports'] / balance_df['TotalImports'],
                                       np.inf)
    
    return balance_df

def get_top_products(data: pd.DataFrame, value_col: str, 
                    n_top: int = 10, year: Optional[int] = None) -> pd.DataFrame:
    """Obté els top N productes per un valor determinat"""
    
    if year is not None and 'Year' in data.columns:
        data = data[data['Year'] == year]
    
    if 'ItemName' not in data.columns:
        return pd.DataFrame()
    
    top_products = data.groupby('ItemName')[value_col].sum().sort_values(ascending=False).head(n_top)
    
    return pd.DataFrame({
        'ItemName': top_products.index,
        value_col: top_products.values
    })

def calculate_diversity_index(data: pd.DataFrame, 
                            group_col: str = 'AreaName',
                            value_col: str = 'Production') -> pd.DataFrame:
    """Calcula un índex de diversitat de producció (similar a Shannon)"""
    
    def shannon_diversity(series):
        proportions = series / series.sum()
        return -np.sum(proportions * np.log(proportions + 1e-10))  # Evitar log(0)
    
    diversity = data.groupby(group_col)[value_col].apply(shannon_diversity).reset_index()
    diversity.columns = [group_col, 'DiversityIndex']
    
    return diversity

def calculate_food_security_metrics(ssr_data: pd.DataFrame,
                                  production_data: pd.DataFrame,
                                  year: int = 2020) -> Dict[str, float]:
    """Calcula mètriques globals de seguretat alimentària"""
    
    ssr_year = ssr_data[ssr_data['Year'] == year]
    prod_year = production_data[production_data['Year'] == year]
    
    metrics = {}
    
    if not ssr_year.empty:
        metrics['global_ssr_mean'] = ssr_year['SelfSufficiency'].mean()
        metrics['global_ssr_std'] = ssr_year['SelfSufficiency'].std()
        metrics['countries_above_1'] = (ssr_year['SelfSufficiency'] >= 1.0).sum()
        metrics['countries_below_0_5'] = (ssr_year['SelfSufficiency'] < 0.5).sum()
        metrics['total_countries'] = len(ssr_year)
    
    if not prod_year.empty:
        metrics['total_production'] = prod_year['Production'].sum()
        metrics['mean_production_per_country'] = prod_year.groupby('AreaName')['Production'].sum().mean()
    
    return metrics

def analyze_gender_impact(ssr_data: pd.DataFrame, year: int = 2020) -> Dict[str, float]:
    """Analitza l'impacte del gènere en l'agricultura"""
    
    if 'WomenAgriShare' not in ssr_data.columns:
        return {'error': 'No hi ha dades de gènere disponibles'}
    
    year_data = ssr_data[ssr_data['Year'] == year].dropna(subset=['WomenAgriShare', 'SelfSufficiency'])
    
    if len(year_data) < 5:
        return {'error': 'Insuficients dades per a l\'anàlisi'}
    
    # Dividir en grups segons participació femenina
    high_women = year_data[year_data['WomenAgriShare'] >= year_data['WomenAgriShare'].median()]
    low_women = year_data[year_data['WomenAgriShare'] < year_data['WomenAgriShare'].median()]
    
    analysis = {
        'correlation_women_ssr': year_data['WomenAgriShare'].corr(year_data['SelfSufficiency']),
        'ssr_high_women_participation': high_women['SelfSufficiency'].mean(),
        'ssr_low_women_participation': low_women['SelfSufficiency'].mean(),
        'women_participation_mean': year_data['WomenAgriShare'].mean(),
        'women_participation_std': year_data['WomenAgriShare'].std(),
        'countries_analyzed': len(year_data)
    }
    
    analysis['gender_impact'] = analysis['ssr_high_women_participation'] - analysis['ssr_low_women_participation']
    
    return analysis
