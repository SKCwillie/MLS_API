import pandas as pd
import requests
from bs4 import BeautifulSoup

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


def get_this_year():
    url = 'https://fbref.com/en/comps/22/schedule/Major-League-Soccer-Scores-and-Fixtures'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find_all('table', {'id': 'sched_11499_1'})
    df_results = pd.read_html(str(table))[0]
    df_fixtures = pd.read_html(str(table))[0]

    for i in df_results.index:
        if df_results.at[i, 'Date'] == 'Date':
            df_results.drop([i], inplace=True)
            df_fixtures.drop([i], inplace=True)
        elif df_results.at[i, 'Score'] != df.at[i, 'Score']:
            df_results.drop([i], inplace=True)
        else:
            df_fixtures.drop([i], inplace=True)
    ### This current goes and scrapes this years results
    ### Need to append df_results to current csv
    ### Then go get next weeks matches to output


get_this_year()
