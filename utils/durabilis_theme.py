#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuration des couleurs et du design Durabilis&Co
"""

# Couleurs principales Durabilis&Co
DURABILIS_COLORS = {
    # Couleurs principales
    'light_blue': '#2ea9df',      # Bleu clair
    'medium_blue': '#1970b4',     # Bleu moyen  
    'dark_blue': '#2d3381',       # Bleu foncé
    
    # Mapping pour compatibilité
    'primary': '#1970b4',         # Bleu moyen comme couleur principale
    'secondary': '#2ea9df',       # Bleu clair comme secondaire
    'accent': '#2d3381',          # Bleu foncé comme accent
    
    # Couleurs système
    'success': '#28a745',
    'warning': '#ffc107', 
    'danger': '#dc3545',
    'info': '#17a2b8',
    'light': '#f8f9fa',
    'dark': '#343a40',
    'white': '#ffffff',
    
    # Dégradés Durabilis
    'gradient_primary': 'linear-gradient(135deg, #2ea9df 0%, #1970b4 50%, #2d3381 100%)',
    'gradient_light': 'linear-gradient(135deg, #2ea9df 0%, #1970b4 100%)',
    'gradient_dark': 'linear-gradient(135deg, #1970b4 0%, #2d3381 100%)',
}

# Configuration du thème Durabilis
DURABILIS_THEME = {
    'font_family': '"Segoe UI", "Roboto", "Helvetica Neue", Arial, sans-serif',
    'header_font': '"Segoe UI", "Roboto", "Helvetica Neue", Arial, sans-serif',
    'border_radius': '12px',
    'box_shadow': '0 2px 8px rgba(25, 112, 180, 0.1)',
    'transition': 'all 0.2s ease',
}

# CSS Variables pour Streamlit
DURABILIS_CSS_VARS = f"""
:root {{
    --durabilis-light: {DURABILIS_COLORS['light_blue']};
    --durabilis-medium: {DURABILIS_COLORS['medium_blue']};
    --durabilis-dark: {DURABILIS_COLORS['dark_blue']};
    --durabilis-gradient: {DURABILIS_COLORS['gradient_primary']};
    --durabilis-success: {DURABILIS_COLORS['success']};
    --durabilis-warning: {DURABILIS_COLORS['warning']};
    --durabilis-danger: {DURABILIS_COLORS['danger']};
}}
"""

def get_plotly_color_scale():
    """Retourne une échelle de couleurs Plotly compatible Durabilis"""
    return [
        [0.0, DURABILIS_COLORS['light_blue']],
        [0.5, DURABILIS_COLORS['medium_blue']],
        [1.0, DURABILIS_COLORS['dark_blue']]
    ]

def get_plotly_colors():
    """Retourne une liste de couleurs pour les graphiques Plotly"""
    return [
        DURABILIS_COLORS['medium_blue'],
        DURABILIS_COLORS['light_blue'], 
        DURABILIS_COLORS['dark_blue'],
        DURABILIS_COLORS['success'],
        DURABILIS_COLORS['warning'],
        DURABILIS_COLORS['danger'],
        DURABILIS_COLORS['info']
    ]

def get_metric_card_style():
    """Retourne le style CSS pour les cartes de métriques"""
    return f"""
    background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
    padding: 1.5rem;
    border-radius: {DURABILIS_THEME['border_radius']};
    border-left: 5px solid {DURABILIS_COLORS['medium_blue']};
    box-shadow: {DURABILIS_THEME['box_shadow']};
    transition: {DURABILIS_THEME['transition']};
    """
