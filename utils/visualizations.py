import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

# Couleurs Durabilis&Co
COLORS = {
    'primary': '#1970b4',     # Bleu moyen Durabilis
    'secondary': '#2ea9df',   # Bleu clair Durabilis
    'accent': '#2d3381',      # Bleu foncé Durabilis
    'success': '#28a745',
    'warning': '#ffc107',
    'danger': '#dc3545',
    'light': '#f8f9fa',
    'white': '#ffffff',
    'gradient': 'linear-gradient(135deg, #2ea9df 0%, #1970b4 50%, #2d3381 100%)'
}

def create_performance_evolution(df):
    """
    Crée un graphique d'évolution des performances dans le temps
    """
    # Agrégation par année
    yearly_stats = df.groupby('year').agg({
        'result': lambda x: (x == 'Victoire').sum() / len(x) * 100,
        'france_score': 'mean',
        'opponent_score': 'mean',
        'goal_difference': 'mean'
    }).reset_index()
    
    yearly_stats.columns = ['year', 'win_rate', 'avg_goals_scored', 'avg_goals_conceded', 'avg_goal_diff']
    
    # Création du graphique
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Pourcentage de Victoires', 'Buts Marqués/Encaissés (Moyenne)', 
                       'Différence de Buts Moyenne', 'Répartition des Résultats'),
        specs=[[{"secondary_y": False}, {"secondary_y": True}],
               [{"secondary_y": False}, {"type": "domain"}]],
        vertical_spacing=0.12
    )
    
    # Pourcentage de victoires
    fig.add_trace(
        go.Scatter(
            x=yearly_stats['year'], 
            y=yearly_stats['win_rate'],
            mode='lines+markers',
            name='% Victoires',
            line=dict(color=COLORS['primary'], width=3),
            marker=dict(size=8)
        ),
        row=1, col=1
    )
    
    # Buts marqués vs encaissés
    fig.add_trace(
        go.Scatter(
            x=yearly_stats['year'], 
            y=yearly_stats['avg_goals_scored'],
            mode='lines+markers',
            name='Buts Marqués',
            line=dict(color=COLORS['success'], width=2),
            marker=dict(size=6)
        ),
        row=1, col=2
    )
    
    fig.add_trace(
        go.Scatter(
            x=yearly_stats['year'], 
            y=yearly_stats['avg_goals_conceded'],
            mode='lines+markers',
            name='Buts Encaissés',
            line=dict(color=COLORS['danger'], width=2),
            marker=dict(size=6)
        ),
        row=1, col=2
    )
    
    # Différence de buts
    colors = ['green' if x >= 0 else 'red' for x in yearly_stats['avg_goal_diff']]
    fig.add_trace(
        go.Bar(
            x=yearly_stats['year'], 
            y=yearly_stats['avg_goal_diff'],
            name='Diff. Buts',
            marker_color=colors,
            opacity=0.7
        ),
        row=2, col=1
    )
    
    # Répartition des résultats (secteurs)
    result_counts = df['result'].value_counts()
    fig.add_trace(
        go.Pie(
            labels=result_counts.index,
            values=result_counts.values,
            name="Résultats",
            marker_colors=[COLORS['success'], COLORS['danger'], COLORS['warning']]
        ),
        row=2, col=2
    )
    
    fig.update_layout(
        title="🇫🇷 Évolution des Performances de l'Équipe de France Féminine",
        height=800,
        showlegend=True,
        template="plotly_white"
    )
    
    return fig

def create_comparison_charts(df):
    """
    Crée des graphiques de comparaison internationale
    """
    # Performance contre les principales nations
    top_opponents = df['opponent'].value_counts().head(8).index
    top_opponents_data = df[df['opponent'].isin(top_opponents)]
    
    # Calcul des statistiques par adversaire
    comparison_stats = []
    for opponent in top_opponents:
        opp_data = df[df['opponent'] == opponent]
        wins = len(opp_data[opp_data['result'] == 'Victoire'])
        total = len(opp_data)
        win_rate = (wins / total * 100) if total > 0 else 0
        
        comparison_stats.append({
            'opponent': opponent,
            'matches': total,
            'win_rate': win_rate,
            'avg_goals_scored': opp_data['france_score'].mean(),
            'avg_goals_conceded': opp_data['opponent_score'].mean()
        })
    
    comparison_df = pd.DataFrame(comparison_stats)
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Pourcentage de Victoires par Adversaire', 'Buts Marqués vs Encaissés',
                       'Nombre de Confrontations', 'Performance Offensive vs Défensive'),
        specs=[[{"type": "bar"}, {"type": "scatter"}],
               [{"type": "bar"}, {"type": "polar"}]]
    )
    
    # Pourcentage de victoires par adversaire
    fig.add_trace(
        go.Bar(
            x=comparison_df['opponent'],
            y=comparison_df['win_rate'],
            name='% Victoires',
            marker_color=COLORS['primary'],
            text=[f"{x:.1f}%" for x in comparison_df['win_rate']],
            textposition='outside'
        ),
        row=1, col=1
    )
    
    # Buts marqués vs encaissés
    fig.add_trace(
        go.Scatter(
            x=comparison_df['avg_goals_conceded'],
            y=comparison_df['avg_goals_scored'],
            mode='markers+text',
            text=comparison_df['opponent'],
            textposition='top center',
            marker=dict(
                size=comparison_df['matches'],
                color=comparison_df['win_rate'],
                colorscale='RdYlGn',
                showscale=True,
                colorbar=dict(title="% Victoires")
            ),
            name='Performance'
        ),
        row=1, col=2
    )
    
    # Nombre de confrontations
    fig.add_trace(
        go.Bar(
            x=comparison_df['opponent'],
            y=comparison_df['matches'],
            name='Matchs Joués',
            marker_color=COLORS['secondary'],
            text=comparison_df['matches'],
            textposition='outside'
        ),
        row=2, col=1
    )
    
    # Radar chart des performances
    categories = ['Buts Marqués', 'Buts Encaissés (Inv)', '% Victoires', 'Expérience']
    
    for i, opponent in enumerate(comparison_df['opponent'][:4]):  # Top 4 seulement
        opp_data = comparison_df[comparison_df['opponent'] == opponent].iloc[0]
        
        values = [
            opp_data['avg_goals_scored'] / comparison_df['avg_goals_scored'].max() * 100,
            (comparison_df['avg_goals_conceded'].max() - opp_data['avg_goals_conceded']) / comparison_df['avg_goals_conceded'].max() * 100,
            opp_data['win_rate'],
            opp_data['matches'] / comparison_df['matches'].max() * 100
        ]
        
        fig.add_trace(
            go.Scatterpolar(
                r=values + [values[0]],  # Fermer le polygone
                theta=categories + [categories[0]],
                fill='toself',
                name=opponent,
                opacity=0.6
            ),
            row=2, col=2
        )
    
    fig.update_layout(
        title="📊 Analyse Comparative Internationale",
        height=800,
        showlegend=True,
        template="plotly_white"
    )
    
    return fig

def create_home_advantage_chart(df):
    """
    Crée un graphique analysant l'avantage du terrain
    """
    home_data = df[df['is_home'] == True]
    away_data = df[df['is_home'] == False]
    neutral_data = df[df['neutral'] == True] if 'neutral' in df.columns else pd.DataFrame()
    
    # Calcul des statistiques
    venues = ['Domicile', 'Extérieur']
    if len(neutral_data) > 0:
        venues.append('Terrain Neutre')
        datasets = [home_data, away_data, neutral_data]
    else:
        datasets = [home_data, away_data]
    
    stats = []
    for i, data in enumerate(datasets):
        if len(data) > 0:
            wins = len(data[data['result'] == 'Victoire'])
            draws = len(data[data['result'] == 'Nul'])
            defeats = len(data[data['result'] == 'Défaite'])
            total = len(data)
            
            stats.append({
                'venue': venues[i],
                'win_rate': wins / total * 100,
                'draw_rate': draws / total * 100,
                'defeat_rate': defeats / total * 100,
                'avg_goals_scored': data['france_score'].mean(),
                'avg_goals_conceded': data['opponent_score'].mean(),
                'total_matches': total
            })
    
    venue_df = pd.DataFrame(stats)
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Répartition des Résultats par Lieu', 'Performance Offensive/Défensive',
                       'Pourcentage de Victoires', 'Nombre de Matchs'),
        specs=[[{"type": "bar"}, {"type": "bar"}],
               [{"type": "bar"}, {"type": "bar"}]]
    )
    
    # Répartition des résultats (barres empilées)
    fig.add_trace(
        go.Bar(name='Victoires', x=venue_df['venue'], y=venue_df['win_rate'], 
               marker_color=COLORS['success']),
        row=1, col=1
    )
    fig.add_trace(
        go.Bar(name='Nuls', x=venue_df['venue'], y=venue_df['draw_rate'], 
               marker_color=COLORS['warning']),
        row=1, col=1
    )
    fig.add_trace(
        go.Bar(name='Défaites', x=venue_df['venue'], y=venue_df['defeat_rate'], 
               marker_color=COLORS['danger']),
        row=1, col=1
    )
    
    # Performance offensive/défensive
    fig.add_trace(
        go.Bar(name='Buts Marqués', x=venue_df['venue'], y=venue_df['avg_goals_scored'], 
               marker_color=COLORS['primary'], opacity=0.7),
        row=1, col=2
    )
    fig.add_trace(
        go.Bar(name='Buts Encaissés', x=venue_df['venue'], y=venue_df['avg_goals_conceded'], 
               marker_color=COLORS['secondary'], opacity=0.7),
        row=1, col=2
    )
    
    # Pourcentage de victoires
    fig.add_trace(
        go.Bar(x=venue_df['venue'], y=venue_df['win_rate'], 
               marker_color=[COLORS['primary'] if x == 'Domicile' else COLORS['secondary'] for x in venue_df['venue']],
               text=[f"{x:.1f}%" for x in venue_df['win_rate']],
               textposition='outside',
               showlegend=False),
        row=2, col=1
    )
    
    # Nombre de matchs
    fig.add_trace(
        go.Bar(x=venue_df['venue'], y=venue_df['total_matches'], 
               marker_color=COLORS['light'],
               marker_line_color=COLORS['primary'],
               marker_line_width=2,
               text=venue_df['total_matches'],
               textposition='outside',
               showlegend=False),
        row=2, col=2
    )
    
    fig.update_layout(
        title="🏠 Analyse de l'Avantage du Terrain",
        height=700,
        barmode='stack',
        template="plotly_white"
    )
    
    return fig

def create_momentum_chart(df):
    """
    Crée un graphique de momentum et tendances récentes
    """
    from utils.data_processing import calculate_trend_metrics
    
    df_trend = calculate_trend_metrics(df, window=10)
    
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Évolution du Momentum (Moyenne Mobile 10 Matchs)', 
                       'Performance Récente vs Historique'),
        shared_xaxes=True,
        vertical_spacing=0.15
    )
    
    # Momentum avec moyenne mobile
    fig.add_trace(
        go.Scatter(
            x=df_trend['date'],
            y=df_trend['rolling_points'],
            mode='lines',
            name='Points (Moyenne Mobile)',
            line=dict(color=COLORS['primary'], width=3),
            fill='tonexty'
        ),
        row=1, col=1
    )
    
    # Ligne de référence (performance moyenne)
    avg_points = df_trend['points'].mean()
    fig.add_hline(y=avg_points, line_dash="dash", line_color="gray", 
                  annotation_text=f"Moyenne: {avg_points:.1f}", row=1, col=1)
    
    # Buts marqués vs encaissés
    fig.add_trace(
        go.Scatter(
            x=df_trend['date'],
            y=df_trend['rolling_goals_scored'],
            mode='lines',
            name='Buts Marqués (Moy. Mobile)',
            line=dict(color=COLORS['success'], width=2)
        ),
        row=2, col=1
    )
    
    fig.add_trace(
        go.Scatter(
            x=df_trend['date'],
            y=df_trend['rolling_goals_conceded'],
            mode='lines',
            name='Buts Encaissés (Moy. Mobile)',
            line=dict(color=COLORS['danger'], width=2)
        ),
        row=2, col=1
    )
    
    fig.update_layout(
        title="📈 Analyse du Momentum et des Tendances",
        height=600,
        template="plotly_white",
        hovermode='x unified'
    )
    
    return fig

def create_tournament_performance_chart(df):
    """
    Crée un graphique de performance par type de compétition
    """
    tournament_stats = df.groupby('tournament').agg({
        'result': lambda x: (x == 'Victoire').sum() / len(x) * 100,
        'france_score': 'mean',
        'opponent_score': 'mean',
        'date': 'count'  # Utiliser 'date' pour compter le nombre de matchs
    }).reset_index()
    
    tournament_stats.columns = ['tournament', 'win_rate', 'avg_goals_scored', 'avg_goals_conceded', 'matches']
    tournament_stats = tournament_stats.sort_values('matches', ascending=False)
    
    fig = px.scatter(
        tournament_stats,
        x='avg_goals_conceded',
        y='avg_goals_scored',
        size='matches',
        color='win_rate',
        hover_name='tournament',
        color_continuous_scale='RdYlGn',
        title="Performance par Type de Compétition",
        labels={
            'avg_goals_conceded': 'Buts Encaissés (Moyenne)',
            'avg_goals_scored': 'Buts Marqués (Moyenne)',
            'win_rate': '% Victoires'
        }
    )
    
    # Ligne de parité
    max_goals = max(tournament_stats['avg_goals_scored'].max(), tournament_stats['avg_goals_conceded'].max())
    fig.add_shape(
        type="line",
        x0=0, y0=0, x1=max_goals, y1=max_goals,
        line=dict(dash="dash", color="gray")
    )
    
    fig.update_layout(template="plotly_white")
    
    return fig
