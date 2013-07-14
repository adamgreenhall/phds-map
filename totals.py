import pandas as pd
import utils, simplejson
from ipdb import set_trace



def get_totals():
    cols = {
        'Year': 'year',
        'Academic Institution (standardized)': 'institution',
        'Academic Discipline, Detailed (standardized)': 'discipline',
        'Number of Doctorate Recipients by Doctorate Institution(Sum)': 'num_docs',
        'Number of Doctorate Recipients by Baccalaureate Institution(Sum)': 'num_bac_docs',
        }
    cols_counts = ['num_bac_docs', 'num_docs']

    df = pd.read_csv('phds-by-institution.csv', na_values='.')\
        [cols.keys()].rename(columns=cols).dropna(how='all')\
        .sort(['institution', 'year', 'discipline']).reset_index(drop=True)

    for col in cols_counts: df[col] = df[col].fillna(0).astype(int)

    # get average PhD count for all disciplines for each university
    totals_by_year = df.groupby(['institution', 'year']).sum()
    totals_by_discipline = df.groupby(['institution', 'discipline'])[cols_counts].sum()

    totals = totals_by_year.reset_index()\
        .groupby('institution')[cols_counts].sum().reset_index()
    return totals, totals_by_discipline, totals_by_year

def get_locs():
    cols = {
        'Academic Institution (standardized)': 'institution',
        'Zip': 'zip'}

    schools = pd.read_csv('phds-by-institution.csv')\
        [cols.keys()].rename(columns=cols)\
        .groupby('institution').first().reset_index()
    schools['zip'] = schools.zip.astype(str)

    zipcodes = pd.read_csv('zip_code_database.csv', dtype={'zip':str})[
        ['zip', 'state', 'latitude', 'longitude']
    ]

    return pd.merge(schools, zipcodes, on='zip', how='inner').dropna()


def make_summary(totals):
    # get the locations of the schools (lat, long from zipcode)
    schools = get_locs()

    # merge the datasets and add back in the international doctors too
    # (place them somewhere off Baja)
    summary = pd.merge(schools, totals.reset_index(), on='institution').append(
        pd.Series(dict(
            institution='International',
            num_bac_docs=totals.num_bac_docs.iloc[1],
            num_docs=0,
            latitude=29.228359, longitude=-123.072512)), 
        ignore_index=True)
    
    summary.to_csv('phd-averages.csv', index=False)
    return summary

def make_json(totals_by_year, summary=None):
    if summary is None: 
        summary = pd.read_csv('phd-averages-w-pop.csv')

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
    summary = make_summary(totals)
    # make_json(totals_by_year)