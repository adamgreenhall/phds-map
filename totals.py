import pandas as pd
import utils
import simplejson

from ipdb import set_trace

def get_totals():
    cols = {
        'Year': 'year',
        'Academic Institution (standardized)': 'institution',
        'Zip': 'zip',
        'Academic Discipline, Detailed (standardized)': 'discipline',
        'Number of Doctorate Recipients by Doctorate Institution(Sum)': 'num_docs',
        'Number of Doctorate Recipients by Baccalaureate Institution(Sum)': 'num_bac_docs',
        }
    cols_counts = ['num_bac_docs', 'num_docs']

    df = pd.read_csv('phds-by-institution.csv', 
        na_values='.', dtype={'Zip': str})\
        [cols.keys()].rename(columns=cols).dropna(how='all')\
        .sort(['institution', 'year', 'discipline']).reset_index(drop=True)

    for col in cols_counts: df[col] = df[col].fillna(0).astype(int)

    # get average PhD count for all disciplines for each university
    totals_by_year = df.groupby(['institution', 'year']).sum()
    totals_by_discipline = df.groupby(['institution', 'discipline'])[cols_counts].sum()

    totals = totals_by_year.reset_index()\
        .groupby('institution')[cols_counts].sum().reset_index()
    # add zipcodes back in
    locations = df.groupby(['zip', 'institution']).first()\
        .reset_index()[['zip', 'institution']]
    totals = pd.merge(totals, locations, on='institution', how='inner')
    
    return totals, totals_by_discipline, totals_by_year

def add_locs(totals):
    zipcodes = pd.read_csv('zip_code_database.csv', dtype={'zip':str})[
        ['zip', 'state', 'latitude', 'longitude']
    ]

    # merge the datasets and add back in the grouped international 
    # PhD almamater too (place it somewhere off Baja)
    return pd.merge(totals, zipcodes, on='zip', how='inner').append(
        pd.Series(dict(
            institution='International',
            num_bac_docs=totals.num_bac_docs.iloc[1],
            num_docs=0,
            latitude=29.228359, longitude=-123.072512)), 
        ignore_index=True)


def make_json(summary, totals_by_year): 
    json = summary.to_jsonblob()
    for i, row in summary.iterrows():
        name = row['institution']
        if name == 'International': name = '. Foreign Institutions'
        json[i]['by_year'] = totals_by_year.ix[name].to_jsonblob(reset=True)
        # json[i]['by_discipline'] = totals_by_discipline.ix[name].to_jsonblob(reset=True)
    
    with open('phds.json', 'w+') as f:
        simplejson.dump(json, f)    

if __name__ == '__main__':
    totals, totals_by_discipline, totals_by_year = get_totals()
    make_json(add_locs(totals), totals_by_year)