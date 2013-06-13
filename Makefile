.PHONY: install


### get the data ###

# phds-by-institution.csv:
# sadly the SED survey results are not machine accessable and must be downloaded by hand from https://webcaspar.nsf.gov/

zipcode.csv:
	curl "http://www.boutell.com/zipcodes/zipcode.zip" -o zipcodes.zip
	unzip zipcodes.zip zipcode.csv

# academic-institutions.csv:
# 	curl "http://ope.ed.gov/accreditation/dataFiles/Accreditation_2013_03.zip" -o institutions.zip
# 	unzip institutions.zip Accreditation_2013_03.csv
# 	python get_school_loc.py



install:
	pip install -r Requirements

phd-averages.csv:
	python totals.py
	cp phd-averages.csv ~/design/website-adamgreenhall/public/phd-averages.csv