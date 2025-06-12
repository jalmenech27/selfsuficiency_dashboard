"""
Plotting - Funcions per crear visualitzacions personalitzades
"""

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple

# ==========================================
# PALETES DE COLORS I CONFIGURACIÓ
# ==========================================

SUSTAINABILITY_COLORS = {
    'primary': '#2E8B57',      # Verd bosc
    'secondary': '#90EE90',    # Verd clar
    'accent': '#FF6347',       # Tomato
    'warning': '#FFD700',      # Daurat
    'info': '#4682B4',         # Steel blue
    'neutral': '#708090'       # Slate gray
}

REGIONAL_COLORS = {
    'EU27': '#1f77b4',
    'Amèrica Llatina i Carib': '#ff7f0e',
    'Àfrica Subsahariana': '#2ca02c',
    'Nord d\'Àfrica': '#d62728',
    'Àsia Oriental i Sud-oriental': '#9467bd',
    'Àsia Meridional': '#8c564b',
    'Àsia Occidental i Àsia Central': '#e377c2',
    'Amèrica del Nord': '#7f7f7f',
    'Oceania': '#bcbd22',
    'Altres': '#17becf'
}

def create_color_palette(items: List[str], palette_name: str = 'Set3') -> Dict[str, str]:
    """Crea una paleta de colors per a una llista d'elements"""
    
    if palette_name == 'regional':
        return {item: REGIONAL_COLORS.get(item, SUSTAINABILITY_COLORS['neutral']) 
                for item in items}
    
    colors = px.colors.qualitative.Set3
    if palette_name == 'sustainability':
        colors = [SUSTAINABILITY_COLORS['primary'], SUSTAINABILITY_COLORS['accent'], 
                 SUSTAINABILITY_COLORS['warning'], SUSTAINABILITY_COLORS['info']]
    
    return {item: colors[i % len(colors)] for i, item in enumerate(items)}

# ==========================================
# MAPES COROPLÉTICS
# ==========================================

def plot_choropleth_map(df: pd.DataFrame, 
                       value_col: str,
                       title: str,
                       color_scale: str = 'RdYlGn',
                       location_col: str = 'AreaName',
                       hover_data: Optional[List[str]] = None) -> go.Figure:
    """Crea un mapa coroplètic personalitzat"""
    
    fig = px.choropleth(
        df,
        locations=location_col,
        color=value_col,
        locationmode='country names',
        title=title,
        color_continuous_scale=color_scale,
        labels={value_col: value_col.replace('_', ' ').title()},
        hover_data=hover_data or []
    )
    
    fig.update_layout(
        height=600,
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type='natural earth'
        ),
        title={
            'text': title,
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 18, 'color': SUSTAINABILITY_COLORS['primary']}
        }
    )
    
    return fig

# ==========================================
# GRÀFICS DE LÍNIES I EVOLUCIÓ
# ==========================================

def plot_multi_line_evolution(df: pd.DataFrame,
                             x_col: str,
                             y_col: str,
                             group_col: str,
                             title: str,
                             color_palette: Optional[Dict] = None) -> go.Figure:
    """Crea un gràfic de línies múltiples per evolució temporal"""
    
    fig = go.Figure()
    
    groups = df[group_col].unique()
    colors = color_palette or create_color_palette(groups, 'regional')
    
    for group in groups:
        group_data = df[df[group_col] == group].sort_values(x_col)
        
        fig.add_trace(go.Scatter(
            x=group_data[x_col],
            y=group_data[y_col],
            mode='lines+markers',
            name=group,
            line=dict(color=colors.get(group, SUSTAINABILITY_COLORS['neutral']), width=2),
            marker=dict(size=6),
            hovertemplate=f'<b>{group}</b><br>' +
                         f'{x_col}: %{{x}}<br>' +
                         f'{y_col}: %{{y:.3f}}<extra></extra>'
        ))
    
    fig.update_layout(
        title={
            'text': title,
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 18, 'color': SUSTAINABILITY_COLORS['primary']}
        },
        xaxis_title=x_col.replace('_', ' ').title(),
        yaxis_title=y_col.replace('_', ' ').title(),
        hovermode='x unified',
        showlegend=True,
        height=500
    )
    
    return fig

# ==========================================
# GRÀFICS DE BARRES
# ==========================================

def plot_horizontal_bar_chart(df: pd.DataFrame,
                             x_col: str,
                             y_col: str,
                             title: str,
                             color_col: Optional[str] = None,
                             top_n: Optional[int] = None) -> go.Figure:
    """Crea un gràfic de barres horitzontal"""
    
    plot_data = df.copy()
    
    if top_n:
        plot_data = plot_data.head(top_n)
    
    if color_col and color_col in plot_data.columns:
        colors = create_color_palette(plot_data[color_col].unique())
        color_map = plot_data[color_col].map(colors)
    else:
        color_map = SUSTAINABILITY_COLORS['primary']
    
    fig = go.Figure(go.Bar(
        x=plot_data[x_col],
        y=plot_data[y_col],
        orientation='h',
        marker_color=color_map,
        hovertemplate=f'<b>%{{y}}</b><br>{x_col}: %{{x}}<extra></extra>'
    ))
    
    fig.update_layout(
        title={
            'text': title,
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 16, 'color': SUSTAINABILITY_COLORS['primary']}
        },
        xaxis_title=x_col.replace('_', ' ').title(),
        yaxis_title=y_col.replace('_', ' ').title(),
        height=max(400, len(plot_data) * 25)  # Altura dinàmica
    )
    
    return fig

# ==========================================
# SCATTER PLOTS I CORRELACIONS
# ==========================================

def plot_correlation_scatter(df: pd.DataFrame,
                            x_col: str,
                            y_col: str,
                            title: str,
                            trendline: bool = True,
                            color_col: Optional[str] = None,
                            size_col: Optional[str] = None,
                            hover_col: Optional[str] = None) -> go.Figure:
    """Crea un scatter plot per analitzar correlacions"""
    
    # Scatter plot base
    hover_data = [hover_col] if hover_col else []
    
    fig = px.scatter(
        df,
        x=x_col,
        y=y_col,
        color=color_col,
        size=size_col,
        title=title,
        trendline='ols' if trendline else None,
        hover_data=hover_data,
        labels={
            x_col: x_col.replace('_', ' ').title(),
            y_col: y_col.replace('_', ' ').title()
        }
    )
    
    # Personalitzar colors si no hi ha color_col
    if not color_col:
        fig.update_traces(marker_color=SUSTAINABILITY_COLORS['primary'])
    
    # Calcular i mostrar correlació
    correlation = df[x_col].corr(df[y_col])
    
    fig.add_annotation(
        x=0.02,
        y=0.98,
        xref='paper',
        yref='paper',
        text=f'Correlació: {correlation:.3f}',
        showarrow=False,
        bgcolor='white',
        bordercolor='black',
        borderwidth=1,
        font=dict(size=12)
    )
    
    fig.update_layout(
        title={
            'text': title,
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 16, 'color': SUSTAINABILITY_COLORS['primary']}
        },
        height=500
    )
    
    return fig

# ==========================================
# HISTOGRAMES I DISTRIBUCIONS
# ==========================================

def plot_distribution_histogram(df: pd.DataFrame,
                               value_col: str,
                               title: str,
                               bins: int = 30,
                               show_stats: bool = True) -> go.Figure:
    """Crea un histograma per mostrar distribucions"""
    
    fig = px.histogram(
        df,
        x=value_col,
        nbins=bins,
        title=title,
        labels={value_col: value_col.replace('_', ' ').title()},
        color_discrete_sequence=[SUSTAINABILITY_COLORS['primary']]
    )
    
    if show_stats:
        mean_val = df[value_col].mean()
        median_val = df[value_col].median()
        
        # Afegir línies de mitjana i mediana
        fig.add_vline(
            x=mean_val,
            line_dash="dash",
            line_color="red",
            annotation_text=f"Mitjana: {mean_val:.2f}"
        )
        
        fig.add_vline(
            x=median_val,
            line_dash="dot",
            line_color="blue",
            annotation_text=f"Mediana: {median_val:.2f}"
        )
    
    fig.update_layout(
        title={
            'text': title,
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 16, 'color': SUSTAINABILITY_COLORS['primary']}
        },
        height=400
    )
    
    return fig

# ==========================================
# GRÀFICS COMPOSTOS I SUBPLOTS
# ==========================================

def create_comparison_subplot(df1: pd.DataFrame,
                            df2: pd.DataFrame,
                            config1: Dict,
                            config2: Dict,
                            main_title: str) -> go.Figure:
    """Crea un subplot amb dues visualitzacions comparatives"""
    
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=(config1.get('title', ''), config2.get('title', '')),
        horizontal_spacing=0.1
    )
    
    # Primer gràfic
    if config1.get('type') == 'bar':
        fig.add_trace(
            go.Bar(
                x=df1[config1['x']],
                y=df1[config1['y']],
                name=config1.get('name', 'Dataset 1'),
                marker_color=SUSTAINABILITY_COLORS['primary']
            ),
            row=1, col=1
        )
    
    # Segon gràfic
    if config2.get('type') == 'bar':
        fig.add_trace(
            go.Bar(
                x=df2[config2['x']],
                y=df2[config2['y']],
                name=config2.get('name', 'Dataset 2'),
                marker_color=SUSTAINABILITY_COLORS['accent']
            ),
            row=1, col=2
        )
    
    fig.update_layout(
        title={
            'text': main_title,
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 18, 'color': SUSTAINABILITY_COLORS['primary']}
        },
        height=500,
        showlegend=False
    )
    
    return fig

# ==========================================
# INDICADORS I MÈTRIQUES VISUALS
# ==========================================

def create_gauge_chart(value: float,
                      title: str,
                      min_val: float = 0,
                      max_val: float = 2,
                      thresholds: Optional[Dict[str, float]] = None) -> go.Figure:
    """Crea un gràfic de gauge per mostrar un indicador"""
    
    if thresholds is None:
        thresholds = {'red': 0.5, 'yellow': 1.0, 'green': 2.0}
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title},
        gauge={
            'axis': {'range': [None, max_val]},
            'bar': {'color': SUSTAINABILITY_COLORS['primary']},
            'steps': [
                {'range': [min_val, thresholds['red']], 'color': "lightgray"},
                {'range': [thresholds['red'], thresholds['yellow']], 'color': "yellow"},
                {'range': [thresholds['yellow'], max_val], 'color': "lightgreen"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': thresholds['yellow']
            }
        }
    ))
    
    fig.update_layout(height=400)
    
    return fig

# ==========================================
# UTILITATS GENERALS
# ==========================================

def add_custom_styling(fig: go.Figure) -> go.Figure:
    """Afegeix estil personalitzat a qualsevol figura"""
    
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family="Arial, sans-serif", size=12),
        title_font=dict(size=16, color=SUSTAINABILITY_COLORS['primary']),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig

def format_hover_template(base_template: str, **kwargs) -> str:
    """Crea templates personalitzats per hover"""
    
    template = base_template
    for key, value in kwargs.items():
        template = template.replace(f'{{{key}}}', str(value))
    
    return template + '<extra></extra>'
