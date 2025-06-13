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
    page_title="🌾 Panell de l'Autosuficiència Alimentària Global",
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
    
    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
    
    with col1:
        if st.button("📊 Resum", use_container_width=True):
            st.query_params = {"section": "resum"}
    with col2:
        if st.button("🗺️ Mapa", use_container_width=True):
            st.query_params = {"section": "mapa"}
    with col3:
        if st.button("🌍 Global", use_container_width=True):
            st.query_params = {"section": "global"}
    with col4:
        if st.button("📈 Evolució", use_container_width=True):
            st.query_params = {"section": "evolucio"}
    with col5:
        if st.button("🥗 Productes", use_container_width=True):
            st.query_params = {"section": "productes"}
    with col6:
        if st.button("🔗 Correlacions", use_container_width=True):
            st.query_params = {"section": "correlacions"}
    with col7:
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
    
    st.markdown("""
    <div style='background: linear-gradient(90deg, #f0f8f0 0%, #e8f5e8 100%); 
                padding: 1rem; border-radius: 10px; margin-bottom: 2rem;'>
        <h4 style='color: #1e5631; margin-bottom: 0.5rem;'>📊 Resum Executiu dels Indicadors Clau</h4>
        <p style='margin: 0; color: #374151;'>
            Visualitza les mètriques fonamentals d'autosuficiència alimentària, petjada de carboni i participació femenina 
            per comprendre l'estat actual del sistema alimentari mundial.
        </p>
        <p style='margin: 0.5rem 0 0 0; color: #dc2626; font-weight: 600;'>
            ⚠️ Nota important: Les dades de SSR (Self-Sufficiency Ratio) només estan disponibles fins a l'any 2013.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
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
            format_number(avg_ssr, 3),  # Canviat a 3 decimals
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
            format_number(avg_ff, 4),  # Canviat a 4 decimals
            "Emissions mitjanes de CO₂ per unitat de producció alimentària"
        )
    
    with col4:
        if 'WomenAgriShare' in ssr_year.columns:
            avg_women = ssr_year['WomenAgriShare'].mean()
            create_metric_card(
                "% Dones en Agricultura",
                format_number(avg_women, 1, "%"),  # Mantenim 1 decimal per percentatges
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
    
    st.markdown("""
    <div style='background: linear-gradient(90deg, #f0f8ff 0%, #e6f3ff 100%); 
                padding: 1rem; border-radius: 10px; margin-bottom: 2rem;'>
        <h4 style='color: #1e3a8a; margin-bottom: 0.5rem;'>🗺️ Perspectiva Geogràfica de l'Autosuficiència Alimentària</h4>
        <p style='margin: 0; color: #374151;'>
            Explora la distribució espacial de l'autosuficiència alimentària i la petjada de carboni per països. 
            Els mapes coroplets revelen patrons geogràfics i permeten identificar regions amb major o menor            dependència alimentària externa.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
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
    
    st.markdown("""
    <div style='background: linear-gradient(90deg, #fff8f0 0%, #fef3e2 100%); 
                padding: 1rem; border-radius: 10px; margin-bottom: 2rem;'>
        <h4 style='color: #8b4513; margin-bottom: 0.5rem;'>📈 Tendències Temporals dels Indicadors Alimentaris</h4>
        <p style='margin: 0; color: #374151;'>
            Analitza l'evolució històrica de l'autosuficiència alimentària i la petjada de carboni per blocs regionals. 
            Les línies destacades en negre mostren la mitjana mundial per contextualitzar les tendències regionals.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Evolució de l'autosuficiència per blocs regionals
    ssr_data = data_dict['ssr'].copy()
    
    # Calcular mitjana mundial (sempre amb totes les dades)
    global_evolution = data_dict['ssr'].groupby('Year')['SelfSufficiency'].mean().reset_index()
    
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
        
        # Afegir línia de mitjana mundial destacada
        fig_evolution.add_trace(
            go.Scatter(
                x=global_evolution['Year'],
                y=global_evolution['SelfSufficiency'],
                mode='lines',
                name='🌍 Mitjana Mundial',
                line=dict(color='black', width=4, dash='solid'),
                hovertemplate='<b>Mitjana Mundial</b><br>Any: %{x}<br>Autosuficiència: %{y:.3f}<extra></extra>'
            )
        )
        
        fig_evolution.update_layout(
            height=500,
            hovermode='x unified',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        st.plotly_chart(fig_evolution, use_container_width=True)
      # Evolució de la petjada de carboni
    ff_data = data_dict['footprint'].copy()
    
    # Calcular mitjana mundial de petjada de carboni
    global_ff_evolution = data_dict['footprint'].groupby('Year')['FoodFootprintCO2'].mean().reset_index()
    
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
        
        # Afegir línia de mitjana mundial destacada
        fig_ff_evolution.add_trace(
            go.Scatter(
                x=global_ff_evolution['Year'],
                y=global_ff_evolution['FoodFootprintCO2'],
                mode='lines',
                name='🌍 Mitjana Mundial',
                line=dict(color='black', width=4, dash='solid'),
                hovertemplate='<b>Mitjana Mundial</b><br>Any: %{x}<br>Petjada CO₂: %{y:.4f}<extra></extra>'
            )
        )
        
        fig_ff_evolution.update_layout(
            height=500,
            hovermode='x unified',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        st.plotly_chart(fig_ff_evolution, use_container_width=True)

def create_color_palette_for_products(prod_top_df=None, imports_top_df=None, exports_top_df=None):
    """Crea una paleta de colors consistents per als productes entre diferents gràfics (del notebook)"""
    # Recollir tots els noms de productes únics
    all_top_product_names = set()
    
    if prod_top_df is not None and not prod_top_df.empty:
        all_top_product_names.update(prod_top_df.index.tolist())
    
    if imports_top_df is not None and not imports_top_df.empty:
        all_top_product_names.update(imports_top_df.index.tolist())
    
    if exports_top_df is not None and not exports_top_df.empty:
        all_top_product_names.update(exports_top_df.index.tolist())
    
    # Si no hi ha productes, retorna un diccionari buit
    if not all_top_product_names:
        return {}
    
    # Crear mapa de colors
    color_palette = px.colors.qualitative.Light24
    sorted_names_list = sorted(list(all_top_product_names))
    product_color_map = {
        name: color_palette[i % len(color_palette)] 
        for i, name in enumerate(sorted_names_list)
    }
    
    return product_color_map

def render_products_section(data_dict, selected_year):
    """SECCIÓ 4: Anàlisi de Productes"""
    st.markdown('<h2 class="section-header" id="productes">🥗 Anàlisi de Productes</h2>', 
                unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background: linear-gradient(90deg, #f0fff4 0%, #e6fffa 100%); 
                padding: 1rem; border-radius: 10px; margin-bottom: 2rem;'>
        <h4 style='color: #065f46; margin-bottom: 0.5rem;'>🥗 Panorama dels Productes Alimentaris Globals</h4>
        <p style='margin: 0; color: #374151;'>
            Descobreix els principals productes alimentaris a nivell mundial per producció, importació i exportació. 
            L'anàlisi del balanç comercial revela quin productes són exportadors o importadors nets, 
            proporcionant una visió del comerç alimentari global.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Preparar dades agregades per a tots els gràfics
    prod_year = data_dict['production'][data_dict['production']['Year'] == selected_year] if 'production' in data_dict else pd.DataFrame()
    imports_year = data_dict['imports'][data_dict['imports']['Year'] == selected_year] if 'imports' in data_dict else pd.DataFrame()
    exports_year = data_dict['exports'][data_dict['exports']['Year'] == selected_year] if 'exports' in data_dict else pd.DataFrame()
    
    # Calcular tops per a cada categoria
    prod_top = prod_year.groupby('ItemName')['Production'].sum().sort_values(ascending=False).head(20) if not prod_year.empty else pd.Series()
    imports_top = imports_year.groupby('ItemName')['ImportQuantity'].sum().sort_values(ascending=False).head(20) if not imports_year.empty else pd.Series()
    exports_top = exports_year.groupby('ItemName')['ExportQuantity'].sum().sort_values(ascending=False).head(20) if not exports_year.empty else pd.Series()
    
    # Crear paleta de colors consistent
    product_color_map = create_color_palette_for_products(prod_top, imports_top, exports_top)
    
    # 1. TOP PRODUCTES PER CATEGORIA
    st.subheader("📊 Top 20 Productes per Categoria")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Producció Mundial**")
        
        if not prod_top.empty:
            # Convertir a milions de tones
            prod_top_display = (prod_top / 1000).head(10)  # Mostrar top 10
            
            # Crear colors per als productes
            colors = [product_color_map.get(item, '#2E8B57') for item in prod_top_display.index]
            
            fig_prod = px.bar(
                x=prod_top_display.values,
                y=prod_top_display.index,
                orientation='h',
                title=f'Top 10 Productes per Producció ({selected_year})',
                labels={'x': 'Producció Total (Milions de Tones)', 'y': 'Producte'},
                color=prod_top_display.index,
                color_discrete_map=product_color_map
            )
            fig_prod.update_layout(height=500, showlegend=False)
            st.plotly_chart(fig_prod, use_container_width=True)
    
    with col2:
        st.markdown("**Importacions Mundials**")
        
        if not imports_top.empty:
            imports_top_display = (imports_top / 1000).head(10)  # Convertir i mostrar top 10
            
            fig_imports = px.bar(
                x=imports_top_display.values,
                y=imports_top_display.index,
                orientation='h',
                title=f'Top 10 Productes per Importació ({selected_year})',
                labels={'x': 'Importació Total (Milions de Tones)', 'y': 'Producte'},
                color=imports_top_display.index,
                color_discrete_map=product_color_map
            )
            fig_imports.update_layout(height=500, showlegend=False)
            st.plotly_chart(fig_imports, use_container_width=True)
    
    # 2. TOP PRODUCTES PER EXPORTACIÓ
    if not exports_top.empty:
        st.subheader("📤 Top 20 Productes per Exportació")
        
        exports_top_display = (exports_top / 1000).head(20)  # Convertir i mostrar top 20
        
        fig_exports = px.bar(
            exports_top_display,
            x=exports_top_display.index,
            y=exports_top_display.values,
            title=f"Top 20 Productes per Volum d'Exportació Total ({selected_year})",
            labels={'y': "Exportació Total (Milions de Tones)", 'x': 'Producte'},
            color=exports_top_display.index,
            color_discrete_map=product_color_map
        )
        fig_exports.update_xaxes(tickangle=45)
        fig_exports.update_layout(showlegend=False, height=500)
        st.plotly_chart(fig_exports, use_container_width=True)
      # 3. ANÀLISI AVANÇADA DE BALANÇ COMERCIAL
    st.subheader("⚖️ Anàlisi Detallada del Balanç Comercial")
    
    if not imports_year.empty and not exports_year.empty:
        # Agregar imports i exports
        imports_agg = imports_year.groupby('ItemName')['ImportQuantity'].sum()
        exports_agg = exports_year.groupby('ItemName')['ExportQuantity'].sum()
        
        # Productes comuns amb volums significatius
        common_items = set(imports_agg.index) & set(exports_agg.index)
        
        if common_items:
            balance_data = []
            for item in common_items:
                imports_val = imports_agg[item] / 1000  # Convertir a milions de tones
                exports_val = exports_agg[item] / 1000  # Convertir a milions de tones
                balance_val = exports_val - imports_val
                
                # Només incloure productes amb volums significatius (> 0.1M tones)
                if imports_val > 0.1 or exports_val > 0.1:
                    balance_data.append({
                        'Producte': item,
                        'Importacions': imports_val,
                        'Exportacions': exports_val,
                        'Balanç': balance_val,
                        'Volum Total': imports_val + exports_val
                    })
            
            if balance_data:
                balance_df = pd.DataFrame(balance_data)
                
                # Ordenar per volum absolut de balanç i prendre top 15
                balance_df['Balanç Absolut'] = balance_df['Balanç'].abs()
                balance_df = balance_df.sort_values('Balanç Absolut', ascending=False).head(15)
                
                # Classificar tipus de balanç
                balance_df['Tipus'] = balance_df['Balanç'].apply(
                    lambda x: 'Exportador Net' if x > 0 else 'Importador Net'
                )
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Gràfic de balanç net
                    fig_balance_net = px.bar(
                        balance_df.sort_values('Balanç'),
                        x='Balanç',
                        y='Producte',
                        orientation='h',
                        color='Tipus',
                        color_discrete_map={'Exportador Net': 'green', 'Importador Net': 'red'},
                        title=f'Balanç Comercial Net per Producte ({selected_year})',
                        labels={'Balanç': 'Balanç Net (Milions de Tones)', 'Producte': 'Producte'}
                    )
                    fig_balance_net.add_vline(x=0, line_dash="dash", line_color="black", opacity=0.5)
                    fig_balance_net.update_layout(height=500)
                    st.plotly_chart(fig_balance_net, use_container_width=True)
                
                with col2:
                    # Gràfic comparatiu imports vs exports
                    fig_balance_comp = go.Figure()
                    
                    # Ordenar per balanç per a millor visualització
                    balance_sorted = balance_df.sort_values('Balanç')
                    
                    fig_balance_comp.add_trace(go.Bar(
                        name='Importacions',
                        y=balance_sorted['Producte'],
                        x=-balance_sorted['Importacions'],  # Negatiu per posar a l'esquerra
                        orientation='h',
                        marker_color='red',
                        opacity=0.7,
                        hovertemplate='<b>%{y}</b><br>Importacions: %{x:.2f}M tones<extra></extra>'
                    ))
                    
                    fig_balance_comp.add_trace(go.Bar(
                        name='Exportacions',
                        y=balance_sorted['Producte'],
                        x=balance_sorted['Exportacions'],
                        orientation='h',
                        marker_color='green',
                        opacity=0.7,
                        hovertemplate='<b>%{y}</b><br>Exportacions: %{x:.2f}M tones<extra></extra>'
                    ))
                    
                    fig_balance_comp.update_layout(
                        title=f'Comparativa Import-Export per Producte ({selected_year})',
                        xaxis_title='Volum (Milions de Tones)',
                        yaxis_title='Producte',
                        barmode='relative',
                        height=500,
                        xaxis=dict(tickformat='.1f')
                    )
                    
                    # Afegir línia vertical a zero
                    fig_balance_comp.add_vline(x=0, line_dash="dash", line_color="black", opacity=0.5)
                    
                    st.plotly_chart(fig_balance_comp, use_container_width=True)
                
                # Estadístiques del balanç comercial
                st.subheader("📈 Estadístiques del Balanç Comercial")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    net_exporters = len(balance_df[balance_df['Balanç'] > 0])
                    create_metric_card(
                        "Productes Exportadors Nets",
                        str(net_exporters),
                        "Productes amb més exportacions que importacions"
                    )
                
                with col2:
                    net_importers = len(balance_df[balance_df['Balanç'] < 0])
                    create_metric_card(
                        "Productes Importadors Nets",
                        str(net_importers),
                        "Productes amb més importacions que exportacions"
                    )
                
                with col3:
                    total_trade_volume = balance_df['Volum Total'].sum()
                    create_metric_card(
                        "Volum Total de Comerç",
                        f"{total_trade_volume:.1f}M",
                        "Suma d'importacions i exportacions (milions de tones)"
                    )
                
                with col4:
                    avg_balance = balance_df['Balanç'].abs().mean()
                    create_metric_card(
                        "Desequilibri Mitjà",
                        f"{avg_balance:.1f}M",
                        "Desequilibri absolut mitjà entre imports i exports"
                    )

def render_correlations_section(data_dict, selected_year):
    """SECCIÓ 5: Anàlisi de Correlacions"""
    st.markdown('<h2 class="section-header" id="correlacions">🔗 Anàlisi de Correlacions</h2>', 
                unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background: linear-gradient(90deg, #fef7ff 0%, #f3e8ff 100%); 
                padding: 1rem; border-radius: 10px; margin-bottom: 2rem;'>
        <h4 style='color: #581c87; margin-bottom: 0.5rem;'>🔗 Relacions entre Indicadors del Sistema Alimentari</h4>
        <p style='margin: 0; color: #374151;'>
            Explora les correlacions estadístiques entre autosuficiència, petjada de carboni i participació femenina. 
            Els gràfics animats mostren l'evolució temporal de les relacions per blocs regionals, 
            revelant patrons de canvi en les últimes dècades.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Combinar dades per a l'anàlisi de correlacions
    ssr_year = data_dict['ssr'][data_dict['ssr']['Year'] == selected_year]
    ff_year = data_dict['footprint'][data_dict['footprint']['Year'] == selected_year]
    
    # 1. CORRELACIONS BÀSIQUES (scatter plots)
    if not ssr_year.empty and not ff_year.empty:
        merged_data = pd.merge(
            ssr_year[['AreaName', 'SelfSufficiency', 'WomenAgriShare']],
            ff_year[['AreaName', 'FoodFootprintCO2']],
            on='AreaName',
            how='inner'
        )
        
        if len(merged_data) > 5:
            col1, col2 = st.columns(2)
            
            with col1:
                # Correlació Autosuficiència vs Petjada CO2
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
            
            with col2:
                # Correlació Participació Femenina vs Autosuficiència
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
    
    # 2. ANÀLISI DE CANVIS TEMPORALS (del notebook)
    st.subheader("📊 Canvis Temporals en l'Autosuficiència")
    
    # Definir blocs regionals per assignar països
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
    
    # Crear mapa de països a blocs regionals
    country_to_bloc_map = {}
    for bloc_name, countries in REGIONAL_BLOCS.items():
        for country in countries:
            country_to_bloc_map[country] = bloc_name
    
    # Filtrar dades útils per al canvi temporal
    ssr_useful = data_dict['ssr'][data_dict['ssr']['SelfSufficiency'] != 1].copy()
    
    if not ssr_useful.empty and 'AreaName' in ssr_useful.columns:
        # Calcular canvi SSR (2000-2013)
        ssr_2000 = ssr_useful[ssr_useful['Year'] == 2000]
        ssr_2013 = ssr_useful[ssr_useful['Year'] == 2013]
        
        if not ssr_2000.empty and not ssr_2013.empty:
            change_df = pd.merge(
                ssr_2000[['AreaCode', 'AreaName', 'SelfSufficiency']],
                ssr_2013[['AreaCode', 'AreaName', 'SelfSufficiency']], 
                on=['AreaCode', 'AreaName'], 
                suffixes=('_2000', '_2013')
            )
            change_df['Variació SSR'] = change_df['SelfSufficiency_2013'] - change_df['SelfSufficiency_2000']
            change_df = change_df.dropna(subset=['Variació SSR']).sort_values('Variació SSR', ascending=False)
            
            if len(change_df) >= 20: 
                top_bottom = pd.concat([change_df.head(10), change_df.tail(10)])
                top_bottom['Tipus'] = ['Augment' if v > 0 else 'Disminució' for v in top_bottom['Variació SSR']]
                
                fig_top_bottom = px.bar(
                    top_bottom.sort_values('Variació SSR'), 
                    x='Variació SSR', 
                    y='AreaName',
                    orientation='h',
                    color='Tipus',
                    color_discrete_map={'Augment': 'royalblue', 'Disminució': 'crimson'},
                    text='AreaName',
                    title="Països amb Major Variació d'Autosuficiència (SSR) (2000-2013)",
                    labels={'AreaName': 'País', 'Variació SSR': "Canvi en l'índex SSR"}
                )
                fig_top_bottom.update_traces(texttemplate='%{text}', textposition='outside')
                fig_top_bottom.update_layout(
                    uniformtext_minsize=8, 
                    legend_title_text='Tipus de Variació',
                    margin=dict(l=50, r=20, t=50, b=40),
                    yaxis_visible=False,
                    height=600
                )
                st.plotly_chart(fig_top_bottom, use_container_width=True)
    
    # 3. GRÀFIC ANIMAT DE CORRELACIÓ PER BLOCS REGIONALS (del notebook)
    st.subheader("🎬 Evolució Anual: Autosuficiència vs. Petjada de Carboni per Blocs")
    
    if not ssr_useful.empty and 'footprint' in data_dict and not data_dict['footprint'].empty:
        # Preparació de dades per al gràfic animat
        ssr_agg_scatter = ssr_useful.groupby(['AreaCode', 'AreaName', 'Year'])['SelfSufficiency'].mean().reset_index()
        ff_copy = data_dict['footprint'].copy()
        
        cols_ff_scatter = ['AreaCode', 'Year', 'FoodFootprintCO2', 'TotalProduction']
        if all(col in ff_copy.columns for col in cols_ff_scatter):
            combined_scatter = ssr_agg_scatter.merge(
                ff_copy[cols_ff_scatter], 
                on=['AreaCode', 'Year'], 
                how='inner'
            )

            if not combined_scatter.empty:
                # Assignar bloc regional
                combined_scatter['BlocRegional'] = combined_scatter['AreaName'].map(country_to_bloc_map)
                combined_scatter['BlocRegional'] = combined_scatter['BlocRegional'].fillna('Altres')

                # Filtrar el bloc "Altres"
                combined_scatter_filtered = combined_scatter[combined_scatter['BlocRegional'] != 'Altres'].copy()

                if not combined_scatter_filtered.empty:
                    # Convertir i netejar
                    combined_scatter_filtered['Year'] = pd.to_numeric(combined_scatter_filtered['Year'], errors='coerce')
                    combined_scatter_filtered = combined_scatter_filtered.dropna(subset=['Year'])
                    
                    combined_scatter_sorted = combined_scatter_filtered.sort_values(by=['Year', 'AreaName'])

                    # Aplicar filtrat per quantils
                    q_ff_upper = combined_scatter_sorted['FoodFootprintCO2'].quantile(0.95)
                    q_ss_upper = combined_scatter_sorted['SelfSufficiency'].quantile(0.95)

                    combined_clean_scatter = combined_scatter_sorted[
                        (combined_scatter_sorted['FoodFootprintCO2'] < q_ff_upper) &
                        (combined_scatter_sorted['SelfSufficiency'] < q_ss_upper)
                    ].copy()

                    if not combined_clean_scatter.empty:
                        combined_clean_scatter = combined_clean_scatter.sort_values(by=['Year', 'AreaName'])

                        # Recalcular rangs dels eixos
                        min_x = combined_clean_scatter['SelfSufficiency'].min()
                        max_x = combined_clean_scatter['SelfSufficiency'].max()
                        min_y = combined_clean_scatter['FoodFootprintCO2'].min()
                        max_y = combined_clean_scatter['FoodFootprintCO2'].max()

                        # Afegir un petit marge als eixos
                        range_x = [min_x, max_x]
                        if min_x != max_x:
                            padding_x = (max_x - min_x) * 0.05
                            range_x = [min_x - padding_x, max_x + padding_x]
                        
                        range_y = [min_y, max_y]
                        if min_y != max_y:
                            padding_y = (max_y - min_y) * 0.05
                            range_y = [min_y - padding_y, max_y + padding_y]

                        # Crear el gràfic animat
                        fig_scatter_blocs = px.scatter(
                            combined_clean_scatter, 
                            x='SelfSufficiency', 
                            y='FoodFootprintCO2',
                            size='TotalProduction', 
                            color='BlocRegional',
                            animation_frame="Year",
                            animation_group="AreaName",
                            hover_data=['AreaName', 'TotalProduction'],
                            title='Evolució Anual: Autosuficiència vs. Petjada de Carboni per Blocs Regionals',
                            labels={
                                'SelfSufficiency': 'Autosuficiència Mitjana (Índex SSR)',
                                'FoodFootprintCO2': 'Emissions per Tonelada Produïda (FoodFootprintCO2)',
                                'TotalProduction': 'Producció Total (tones)',
                                'BlocRegional': 'Bloc Regional'
                            },
                            size_max=40
                        )
                        
                        fig_scatter_blocs.update_layout(
                            template='plotly_white',
                            xaxis=dict(range=range_x),
                            yaxis=dict(range=range_y),
                            height=600
                        )
                        st.plotly_chart(fig_scatter_blocs, use_container_width=True)
                        
                        st.info("💡 **Consell:** Utilitza els controls d'animació per veure l'evolució temporal de la relació entre autosuficiència i petjada de carboni per cada bloc regional.")

def render_gender_section(data_dict, selected_year, selected_regions):
    """SECCIÓ 6: Anàlisi de Gènere"""
    st.markdown('<h2 class="section-header" id="genere">👩‍🌾 Perspectiva de Gènere</h2>', 
                unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background: linear-gradient(90deg, #fef7f7 0%, #ffe4e6 100%); 
                padding: 1rem; border-radius: 10px; margin-bottom: 2rem;'>
        <h4 style='color: #881337; margin-bottom: 0.5rem;'>👩‍🌾 Participació Femenina en l'Agricultura Mundial</h4>
        <p style='margin: 0; color: #374151;'>
            Analitza el paper de les dones en l'agricultura global i la seva relació amb l'autosuficiència alimentària. 
            Descobreix les diferències regionals en la participació femenina i com ha evolucionat al llarg del temps, 
            proporcionant una perspectiva de gènere essencial per entendre el sistema alimentari.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
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
            # Calcular evolució per blocs regionals
            gender_evolution = gender_data.groupby(['Year', 'BlocRegional'])['WomenAgriShare'].mean().reset_index()
            
            # Calcular mitjana mundial (sempre amb totes les dades disponibles)
            all_gender_data = data_dict['ssr'][data_dict['ssr']['WomenAgriShare'].notna()]
            global_gender_evolution = all_gender_data.groupby('Year')['WomenAgriShare'].mean().reset_index()
            
            fig_gender_evolution = px.line(
                gender_evolution,
                x='Year',
                y='WomenAgriShare',
                color='BlocRegional',
                title='Evolució de la Participació Femenina per Bloc Regional',
                labels={'WomenAgriShare': '% Dones en Agricultura', 'Year': 'Any'}
            )
            
            # Afegir línia de mitjana mundial destacada
            if not global_gender_evolution.empty:
                fig_gender_evolution.add_trace(
                    go.Scatter(
                        x=global_gender_evolution['Year'],
                        y=global_gender_evolution['WomenAgriShare'],
                        mode='lines',
                        name='🌍 Mitjana Mundial',
                        line=dict(color='black', width=4, dash='solid'),
                        hovertemplate='<b>Mitjana Mundial</b><br>Any: %{x}<br>% Dones: %{y:.1f}%<extra></extra>'
                    )
                )
            
            fig_gender_evolution.update_layout(
                height=500,
                hovermode='x unified',
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                )
            )
            st.plotly_chart(fig_gender_evolution, use_container_width=True)

def render_global_analysis_section(data_dict, selected_year):
    """SECCIÓ: Anàlisi Global del Sistema Alimentari"""
    st.markdown('<h2 class="section-header" id="global">🌍 Anàlisi Global</h2>', 
                unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background: linear-gradient(90deg, #f0f8ff 0%, #e6f3ff 100%); 
                padding: 1rem; border-radius: 10px; margin-bottom: 2rem;'>
        <h4 style='color: #1e3a8a; margin-bottom: 0.5rem;'>📈 Visió Panoràmica del Sistema Alimentari Mundial</h4>
        <p style='margin: 0; color: #374151;'>
            Explora els patrons globals de producció, comerç i distribucions estadístiques 
            per comprendre millor el context de l'autosuficiència alimentària mundial.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # 1. Evolució de Fluxos Mundials (Producció vs Comerç)
    st.subheader("📊 Evolució de la Producció i Comerç Mundial")
    
    # Preparar dades per a la producció mundial
    if 'production' in data_dict and not data_dict['production'].empty:
        prod_global = data_dict['production'].groupby('Year')['Production'].sum().reset_index()
        prod_global['Production'] = prod_global['Production'] / 1_000_000  # Convertir a milions de tones
    else:
        prod_global = pd.DataFrame()
    
    # Preparar dades per imports i exports mundials
    ssr_data = data_dict['ssr']
    if not ssr_data.empty:
        imports_global = ssr_data.groupby('Year')['Imports'].sum().reset_index()
        exports_global = ssr_data.groupby('Year')['Exports'].sum().reset_index()
        imports_global['Imports'] = imports_global['Imports'] / 1_000_000  # Convertir a milions de tones
        exports_global['Exports'] = exports_global['Exports'] / 1_000_000  # Convertir a milions de tones
    else:
        imports_global = pd.DataFrame()
        exports_global = pd.DataFrame()
    
    # Crear gràfic amb eix dual
    if not prod_global.empty or not imports_global.empty:
        fig_global_flows = make_subplots(specs=[[{"secondary_y": True}]])
        
        # Producció (eix primari)
        if not prod_global.empty:
            fig_global_flows.add_trace(
                go.Scatter(
                    x=prod_global['Year'], 
                    y=prod_global['Production'],
                    name='Producció',
                    line=dict(color='royalblue', width=3),
                    hovertemplate='<b>Producció</b><br>Any: %{x}<br>Producció: %{y:.0f}M tones<extra></extra>'
                ),
                secondary_y=False
            )
        
        # Imports (eix secundari)
        if not imports_global.empty:
            fig_global_flows.add_trace(
                go.Scatter(
                    x=imports_global['Year'], 
                    y=imports_global['Imports'],
                    name='Importacions',
                    line=dict(color='red', width=2),
                    hovertemplate='<b>Importacions</b><br>Any: %{x}<br>Importacions: %{y:.0f}M tones<extra></extra>'
                ),
                secondary_y=True
            )
        
        # Exports (eix secundari)
        if not exports_global.empty:
            fig_global_flows.add_trace(
                go.Scatter(
                    x=exports_global['Year'], 
                    y=exports_global['Exports'],
                    name='Exportacions',
                    line=dict(color='green', width=2),
                    hovertemplate='<b>Exportacions</b><br>Any: %{x}<br>Exportacions: %{y:.0f}M tones<extra></extra>'
                ),
                secondary_y=True
            )
        
        # Configurar títols i etiquetes
        fig_global_flows.update_layout(
            title='Evolució de la Producció i Comerç Alimentari Mundial',
            template='plotly_white',
            height=500,
            hovermode='x unified',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        # Configurar eixos Y
        fig_global_flows.update_yaxes(
            title_text='Producció (Milions de Tones)',
            secondary_y=False
        )
        fig_global_flows.update_yaxes(
            title_text='Comerç (Milions de Tones)',
            secondary_y=True
        )
        
        st.plotly_chart(fig_global_flows, use_container_width=True)
    
    # 2. Distribucions Estadístiques Avançades
    st.subheader("📈 Distribucions Estadístiques Globals")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Distribució de l'Autosuficiència**")
        
        # Filtrar dades útils (SSR != 1)
        ssr_useful = data_dict['ssr'][data_dict['ssr']['SelfSufficiency'] != 1]
        
        if not ssr_useful.empty:
            median_ssr = ssr_useful['SelfSufficiency'].median()
            mean_ssr = ssr_useful['SelfSufficiency'].mean()
            
            fig_ssr_dist = px.histogram(
                ssr_useful,
                x='SelfSufficiency',
                nbins=50,
                title='Distribució de l\'Autosuficiència (SSR ≠ 1)',
                labels={'SelfSufficiency': 'Índex d\'Autosuficiència', 'count': 'Freqüència'},
                color_discrete_sequence=['#2E8B57']
            )
            
            # Afegir línies de mediana i mitjana
            fig_ssr_dist.add_vline(
                x=median_ssr,
                line_dash="dash",
                line_color="red",
                annotation_text=f"Mediana: {median_ssr:.3f}",
                annotation_position="top left"
            )
            fig_ssr_dist.add_vline(
                x=mean_ssr,
                line_dash="dot",
                line_color="green",
                annotation_text=f"Mitjana: {mean_ssr:.3f}",
                annotation_position="top right"
            )
            
            fig_ssr_dist.update_layout(height=400, template='plotly_white')
            st.plotly_chart(fig_ssr_dist, use_container_width=True)
    
    with col2:
        st.markdown("**Distribució de la Petjada de Carboni**")
        
        ff_data = data_dict['footprint']
        if not ff_data.empty:
            # Filtrar outliers (95è percentil)
            ff_filtered = ff_data[ff_data['FoodFootprintCO2'] < ff_data['FoodFootprintCO2'].quantile(0.95)]
            
            if not ff_filtered.empty:
                median_ff = ff_filtered['FoodFootprintCO2'].median()
                mean_ff = ff_filtered['FoodFootprintCO2'].mean()
                
                fig_ff_dist = px.histogram(
                    ff_filtered,
                    x='FoodFootprintCO2',
                    nbins=50,
                    title='Distribució de la Petjada de Carboni',
                    labels={'FoodFootprintCO2': 'Petjada CO₂', 'count': 'Freqüència'},
                    color_discrete_sequence=['#CD853F']
                )
                
                # Afegir línies de mediana i mitjana
                fig_ff_dist.add_vline(
                    x=median_ff,
                    line_dash="dash",
                    line_color="red",
                    annotation_text=f"Mediana: {median_ff:.4f}",
                    annotation_position="top left"
                )
                fig_ff_dist.add_vline(
                    x=mean_ff,
                    line_dash="dot",
                    line_color="green",
                    annotation_text=f"Mitjana: {mean_ff:.4f}",
                    annotation_position="top right"
                )
                
                fig_ff_dist.update_layout(height=400, template='plotly_white')
                st.plotly_chart(fig_ff_dist, use_container_width=True)
    
    # 3. Estadístiques Globals Destacades
    st.subheader("🎯 Estadístiques Clau del Sistema Alimentari Mundial")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if not data_dict['ssr'].empty:
            total_countries = len(data_dict['ssr']['AreaName'].unique())
            create_metric_card(
                "Països Analitzats",
                f"{total_countries:,}",
                "Nombre total de països amb dades disponibles"
            )
    
    with col2:
        if not ssr_useful.empty:
            deficit_countries = len(ssr_useful[ssr_useful['SelfSufficiency'] < 1])
            surplus_countries = len(ssr_useful[ssr_useful['SelfSufficiency'] > 1])
            create_metric_card(
                "Dèficit vs Superàvit",
                f"{deficit_countries:,} / {surplus_countries:,}",
                "Països amb dèficit vs superàvit alimentari"
            )
    
    with col3:
        if not data_dict['production'].empty:
            years_span = data_dict['production']['Year'].max() - data_dict['production']['Year'].min()
            create_metric_card(
                "Període Temporal",
                f"{years_span:,} anys",
                f"Des de {data_dict['production']['Year'].min()} fins {data_dict['production']['Year'].max()}"
            )
    
    with col4:
        if not data_dict['footprint'].empty:
            co2_total = data_dict['footprint']['FoodFootprintCO2'].sum()
            create_metric_card(
                "Impacte CO₂ Acumulat",
                f"{co2_total:.2e}",
                "Emissions totals acumulades del sistema alimentari"
            )

# ==========================================
# APLICACIÓ PRINCIPAL
# ==========================================

def main():
    """Aplicació principal del panell"""
    
    # Títol principal
    st.markdown("""
    <div style='text-align: center; margin-bottom: 3rem;'>
        <h1 style='color: #2E8B57; font-size: 4rem; font-weight: 700; margin-bottom: 0.5rem;'>
            🌍 Panell Global
        </h1>
        <h2 style='color: #4682B4; font-size: 2.5rem; font-weight: 300; margin-top: 0;'>
            Autosuficiència Alimentària 🌾
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
    render_global_analysis_section(data_dict, selected_year)
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
