# wx2pfpx

## A simple weather data provider script for the discontinuated Professional Flight Plan X software.

### How to install :

The folder can be placed anywhere on the computer, a shortcut to the "wx2pfpx.exe" file can be created and put on the Desktop for quick access. The output files are generated and stored in the folder named "output". This folder has to be selected in the PFPX as the "Active Sky" folder (settings on lower bar of screen), the data displayed in PFPX is then automatically refreshed each time the data is updated.


### How to use :

PLEASE NOTE : the program freezes sometimes during processing, this is not an issue, just be patient, the download can sometimes take a few minutes.

Open the script by double clicking on wx2pfpx.exe or the created shortcut on the Desktop.

The script keeps track of last downloaded data and they can be directly browsed, if available, by using the cursor on the  to left through the different forecast times and display them in PFPX.

To download new data, you have the following options : 
- select a starting time (up to 24 hours in the future). 
- The number of forecasts you want to fetch (steps of 3 hours from the given starting time)
- Using either the included stations network or import iporting the full data grid.

Clicking on the download button will generate a new dataset that will be saved on the Hard Drive and replace the previous one.

When available for an airport, the METAR and TAF data is also displayed. 

Keep in mind that the weather data source is a free, but limited service. It is designed to prevent abuse and making a lot of requests will increase downloading time or make it fail.


### How it works :

The script fetches raw weather data, METAR and TAF data from the NOAA, US national weather service, which is then compiled to a single file that can be imported in PFPX. The data source is updated 4 times a day, and provides forecasts for every 3 following hours up to 16 days. When available, METAR and TAF data is also provided for more than 5000 airports. 

The stations network consists of about 15000 reference airports from PFPX as well as about 500 additional stations located in remote areas (See stations image file). Wind/temperature data is provided for each of them by using a weighted interpolation of the NOAA grid data. Imported data is then extrapolated in a grid by PFPX. This method allows to access the data quickly and in an optimized way, covering mostly the whole map and fits well for flying on continents with a high airport density.  

For more precision, it is also possible to generate an output file containing the whole NOAA grid (resolution  of at least 1°/~111km, 65160 points.) dataset. this takes more time to process, but will cover precisely and homogeneously the whole map. That method could fit better for long haul flights over remote areas.


Main differences with official server :

- Only one single forecast can be displayed and used to compute the whole flight performance.
- When the METAR data is unavailable for an airport, usually the data from the nearest airport is automatically displayed. Here the data is simply not provided.
- The general quality/compatibility, please pay for the official subscription if you can afford it, it will give you what's best and allows to reward the team for their work.


###Advanced settings :

You can edit the file settings.cfg as a normal text file. It allows to set the resolutions of the grid used for data interpolation on stations, and also the grid imported when using full grid mode (see documentation folder for exemples of grid effect on precision). Increasing resolution can make processing and loading times much higher, 0.25° resolution is not available for full grid mode as data amount is too high for PFPX.

Other settings are available allowing to export the whole data in JSON format, or setting the default forecast time used when starting time is left blank.



### Troubleshooting :

1) If you don't get result files in the "output" folder after the download and can't restart the app, this is very probably due to the antivirus software preventing the script from writing files. Try to whitelist and empty the "output" folder before trying again.

2) Using higher resolution can make the script lag depending on your computer, try setting the values at 1 and see if it solves the issue.