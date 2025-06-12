"""
Panell de l'Autosuficiència Alimentària Global - Versió Integrada
Una sola pàgina amb navegació per seccions

Autor: Jordi Almiñana Domènech
Màster en Ciència de Dades (UOC) - Visualització de Dades
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from utils.loaders import load_all_data
from utils.indicators import calculate_correlations
from utils.plotting import create_color_palette, plot_choropleth_map

# ==========================================
# CONFIGURACIÓ PRINCIPAL
# ==========================================

st.set_page_config(
    page_title="🌾 Panell Global sobre \n l\'Autosuficiència Alimentària",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalitzat per millorar la navegació
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #2E8B57;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 2rem;
        font-weight: bold;
        color: #1E6B3F;
        border-bottom: 3px solid #90EE90;
        padding-bottom: 0.5rem;
        margin: 2rem 0 1rem 0;
    }
    .metric-container {
        background: linear-gradient(90deg, #f0f8f0 0%, #e8f5e8 100%);
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #2E8B57;
    }
    .quick-nav {
        position: sticky;
        top: 0;
        background: white;
        z-index: 999;
        padding: 1rem 0;
        border-bottom: 2px solid #90EE90;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# NAVEGACIÓ RÀPIDA
# ==========================================

def render_quick_navigation():
    """Renderitza la navegació ràpida entre seccions"""
    st.markdown('<div class="quick-nav">', unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        if st.button("📊 Resum", use_container_width=True):
            st.query_params = {"section": "resum"}
    with col2:
        if st.button("🗺️ Mapa", use_container_width=True):
            st.query_params = {"section": "mapa"}
    with col3:
        if st.button("📈 Evolució", use_container_width=True):
            st.query_params = {"section": "evolucio"}
    with col4:
        if st.button("🥗 Productes", use_container_width=True):
            st.query_params = {"section": "productes"}
    with col5:
        if st.button("🔗 Correlacions", use_container_width=True):
            st.query_params = {"section": "correlacions"}
    with col6:
        if st.button("👩‍🌾 Gènere", use_container_width=True):
            st.query_params = {"section": "genere"}
    
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# FUNCIONS AUXILIARS
# ==========================================

def format_number(value, decimals=2, suffix=""):
    """Formata números per a les mètriques"""
    if pd.isna(value):
        return "N/D"
    return f"{value:.{decimals}f}{suffix}"

def create_metric_card(title, value, help_text="", delta=None):
    """Crea una targeta de mètrica personalitzada"""
    with st.container():
        st.markdown(f'<div class="metric-container">', unsafe_allow_html=True)
        col1, col2 = st.columns([3, 1])
        with col1:
            st.metric(
                label=title,
                value=value,
                delta=delta,
                help=help_text
            )
        st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# SECCIONS DEL DASHBOARD
# ==========================================

def render_summary_section(data_dict, selected_year, selected_regions):
    """SECCIÓ 1: Resum i Indicadors Principals"""
    st.markdown('<h2 class="section-header" id="resum">📊 Indicadors Principals</h2>', 
                unsafe_allow_html=True)
    
    # Filtrar dades per l'any seleccionat
    ssr_year = data_dict['ssr'][data_dict['ssr']['Year'] == selected_year]
    ff_year = data_dict['footprint'][data_dict['footprint']['Year'] == selected_year]
    
    # Aplicar filtre regional si no és "Tots"
    if selected_regions != ["Tots"]:
        ssr_year = ssr_year[ssr_year['BlocRegional'].isin(selected_regions)]
        ff_year = ff_year[ff_year['BlocRegional'].isin(selected_regions)]
    
    # Mètriques principals
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_ssr = ssr_year['SelfSufficiency'].mean()
        create_metric_card(
            "Autosuficiència Mitjana",
            format_number(avg_ssr, 5),
            "Ràtio mitjana d'autosuficiència alimentària (1.0 = autosuficient)"
        )
    
    with col2:
        countries_count = len(ssr_year)
        create_metric_card(
            "Països Analitzats",
            str(countries_count),
            f"Nombre de països amb dades per {selected_year}"
        )
    
    with col3:
        avg_ff = ff_year['FoodFootprintCO2'].mean()
        create_metric_card(
            "Petjada CO₂ Mitjana",
            format_number(avg_ff, 5),
            "Emissions mitjanes de CO₂ per unitat de producció alimentària"
        )
    
    with col4:
        if 'WomenAgriShare' in ssr_year.columns:
            avg_women = ssr_year['WomenAgriShare'].mean()
            create_metric_card(
                "% Dones en Agricultura",
                format_number(avg_women, 2, "%"),  
                "Percentatge mitjà de participació femenina en agricultura"
            )
    
    # Distribucions dels indicadors
    st.subheader("Distribució dels Indicadors")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if not ssr_year.empty:
            fig_ssr_dist = px.histogram(
                ssr_year,
                x='SelfSufficiency',
                title='Distribució de l\'Autosuficiència Alimentària',
                labels={'SelfSufficiency': 'Autosuficiència', 'count': 'Nombre de Països'},
                nbins=30,
                color_discrete_sequence=['#2E8B57']
            )
            fig_ssr_dist.update_layout(height=400)
            st.plotly_chart(fig_ssr_dist, use_container_width=True)
    
    with col2:
        if not ff_year.empty:
            fig_ff_dist = px.histogram(
                ff_year,
                x='FoodFootprintCO2',
                title='Distribució de la Petjada de Carboni',
                labels={'FoodFootprintCO2': 'Petjada CO₂', 'count': 'Nombre de Països'},
                nbins=30,
                color_discrete_sequence=['#CD853F']
            )
            fig_ff_dist.update_layout(height=400)
            st.plotly_chart(fig_ff_dist, use_container_width=True)

def render_map_section(data_dict, selected_year, selected_regions):
    """SECCIÓ 2: Visualització Geogràfica"""
    st.markdown('<h2 class="section-header" id="mapa">🗺️ Distribució Global</h2>', 
                unsafe_allow_html=True)
    
    # Preparar dades per al mapa
    ssr_map_data = data_dict['ssr'][data_dict['ssr']['Year'] == selected_year]
    
    if not ssr_map_data.empty:
        ssr_aggregated = ssr_map_data.groupby('AreaName')['SelfSufficiency'].mean().reset_index()
        
        fig_map = px.choropleth(
            ssr_aggregated,
            locations='AreaName',
            color='SelfSufficiency',
            locationmode='country names',
            title=f'Autosuficiència Alimentària per País ({selected_year})',
            color_continuous_scale='RdYlGn',
            labels={'SelfSufficiency': 'Autosuficiència'},
            range_color=[0, 2]
        )
        
        fig_map.update_layout(
            height=600,
            geo=dict(
                showframe=False,
                showcoastlines=True,
                projection_type='equirectangular'
            )
        )
        
        st.plotly_chart(fig_map, use_container_width=True)
        
        # Mapa de petjada de carboni
        ff_map_data = data_dict['footprint'][data_dict['footprint']['Year'] == selected_year]
        
        if not ff_map_data.empty:
            ff_aggregated = ff_map_data.groupby('AreaName')['FoodFootprintCO2'].mean().reset_index()
            
            fig_map_ff = px.choropleth(
                ff_aggregated,
                locations='AreaName',
                color='FoodFootprintCO2',
                locationmode='country names',
                title=f'Petjada de Carboni per País ({selected_year})',
                color_continuous_scale='Reds',
                labels={'FoodFootprintCO2': 'Petjada CO₂'}
            )
            
            fig_map_ff.update_layout(
                height=600,
                geo=dict(
                    showframe=False,
                    showcoastlines=True,
                    projection_type='equirectangular'
                )
            )
            
            st.plotly_chart(fig_map_ff, use_container_width=True)

def render_evolution_section(data_dict, selected_regions):
    """SECCIÓ 3: Evolució Temporal"""
    st.markdown('<h2 class="section-header" id="evolucio">📈 Evolució Temporal</h2>', 
                unsafe_allow_html=True)
    
    # Evolució de l'autosuficiència per blocs regionals
    ssr_data = data_dict['ssr'].copy()
    
    if selected_regions != ["Tots"]:
        ssr_data = ssr_data[ssr_data['BlocRegional'].isin(selected_regions)]
    
    if not ssr_data.empty:
        ssr_evolution = ssr_data.groupby(['Year', 'BlocRegional'])['SelfSufficiency'].mean().reset_index()
        
        fig_evolution = px.line(
            ssr_evolution,
            x='Year',
            y='SelfSufficiency',
            color='BlocRegional',
            title='Evolució de l\'Autosuficiència per Bloc Regional',
            labels={'SelfSufficiency': 'Autosuficiència', 'Year': 'Any'}
        )
        
        fig_evolution.update_layout(height=500)
        st.plotly_chart(fig_evolution, use_container_width=True)
    
    # Evolució de la petjada de carboni
    ff_data = data_dict['footprint'].copy()
    
    if selected_regions != ["Tots"]:
        ff_data = ff_data[ff_data['BlocRegional'].isin(selected_regions)]
    
    if not ff_data.empty:
        ff_evolution = ff_data.groupby(['Year', 'BlocRegional'])['FoodFootprintCO2'].mean().reset_index()
        
        fig_ff_evolution = px.line(
            ff_evolution,
            x='Year',
            y='FoodFootprintCO2',
            color='BlocRegional',
            title='Evolució de la Petjada de Carboni per Bloc Regional',
            labels={'FoodFootprintCO2': 'Petjada CO₂', 'Year': 'Any'}
        )
        
        fig_ff_evolution.update_layout(height=500)
        st.plotly_chart(fig_ff_evolution, use_container_width=True)

def render_products_section(data_dict, selected_year):
    """SECCIÓ 4: Anàlisi de Productes"""
    st.markdown('<h2 class="section-header" id="productes">🥗 Anàlisi de Productes</h2>', 
                unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Top 10 Productes per Producció")
        
        prod_year = data_dict['production'][data_dict['production']['Year'] == selected_year]
        if not prod_year.empty:
            prod_top = prod_year.groupby('ItemName')['Production'].sum().sort_values(ascending=False).head(10)
            
            fig_prod = px.bar(
                x=prod_top.values,
                y=prod_top.index,
                orientation='h',
                title=f'Top 10 Productes per Producció ({selected_year})',
                labels={'x': 'Producció Total', 'y': 'Producte'},
                color_discrete_sequence=['#2E8B57']
            )
            fig_prod.update_layout(height=500)
            st.plotly_chart(fig_prod, use_container_width=True)
    
    with col2:
        st.subheader("Top 10 Productes per Importació")
        
        imports_year = data_dict['imports'][data_dict['imports']['Year'] == selected_year]
        if not imports_year.empty:
            imports_top = imports_year.groupby('ItemName')['ImportQuantity'].sum().sort_values(ascending=False).head(10)
            
            fig_imports = px.bar(
                x=imports_top.values,
                y=imports_top.index,
                orientation='h',
                title=f'Top 10 Productes per Importació ({selected_year})',
                labels={'x': 'Importació Total', 'y': 'Producte'},
                color_discrete_sequence=['#FF6347']
            )
            fig_imports.update_layout(height=500)
            st.plotly_chart(fig_imports, use_container_width=True)
    
    # Comparativa Import/Export dels mateixos productes
    st.subheader("Balanç Comercial per Producte")
    
    if not imports_year.empty and 'exports' in data_dict:
        exports_year = data_dict['exports'][data_dict['exports']['Year'] == selected_year]
        
        if not exports_year.empty:
            imports_agg = imports_year.groupby('ItemName')['ImportQuantity'].sum()
            exports_agg = exports_year.groupby('ItemName')['ExportQuantity'].sum()
            
            # Productes comuns
            common_items = set(imports_agg.index) & set(exports_agg.index)
            if common_items:
                balance_data = []
                for item in list(common_items)[:15]:  # Top 15 per evitar saturació
                    balance_data.append({
                        'Producte': item,
                        'Importacions': imports_agg[item],
                        'Exportacions': exports_agg[item],
                        'Balanç': exports_agg[item] - imports_agg[item]
                    })
                
                balance_df = pd.DataFrame(balance_data)
                balance_df = balance_df.sort_values('Balanç', key=abs, ascending=False).head(10)
                
                fig_balance = go.Figure()
                
                fig_balance.add_trace(go.Bar(
                    name='Importacions',
                    x=balance_df['Producte'],
                    y=balance_df['Importacions'],
                    marker_color='red',
                    opacity=0.7
                ))
                
                fig_balance.add_trace(go.Bar(
                    name='Exportacions',
                    x=balance_df['Producte'],
                    y=balance_df['Exportacions'],
                    marker_color='green',
                    opacity=0.7
                ))
                
                fig_balance.update_layout(
                    title='Comparativa Import-Export per Producte',
                    xaxis_title='Producte',
                    yaxis_title='Quantitat',
                    barmode='group',
                    height=500
                )
                
                st.plotly_chart(fig_balance, use_container_width=True)

def render_correlations_section(data_dict, selected_year):
    """SECCIÓ 5: Anàlisi de Correlacions"""
    st.markdown('<h2 class="section-header" id="correlacions">🔗 Anàlisi de Correlacions</h2>', 
                unsafe_allow_html=True)
    
    # Combinar dades per a l'anàlisi de correlacions
    ssr_year = data_dict['ssr'][data_dict['ssr']['Year'] == selected_year]
    ff_year = data_dict['footprint'][data_dict['footprint']['Year'] == selected_year]
    
    if not ssr_year.empty and not ff_year.empty:
        merged_data = pd.merge(
            ssr_year[['AreaName', 'SelfSufficiency', 'WomenAgriShare']],
            ff_year[['AreaName', 'FoodFootprintCO2']],
            on='AreaName',
            how='inner'
        )
        
        if len(merged_data) > 5:
            col1, col2 = st.columns(2)
            
            with col1:                # Correlació Autosuficiència vs Petjada CO2
                try:
                    fig_corr1 = px.scatter(
                        merged_data,
                        x='SelfSufficiency',
                        y='FoodFootprintCO2',
                        title='Autosuficiència vs Petjada de Carboni',
                        labels={
                            'SelfSufficiency': 'Autosuficiència',
                            'FoodFootprintCO2': 'Petjada CO₂'
                        },
                        trendline='ols',
                        hover_data=['AreaName']
                    )
                except Exception:
                    # Fallback sense trendline si statsmodels no està disponible
                    fig_corr1 = px.scatter(
                        merged_data,
                        x='SelfSufficiency',
                        y='FoodFootprintCO2',
                        title='Autosuficiència vs Petjada de Carboni',
                        labels={
                            'SelfSufficiency': 'Autosuficiència',
                            'FoodFootprintCO2': 'Petjada CO₂'
                        },
                        hover_data=['AreaName']
                    )
                fig_corr1.update_traces(marker=dict(size=8, opacity=0.7))
                st.plotly_chart(fig_corr1, use_container_width=True)
                
                # Estadístiques de correlació
                correlation_1 = merged_data['SelfSufficiency'].corr(merged_data['FoodFootprintCO2'])
                
                if correlation_1 < -0.3:
                    st.success(f"📈 Correlació negativa moderada: {correlation_1:.3f}")
                elif correlation_1 > 0.3:
                    st.warning(f"📉 Correlació positiva moderada: {correlation_1:.3f}")
                else:
                    st.info(f"➡️ Correlació feble: {correlation_1:.3f}")
            
            with col2:                # Correlació Participació Femenina vs Autosuficiència
                if 'WomenAgriShare' in merged_data.columns:
                    merged_gender = merged_data.dropna(subset=['WomenAgriShare'])
                    if len(merged_gender) > 5:
                        try:
                            fig_corr2 = px.scatter(
                                merged_gender,
                                x='WomenAgriShare',
                                y='SelfSufficiency',
                                title='Participació Femenina vs Autosuficiència',
                                labels={
                                    'WomenAgriShare': '% Dones en Agricultura',
                                    'SelfSufficiency': 'Autosuficiència'
                                },
                                trendline='ols',
                                hover_data=['AreaName']
                            )
                        except Exception:
                            # Fallback sense trendline
                            fig_corr2 = px.scatter(
                                merged_gender,
                                x='WomenAgriShare',
                                y='SelfSufficiency',
                                title='Participació Femenina vs Autosuficiència',
                                labels={
                                    'WomenAgriShare': '% Dones en Agricultura',
                                    'SelfSufficiency': 'Autosuficiència'
                                },
                                hover_data=['AreaName']
                            )
                        fig_corr2.update_traces(marker=dict(size=8, opacity=0.7))
                        st.plotly_chart(fig_corr2, use_container_width=True)
                        
                        correlation_2 = merged_gender['WomenAgriShare'].corr(merged_gender['SelfSufficiency'])
                        
                        if correlation_2 < -0.3:
                            st.warning(f"📉 Correlació negativa moderada: {correlation_2:.3f}")
                        elif correlation_2 > 0.3:
                            st.success(f"📈 Correlació positiva moderada: {correlation_2:.3f}")
                        else:
                            st.info(f"➡️ Correlació feble: {correlation_2:.3f}")

def render_gender_section(data_dict, selected_year, selected_regions):
    """SECCIÓ 6: Anàlisi de Gènere"""
    st.markdown('<h2 class="section-header" id="genere">👩‍🌾 Perspectiva de Gènere</h2>', 
                unsafe_allow_html=True)
    
    ssr_data = data_dict['ssr']
    
    if 'WomenAgriShare' in ssr_data.columns:
        # Filtrar per regions si no és "Tots"
        if selected_regions != ["Tots"]:
            ssr_data = ssr_data[ssr_data['BlocRegional'].isin(selected_regions)]
        
        gender_data = ssr_data[ssr_data['WomenAgriShare'].notna()]
        gender_year = gender_data[gender_data['Year'] == selected_year]
        
        if not gender_year.empty:
            col1, col2 = st.columns(2)
            
            with col1:
                # Distribució de participació femenina
                fig_gender_dist = px.histogram(
                    gender_year,
                    x='WomenAgriShare',
                    title='Distribució de Participació Femenina en Agricultura',
                    labels={'WomenAgriShare': '% Dones en Agricultura'},
                    nbins=20,
                    color_discrete_sequence=['#FF69B4']
                )
                st.plotly_chart(fig_gender_dist, use_container_width=True)
            
            with col2:
                # Participació femenina per bloc regional
                if 'BlocRegional' in gender_year.columns:
                    gender_by_bloc = gender_year.groupby('BlocRegional')['WomenAgriShare'].mean().sort_values(ascending=True)
                    
                    fig_gender_bloc = px.bar(
                        x=gender_by_bloc.values,
                        y=gender_by_bloc.index,
                        orientation='h',
                        title='Participació Femenina Mitjana per Bloc Regional',
                        labels={'x': '% Dones en Agricultura', 'y': 'Bloc Regional'},
                        color_discrete_sequence=['#FF69B4']
                    )
                    fig_gender_bloc.update_layout(height=400)
                    st.plotly_chart(fig_gender_bloc, use_container_width=True)
        
        # Evolució temporal de la participació femenina
        st.subheader("Evolució de la Participació Femenina")
        
        if not gender_data.empty:
            gender_evolution = gender_data.groupby(['Year', 'BlocRegional'])['WomenAgriShare'].mean().reset_index()
            
            fig_gender_evolution = px.line(
                gender_evolution,
                x='Year',
                y='WomenAgriShare',
                color='BlocRegional',
                title='Evolució de la Participació Femenina per Bloc Regional',
                labels={'WomenAgriShare': '% Dones en Agricultura', 'Year': 'Any'}
            )
            
            fig_gender_evolution.update_layout(height=500)
            st.plotly_chart(fig_gender_evolution, use_container_width=True)

# ==========================================
# APLICACIÓ PRINCIPAL
# ==========================================

def main():
    """Aplicació principal del panell"""
    
    # Títol principal
    st.markdown("""
    <div style='text-align: center; margin-bottom: 3rem;'>
        <h1 style='color: #2E8B57; margin-bottom: 0.5rem; font-size: 4rem; font-weight: 700;'>
            🌍 Panell Global
        </h1>
        <h2 style='color: #4682B4; margin-top: 0; font-weight: 300; font-size: 2.5rem;'>
            Autosuficiència Alimentària
        </h2>
        <hr style='width: 50%; margin: 1rem auto; border: 2px solid #2E8B57;'>
    </div>
    """, unsafe_allow_html=True)
    
    # Navegació ràpida
    render_quick_navigation()
    
    # Sidebar per controls
    st.sidebar.header("⚙️ Controls del Panell")
    
    # Càrrega de dades
    with st.spinner("Carregant dades..."):
        try:
            data_dict = load_all_data()
            st.sidebar.success("✅ Dades carregades correctament")
        except Exception as e:
            st.error(f"❌ Error carregant dades: {str(e)}")
            st.stop()
    
    # Controls del sidebar
    years_available = sorted(data_dict['ssr']['Year'].dropna().unique())
    selected_year = st.sidebar.selectbox(
        "📅 Selecciona l'any:",
        years_available,
        index=len(years_available)-5 if len(years_available) > 5 else -1
    )
    
    # Filtre per blocs regionals
    available_blocs = ['Tots'] + sorted(data_dict['ssr']['BlocRegional'].dropna().unique().tolist())
    selected_regions = st.sidebar.multiselect(
        "🌐 Selecciona blocs regionals:",
        available_blocs,
        default=["Tots"]
    )
    
    if not selected_regions:
        selected_regions = ["Tots"]
    
    # Informació del sidebar
    st.sidebar.markdown("---")
    st.sidebar.info("""
    **Fonts de Dades:**
    - FAOSTAT (FAO)
    - World Bank
    
    **Període:** 1961-2023
    **Països:** 245+
    """)
    
    # Renderitzar totes les seccions
    render_summary_section(data_dict, selected_year, selected_regions)
    render_map_section(data_dict, selected_year, selected_regions)
    render_evolution_section(data_dict, selected_regions)
    render_products_section(data_dict, selected_year)
    render_correlations_section(data_dict, selected_year)
    render_gender_section(data_dict, selected_year, selected_regions)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p><strong>Panell de l'Autosuficiència Alimentària Global</strong></p>
        <p>Desenvolupat per <strong>Jordi Almiñana Domènech</strong> - Màster en Ciència de Dades (UOC)</p>
        <p>Assignatura: Visualització de Dades | Fonts: FAOSTAT, World Bank</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
