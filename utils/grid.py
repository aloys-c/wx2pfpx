import json
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt



with open("grid_list","w") as grid_file:
    n =1000
    line_out = ""
    json_item = []
    for i in range(-90,90,1):
        for j in range(-180,180,1):
            n+=1
            line_out +="$"+str(n)+","+str(i)+","+str(j)+",1000\n"
            json_item.extend([{"code":"$"+str(n),"lat":i,"lon":j}])

    with open("grid","w") as json_file:
        json.dump(json_item,json_file)
    grid_file.write(line_out)

if(1):

    with open("./data/airports") as arpts_file:
            airports = json.load(arpts_file)
    n=0

    handle_dict = {
    "Airports" : 0,
    "Grid" : 0,
    }
    fig = plt.figure(figsize=(36, 18))
    m = Basemap(projection='cyl',lon_0=0.0, lat_0=0.0,width=36E6, height=18E6, resolution='c')
    m.drawcoastlines()

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

    for i in range(-90,90,1):
        for j in range(-180,180,1):
            if(n%1000==0):
                print(n)
            n=n+1
            m.scatter(j,i,color="blue",s=1,label = 
                "Airports" if handle_dict['Airports'] == 0
                else "_no-legend_")
            handle_dict['Airports'] += 1
   
   
    plt.legend(loc="lower center", ncol=2,bbox_to_anchor =(0.5, -0.08))
    plt.show()
