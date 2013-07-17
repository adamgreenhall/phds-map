# import urllib2
# from pygeocoder import Geocoder
# xls = pd.ExcelFile(urllib2.urlopen(
#     'http://classifications.carnegiefoundation.org/downloads/2000_edition_data.xls'))
# schools = xls.parse('Data')
# 
# # get the FICE code for each university
# FICE = pd.read_csv('phds-by-institution.csv').FICE.dropna().unique().astype(int)
# schools = schools[schools.FICE.astype(int).isin(FICE)]
# 
# # schools = pd.read_csv('Accreditation_2013_03.csv')\
# #     .groupby('Institution_ID').first()
# 
# schools['address'] = schools.CITY + ', ' + schools.ST
# 
# # schools['address'] = \
# #     schools.Institution_Address + ', ' + \
# #     schools.Institution_City + ', ' + \
# #     schools.Institution_State
# 
# for i, address in schools.address.dropna().iteritems():
#     pos = Geocoder.geocode(address)
#     schools.ix[i, 'latitude'] = pos.latitude
#     schools.ix[i, 'longitude'] = pos.longitude
# 
# schools.drop('address', axis=1).to_csv('academic-institutions.csv')