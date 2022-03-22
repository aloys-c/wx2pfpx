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

if(0):
    n=0
    fig = plt.figure(figsize=(36, 18))
    m = Basemap(projection='cyl',lon_0=0.0, lat_0=0.0,width=36E6, height=18E6, resolution='c')
    m.drawcoastlines()
    for i in range(-90,90,1):
        for j in range(-180,180,1):
            if(n%1000==0):
                print(n)
            n=n+1
            m.scatter(j,i,color="red",s=1)

    plt.show()