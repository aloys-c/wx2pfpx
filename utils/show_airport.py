import json
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap


with open("./output/export100.0") as data:
    stations = json.load(data)

code = "UOOO"  
size = 10
  


if(any(stations.get('code') == code for stations in stations)):
    index = next((index for (index, d) in enumerate(stations) if d["code"] == code), None)
    target = stations[index]
    print(target)

fig = plt.figure(figsize=(size, size))
m = Basemap(projection='cyl',llcrnrlon=(target['lon']-size/2),llcrnrlat=(target['lat']-size/2),urcrnrlon=(target['lon']+size/2),urcrnrlat=(target['lat']+size/2), resolution = 'c')
m.drawcounties()
n = 0
tot = len(stations)
for station in stations:
    n=n+1
    if(n%1000 == 0):
        print(str(round(n/tot*100))+"%\n")
    if ((abs(station['lat']-target['lat'])<size/2) and (abs(station['lon']-target['lon'])<size/2)):
        if((station['code'][0]=="$")):
            col = "black"
        else:
            col = "orange"
    try:       
        m.quiver(station['lon'],station['lat'],station['data'][0]['u'],station['data'][0]['v'],width = 0.002,scale=3.0,scale_units='xy',color=col)
        m.scatter(station['lon'],station['lat'],color=col)
    except:
        pass


m.quiver(target['lon'],target['lat'],target['data'][0]['u'],target['data'][0]['v'],width = 0.002,scale=3.0,color="red",scale_units='xy')
m.scatter(target['lon'],target['lat'],color = "red")
plt.show()

    