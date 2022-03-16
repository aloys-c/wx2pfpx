from cmath import sqrt
from encodings import utf_8
from math import atan2
import requests
import xml.etree.ElementTree as ET
import pygrib
import matplotlib.pyplot as plt
import json
import math
#grbs = pygrib.open("gfs.t12z.pgrb2.1p00.anl")

metar_url = "https://aviationweather.gov/adds/dataserver_current/httpparam?datasource=metars&requestType=retrieve&fields=raw_text&format=xml&mostRecentForEachStation=constraint&hoursBeforeNow=3&stationString="
taf_url = "https://aviationweather.gov/adds/dataserver_current/httpparam?datasource=tafs&requestType=retrieve&fields=raw_text&format=xml&mostRecentForEachStation=constraint&hoursBeforeNow=3&stationString="

#chars = list(map(chr,range(65,91)))+list(map(chr,range(48,58)))
#ids = chars[0:10]+["K" + c for c in chars]+chars[11:26]


def mb2feet(mb):
    return (1-pow(mb/1013.25,0.190284))*145366.45

def xml2array(xml):
        array = []
        root = ET.fromstring(xml)
        for child in root.iter('*'):
            if("raw_text" in child.tag):
                array.append({"ICAO":child.text[0:4],"METAR":child.text})
        return array

def get_metars():
    print("Dowloading metars...")
    ids = ["A B C D","E F G H"] + ["KA KB KC KD KE KF KG"," KH KI KJ KK KL KM KN KO KP KQ KR"," KS KT KU KV KW KX KY KZ K1 K2 K3 K4 K5 K6 K7 K8 K9 K0"]+["L M N O P Q","R S T U V W X Y Z"]

    metars = []
    tafs = []

    for i in ids:
        
        response = requests.get(metar_url+i)
        temp = xml2array(response.content)
        metars.extend(temp)

        #response = requests.get(taf_url+i)
        #temp = xml2array(response.content)
        #tafs.extend(temp)
    return metars
    with open("metars.json","w") as data_file:
        json.dump(metars,data_file)

def get_d(tab,lat,lon):

    return tab[int(round(90+lat,0))][int(round(180+lon,0))%360]

def get_wind(u,v,lat,lon):
    x = get_d(u,lat,lon)
    y = get_d(v,lat,lon)
    return {"u":x,"v":y,"speed":((pow(x,2)+pow(y,2))**0.5)*1.943,"head":(math.degrees(atan2(x,y))+360)%360}

def get_grib():
    print("Dowloading wind datas...")
    date = "20220315"
    cycle = "18"
    moment ="f006"

    data = "https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_1p00.pl?file=gfs.t"+cycle+"z.pgrb2.1p00."+moment+"&lev_100_mb=on&lev_150_mb=on&lev_200_mb=on&lev_250_mb=on&lev_300_mb=on&lev_350_mb=on&lev_400_mb=on&lev_450_mb=on&lev_500_mb=on&lev_550_mb=on&lev_600_mb=on&lev_650_mb=on&lev_700_mb=on&lev_750_mb=on&lev_800_mb=on&lev_850_mb=on&var_TMP=on&var_UGRD=on&var_VGRD=on&leftlon=0&rightlon=360&toplat=90&bottomlat=-90&dir=%2Fgfs."+date+"%2F"+cycle+"%2Fatmos"

    grbs_file = requests.get(data).content
    open('data_file', 'wb').write(grbs_file)


def extract_grib():
    print("Extracting wind data...")
    data = airports.copy()
    for arpts in data :
        arpts['data'] = []
    for i in range(1,48,3):
        temp = grbs[i].values
        u = grbs[i+1].values
        v = grbs[i+2].values
        alt = grbs[i].level
        print(str(round(i/48*100))+"%")
        
        for arpts in data :
            lat = float(arpts['lat']) #180
            lon = float(arpts ['lon'])#360
            arpts['data'].extend([{"altitude":mb2feet(alt),"T":get_d(temp,lat,lon)-273.15}|get_wind(u,v,lat,lon)]) 

    return data
    with open("data.json","w") as data_file:
        json.dump(data,data_file)

def compile_data():
    print("Compiling to output_format")
    with open("current_weather.txt","w") as out_file:
        line = []
        length = len(data)
        n = 0
        for arpts in data:
            n = n+1
            if(n%1000==0):
                print(str(round(n/length*100))+"%")
            if(any(metars.get('ICAO') == arpts['ICAO'] for metars in metars)):
                index = next((index for (index, d) in enumerate(metars) if d["ICAO"] == arpts['ICAO']), None)
                line = metars[index]['METAR']
            else:
                line = arpts['ICAO']
            line = line+"~"
            for i in range(n_layer-1,-1,-1):
                alt = str(round(arpts['data'][i]['altitude']))
                head = str(round(arpts['data'][i]['head']))
                speed = str(round(arpts['data'][i]['speed']))
                temp = str(round(arpts['data'][i]['T']))
                turb = "0"
                line = line +alt+";"+head+";"+speed+";"+temp+";0|"
            out_file.write(line+"\n")



#metars = get_metars()
#get_grib()


#n_layer = 16

#with open("./airports.json") as arpts_file:
   # airports = json.load(arpts_file)
grbs = pygrib.open("data_file")
#metars = json.load(open("metars.json"))

#data = compile_grib()

#data = json.load(open("data.json"))

#compile_data()
print("Complete")
print("Data validity :"+str(grbs[1].forecastTime))
print(grbs[1].keys())

# ------------------------- GRAPHICS ----------------------
#fig, ax = plt.subplots(figsize = (36,18))
#img = plt.imread("world-map.jpg")
#ax.imshow(img,extent=[0, 36, 0, 18])
#n = 17
#u = grbs[n].values
#v = grbs[n+1].values
#for x in range(0,360,5):
    #for y in range(0,180,5):
        #ax.quiver(x/10,y/10,u[y][x]/25,v[y][x]/25,color="red",width = 0.002,scale = 1,scale_units ='xy')

#ax.axis([0,36,0,18])


#plt.show()    