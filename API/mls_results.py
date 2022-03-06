import pandas as pd
import json

csv_url = 'https://raw.githubusercontent.com/SKCwillie/MLS_API/main/Data/96_21.csv'
PastYears = pd.read_csv(csv_url)
PastYears.dropna(inplace=True)
PastYears.Season = PastYears.Season.astype('int64')
PastYears.GHome = PastYears.GHome.astype('int64')
PastYears.GAway = PastYears.GAway.astype('int64')
PastYears.Date = pd.to_datetime(PastYears.Date, format='%Y-%m-%d')
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

CURRENT_YEAR = 2022
years_list = list(range(1996, CURRENT_YEAR))


def get_all_results(years=years_list):
    results = {}
    for year in years:
        results[year] = {'Regular Season': {}, 'Playoffs': {}}
        df = PastYears[PastYears.Season == year]
        for i in df.index:

            if df.at[i, 'Round'] != 'Regular Season':
                results[year]['Playoffs'][i] = {'date': df.at[i, 'Date'],
                                                'home_team': teams[df.at[i, 'Home']][0],
                                                'home_goals': str(df.at[i, 'GHome']),
                                                'away_team': teams[df.at[i, 'Away']][0],
                                                'away_goals': str(df.at[i, 'GAway']),
                                                'venue': df.at[i, 'Venue'],
                                                'winner': teams[df.at[i, 'Winner']][0]
                                                      }
            else:
                results[year]['Regular Season'][i] = {'date': df.at[i, 'Date'],
                                                        'home_team': teams[df.at[i, 'Home']][0],
                                                        'home_goals': str(df.at[i, 'GHome']),
                                                        'away_team': teams[df.at[i, 'Away']][0],
                                                        'away_goals': str(df.at[i, 'GAway']),
                                                        'venue': df.at[i, 'Venue'],
                                                        'winner': teams[df.at[i, 'Winner']][0]
                                                        }
    return results


if __name__=='__main__':
    print(json.dumps(get_all_results([1996]), indent=4))
