import pandas as pd
import requests
from bs4 import BeautifulSoup
import numpy as np
import re


PastYears = pd.read_csv('./API/Data/96_21.csv', index_col=0)
SEASON = 2022
teams = {'Atlanta Utd': ['ATL', 'Atlanta'],
         'Austin FC': ['ATX', 'Austin'],
         'CF Montréal': ['MTL', 'Montreal'],
         'Charlotte FC': ['CLT', 'Charlotte'],
         'Chicago Fire': ['CHI', 'Chicago'],
         'Chivas USA': ['CHV', 'Los Angeles'],
         'Colorado Rapids': ['COL', 'Denver'],
         'Columbus Crew': ['CLB', 'Columbus'],
         'D.C. United': ['DC', 'Washington DC'],
         'Dallas Burn': ['DAL', 'Dallas'],
         'FC Cincinnati': ['CIN', 'Cincinnati'],
         'FC Dallas': ['DAL', 'Dallas'],
         'Houston Dynamo': ['HOU', 'Houston'],
         'Inter Miami': ['MIA', 'Miami'],
         'KC Wiz': ['SKC', 'Kansas City'],
         'KC Wizards': ['SKC', 'Kansas City'],
         'LA Galaxy': ['LA', 'Los Angeles'],
         'Los Angeles FC': ['LAFC', 'Los Angeles'],
         'MetroStars': ['RBNY', 'New York'],
         'Miami Fusion': ['MIAF', 'Miami'],
         'Minnesota Utd': ['MIN', 'Saint Paul'],
         'Montreal Impact': ['MTL', 'Montreal Impact'],
         'NY Red Bulls': ['RBNY', 'New York'],
         'NYCFC': ['NYC', 'New York'],
         'Nashville': ['NSH', 'Nashville'],
         'New England': ['NE', 'Foxborough'],
         'Orlando City': ['ORL', 'Orlando'],
         'Philadelphia': ['PHI', 'Chester'],
         'Portland Timbers': ['POR', 'Portland'],
         'Real Salt Lake': ['RSL', 'Sandy'],
         'San Jose': ['SJ', 'San Jose'],
         'Seattle': ['SEA', 'Seattle'],
         'Sporting KC': ['SKC', 'Kansas City'],
         'Tampa Bay': ['TB', 'Tampa Bay'],
         'Toronto FC': ['TOR', 'Toronto'],
         'Vancouver': ['VAN', 'Vancouver']
         }


def split_score(score):
    split = score.split('-')
    if '(' not in score:
        return split[0], split[1]
    else:
        return split[0].split(') ')[1], split[1].split(' (')[0]


def get_winner(home_team, away_team, score):
    home_score, away_score = split_score(score)
    if home_score > away_score:
        return home_team
    elif away_score > home_score:
        return away_team
    # Return regular season Tie
    elif '(' not in score and home_score == away_score:
        return np.nan
    elif '(' in score and home_score == away_score:
        home_pen = score.split('-')[0]
        home_pen = int(re.search('\(([^)]+)', home_pen).group(1))
        away_pen = score.split('-')[1]
        away_pen = int(re.search('\(([^)]+)', away_pen).group(1))
        if home_pen > away_pen:
            return home_team
        else:
            return away_team


def add_current_year(past_years):
    url = 'https://fbref.com/en/comps/22/schedule/Major-League-Soccer-Scores-and-Fixtures'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find_all('table', {'id': 'sched_11499_1'})
    df_results = pd.read_html(str(table))[0]
    df_fixtures = pd.read_html(str(table))[0]
    df_results['GHome'], df_fixtures['GHome'] = 0, 0
    df_results['GAway'], df_fixtures['GAway'] = 0, 0
    df_results['Winner'], df_fixtures['Winner'] = 0, 0
    df_results['Season'], df_fixtures['Season'] = SEASON, SEASON

    for i in df_results.index:
        if df_results.at[i, 'Date'] == 'Date':
            df_results.drop([i], inplace=True)
            df_fixtures.drop([i], inplace=True)
        elif df_results.at[i, 'Score'] != df_results.at[i, 'Score']:
            df_results.drop([i], inplace=True)
        else:
            df_fixtures.drop([i], inplace=True)
        try:
            df_results.at[i, 'Score'] = df_results.at[i, 'Score'].replace('–', '-')
            df_results.at[i, 'GHome'], df_results.at[i, 'GAway'] = split_score(df_results.at[i, 'Score'])
            df_results.at[i, 'Winner'] = get_winner(df_results.at[i, 'Home'], df_results.at[i, 'Away'],
                                                    df_results.at[i, 'Score'])
        except:
            continue
        try:
            df_results.at[i, 'Home'] = teams[df_results.at[i, 'Home']][0]
            df_results.at[i, 'Away'] = teams[df_results.at[i, 'Away']][0]
            df_results.at[i, 'Winner'] = teams[df_results.at[i, 'Winner']][0]
        except KeyError:
            continue

    df_results.Winner.fillna('Draw', inplace=True)

    try:
        df_results = df_results[['Season', 'Round', 'Venue', 'Date', 'Home', 'GHome', 'GAway', 'Away', 'Winner']]
    except KeyError:
        df_results['Round'] = 'Regular Season'
        df_results = df_results[['Season', 'Round', 'Venue', 'Date', 'Home', 'GHome', 'GAway', 'Away', 'Winner']]

    AllYears = pd.concat([past_years, df_results])
    AllYears.drop(['Unnamed: 0'], inplace=True, axis=1)
    AllYears.reset_index(inplace=True)
    AllYears.drop(['index'], inplace=True, axis=1)
    AllYears.to_csv('./API/Data/AllYears.csv')


sched = BlockingScheduler()
