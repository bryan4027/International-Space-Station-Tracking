from flask import Flask
import xmltodict
import json
import logging
import sys
app = Flask(__name__)


@app.route('/load_data', methods = ['POST'])
def load_data_into_file():
    
    logging.info('Files have been loaded into the memory.\n')
    global epochsdata
    global sightings
    with open('ISS.OEM_J2K_EPH.xml','r') as epochs:
        epochsdata = xmltodict.parse(epochs.read())
    with open('XMLsightingData_citiesINT01.xml', 'r') as sightingdata:
        sightings = xmltodict.parse(sightingdata.read())

        return 'Data loading is complete.\n'

# All the GET Defintions

@app.route('/help', methods=['GET'])
def return_instructions():
    '''
    This Route returns all of the available commands and instructions on
    how to use them.
    '''
    logging.info("Instructions on requesting data printed below.")
    output = "/help - (GET) - outputs instructions/help information."
    output = output + "\n/load_data - (POST) - loads data into memory. "
    output = output + "\n/epoch - (GET) - Returns all EPOCHs. "
    output = output + "\n/epoch/<epoch> - (GET) - Returns information for requested epoch. " 
    output = output + "\n/countries - (GET) - Returns information for all countries in data. "
    output = output + "\n/countries/<country> - (GET) - Returns all information for requested country. "
    output = output + "\n/countries/<country>/regions - (GET) - Returns all requested information for requested country."
    output = output + "\n/countries/<country>/regions/<region> - (GET) - Returns all information for requested region. "
    output = output + "\n/countries/<country>/regions/<region>/cities - (GET) - Returns all information for all cities."
    output = output + "\n/countries/<country>/regions/<region>/city - (GET) - Returns all information for requested city. "

    return output

@app.route('/epoch', methods=['GET'])
def return_epoch():
    """
    This route grabs all of the epochs and makes it a list.

    Return: it returns the list of epochs
    """
    output = "\n"
    logging.info("Looking for all of the Epoch Positions\n")
    global epoch_length
    global epoch_list #also output
    global epoch_data
    epoch_list = ""
    epoch_data = epochsdata['ndm']['oem']['body']['segment']['data']['stateVector']
    epoch_length = len(epoch_data)
    for i in range(epoch_length):
        epoch_list = epoch_list + epoch_data[i]['EPOCH'] + '\n'

    return epoch_list

@app.route('/epoch/<epoch>', methods=['GET'])
def return_specific_epoch(epoch: str):
    """
    Input: This route reads in an input indicating which epoch's information is requested

    The route loops through the list of epochs and returns the data for the requested epoch. 

    Output: The route outputs the requested epoch's information in the form of a JSON
    """
    logging.info("Looking for requested epoch")
    epoch_data = epochsdata['ndm']['oem']['body']['segment']['data']['stateVector']
    output_list = []
    for pos in range(len(epoch_data)):
        current_epoch = epoch_data[pos]['EPOCH']
        if epoch == current_epoch:
            specific_epoch_data = epoch_data[pos]
            output_list.append(specific_epoch_data)
    
    return json.dumps(output_list, indent=2)
                 
@app.route('/countries', methods=['GET'])
def return_all_countries():
    """
    This route loops through all of the data and returns the countries that are included with data in a list. 

    The route outputs the list of countries in the data
    """
    logging.info("Looking for all countries")
    global sighting_data
    global sighting_list
    global sighting_n
    global country_list
    country_list = ""
    sighting_data = sightings['visible_passes']['visible_pass']
    sighting_n = len(sighting_data)
    for country in range(sighting_n):
        current_country = sighting_data[country]['country']
        if current_country not in country_list:
            country_list = country_list + current_country + '\n'
        
    return country_list  
@app.route('/countries/<country>', methods=['GET'])
def return_specific_country(country: str):
    """
    Input: this route inputs a string for a requested country from the outputed list from the /countries route
    
    the route iterates through the data and compiles all the data that goes through the requested country and puts it into a JSON formatted list

    output: the route outputs JSON formatted data for all the positons above the requested country.
    """
    logging.info("Looking for requested country")
    sighting_data = sightings['visible_passes']['visible_pass']
    #needed_index = sighting_data.index(country)
    needed_data = ['region', 'city', 'spacecraft', 'sighting_date','duration_minutes','max_elevation','enters','exits','utc_offset','utc_time', 'utc_date']
    output_list = []
    for sighting in range(len(sighting_data)):
        current_country = sighting_data[sighting]['country']
        if country == current_country:
            country_data = sighting_data[sighting]
            output_list.append(country_data)

    return json.dumps(output_list, indent  = 2)

        
@app.route('/countries/<country>/regions', methods=['GET'])
def return_regions(country: str):
    """
    input: the route requests a specific country so that it can get the data from that coutnry.

    the route iterates through the outputted json formatted data from the previous route to find all data positioned over a specific region.

    output: it returns a string list of all of the regions
    """
    logging.info("looking for list of all regions")
    regions_list = ""
    output_list = []
    sighting_data = sightings['visible_passes']['visible_pass']
    for sighting in range(len(sighting_data)):
        current_country = sighting_data[sighting]['country']
        if current_country == country:
            country_data = sighting_data[sighting]
            output_list.append(country_data)
    #output_json = json.dumps(output_list, indent  = 2)
    for sighting in range(len(output_list)):
        current_region = output_list[sighting]['region']
        if current_region not in regions_list:
            regions_list = regions_list + current_region + '\n'
    return regions_list

@app.route('/countries/<country>/regions/<region>', methods=['GET'])
def return_a_region(country: str, region: str):
    """
    Input: the route requests an input for a country and region to specify which country and region you want to search for data

    the route iterates through the data and compiles all of the data from the requested region into a JSON format.

    output: this outputs all of the positions that are within the requested country and requested region.
    """
    logging.info("Currently looking for data within requested region")
    output_list = []
    region_data = []
    sighting_data = sightings['visible_passes']['visible_pass']
    for sighting in range(len(sighting_data)):
        current_country = sighting_data[sighting]['country']
        if current_country == country:
            country_data = sighting_data[sighting]
            output_list.append(country_data)
    for sighting in range(len(output_list)):
        
        if region == output_list[sighting]['region']:
            region_data.append(output_list[sighting])

    return json.dumps(region_data, indent=2)

@app.route('/countries/<country>/regions/<region>/cities', methods=['GET'])
def return_cities(country: str, region: str):
    """
    Input: the route requests an input for a country and region to specify which country and region you want to search for data

    the route iterates through the data for the requested country and region to compile a list of all the cities in the data. The list is inputted into a string.

    Output: The route outputs the string, a list of all the cities in the requested data.
    """
    logging.info("Currently looking for list of cities")
    output_list = []
    region_data = []    
    sighting_data = sightings['visible_passes']['visible_pass']
    for sighting in range(len(sighting_data)):
        current_country = sighting_data[sighting]['country']
        if current_country == country:
            country_data = sighting_data[sighting]
            output_list.append(country_data)
    for sighting in range(len(output_list)):
        if region == output_list[sighting]['region']:
            region_data.append(output_list[sighting])
            
    city_list = ""
    for data in range(len(region_data)):
        current_city = region_data[data]['city']
        if current_city not in city_list:
            city_list = city_list + current_city+ '\n'

    return city_list
@app.route('/countries/<country>/regions/<region>/cities/<city>', methods=['GET'\
])
def return_a_city(country: str, region: str,city: str):
    """
    input: the route requests a country, region, and city where the user wants to grab the data from. They are all strings.

    The route iterates through the list of data that pertains to the requested city and compiles it onto a JSON formatted list.

    output: The route outputs a JSON formatted compilation of data within a city.
    """
    logging.info("Currently looking for specific city")
    output_list = []
    region_data = []
    city_data = []
    sighting_data = sightings['visible_passes']['visible_pass']
    for sighting in range(len(sighting_data)):
        current_country = sighting_data[sighting]['country']
        if current_country == country:
            country_data = sighting_data[sighting]
            output_list.append(country_data)
    for sighting in range(len(output_list)):
        if region == output_list[sighting]['region']:
            region_data.append(output_list[sighting])
    for sighting in range(len(region_data)):
        if city == region_data[sighting]['city']:
            city_data.append(region_data[sighting])

    return json.dumps(city_data,indent=2)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
