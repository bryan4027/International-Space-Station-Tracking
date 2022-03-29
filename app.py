from flask import Flask
import xmltodict
import json
import logging
import sys
app = Flask(__name__)


@app.route('/load_data', methods = ['POST'])
def load_data_into_file():
    
    logging.info('Files have been loaded into the memory.')
    global positions 
    global sightings
    with open('positions.xml','r') as pos:
        positions = xmltodict.parse(pos.read())
    with open('cities.xml', 'r') as cities:
        sightings = xmltodict.parse(cities.read())

        return 'Data loading is complete.'

# All the GET Defintions

@app.route('/help', methods=['GET'])
def return_instructions():
    logging.info("Instructions on requesting data printed below.")
    output = "/help - (GET) - outputs instructions/help information."
    output = output + "\n/load_data - (POST) - loads data into memory. "
    output = output + "\n/epoch - (GET) - Returns all EPOCHs. "
    output = output + "\n/epoch/<epoch> - (GET) - Returns information for requested epoch. " 
    output = output + "\n/countries - (GET) - Returns information for all countries in data. "
    output = output + "\n/countries/<country> - (GET) - Returns all information for requested country. "
    output = output + "\n/countries/<country>/regions - (GET) - Returns all requested information for requested country. "
    output = output + "\n/countries/<country>/regions/<region> - (GET) - Returns all information for requested region. "
    output = output + "\n/countries/<country>/regions/<region>/cities - (GET) - Returns all information for all cities. "
    output = output + "\n/countries/<country>/regions/<region>/city - (GET) - Returns all information for requested city. "

    return output

@app.route('/epoch', methods=['GET'])
def return_epoch():
    """
    Hello
    """
    output = "\n"
    logging.info("Looking for all of the Epoch Positions\n")
    global epoch_length
    global epoch_list #also output
    global epoch_data
    epoch_list = []
    epoch_data = positions['ndm']['oem']['body']['segment']['data']['stateVector']
    epoch_length = len(epoch_data)
    for i in range(epoch_length):
        epoch_list = epoch_list + epoch_data[i]['EPOCH'] + '\n'

    return epoch_list

@app.route('/epoch/<epoch>', methods=['GET'])
def return_specific_epoch(epoch):
    """
    Ite
    """
    logging.info("Looking for requested epoch")
    epoch_data = positions['ndm']['oem']['body']['segment']['data']['stat\
eVector']
    epoch_length = len(epoch_data)
    epoch_list = []
    for i in range(epoch_length):
        epoch_list = epoch_list + epoch_data[i]['EPOCH'] + '\n'
    neededindex = epoch_list.index(input_epoch)
    needed_data = ['X', 'Y', 'Z', 'X_DOT', 'Y_DOT', 'Z_DOT']
    output = {}
    for stuff in range(needed_data):
        output[stuff] = epoch_data[found_index][stuff]
    return output
                 
@app.route('/countries', methods=['GET'])
def return_all_countries():
    """
    Ite
    """
    logging.info("Looking for all countries")
    global sighting_data
    global sighting_list
    global sighting_n
    global country_list
    country_list = {}
    sighting_data = sightings['visible_passes']['visible_pass']
    sighting_n = len(sighting_data)
    for country in range(sighting_n):
        country_list[country] = sighting_data[country]['country']
        
    return country_list  
@app.route('/countries/<country>', methods=['GET'])
def return_specific_country(requested_country):
    """
    Ite
    """
    logging.info("Looking for requested country")
    sighting_data = sightings['visible_passes']['visible_pass']
    needed_index = sighting_data.index(requested_country)
    needed_data = ['region', 'city', 'spacecraft', 'sighting_date','duration_minutes','max_elevation','enters','exits','utc_offset','utc_time', 'utc_date']
    output_list = []
    for country in sighting_data:
        current_country = sighting_data[country]['country']
        if requested_country == current_country:
            country_data = sighting_data['visible_passes']['visible_pass'][country]
            output_list = output_list + country_data

    return json.dumps(output_list, indent  = 2)

        
@app.route('/countries/<country>/regions', methods=['GET'])
def return_regions(country):
    """
    Ite
    """
    logging.info("looking for list of all regions")
    regions_list = {}
    output_list = []
    for country in sighting_data:
        if requested_country == country:
            country_data = sighting_data['visible_passes']['visible_pass'][country]
        output_list = output_list + country_data
    for sighting in output_list:
        current_region = iss_sighting_data['visible_passes']['visible_pass'][i]['region']
        if current_region not in regions_list:
            regions_list = regions_list + current_region
    return regions_list

@app.route('/countries/<country>/regions/<region>', methods=['GET'])
def return_a_region(country, region):
    """
    Ite
    """
    logging.info("Currently looking for data within requested region")
    output_list = []
    region_data = []
    for country in sighting_data:
        if requested_country == country:
            country_data = sighting_data['visible_passes']['visible_pass'][country]
        output_list = output_list + country_data
    for sighting in output_list:
        if region == output_list[sighting]['region']:
            region_data = region_data + output_list[sighting]

    return json.dumps(region_data, indent=2)

@app.route('/countries/<country>/regions/<region>/cities', methods=['GET'])
def return_cities(country, region):
    """
    Ite
    """
    logging.info("Currently looking for list of cities")
    output_list = []
    region_data = []    
    for country in sighting_data:
        if requested_country == country:
            country_data = sighting_data['visible_passes']['visible_pass'\
][country]
        output_list = output_list + country_data
    for sighting in output_list:
        if region == output_list[sighting]['region']:
            region_data = region_data + output_list[sighting]
            
    city_list = {}
    for data in region_data:
        if current_city not in city_list:
            city_list = city_list + current_city

    return city_list
@app.route('/countries/<country>/regions/<region>/cities/<city>', methods=['GET'\
])
def return_a_city(country, region,city):
    """
    Ite
    """
    logging.info("Currently looking for specific city")
    output_list = []
    region_data = []
    city_data = []
    for country in sighting_data:
        if requested_country == country:
            country_data = sighting_data['visible_passes']['visible_pass'\
\
][country]
        output_list = output_list + country_data
    for sighting in output_list:
        if region == output_list[sighting]['region']:
            region_data = region_data + output_list[sighting]

    for sighting in region_data:
        if city == output_list[sighting]['city']:
            city_data = city_data + output_list[sighting]

    return json.dumps(city_list,indent=2)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
