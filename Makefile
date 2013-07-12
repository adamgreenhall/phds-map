.PHONY: install


### get the data ###

# phds-by-institution.csv:
# sadly the SED survey results are not machine accessable and must be downloaded by hand from https://webcaspar.nsf.gov/

# 

zipcode.csv:
	curl "http://www.boutell.com/zipcodes/zipcode.zip" -o zipcodes.zip
	unzip zipcodes.zip zipcode.csv

populations-costs.csv:
	python get_undergrad_pop.py

install:
	pip install -r Requirements

phd-averages.csv:
	python totals.py

us-10m.json:
	cd ~/code/us-atlas && make topo/us-10m.json
	cp ~/code/us-atlas/topo/us-10m.json .

us-counties-graduates.json: 
	# depends on us-counties.json us-counties-graduates.csv
	topojson --external-properties us-counties-graduates.csv \
	  --id-property id_county \
	  --properties percent_graduates=+percent_graduates \
	  -o us-counties-graduates.json \
	  -- us-counties.json
	  #     -q 1e5 -s 7e-7 \
	  # -- ~/code/us-atlas/shp/us/counties.shp