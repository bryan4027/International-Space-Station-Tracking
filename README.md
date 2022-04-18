# This folder belongs to Bryan Acosta's International-Space-Station-Tracking Midterm Project.
Eid ba25389. TACC id: ba25389.

# Tracking the International Space Station
The purpose of this project is to read in a data set directly from NASA's website and use that data to find information of where the ISS has been spotted throughout the world. It orgnizaes the data in JSON format where it has information about sightings including but not limited to the country, region, and city the sighting took place. The application created is made into a flask application than can be accessed from other computers. The application is then tested with a PyTest application, ran with a Makefile and containerized using Docker which is built using the Makefile.

# Part 1 Python Script:
This python script's purpose is to read in a xml file, converted to JSON format, and manipulating the data using different loops and strategies to search through the data.

<details>
<summary>Show python script 1: app.py</summary>
Python

```python:
from flask import Flask
import xmltodict
import json
import logging
import sys
app = Flask(__name__)


@app.route('/load_data', methods = ['POST'])
def load_data_into_file():
    
    logging.info('Files have been loaded into the memory.\n')
    global positions 
    global sightings
    with open('positions.xml','r') as pos:
        positions = xmltodict.parse(pos.read())
    with open('cities.xml', 'r') as cities:
        sightings = xmltodict.parse(cities.read())

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
    epoch_data = positions['ndm']['oem']['body']['segment']['data']['stateVector']
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
    epoch_data = positions['ndm']['oem']['body']['segment']['data']['stateVector']
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

    
```
</details>

# Part 2 Test Python Script:
This second Python Script is used to test the correctness of the `app.py` file. It uses unit testing to individually test if the functions input and output are correct and more using Pytest.

<details>
<summary>Show python script 2: test_app.py </summary>
Python

```python:
	
import pytest
from app import *


load_data_into_file()
def return_instructions():
    assert isinstance(return_instructions(),str)==True

def test_return_epoch():
    assert isinstance(return_epoch(),str)==True

def test_return_specific_epoc():
    assert isinstance(return_specific_epoch('2022-057T11:48:56.869Z'),dict)!=True

def test_return_all_countries():
    assert isinstance(return_all_countries(),str)==True

def test_return_specific_country():
    assert isinstance(return_specific_country('Belgium'),dict)!=True

def test_return_regions():
    assert isinstance(return_regions('Belgium'),str)==True

def test_return_a_region():
    assert isinstance(return_a_region('Belgium', 'None'),dict)!=True
def test_return_cities():
    assert isinstance(return_cities('Belgium','None'),str)==True
def test_return_a_city():
    assert isinstance(return_a_city('Belgium','None','Wervik'),dict)!=True

```
</details>

# Part 3 Make File Script:
This File is used to build, containerize, run, and push the folder onto Docker. 

<details>
<summary>Show python script 2: Makefile </summary>
Python

```python:
all: build run push

images:
	docker images | grep bryan4027
ps:
	docker ps -a | grep bryan4027
build:
	docker build -t bryan4027/iss_tracking10:1.3 .
run:
	docker run --name "iss_tracking10" -it -p 5001:5000 bryan4027/iss_tracking10:1.3
push:
	docker push bryan4027/iss_tracking0:1.3	  
    
```
</details>

# Part 4 Dockerfile Script:
This File is used to build, containerize, and set up the Docker Image so that it is ready to run the application without having to manually install anything.

<details>
<summary>Dockerfile </summary>
Python

```python:
FROM centos:7.9.2009

RUN yum update -y && yum install -y python3
RUN pip3 install pytest==7.0.0
RUN pip3 install --user xmltodict
RUN mkdir /code
RUN pip3 install flask

COPY app.py /code/app.py
COPY pytest_app.py /code/pytest_app.py
COPY cities.xml /code/cities.xml
COPY positions.xml /code/positions.xml
COPY . /app

RUN chmod +rx /code/app.py
RUN chmod +rx /code/pytest_app.py

ENV PATH "/code:$PATH"
    
```
</details>
    
# Instructions for Program: 
1. Download `ISS.OEM_J2K_EPH.xml` by running the following into the terminal:
```python:
wget https://nasa-public-data.s3.amazonaws.com/iss-coords/2022-02-13/ISS_OEM/ISS.OEM_J2K_EPH.xml
```
2. Observe the produced JSON file `ISS.OEM_J2K_EPH.xml` to ensure that the file was produced correctly. It should look like the following:
<details>
<summary>Show ISS.OEM_J2K_EPH.xml </summary>
Python

```python:
{
{
   "oem": {
      "@id": "CCSDS_OEM_VERS",
      "@version": "2.0",
      "header": {
         "CREATION_DATE": "2022-042T18:53:27.821Z",
         "ORIGINATOR": "JSC"
      },
      "body": {
         "segment": {
            "metadata": {
               "OBJECT_NAME": "ISS",
               "OBJECT_ID": "1998-067-A",
               "CENTER_NAME": "EARTH",
               "REF_FRAME": "EME2000",
               "TIME_SYSTEM": "UTC",
               "START_TIME": "2022-042T12:00:00.000Z",
               "STOP_TIME": "2022-057T12:00:00.000Z"
            },
            "data": {
               "COMMENT": [
                  "Units are in kg and m^2",
                  "MASS=445386.00",
                  "DRAG_AREA=1439.70",
                  "DRAG_COEFF=3.40",
                  "SOLAR_RAD_AREA=0.00",
                  "SOLAR_RAD_COEFF=0.00",
                  "Orbits start at the ascending node epoch",
                  "ISS first asc. node: EPOCH = 2022-02-11T12:08:41.500 $ ORBIT = 568 $ LAN(DEG) = -84.71503",
                  "ISS last asc. node : EPOCH = 2022-02-26T11:10:09.027 $ ORBIT = 800 $ LAN(DEG) = -158.91754",
                  "Begin sequence of events",
                  "TRAJECTORY EVENT SUMMARY:",
                  [],
                  "|       EVENT        |       TIG        | ORB |   DV    |   HA    |   HP    |",
                  "|                    |       GMT        |     |   M/S   |   KM    |   KM    |",
                  "|                    |                  |     |  (F/S)  |  (NM)   |  (NM)   |",
                  "=============================================================================",
                  "80P Launch            046:04:25:40.000             0.0     426.3     408.0",
                  "(0.0)   (230.2)   (220.3)",
                  [],
                  "80P Arrivals          048:07:06:29.000             0.0     425.6     408.2",
                  "(0.0)   (229.8)   (220.4)",
                  [],
                  "NG-17 Launch          050:17:39:59.000             0.0     425.4     408.4",
                  "(0.0)   (229.7)   (220.5)",
                  [],
                  "NG-17 Arrival         052:09:35:00.000             0.0     424.8     408.6",
                  "(0.0)   (229.4)   (220.6)",
                  [],
                  "GMT057 Reboost        057:01:37:00.000             0.4     423.8     409.1",
                  "(1.3)   (228.8)   (220.9)",
                  [],
                  "=============================================================================",
                  "End sequence of events"
               ],
               "stateVector": [
                  {
                     "EPOCH": "2022-042T12:00:00.000Z",
                     "X": {
                        "@units": "km",
                        "#text": "-4945.2048874258298"
                     },
                     "Y": {
                        "@units": "km",
                        "#text": "-3625.9704508659102"
                     },
                     "Z": {
                        "@units": "km",
                        "#text": "-2944.7433487186099"
                     },
                     "X_DOT": {
                        "@units": "km/s",
                        "#text": "1.19203952554952"
                     },
                     "Y_DOT": {
                        "@units": "km/s",
                        "#text": "-5.67286420497775"
                     },
                     "Z_DOT": {
                        "@units": "km/s",
                        "#text": "4.99593211898374"
                     }
                  },
                  {
                     "EPOCH": "2022-042T12:04:00.000Z",
                     "X": {
                        "@units": "km",
                        "#text": "-4483.2181885642003"
                     },
                     "Y": {
                        "@units": "km",
                        "#text": "-4839.4374260438099"
                     },
                     "Z": {
                        "@units": "km",
                        "#text": "-1653.1850590663901"
                     },
                     "X_DOT": {
                        "@units": "km/s",
                        "#text": "2.63479158884966"
                     },
                     "Y_DOT": {
                        "@units": "km/s",
                        "#text": "-4.3774148889971602"
                     },
                     "Z_DOT": {
                        "@units": "km/s",
                        "#text": "5.7014974180323597"
                     }
                  },
```
</details>
    
3. Download `XMLsightingData_citiesINT01.xml` by running the following into the terminal:
```python:
wget https://nasa-public-data.s3.amazonaws.com/iss-coords/2022-02-13/ISS_sightings/XMLsightingData_citiesINT01.xml
```
4. Observe the produced JSON file `XMLsightingData_citiesINT01.xml` to ensure that the file was produced correctly. It should look like the following:
<details>
<summary>Show XMLsightingData_citiesINT01.xml </summary>
Python

```python:
{
{
    "country": "Belgium",
    "region": "None",
    "city": "Aalst",
    "spacecraft": "ISS",
    "sighting_date": "Thu Feb 17/07:07 AM",
    "duration_minutes": "1",
    "max_elevation": "10",
    "enters": "10 above SE",
    "exits": "10 above SE",
    "utc_offset": "1.0",
    "utc_time": "06:07",
    "utc_date": "Feb 17, 2022"
  },
  {
    "country": "Belgium",
    "region": "None",
    "city": "Aalst",
    "spacecraft": "ISS",
    "sighting_date": "Sat Feb 19/07:04 AM",
    "duration_minutes": "5",
    "max_elevation": "22",
    "enters": "10 above SSW",
    "exits": "10 above E",
    "utc_offset": "1.0",
    "utc_time": "06:04",
    "utc_date": "Feb 19, 2022"
  },
```
</details>
	
5.  Start the Flask application so it is accessible from the web. Type the following into the terminal one by one. For the last program, replace the 5001 with your respective port.
	
```python: 
export FLASK_APP=app.py
export FLASK_ENV=development
flask run -p 5001	
``` 
	
6. Observe Output. If the application was successfully loaded then the following will be outputed.
```python:
 * Serving Flask app 'app.py' (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5001/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 106-306-171
```
    
7. In order to test the flask, open another terminal window and log back into your SSH server. Load the application using `curl localhost:5001/load_data -X POST`. That command will load all the data into the correct files. Then, you can see a list of instructions on how to use the application using `curl localhost:5001/help`. The output should look like this:
	
```python:
/help - (GET) - outputs instructions/help information.
/load_data - (POST) - loads data into memory.
/epoch - (GET) - Returns all EPOCHs.
/epoch/<epoch> - (GET) - Returns information for requested epoch.
/countries - (GET) - Returns information for all countries in data.
/countries/<country> - (GET) - Returns all information for requested country.
/countries/<country>/regions - (GET) - Returns all requested information for requested country.
/countries/<country>/regions/<region> - (GET) - Returns all information for requested region.
/countries/<country>/regions/<region>/cities - (GET) - Returns all information for all cities.
/countries/<country>/regions/<region>/city - (GET) - Returns all information for requested city.	
	
```	
	
8. You can now interact with and use the Flask application to observe the data. You can use `curl localhost:5001/countries/Belgium/regions/None/cities/Wervik` to see the data of the sightings observed in the city of Wervik in Belgium. Test out other data by starting with `curl localhost:5001/countries` and following the instructions from there.
9. You can now test the program is running correctly by running `pytest emacs pytest_app.py` and the output should look like this if it ran correctly:
	
```python:
============================ test session starts ============================
platform linux -- Python 3.6.8, pytest-7.0.1, pluggy-1.0.0
rootdir: /home/ba25389/332/midterm/International-Space-Station-Tracking
collected 8 items

pytest_app.py ........                                                [100%]

============================= 8 passed in 1.26s =============================
	
```
10. Run the Makefile to build the Docker Image. Run `Make all`
<details>
<summary>Show output </summary>
Python

```python:	 	
Sending build context to Docker daemon  5.352MB
Step 1/14 : FROM centos:7.9.2009
 ---> eeb6ee3f44bd
Step 2/14 : RUN yum update -y && yum install -y python3
 ---> Using cache
 ---> d605a0dae43f
Step 3/14 : RUN pip3 install pytest==7.0.0
 ---> Using cache
 ---> f4be093b12b2
Step 4/14 : RUN pip3 install --user xmltodict
 ---> Using cache
 ---> 34959355fb0b
Step 5/14 : RUN mkdir /code
 ---> Using cache
 ---> ea5ed6ac6547
Step 6/14 : RUN pip3 install flask
 ---> Using cache
 ---> 35feace33255
Step 7/14 : COPY app.py /code/app.py
 ---> Using cache
 ---> 62a624a13d4c
Step 8/14 : COPY pytest_app.py /code/pytest_app.py
 ---> 0316dfd3d98f
Step 9/14 : COPY cities.xml /code/cities.xml
 ---> 819d589968b7
Step 10/14 : COPY positions.xml /code/positions.xml
 ---> e151f2ebbe76
Step 11/14 : COPY . /app
 ---> d0bcba186a2e
Step 12/14 : RUN chmod +rx /code/app.py
 ---> Running in a69b09c4989b
Removing intermediate container a69b09c4989b
 ---> 693488abb066
Step 13/14 : RUN chmod +rx /code/pytest_app.py
 ---> Running in cce0b7ffc546
Removing intermediate container cce0b7ffc546
 ---> 5cb7aa2d2e18
Step 14/14 : ENV PATH "/code:$PATH"
 ---> Running in b88a4d3232ee
Removing intermediate container b88a4d3232ee
 ---> d939ea72f19d
Successfully built d939ea72f19d
Successfully tagged bryan4027/iss_tracking10:1.3
docker run --name "iss_tracking10" -it -p 5001:5000 bryan4027/iss_tracking10:1.3
```
</details>
	
# Citations
Goodwin, S. (n.d.). ISS_COORDS_2022-02-13. NASA. https://nasa-public-data.s3.amazonaws.com/iss-coords/2022-02-13/ISS_OEM/ISS.OEM_J2K_EPH.xml Retrieved March 17, 2022, from https://data.nasa.gov/Space-Science/ISS_COORDS_2022-02-13/r6u8-bhhq

Goodwin, S. (n.d.). XMLsightingData_citiesINT01. NASA. Retrieved April 17, 2022, from https://nasa-public-data.s3.amazonaws.com/iss-coords/2022-02-13/ISS_sightings/XMLsightingData_citiesINT01.xml	
