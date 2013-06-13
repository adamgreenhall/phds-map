import pandas as pd

def get_locs():
    cols = {
        'Academic Institution (standardized)': 'institution',
        'Zip': 'zip'}

    schools = pd.read_csv('phds-by-institution.csv')\
        [cols.keys()].rename(columns=cols)\
        .groupby('institution').first().reset_index()
    schools['zip'] = schools.zip.astype(str)

    zipcodes = pd.read_csv('zipcode.csv', dtype={'zip': object}
        )[['zip', 'latitude', 'longitude']]
    zipcodes['zip'] = zipcodes.zip.astype(str)

    return pd.merge(schools, zipcodes, on='zip', how='inner').dropna()
    
cols = {
    'Year': 'year',
    'Academic Institution (standardized)': 'institution',
    'Academic Discipline, Detailed (standardized)': 'discipline',
    'Number of Doctorate Recipients by Doctorate Institution(Sum)': 'num_docs',
    'Number of Doctorate Recipients by Baccalaureate Institution(Sum)': 'num_bac_docs',
    }

df = pd.read_csv('phds-by-institution.csv', na_values='.')\
    [cols.keys()].rename(columns=cols).fillna(0)

# get average PhD count for all disciplines for each university
totals = df.groupby(['institution', 'year']).sum()\
    .reset_index().groupby('institution').mean()[['num_bac_docs', 'num_docs']]


schools = get_locs()
pd.merge(schools, totals.reset_index(), on='institution').append(
    pd.Series(dict(
        institution='International',
        num_bac_docs=totals.num_bac_docs.iloc[1],
        num_docs=0,
        latitude=29.228359, longitude=-123.072512)), 
    ignore_index=True).to_csv(
        'phd-averages.csv', index=False)