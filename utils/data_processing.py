import pandas as pd
import numpy as np
from datetime import datetime

def load_and_process_data():
    """
    Charge et traite les données de l'équipe de France féminine
    """
    try:
        # Chargement du dataset principal
        df = pd.read_csv('data/results.csv')
        
        # Vérification de la structure des données
        required_columns = ['date', 'home_team', 'away_team', 'home_score', 'away_score', 
                          'tournament', 'city', 'country', 'neutral']
        
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            print(f"Colonnes manquantes dans le fichier: {missing_columns}")
            return generate_sample_data()
        
        # Nettoyage et normalisation des données
        df['home_team'] = df['home_team'].str.lower().str.strip()
        df['away_team'] = df['away_team'].str.lower().str.strip()
        
        # Filtrage pour l'équipe de France (en minuscules)
        france_matches = df[
            (df['home_team'] == 'france') | 
            (df['away_team'] == 'france')
        ].copy()
        
        if len(france_matches) == 0:
            print("Aucun match de l'équipe de France trouvé dans les données. Utilisation des données d'exemple.")
            return generate_sample_data()
        
        # Conversion de la date
        france_matches['date'] = pd.to_datetime(france_matches['date'])
        france_matches['year'] = france_matches['date'].dt.year
        france_matches['month'] = france_matches['date'].dt.month
        
        # Gestion des valeurs manquantes pour les scores
        france_matches = france_matches.dropna(subset=['home_score', 'away_score'])
        
        # Conversion des scores en entiers
        france_matches['home_score'] = france_matches['home_score'].astype(int)
        france_matches['away_score'] = france_matches['away_score'].astype(int)
        
        # Détermination si la France joue à domicile ou à l'extérieur
        france_matches['is_home'] = france_matches['home_team'] == 'france'
        
        # Calcul des scores France avec la méthode apply (plus robuste)
        france_matches['france_score'] = france_matches.apply(
            lambda row: row['home_score'] if row['home_team'] == 'france' else row['away_score'], 
            axis=1
        )
        france_matches['opponent_score'] = france_matches.apply(
            lambda row: row['away_score'] if row['home_team'] == 'france' else row['home_score'], 
            axis=1
        )
        
        # Détermination de l'adversaire
        france_matches['opponent'] = france_matches.apply(
            lambda row: row['away_team'] if row['home_team'] == 'france' else row['home_team'], 
            axis=1
        )
        
        # Calcul du résultat
        france_matches['result'] = france_matches.apply(
            lambda row: 'Victoire' if row['france_score'] > row['opponent_score'] 
                       else 'Défaite' if row['france_score'] < row['opponent_score'] 
                       else 'Nul', 
            axis=1
        )
        
        # Calcul de l'écart de buts
        france_matches['goal_difference'] = france_matches['france_score'] - france_matches['opponent_score']
        
        # Nettoyage des types de compétition
        france_matches['tournament'] = france_matches['tournament'].fillna('Amical')
        
        return france_matches
        
    except FileNotFoundError:
        # Génération de données d'exemple si le fichier n'existe pas
        return generate_sample_data()

def generate_sample_data():
    """
    Génère des données d'exemple pour les tests
    """
    np.random.seed(42)
    
    # Listes d'adversaires et de compétitions réalistes
    opponents = ['Germany', 'USA', 'Brazil', 'England', 'Sweden', 'Netherlands', 'Norway', 'Spain', 'Italy', 'Australia']
    tournaments = ['FIFA World Cup', 'UEFA European Championship', 'Friendly', 'SheBelieves Cup', 'Algarve Cup']
    
    # Génération de 300 matchs sur 20 ans
    dates = pd.date_range(start='2004-01-01', end='2024-01-01', freq='2W')[:300]
    
    data = []
    for i, date in enumerate(dates):
        is_home = np.random.choice([True, False])
        opponent = np.random.choice(opponents)
        tournament = np.random.choice(tournaments)
        
        # Simulation des scores avec une tendance réaliste
        if is_home:
            france_score = np.random.poisson(1.8)  # Légèrement plus de buts à domicile
            opponent_score = np.random.poisson(1.2)
        else:
            france_score = np.random.poisson(1.5)
            opponent_score = np.random.poisson(1.4)
        
        data.append({
            'date': date,
            'home_team': 'France' if is_home else opponent,
            'away_team': opponent if is_home else 'France',
            'home_score': france_score if is_home else opponent_score,
            'away_score': opponent_score if is_home else france_score,
            'tournament': tournament,
            'city': 'Paris' if is_home else 'Various',
            'country': 'France' if is_home else 'Various',
            'neutral': False
        })
    
    df = pd.DataFrame(data)
    
    # Application du même traitement que pour les vraies données
    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    
    df['is_home'] = df['home_team'] == 'France'
    
    df['france_score'] = np.where(df['is_home'], df['home_score'], df['away_score'])
    df['opponent_score'] = np.where(df['is_home'], df['away_score'], df['home_score'])
    df['opponent'] = np.where(df['is_home'], df['away_team'], df['home_team'])
    
    df['result'] = np.where(
        df['france_score'] > df['opponent_score'], 'Victoire',
        np.where(df['france_score'] < df['opponent_score'], 'Défaite', 'Nul')
    )
    
    df['goal_difference'] = df['france_score'] - df['opponent_score']
    
    return df

def calculate_performance_metrics(df, period=None):
    """
    Calcule les métriques de performance clés
    """
    if period:
        df = df[df['year'].between(period[0], period[1])]
    
    total_matches = len(df)
    if total_matches == 0:
        return {}
    
    victories = len(df[df['result'] == 'Victoire'])
    defeats = len(df[df['result'] == 'Défaite'])
    draws = len(df[df['result'] == 'Nul'])
    
    metrics = {
        'total_matches': total_matches,
        'victories': victories,
        'defeats': defeats,
        'draws': draws,
        'win_rate': (victories / total_matches) * 100,
        'defeat_rate': (defeats / total_matches) * 100,
        'draw_rate': (draws / total_matches) * 100,
        'goals_scored': df['france_score'].sum(),
        'goals_conceded': df['opponent_score'].sum(),
        'avg_goals_scored': df['france_score'].mean(),
        'avg_goals_conceded': df['opponent_score'].mean(),
        'goal_difference_total': df['goal_difference'].sum(),
        'avg_goal_difference': df['goal_difference'].mean(),
        'clean_sheets': len(df[df['opponent_score'] == 0]),
        'big_wins': len(df[df['goal_difference'] >= 3]),  # Victoires par 3+ buts
        'narrow_wins': len(df[(df['result'] == 'Victoire') & (df['goal_difference'] == 1)]),
        'heavy_defeats': len(df[df['goal_difference'] <= -3])  # Défaites par 3+ buts
    }
    
    return metrics

def filter_data_by_period(df, start_year, end_year):
    """
    Filtre les données par période
    """
    return df[df['year'].between(start_year, end_year)]

def calculate_home_advantage(df):
    """
    Calcule l'avantage du terrain
    """
    home_matches = df[df['is_home'] == True]
    away_matches = df[df['is_home'] == False]
    
    if len(home_matches) == 0 or len(away_matches) == 0:
        return 0
    
    home_win_rate = len(home_matches[home_matches['result'] == 'Victoire']) / len(home_matches)
    away_win_rate = len(away_matches[away_matches['result'] == 'Victoire']) / len(away_matches)
    
    return (home_win_rate - away_win_rate) * 100

def get_performance_by_opponent(df, min_matches=3):
    """
    Analyse les performances contre chaque adversaire
    """
    opponent_stats = []
    
    for opponent in df['opponent'].unique():
        opp_matches = df[df['opponent'] == opponent]
        
        if len(opp_matches) >= min_matches:
            metrics = calculate_performance_metrics(opp_matches)
            metrics['opponent'] = opponent
            metrics['matches_played'] = len(opp_matches)
            opponent_stats.append(metrics)
    
    return pd.DataFrame(opponent_stats).sort_values('matches_played', ascending=False)

def calculate_trend_metrics(df, window=10):
    """
    Calcule les métriques de tendance avec moyenne mobile
    """
    df_sorted = df.sort_values('date').copy()
    
    # Conversion du résultat en points (3 victoire, 1 nul, 0 défaite)
    df_sorted['points'] = df_sorted['result'].map({'Victoire': 3, 'Nul': 1, 'Défaite': 0})
    
    # Moyennes mobiles
    df_sorted['rolling_points'] = df_sorted['points'].rolling(window=window, min_periods=1).mean()
    df_sorted['rolling_goals_scored'] = df_sorted['france_score'].rolling(window=window, min_periods=1).mean()
    df_sorted['rolling_goals_conceded'] = df_sorted['opponent_score'].rolling(window=window, min_periods=1).mean()
    
    return df_sorted
