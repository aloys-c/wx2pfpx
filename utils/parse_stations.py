import json
from typing_extensions import dataclass_transform
import requests
import xml.etree.ElementTree as ET
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

metar_url = "https://aviationweather.gov/adds/dataserver_current/httpparam?datasource=stations&requestType=retrieve&fields=elevation_m&format=xml&stationString="

def xml2array(xml,s,e,name):
        array = []
        root = ET.fromstring(xml)
        for child in root.iter('*'):
            if("elevation_m" in child.tag):     
                print(child.text)
                return child.text

if(0):
    with open("./output/wx_station_list.txt","w+") as out_file:
        line_out = ""

        data = []
        n = 0
        arpts = open("utils/airports.dat")
        for line in arpts :
            #response = requests.get(metar_url+line[0:4])
            #temp = xml2array(response.content,0,4,"elevation_m")
            if(1):
                n = n+1
                temp = 1000
            data.append({"code":line[0:4],"lat":float(line[4:14]),"lon":float(line[14:25]),"alt":int(temp)})
            line_out +=line[0:4]+","+line[4:14]+","+line[14:25]+","+str(temp)+"\n"

        with open("airports.json","w") as data_file:
            json.dump(data,data_file)

        stations = open("data/stations")
        stations = json.load(stations)

   # for station in stations:
        #station['alt'] = int(station['alt'])
        #station['code'] = station.pop('CODE')
        

    with open("stations.json","w") as new:
        json.dump(stations,new)
    print(line_out)
    out_file.write(line_out+"\n")


if(1):

    with open("./data/airports") as arpts_file:
            airports = json.load(arpts_file)
    with open("./data/stations") as arpts_file:
            stations = json.load(arpts_file)

   
    fig = plt.figure(figsize=(36, 18))
    m = Basemap(projection='cyl',lon_0=0.0, lat_0=0.0,width=36E6, height=18E6, resolution='c')
    m.drawcoastlines()
    
    handle_dict = {
    "Airports" : 0,
    "Extra stations" : 0,
    }
   

    for i in range(0,len(airports)):
        if(i%1 ==0):
            if(i%1000 ==0):
                print(i)
            y = round(float(airports[i]['lat']))
            x = round(float(airports[i]['lon']))
            m.scatter(x,y,color="red",s=1,label = 
                "Airports" if handle_dict['Airports'] == 0
                else "_no-legend_")
            handle_dict['Airports'] += 1
    
    
    for i in range(0,len(stations)):
        if(i%1 ==0):
            if(i%100 ==0):
                print(i)
            y = round(float(stations[i]['lat']))
            x = round(float(stations[i]['lon']))
            m.scatter(x,y,color="blue",s=1,label = 
                "Extra stations" if handle_dict['Extra stations'] == 0
                else "_no-legend_")
            handle_dict['Extra stations'] += 1
   
    plt.legend(loc="lower center", ncol=2,bbox_to_anchor =(0.5, -0.08))
    plt.show()

