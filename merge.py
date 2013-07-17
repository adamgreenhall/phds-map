import pandas as pd
import re
import simplejson
from ipdb import set_trace

def normalize(series):
    return series\
    .str.replace(' at ', ' ')\
    .str.replace(' of ', ' ')\
    .str.replace(',', '')\
    .str.replace('.', '')\
    .str.replace("'", '')\
    .str.replace(' - ', ' ')\
    .str.replace(r"(\w+)-((\w+))", r'\1 \2')\
    .str.replace(', Main Campus', '')\
    .str.replace(' Main Campus', '')\
    .str.replace('All Campuses', '')\
    .str.replace('Campus', '')\
    .str.replace('University Main', 'University')\
    .str.replace('Univ ', 'University ')\
    .str.replace('Univ$', 'University')\
    .str.replace('U$', 'University')\
    .str.replace('The University', 'University')\
    .str.replace('Texas A&M University College Station', 'Texas A&M University')\
    .str.replace('Virginia Polytechnic Institute and State University', 'Virginia Tech')\
    .str.replace(r'Pennsylvania State U$', 'Pennsylvania State University')\
    .str.replace('University Washington Seattle', 'University Washington')\
    .str.replace('Rutgers University New Brunswick', 'Rutgers University')\
    .str.replace('Columbia University in the City New York', 'Columbia University')\
    .str.replace('University Oklahoma Norman', 'University of Oklahoma')\
    .str.replace('Troy State University', 'Troy University')\
    .str.replace('Utah Valley State College', 'Utah Valley University')\
    .str.replace('University Buffalo SUNY', 'SUNY Buffalo')\
    .str.replace('Louisiana State University & Agric & Mechanical Col', 'Louisiana State University')\
    .str.replace('Washington University St Louis', 'Washington University')\
    .str.replace('Miami University Oxford', 'Miami University')\
    .str.replace('New Mexico State University Las Cruces', 'New Mexico State University')\
    .str.replace('SUNY College', 'SUNY')\
    .str.replace('Polytechnic Institute NYUniversity', 'Polytechnic University')\
    .str.replace('New School for Social Research', 'New School')\
    .str.replace('CUNY Graduate School and University Center', 'CUNY City College')\
    .str.replace('Teachers College Columbia University', 'Columbia University')\
    .str.replace('California State Polytechnic U San Luis Obispo', 'California Polytechnic State University')\
    .str.replace('Claremont Graduate School', 'Claremont McKenna College')\
    .str.replace('TX', 'Texas')\
    .str.replace('Texas State University San Marcos', 'Texas State University')\
    .str.replace('St ','Saint ')\
    .str.replace(r"(\w+) \((.+)\)", r'\1')\
    .str.strip()
    ## first regex converts "UC-Davis" -> "UC Davis"
    ## second regex gets rid of places in parens. like "DeVry Institute of Tech (Decatur GA)"

def make_merge(phds, students=None):
    # read in undergrad data
    if students is None:
        students = pd.read_csv('undergrad-populations-costs.csv')
    students['name_norm'] = normalize(students.name)
        
    phds = phds[
        # ((phds.num_docs > 0) | (phds.num_bac_docs > 5)) &
        (phds.institution.str.contains('Community') == False) &
        (phds.institution.str.contains('Pharmacy') == False) & 
        (phds.institution.str.contains('Medical') == False) &
        (phds.institution.str.contains('Health') == False) &
        (phds.institution.str.contains('Dentistry') == False) &
        (phds.institution.str.contains('Hlth Sci') == False) &
        (phds.institution.str.contains('of PR') == False)
    ]
    phds['name_norm'] = normalize(phds.institution)



    # merge
    df = pd.merge(
        phds[['institution', 'name_norm', 'state',
            'num_bac_docs', 'num_docs', 'latitude', 'longitude']],
        students[['name_norm', 'state', 'population', 'cost']],
        on=['name_norm', 'state'], 
        how='inner'
        ).rename(
            columns={'name_norm': 'name'})

    df.to_csv('phd-averages-w-pop.csv', index=False)
    missing_pops = {
        'Hillsdale College': 1402,
        "St Joseph's College, Main Campus": 5037,
        "St Mary's College of California": 2853,
        "University of North Carolina at Charlotte": 21179,
        }
    for nm, pop in missing_pops.iteritems():
        df.ix[df[df.institution == nm].index[0], 'population'] = pop
    return df
    
if __name__ == '__main__':
    phds = pd.read_csv('phd-averages.csv')
    make_merge(phds)