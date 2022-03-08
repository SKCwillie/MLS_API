import pandas as pd
import json

try:
    AllYears = pd.read_csv('./API/Data/AllYears.csv')
except FileNotFoundError:
    AllYears = pd.read_csv('./API/Data/96_21.csv')
AllYears.dropna(inplace=True)
AllYears.drop(['Unnamed: 0'], axis=1, inplace=True)
AllYears.Season = AllYears.Season.astype('int64')
AllYears.GHome = AllYears.GHome.astype('int64')
AllYears.GAway = AllYears.GAway.astype('int64')
print(AllYears)
CURRENT_YEAR = 2022
years_list = list(range(1996, CURRENT_YEAR+1))


def get_all_results(years=years_list, **kwargs):
    team = kwargs.get('team', None)
    if team and team != 'ALL':
        TeamDF = pd.concat([AllYears[AllYears.Home == team], AllYears[AllYears.Away == team]])
    else:
        TeamDF = AllYears
    results = {}
    for year in years:
        results[year] = {'Regular Season': {}, 'Playoffs': {}}
        df = TeamDF[TeamDF.Season == int(year)]
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
