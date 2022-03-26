
import requests
import xml.etree.ElementTree as ET
import configparser
import json
import ctypes
import math
from threading import Thread
from time import sleep
import sys,os,shutil
import tkinter as tk
from tkinter import messagebox,IntVar,Radiobutton,ttk
from datetime import datetime,timezone, timedelta

metar_url = "https://aviationweather.gov/adds/dataserver_current/httpparam?datasource=metars&requestType=retrieve&fields=raw_text,station_id&format=xml&mostRecentForEachStation=constraint&hoursBeforeNow=3&stationString="
taf_url = "https://aviationweather.gov/adds/dataserver_current/httpparam?datasource=tafs&requestType=retrieve&fields=raw_text,station_id&format=xml&mostRecentForEachStation=constraint&hoursBeforeNow=3&stationString="

active = 0

if getattr( sys, 'frozen', False ) :
                # runs in a pyinstaller bundle
                path = sys._MEIPASS+"/"
else :
    path = "./"

#------------------- low level functions --------------------------------


def mb2feet(mb):
    return (1-pow(mb/1013.25,0.190284))*145366.45

def xml2array(xml,name):
        array = []
        item = ""
        n=0
        root = ET.fromstring(xml)
        for child in root.iter('*'):
            if(n):
                n = 0
                array.extend([{"ICAO":child.text,name:item}])
            if(("raw_text" in child.tag) and (not (child.text[0] == "\n"))):
                item = child.text
                n = 1
        return array
           

def print_m(message):
    root.text.configure(state='normal')
    root.text.insert("end",message)
    root.text.see(tk.END)
    root.text.configure(state='disabled')
    root.update()


def print_r(n):
    root.text.configure(state='normal')
    root.text.delete("end-"+str(n+1)+"c","end")
    root.text.configure(state='disabled')

def open_list(name):
    data =[]
    with open(name) as list:
        lines = list.readlines()
        for line in lines:
            l = line.split(",")
            data.extend([{"code":l[0],"lat":float(l[1]),"lon":float(l[2]),"alt":int(l[3])}])

    return data

def read_config(section,name,type,range):
    config = configparser.ConfigParser()
    try:
        config.read('settings.cfg')
    except:
        messagebox.showinfo('', 'Settings file corrupted, please check.')
        return 0,1
    try:
        item = type(config[section][name])
    except:
        messagebox.showinfo('', 'Missing entry "'+name+"' in settings file.")
        return 0,1
    if(item in range):
        return item,0
    else:
        messagebox.showinfo('', 'Value of entry "'+name+"' is incorrect in settings file, should be "+str(range)+".")
        return 0, 1
#------------------------------------ High level functions --------------------------------

def get_metars():
    #print_m("Downloading METAR data...\n")
    ids = ["A B C D","E F G H"] + ["KA KB KC KD KE KF KG"," KH KI KJ KK KL KM KN KO KP KQ KR"," KS KT KU KV KW KX KY KZ K1 K2 K3 K4 K5 K6 K7 K8 K9 K0"]+["L M N O P Q","R S T U V W X Y Z"]

    metars = []

    for i in ids:
        response = requests.get(metar_url+i)
        temp = xml2array(response.content,"METAR")
        metars.extend(temp)
    return metars


def get_tafs():
    #print_m("Downloading TAF data...\n")
    ids = ["A B C D","E F G H"] + ["KA KB KC KD KE KF KG"," KH KI KJ KK KL KM KN KO KP KQ KR"," KS KT KU KV KW KX KY KZ K1 K2 K3 K4 K5 K6 K7 K8 K9 K0"]+["L M N O P Q","R S T U V W X Y Z"]

    tafs = []

    for i in ids:
        response = requests.get(taf_url+i)
        temp = xml2array(response.content,"TAF")
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
            if(any(metars.get('ICAO') == arpts['code'] for metars in metars)):
                index = next((index for (index, d) in enumerate(metars) if d["ICAO"] == arpts['code']), None)
                arpts['METAR'] = metars[index]['METAR']
            else:
                arpts['METAR'] = 0
            
            if(any(tafs.get('ICAO') == arpts['code'] for tafs in tafs)):
                index = next((index for (index, d) in enumerate(tafs) if d["ICAO"] == arpts['code']), None)
                arpts['TAF'] = tafs[index]['TAF']
            else:
                arpts['TAF'] = 0
    return data


def get_grib(dates,n,res):
    print_m("Trying: "+str(dates['date_f'])[0:16]+" UTC release at "+str(dates['offset'])+"th hour forecast...")
    
    date = dates['date_f'].strftime("%Y")+dates['date_f'].strftime("%m")+dates['date_f'].strftime("%d")
    cycle = dates['date_f'].strftime("%H")
    if(dates['offset']>9):
        moment = "f0"+str(dates['offset'])
    else:
        moment = "f00"+str(dates['offset'])

    if(res==50):
        type ="pgrb2full."
        res_file="0p50"
    elif(res==25):
        type="pgrb2."
        res_file="0p25"
    else:
        res_file ="1p00"
        type="pgrb2."

    data = "https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_"+res_file+".pl?file=gfs.t"+cycle+"z."+type+res_file+"."+moment+"&lev_200_mb=on&lev_250_mb=on&lev_300_mb=on&lev_400_mb=on&lev_500_mb=on&lev_650_mb=on&lev_700_mb=on&lev_800_mb=on&lev_900_mb=on&var_TMP=on&var_UGRD=on&var_VGRD=on&leftlon=0&rightlon=360&toplat=90&bottomlat=-90&dir=%2Fgfs."+date+"%2F"+cycle+"%2Fatmos"

    grbs_file = requests.get(data).content
    sleep(5)
    open('./data/data'+str(res)+'.'+str(n), 'wb').write(grbs_file)
    if(sys.getsizeof(grbs_file)<100000):
        print_m("failed.\n")
        return 0
    else :
        print_m("success.\n")
        return 1

    
def compile_output(data,n_layer,n):
    print_m("Compiling forecast "+str(n+1)+" to output format...\n")
    with open("./output/out."+str(n),"w") as out_file:
        line = []
        for station in data:
            line = station["code"]
           
            if station['METAR']:
                line = line+ "::"+station["METAR"]+"::"
            else :
                line = line+ "::*::"
            if(station['TAF']):
                line = line+station["TAF"]+"::"
            else:
                line =line+ "*::"
            
            if "data" in station:
                for i in range(n_layer-1,-1,-1):
                    #alt = str(round(station['data'][i]['altitude']))
                    head = str((round(station['data'][i]['head'])+180)%360)
                    speed = str(round(station['data'][i]['speed']))
                    temp = str(round(station['data'][i]['T']))
                    line = line+head+","+speed+","+temp+"/"
            out_file.write(line+"\n")
    

def find_start_time():
    now = datetime.now(timezone.utc)
    h = now.hour
    now_c = now.replace(second=0, minute = 0, microsecond=0)
    nearest_hour_data = math.floor(h/6)*6
    nearest_hour_forecast = nearest_hour_data + math.floor((now_c-now_c.replace(hour=nearest_hour_data)).seconds/(60*60*3))*3
    nearest_hour_data_t = now_c.replace(hour=nearest_hour_data)
    nearest_hour_forecast_t = nearest_hour_data_t+timedelta(hours=(nearest_hour_forecast-nearest_hour_data)%24)

    return  now, nearest_hour_data_t, nearest_hour_forecast_t
    

def get_data_time():

    #Getting user entry
    now, nearest_h_d,nearest_h_f = find_start_time()
    print_m("Actual time : "+str(now)[0:19]+" UTC\n")

    n_forecast = int(root.for_field.get())-1
    
    entry = root.time_box.get()
    time_entry = root.keys[entry]
    next_forecast_delay,err = read_config("Time","skip_to_next_forecast_delay",int,range(0,180))
    if(time_entry == "--"):
        if((not err) & ((now-nearest_h_f).total_seconds()>(next_forecast_delay*60))):
            time_entry = nearest_h_f+timedelta(hours = 3)
        else:
            time_entry = nearest_h_f
    else :
        format = "%Y-%m-%d %H%z"
        time_entry = datetime.strptime(time_entry[:-12]+"+0000", format)
    
    
    #finding nearest dataset
    date_f1 = nearest_h_d
    date_d = time_entry
    offset1 = int(round(((date_d-date_f1).total_seconds()/(60*60))/3)*3)

    date_f2 = date_f1 - timedelta(hours=6)
    offset2 = int(round(((date_d-date_f2).total_seconds()/(60*60))/3)*3)
    
    return ([{"date_f":date_f1,"offset":offset1},{"date_f":date_f2,"offset":offset2},{"n_forecast":n_forecast}])

grib = ctypes.cdll.LoadLibrary(path+'grib/go_grib.so')
parse_grib = grib.parse_grib
parse_grib.restype = ctypes.c_void_p
#parse_grib.argtypes = [ctypes.c_char_p,ctypes.c_int,ctypes.c_int,ctypes.c_int]

def extract_grib(dic,num,int,res):

    class go_string(ctypes.Structure):
        _fields_ = [
        ("p", ctypes.c_char_p),
        ("n", ctypes.c_int)]
    str= json.dumps(dic)
    str=bytes(str,'UTF-8')
    dic_go = go_string(ctypes.c_char_p(str), len(str))
    ptr = parse_grib(dic_go,ctypes.c_int(num),ctypes.c_int(int),ctypes.c_int(res))
    out = ctypes.string_at(ptr)
    return json.loads(out)

def create_grid(res):
    with open("./output/wx_station_list.txt","w") as file:
        n =0
        line_out = ""
        json_dic = []
        for i in range(-9000,9000,res):
            for j in range(-18000,18000,res):
                n+=1
                fill = ""
                if(n<100):
                    fill ="0"
                if(n<10):
                    fill = "00"
                line_out +="$"+fill+str(n)+","+str(i/100)+"00,"+str(j/100)+"00,1000\n"
                json_dic.extend([{"code":"$"+fill+str(n),"lat":i/100,"lon":j/100}])
        file.write(line_out)
        return json_dic

#------------------------ Main function (Download) ---------------------------------

def start_process():
    global active

    if(not active):
        active = 1
        process = DataProcess()
        process.start()
    

class DataProcess(Thread):
   
    def run(self):
        global active
   #Number of altitude layers in the grib file
        
        n_layer = 9
        grid = int(var_check.get())

        export, err = read_config("Export","generate_export_files",int,[0,1])
        if(err):
            active = 0
            return

        if grid:
            res, err = read_config("Resolution","full_grid_mode_resolution",float,[0.5,1])
            if(err):
                active = 0
                return

        else:
            res, err = read_config("Resolution","default_network_interpolation_resolution",float,[0.25,0.5,1])
            if(err):
                active = 0
                return

        grid_res = int(100*res)
        print_m("Grid resolution is "+str(res)+"°.\n")


        add_airports, err = read_config("Include","add_airports_to_full_grid",int,[0,1])
        if(err):
            active = 0
            return
        
        dates = get_data_time()


        #Get the wind data
        if 1:
            #Get first datasets
            data_log = open("./data/data","w")
            n = 0
            if(not get_grib(dates[n],0,grid_res)):
                n = 1
                print_m("Too early, data not available yet.\n")
                if(not get_grib(dates[n],0,grid_res)):
                    print_m("Error : Couldn't retrieve data...\n")
                    active = 0
                    return
                    
            data_log.write(str(dates[n]['date_f']+timedelta(hours=dates[n]['offset']))[0:16]+"\n")

            #get additional datasets
            if(dates[2]['n_forecast']):
                print_m("Downloading extra forecast data:\n")
                offset = dates[n]['offset']
                for i in range(0,dates[2]['n_forecast']):
                    offset = offset+3
                    sleep(5)
                    dates[n]['offset'] = offset
                    if(not get_grib(dates[n],i+1,grid_res)):
                        print_m("Error : Couldn't retrieve data...\n")
                        active = 0
                        return
                    else:
                        data_log.write(str(dates[n]['date_f']+timedelta(hours=offset))[0:16]+"\n")
            #print_m("Wind data successfully retrieved...\n")

            data_log.close()

        #Get the metars
        if 1:
            airports = open_list("./data/airports")
            print_m("Downloading last weather reports...\n")
            metars = get_metars()
            tafs = get_tafs()

            met_tafs = compile_metars_tafs(airports,metars,tafs)
            with open("./data/met_taf","w") as met_taf_file:
                json.dump(met_tafs,met_taf_file)

        else:
            with open("./data/met_taf","r") as met_taf_file:
                met_tafs = json.load(met_taf_file)
    

        #Uses external module to parse grib to json
        print_m("Extracting wind data...\n")

        if(grid):
            network = create_grid(grid_res)
        else:
            network = open_list('./data/stations')
            shutil.copy("./data/stations","./output/wx_station_list.txt")
            
        data = extract_grib(network,0,0,grid_res)
        
        if((not grid) or add_airports):
            airports_out = extract_grib(met_tafs,0,1,grid_res)
            data.extend(airports_out)
        else:
            data.extend(met_tafs)

        compile_output(data,n_layer,0) 

        if export: 
            print_m("Exporting compiled data...\n")
            with open("./output/export"+str(grid_res)+".0","w") as export_data:
                json.dump(data,export_data)
        
        
        if(dates[2]['n_forecast']):
            for i in range(0,dates[2]['n_forecast']):
                #uses external module
                print_m("Extracting wind data...\n")
                data = extract_grib(network,i+1,0,grid_res)
                if((not grid) or add_airports):
                    airports_out = extract_grib(met_tafs,i+1,1,grid_res)
                    data.extend(airports_out)
                else:
                    data.extend(met_tafs)
                
                compile_output(data,n_layer,i+1)
                
                if export:
                    print_m("Exporting compiled data...\n")
                    with open("./output/export"+str(grid_res)+"."+str(i+1),"w") as export_data:
                        json.dump(data,export_data)
                

        with open("./data/airports","r") as fp: 
            data = fp.read()
            data = "\n"+data
            with open ("./output/wx_station_list.txt", 'a') as out: 
                out.write(data)


        print_m("Complete !\n")
        shutil.copy("./data/data","./output/out")
        init()
    
    
#------------------- UI -------------------------
n_entry = 0

def show_data(n):
    if(os.path.exists("./output/out.0")):
        with open("./output/out") as logs:
            dates = logs.readlines()
        
        root.date_field.delete(0,"end")
        root.date_field.insert(0,dates[int(n)-1])
        root.slider.set(n)
        shutil.copy("./output/out."+str(int(n)-1),"./output/current_wx_snapshot.txt")
        root.update()

def update_time_combox(dummy):
    now, nearest_h_d,nearest_h_f = find_start_time()
    hours = {"--":"--"}
    for i in range(0,8):
        hours.update({str((nearest_h_f.hour+i*3)%24)+":00 (+"+str(3*i)+")":str(nearest_h_f+timedelta(hours=3*i))})

    root.time_box['values']= list(hours)
    root.time_box.set(hours['--'])
    root.keys = hours

def init():
    global active
    active = 0

    if(os.path.exists("./output/out.0")):
        try:
            with open("./output/out") as logs:
                dates = logs.readlines()
                n_entry = len(dates)
        except:
                n_entry = 0  
    else:
        n_entry = 0

    root.slider= tk.Scale(root.left, from_=1, to=n_entry, orient=tk.HORIZONTAL,label = "Forecast :",command = show_data )
    root.slider.grid(column = 0,row = 0,padx = (10,5),pady = (0,2))
   
    update_time_combox(1)
    show_data(1)
    if(var_check.get()==1):
        var_check.set(1)
    root.update()


def read_me():
    executable = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.startfile(path+"ReadMe.txt")
    messagebox.showinfo('', 'Please read ReadMe.txt in:'+executable)
    shutil.copy(path+"ReadMe.txt",executable)
    
root = tk.Tk()
s = ttk.Style()

root.left = tk.LabelFrame(root, text="Curent data", width = 130,height = 110)
root.left.grid_propagate(0)
root.left.grid(row=0,column =0,pady=(0,10))

root.right = tk.LabelFrame(root, text="Update data", width =380,height = 110)
root.right.grid(row=0,column =1,pady=(0,10))
root.right.grid_propagate(0)

root.date_field = tk.Entry(root.left, text = "",width=15)
root.date_field.grid( column = 0,row=1,padx = (10,5))
root.slider = None

root.date_label = tk.Label(root.right,text = "Start hour (optionnal) :",width =20)
root.date_label.grid(column =0,row=1,pady=(0,0),padx = (10,5))
root.time_box = ttk.Combobox(root.right, values = [],width = 5)
root.time_box.grid( column = 1,row=1,sticky=tk.W,pady=(3,0),padx = (5,0))
root.time_box.bind("<Button-1>",update_time_combox)
root.time_box['state'] = 'readonly'

s.theme_create('combostyle', parent='winnative',settings = {'TCombobox':{'configure':{"postoffset":(0,0,15,0),'selectbackground': 'white','selectforeground': 'black'}}})
s.theme_use('combostyle') 

root.for_label = tk.Label(root.right,text = "Number of forecasts :")
root.for_label.grid(column =0,row=0,pady=(13,10),padx = (10,5))
root.for_field = tk.Spinbox(root.right,width=6,from_=1, to=5)
root.for_field.grid( column = 1,row=0,sticky=tk.W,pady=(8,0),padx = (5,5))

var_check = IntVar()
var_check.set(0)
 
root.check_grid = tk.Checkbutton(root.right, text='Use full grid',variable=var_check, onvalue=1, offvalue=0, justify=tk.RIGHT)
root.check_grid.grid(column = 2,row = 0, columnspan=2, padx=(23,0),pady=(12,0),sticky=tk.NW)

      
root.button = tk.Button(root.right,text = "Download data", command = start_process)
root.button.grid(column = 2,row = 1,sticky=tk.NE,pady=(0,0),padx=(25,0))
root.help = tk.Button(root.right,text = "?", command = read_me)
root.help.grid(column = 3,row = 1,sticky=tk.W,pady=(0,0))

root.text = tk.Text(width = 70,height = 10)
root.text.grid(row =2,column =0,columnspan=2)
root.text.configure(state='disabled')

icon = tk.PhotoImage(file = path+'src/icon.png')
root.iconphoto(False, icon)

init()

root.title("wx2pfpx")
root.resizable(0, 0)

# Run and display the window
root.mainloop()