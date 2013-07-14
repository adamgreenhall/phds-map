import pandas as pd
import re

def normalize(series):
    return series\
    .str.replace(' at ', ' ')\
    .str.replace(',', '')\
    .str.replace(' - ', ' ')\
    .str.replace('Wisconsin-', 'Wisconsin ')\
    .str.replace(', Main Campus', '')\
    .str.replace(' Main Campus', '')\
    .str.replace('University Main', 'University')\
    .str.replace('All Campuses', '')\
    .str.replace('The University', 'University')\
    .str.replace('University of California-', 'University of California ')\
    .str.replace('Texas A&M University College Station', 'Texas A&M University')\
    .str.replace('Virginia Polytechnic Institute and State Univ', 'Virginia Tech')\
    .str.replace('Pennsylvania State U', 'Pennsylvania State University')\
    .str.replace('University of Washington Seattle', 'University of Washington')\
    .str.replace(r"(\w+) \((.+)\)", r'\1')\
    .str.strip()
    ## regex gets rid of places in parens. like "DeVry Institute of Tech (Decatur GA)"
    
# read in undergrad data
pop = pd.read_csv('undergrad-populations-costs.csv')
pop['name_norm'] = normalize(pop.name)

# read in phds data
phds = pd.read_csv('phd-averages.csv')
phds = phds[
    ((phds.num_docs > 0) | (phds.num_bac_docs > 5)) &
    phds.zip.notnull() & 
    (phds.institution.str.contains('Community') == False) &
    (phds.institution.str.contains('Pharmacy') == False) & 
    (phds.institution.str.contains('Medical') == False) &
    (phds.institution.str.contains('of PR') == False)
]
phds['name_norm'] = normalize(phds.institution)


# merge

df = pd.merge(phds, pop[['name', 'name_norm', 'population', 'cost']], left_on='name_norm', right_on='name_norm', how='inner')