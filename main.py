from encodings import utf_8
import requests
import xml.etree.ElementTree as ET
import pygrib
import matplotlib.pyplot as plt

grbs = pygrib.open("gfs.t12z.pgrb2.1p00.anl")

metar_url = "https://aviationweather.gov/adds/dataserver_current/httpparam?datasource=metars&requestType=retrieve&fields=raw_text&format=xml&mostRecentForEachStation=constraint&hoursBeforeNow=3&stationString="

taf_url = "https://aviationweather.gov/adds/dataserver_current/httpparam?datasource=tafs&requestType=retrieve&fields=raw_text&format=xml&mostRecentForEachStation=constraint&hoursBeforeNow=3&stationString="

data = "https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_1p00.pl?file=gfs.t12z.pgrb2.1p00.anl&lev_1000_mb=on&lev_100_mb=on&lev_200_mb=on&lev_250_mb=on&lev_300_mb=on&lev_350_mb=on&lev_400_mb=on&lev_450_mb=on&lev_500_mb=on&lev_550_mb=on&lev_600_mb=on&lev_700_mb=on&lev_800_mb=on&lev_850_mb=on&lev_900_mb=on&lev_90-0_mb_above_ground=on&var_TMP=on&var_UGRD=on&var_VGRD=on&leftlon=0&rightlon=360&toplat=90&bottomlat=-90&dir=%2Fgfs.20220315%2F12%2Fatmos"

letters = []
#for i in range(65,91):



chars = list(map(chr,range(65,91)))+list(map(chr,range(48,58)))
ids = chars[0:10]+["K" + c for c in chars]+chars[11:26]

ids = ["A B C D","E F G H"] + ["KA KB KC KD KE KF KG"," KH KI KJ KK KL KM KN KO KP KQ KR"," KS KT KU KV KW KX KY KZ K1 K2 K3 K4 K5 K6 K7 K8 K9 K0"]+["L M N O P Q","R S T U V W X Y Z"]

if 0:

    def xml2array(xml):
        array = []
        root = ET.fromstring(xml)
        for child in root.iter('*'):
            if("raw_text" in child.tag):
                array.append(child.text)
        return array


    metars = []
    tafs = []

    for i in ids:
        
        response = requests.get(metar_url+i)
        temp = xml2array(response.content)
        metars.extend(temp)

        response = requests.get(taf_url+i)
        temp = xml2array(response.content)
        tafs.extend(temp)

    #print(metars)
    print(len(metars))
    print(len(tafs))


#grbs_file = requests.get(data)
#open('data_file', 'wb').write(grbs_file.content)

#grbs = pygrib.open("data_file")

#for g in grbs:
    #print(g)
    #print(g.values[0][0])

#print(len(grbs[1].values[:][90]))

#print(grbs[1])
#print(g.keys())

#pfpx = open("pfpx.pwx","rb")
#import chardet

#pfpx = pfpx.read(10000)
#print(type(pfpx))
#s = ''.join(map(chr, pfpx))
#print(s)
#print(s.encode("unicode"))

fig, ax = plt.subplots(figsize = (36,18))
img = plt.imread("world-map.jpg")
ax.imshow(img,extent=[0, 36, 0, 18])
n = 17
u = grbs[n].values
v = grbs[n+1].values
for x in range(0,360,5):
    for y in range(0,180,5):
        ax.quiver(x/10,y/10,u[y][x]/25,v[y][x]/25,color="red",width = 0.002,scale = 1,scale_units ='xy')
        #ax.quiver(1*x,1*y,1,1)
        #ax.quiver(x/10,y/10,x/100,0.5,color="blue",width = 0.001,scale = 1,scale_units ='xy')

ax.axis([0,36,0,18])

print(grbs[n])
print(grbs[n+1])



plt.show()


    