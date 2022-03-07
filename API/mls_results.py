import pandas as pd
import json

csv_url = 'https://raw.githubusercontent.com/SKCwillie/MLS_API/main/Data/96_21.csv'
PastYears = pd.read_csv(csv_url)
PastYears.dropna(inplace=True)
PastYears.drop(['Unnamed: 0'], axis=1, inplace=True)
PastYears.Season = PastYears.Season.astype('int64')
PastYears.GHome = PastYears.GHome.astype('int64')
PastYears.GAway = PastYears.GAway.astype('int64')

CURRENT_YEAR = 2022
years_list = list(range(1996, CURRENT_YEAR))


def get_all_results(years=years_list, **kwargs):
    team = kwargs.get('team', None)

    if team:
        TeamDF = pd.concat([PastYears[PastYears.Home == team], PastYears[PastYears.Away == team]])
    else:
        TeamDF = PastYears
    results = {}
    for year in years:
        results[year] = {'Regular Season': {}, 'Playoffs': {}}
        df = TeamDF[TeamDF.Season == year]
        for i in df.index:
            if df.at[i, 'Round'] != 'Regular Season':
                results[year]['Playoffs'][i] = {'date': df.at[i, 'Date'],
                                                'home_team': df.at[i, 'Home'],
                                                'home_goals': str(df.at[i, 'GHome']),
                                                'away_team': df.at[i, 'Away'],
                                                'away_goals': str(df.at[i, 'GAway']),
                                                'venue': df.at[i, 'Venue'],
                                                'winner': df.at[i, 'Winner']
                                                }
            else:
                results[year]['Regular Season'][i] = {'date': df.at[i, 'Date'],
                                                      'home_team': df.at[i, 'Home'],
                                                      'home_goals': str(df.at[i, 'GHome']),
                                                      'away_team': df.at[i, 'Away'],
                                                      'away_goals': str(df.at[i, 'GAway']),
                                                      'venue': df.at[i, 'Venue'],
                                                      'winner': df.at[i, 'Winner']
                                                      }
    return results


if __name__ == '__main__':
    print(json.dumps(get_all_results([2021], team='SKC'), indent=4))
