.PHONY: install


### get the data ###

# phds-by-institution.csv:
# sadly the SED survey results are not machine accessable and must be downloaded by hand from https://webcaspar.nsf.gov/

zipcode.csv:
	curl "http://www.boutell.com/zipcodes/zipcode.zip" -o zipcodes.zip
	unzip zipcodes.zip zipcode.csv


install:
	pip install -r Requirements

phd-averages.csv:
	python totals.py