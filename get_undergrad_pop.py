from pandas.io.html import read_html
import pandas as pd
import numpy as np
import utils

cols = {
    1: 'name',
    2: 'state',
    3: 'cost',
    4: 'population'
}
def get_url(pg):
    return 'http://www.forbes.com/lists/2010/94/best-colleges-10_Americas-Best-Colleges_TotStudPop{p}.html'.format(p='_{}'.format(pg) if pg > 1 else '')

def parse(url):
    df = read_html(url, index_col=0, skiprows=1, infer_types=False)[0]\
        .set_index_name('rank').rename(columns=cols)
    
    df['population'] = df.population.str.replace(',', '')\
        .replace('NA', np.nan).astype(float)
    df['cost'] = df.cost.str.replace(',', '')\
        .replace('NA', np.nan).astype(float)
    return df

df = pd.concat([parse(get_url(pg)) for pg in range(1, 26)]).reset_index()

df.to_csv('populations-costs.csv')