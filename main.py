
from math import atan2
import requests
import xml.etree.ElementTree as ET
#import pygrib #Doesn't work well under windows, can be install on anaconda though for testing.
#from mpl_toolkits.basemap import Basemap
#import matplotlib.pyplot as plt
import json
import ctypes
import math
import pytz
from time import sleep
import sys,os,shutil
import tkinter as tk
from tkinter import messagebox
from datetime import datetime,timezone, timedelta

metar_url = "https://aviationweather.gov/adds/dataserver_current/httpparam?datasource=metars&requestType=retrieve&fields=raw_text&format=xml&mostRecentForEachStation=constraint&hoursBeforeNow=3&stationString="
taf_url = "https://aviationweather.gov/adds/dataserver_current/httpparam?datasource=tafs&requestType=retrieve&fields=raw_text&format=xml&mostRecentForEachStation=constraint&hoursBeforeNow=3&stationString="

if getattr( sys, 'frozen', False ) :
                # runs in a pyinstaller bundle
                path = sys._MEIPASS+"/"
else :
    path = "./"


def mb2feet(mb):
    return (1-pow(mb/1013.25,0.190284))*145366.45

def xml2array(xml,s,e,name):
        array = []
        root = ET.fromstring(xml)
        for child in root.iter('*'):
            if("raw_text" in child.tag):
                array.append({"ICAO":child.text[s:e],name:child.text})
        return array

def print_m(message):
    root.text.insert("end",message)
    root.text.see(tk.END)
    root.update()

def line_m():
    root.text.delete("end-2l","end-1l")

def print_r(n):
    root.text.delete("end-"+str(n+1)+"c","end")

def get_metars():
    print_m("Downloading METAR data...\n")
    ids = ["A B C D","E F G H"] + ["KA KB KC KD KE KF KG"," KH KI KJ KK KL KM KN KO KP KQ KR"," KS KT KU KV KW KX KY KZ K1 K2 K3 K4 K5 K6 K7 K8 K9 K0"]+["L M N O P Q","R S T U V W X Y Z"]

    metars = []

    for i in ids:
        response = requests.get(metar_url+i)
        temp = xml2array(response.content,0,4,"METAR")
        metars.extend(temp)

    return metars

# ------------------------- GRAPHICS ----------------------


def get_d(tab,lat,lon):
    return tab[int(180-round(90+lat,0))][int(round(360+lon,0))%360]

def show_data_plot(n):
    #grib = pygrib.open("./data/data."+str(n))
    fig, ax = plt.subplots(figsize = (36,18))
    img = plt.imread("world-map.jpg")
    ax.axis([-18,18,-9,9])
    ax.imshow(img,extent=[-16, 18, -9, 9])
    n = 17
    print(mb2feet(grib[n].level))
    u = grib[n].values
    v = grib[n+1].values
    for x in range(-180,180,5):
        for y in range(-90,90,5):
            #ax.quiver(((x+180)%360)/10,18-y/10,u[y][x]/75,v[y][x]/75,color="red",width = 0.002,scale = 1,scale_units ='xy')
            ax.quiver(x/10,y/10,get_d(u,y,x)/75,get_d(v,y,x)/75,color="red",width = 0.002,scale = 1,scale_units ='xy')
        
    #[lat, lon]
    #cape town, newyork, sydney, moscow,
    cities =[[-33,18.5],[40,-74],[-34,151],[56,37.5]] 
   
    for city in cities:
        ax.scatter((city[1])/10,(city[0])/10)

    plt.show()    

def show_map_density():
    with open("./data/airports") as arpts_file:
            airports = json.load(arpts_file)

   
    fig = plt.figure(figsize=(36, 18))
    m = Basemap(projection='cyl',lon_0=0.0, lat_0=0.0,width=36E6, height=18E6, resolution='c')
    m.drawcoastlines()
    

    for i in range(0,len(airports)):
        if(i%1 ==0):
            if(i%100 ==0):
                print(i)
            y = round(float(airports[i]['lat']))
            x = round(float(airports[i]['lon']))
            m.scatter(x,y,color="red",s=1)

    plt.show()

def show_output_plot(data):
    print(len(data))
    fig, ax = plt.subplots(figsize = (36,18))
    img = plt.imread("world-map.jpg")
    ax.imshow(img,extent=[2, 36, 0, 18])
    n = 17
    print(data[1]['data'][6]['altitude'])
    for i in range(0,len(data)):
        if(i%5 ==0):
            airport = data[i]
            print(i)
          
            y = round(float(airport['lat']))
            x = round(float(airport['lon']))
            u = airport['data'][6]['u']
            v = airport['data'][6]['v']
            
            ax.quiver(((x+180)%360)/10,(90+y)/10,u/50,v/50,color="red",width = 0.001,scale = 1,scale_units ='xy')
        
    #[lat, lon]
    #cape town, newyork, sydney, moscow,
    #cities =[[-33,18.5],[40,-74],[-34,151],[56,37.5]] 
   
    #for city in cities:
        #ax.scatter((180+city[1])/10,(90+city[0])/10)

    #ax.axis([0,36,0,18])
    #plt.show()  

def get_tafs():
    print_m("Downloading TAF data...\n")
    ids = ["A B C D","E F G H"] + ["KA KB KC KD KE KF KG"," KH KI KJ KK KL KM KN KO KP KQ KR"," KS KT KU KV KW KX KY KZ K1 K2 K3 K4 K5 K6 K7 K8 K9 K0"]+["L M N O P Q","R S T U V W X Y Z"]

    tafs = []

    for i in ids:
        response = requests.get(taf_url+i)
        temp = xml2array(response.content,8,12,"TAF")
        tafs.extend(temp)

    return tafs


def compile_metars_tafs(airports,metars,tafs):
    print_m("Compiling METAR and TAF data...")
    n = 0
    data = airports.copy()
    length = len(data)
    print_m(" 0%\n")
    for arpts in data:
            n = n+1
            if(n%1000==0):
                print_r(4)
                perc = str(round(n/length*100))+"%\n"
                if(len(perc)<4):
                    perc = " "+perc
                print_m(perc)
            if(any(metars.get('ICAO') == arpts['ICAO'] for metars in metars)):
                index = next((index for (index, d) in enumerate(metars) if d["ICAO"] == arpts['ICAO']), None)
                arpts['METAR'] = metars[index]['METAR']
            else:
                arpts['METAR'] = arpts['ICAO']
            
            if(any(tafs.get('ICAO') == arpts['ICAO'] for tafs in tafs)):
                index = next((index for (index, d) in enumerate(tafs) if d["ICAO"] == arpts['ICAO']), None)
                arpts['TAF'] = tafs[index]['TAF']
            else:
                arpts['TAF'] = 0
    return data


def get_wind(u,v,lat,lon):
    x = get_d(u,lat,lon)
    y = get_d(v,lat,lon)
    return {"u":x,"v":y,"speed":((pow(x,2)+pow(y,2))**0.5)*1.943,"head":(math.degrees(atan2(x,y))+360)%360}

def get_grib(dates,n):
    print_m("Trying: "+str(dates['date_f'])[0:16]+" UTC release at "+str(dates['offset'])+"th hour forecast...")
    sleep(5)
    date = dates['date_f'].strftime("%Y")+dates['date_f'].strftime("%m")+dates['date_f'].strftime("%d")
    cycle = dates['date_f'].strftime("%H")
    if(dates['offset']>9):
        moment = "f0"+str(dates['offset'])
    else:
        moment = "f00"+str(dates['offset'])
    
    data = "https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_1p00.pl?file=gfs.t"+cycle+"z.pgrb2.1p00."+moment+"&lev_100_mb=on&lev_150_mb=on&lev_200_mb=on&lev_250_mb=on&lev_300_mb=on&lev_350_mb=on&lev_400_mb=on&lev_450_mb=on&lev_500_mb=on&lev_550_mb=on&lev_600_mb=on&lev_650_mb=on&lev_700_mb=on&lev_750_mb=on&lev_800_mb=on&lev_850_mb=on&var_TMP=on&var_UGRD=on&var_VGRD=on&leftlon=0&rightlon=360&toplat=90&bottomlat=-90&dir=%2Fgfs."+date+"%2F"+cycle+"%2Fatmos"
   
    grbs_file = requests.get(data).content
    open('./data/data.'+str(n), 'wb').write(grbs_file)
    if(sys.getsizeof(grbs_file)<100000):
        print_m("failed.\n")
        return 0
    else :
        print_m("success.\n")
        return 1

#Replaced by an external function because of pygrib incompatibility
def extract_grib(grbs,data):
    print_m("Extracting wind data...\n")
    print_m("0%\n")
    for arpts in data :
        arpts['data'] = []
    for i in range(1,48,3):
        temp = grbs[i].values
        u = grbs[i+1].values
        v = grbs[i+2].values
        alt = grbs[i].level
        line_m() 
        print_m(str(round(i/48*100))+"%\n")
        
        for arpts in data :
            lat = float(arpts['lat']) #180
            lon = float(arpts ['lon'])#360
            arpts['data'].extend([{"altitude":mb2feet(alt),"T":get_d(temp,lat,lon)-273.15}|get_wind(u,v,lat,lon)]) 
    line_m()
    print_m("100%\n")

    return data
    

def compile_output(data,n_layer,n):
    print_m("Compiling forecast "+str(n+1)+" to output format...\n")
    with open("./output/out."+str(n),"w+") as out_file:
        line = []
        for arpts in data:
            line = arpts["METAR"]
            if(arpts['TAF']):
                line = line +" | "+arpts["TAF"]
            line = line+"~"
            for i in range(n_layer-1,-1,-1):
                alt = str(round(arpts['data'][i]['altitude']))
                head = str((round(arpts['data'][i]['head'])+180)%360)
                speed = str(round(arpts['data'][i]['speed']))
                temp = str(round(arpts['data'][i]['T']))
                line = line +alt+";"+head+";"+speed+";"+temp+";0|"
            out_file.write(line+"\n")
    


### ------------ Welcome interface -------------------

def get_data_time():
    now = datetime.now(timezone.utc)
    print_m("Actual time : "+str(now)[0:19]+" UTC\n")

    date = root.start_field.get()
    if(date == "dd/hh"):
        date = ""
    n_forecast = int(root.for_field.get())-1
    now = now.replace(second=0, minute = 0, microsecond=0)

    if(date):
        date = date.split("/")
        date = list(map(int,date))
        date_d = datetime(now.year,now.month,date[0],date[1],0,0,0,pytz.UTC)
    else :
        date_d = datetime(now.year,now.month,now.day,now.hour,0,0,0,pytz.UTC)
        date_d = date_d + timedelta(hours=1)
        
    datasets = ["00","06","12","18"]

    #finding nearest dataset
    diff = date_d-now

    if(diff.total_seconds() < -60*60):
        print_m("Sorry can't download past data.\n")
        return 0
    elif(diff.total_seconds()>60*60*24):
        print_m("Sorry can't download data more than 24 hours in advance.\n")
        return 0
    else:
        h = now.hour
        t_h = math.floor(h/6)
        
        date_f1 = now.replace(hour= int(datasets[t_h]))
        offset1 = int(round(((date_d-date_f1).total_seconds()/(60*60))/3)*3)

        date_f2 = date_f1 - timedelta(hours=6)
        offset2 = int(round(((date_d-date_f2).total_seconds()/(60*60))/3)*3)
    
    return([{"date_f":date_f1,"offset":offset1},{"date_f":date_f2,"offset":offset2},{"n_forecast":n_forecast}])


def data_process():
   

    dates = get_data_time()
    if(not dates):
        return



    n_layer = 16

    if 1:
        #Get first datasets
        data_log = open("./data/data","w")
        n = 0
        if(not get_grib(dates[n],0)):
            n = 1
            print_m("Data not available yet.\n")
            if(not get_grib(dates[n],0)):
                print_m("Error : Couldn't retrieve data...\n")
                return
        data_log.write(str(dates[n]['date_f']+timedelta(hours=dates[n]['offset']))[0:16]+"\n")



    #get forecast datasets
        if(dates[2]['n_forecast']):
            print_m("Downloading extra forecast data:\n")
            offset = dates[n]['offset']
            for i in range(0,dates[2]['n_forecast']):
                offset = offset+3
                sleep(5)
                dates[n]['offset'] = offset
                if(not get_grib(dates[n],i+1)):
                    print_m("Error : Couldn't retrieve data...\n")
                    return
                else:
                    data_log.write(str(dates[n]['date_f']+timedelta(hours=offset))[0:16]+"\n")
        print_m("Wind data successfully retrieved...\n")

        data_log.close()

    if 1:
        with open("./data/airports") as arpts_file:
            airports = json.load(arpts_file)

        metars = get_metars()
        tafs = get_tafs()

        met_tafs = compile_metars_tafs(airports,metars,tafs)
        with open("./data/met_taf","w") as met_taf_file:
            json.dump(met_tafs,met_taf_file)

            

    try:
        shutil.rmtree("./output/*")
    except:
        pass
   
   
    if 0:
    #uses internal function
        #grbs = pygrib.open("./data/data.0")
        with open("./data/met_taf","r") as met_taf_file:
            met_tafs = json.load(met_taf_file)

        data = extract_grib(grbs,met_tafs)
        compile_output(data,n_layer,0)

        if(dates[2]['n_forecast']):
            for i in range(0,dates[2]['n_forecast']):
                #uses internal function

                #with pygrib.open("./data/data."+str(i+1)) as grbs:
                    #data = extract_grib(grbs,met_tafs)
                compile_output(data,n_layer,i+1)
    
    else:
        #Uses external module to parse grib to json
        print_m("Extracting wind data...\n")
        grib = ctypes.cdll.LoadLibrary(path+'grib/go_grib.so')
        parse_grib = grib.parse_grib
        parse_grib.restype = ctypes.c_void_p
        parse_grib.argtypes = [ctypes.c_int]
        ptr = parse_grib(ctypes.c_int(0))
        out = ctypes.string_at(ptr)
        data = json.loads(out) 
        compile_output(data,n_layer,0)
    
        if(dates[2]['n_forecast']):
            for i in range(0,dates[2]['n_forecast']):
                #uses external module
                ptr = parse_grib(ctypes.c_int(i+1))
                out = ctypes.string_at(ptr)
                data = json.loads(out) 
                compile_output(data,n_layer,i+1)

   #show_map_density()
    #show_data_plot(0)
    #show_output_plot(data)
    
    print_m("Complete !\n")
    shutil.copy("./data/data","./output/out")
    init()
    
    
#-------- UI -------------------------
n_entry = 0


def show_data(n):
    if(os.path.exists("./output/out.0")):
        with open("./output/out") as logs:
            dates = logs.readlines()

        root.date_field.delete(0,"end")
        root.date_field.insert(0,dates[int(n)-1])
        root.slider.set(n)
        root.update()
        shutil.copy("./output/out."+str(int(n)-1),"./output/current_weather.txt")


def init():
    if(os.path.exists("./output/out.0")):
        with open("./output/out") as logs:
            dates = logs.readlines()
            n_entry = len(dates)
    else:
        n_entry = 0
    root.slider= tk.Scale(root.left, from_=1, to=n_entry, orient=tk.HORIZONTAL,label = "Forecast :",command = show_data )
    root.slider.grid(column = 0,row = 0,padx = (10,5),pady = (0,2))
    show_data(1)
    root.start_field.delete(0,"end")
    root.start_field.insert(0,"dd/hh")
    root.start_field.bind("<Button-1>", clear_search) 
    root.for_field.delete(0,"end")
    root.for_field.insert(0,"1")
    root.update()
    


def clear_search(event):
   root.start_field.delete(0, tk.END) 



def read_me():
    executable = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.startfile(path+"ReadMe.txt")
    messagebox.showinfo('', 'Please read ReadMe.txt in:'+executable)
    shutil.copy(path+"ReadMe.txt",executable)
    

    

root = tk.Tk()
root.left = tk.LabelFrame(root, text="Curent data", width = 130,height = 110)
root.left.grid_propagate(0)
root.left.grid(row=0,column =0,pady=(0,10))

root.right = tk.LabelFrame(root, text="Update data", width =380,height = 110)
root.right.grid(row=0,column =1,pady=(0,10))
root.right.grid_propagate(0)

root.date_field = tk.Entry(root.left, text = "",width=15)
root.date_field.grid( column = 0,row=1,padx = (10,5))
root.slider = None

root.date_label = tk.Label(root.right,text = "Start date (optionnal) :",width =20)
root.date_label.grid(column =0,row=1,pady=(0,10),padx = (10,5))
root.start_field = tk.Entry(root.right,width=8)
root.start_field.grid( column = 1,row=1,sticky=tk.W,pady=(0,10),padx = (5,5))
root.for_label = tk.Label(root.right,text = "Number of forecasts (1-4) :")
root.for_label.grid(column =0,row=0,pady=(16,10),padx = (10,5))
root.for_field = tk.Entry(root.right, text = "0",width=8)
root.for_field.grid( column = 1,row=0,sticky=tk.W,pady=(16,10),padx = (5,5))
root.button = tk.Button(root.right,text = "Download data", command = data_process)
root.button.grid(column = 2,row = 0,rowspan =2,sticky=tk.E,pady=(8,0),padx=(25,0))
root.help = tk.Button(root.right,text = "?", command = read_me)
root.help.grid(column = 3,row = 0,rowspan = 2,sticky=tk.W,pady=(8,0))

root.text = tk.Text(width = 70,height = 10)
root.text.grid(row =2,column =0,columnspan=2)

icon = tk.PhotoImage(file = path+'src/icon.png')
root.iconphoto(False, icon)

init()

root.title("Wx2pfpx")
root.resizable(0, 0)

# Run and display the window
root.mainloop()