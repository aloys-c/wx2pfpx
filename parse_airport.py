import json
from typing_extensions import dataclass_transform

data = []
arpts = open("airports.dat")
for line in arpts :
    data.append({"ICAO":line[0:4],"lat":line[4:14],"lon":line[14:25]})

with open("airports.json","w") as data_file:
    json.dump(data,data_file)