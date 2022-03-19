# wx2pfpx (For requests, contact me on https://github.com/Dakara93/wx2pfpx/issues)

## A simple weather data provider script for the discontinuated Professional Flight Plan X software.

### How to install :

The folder can be placed anywhere on the computer, a shortcut to the "wx2pfpx.exe" file can be created and put on the Desktop for quick access. The output file generated is named "current_weather.txt" and is located in the "output" folder. This folder has to be selected in the PFPX as the FSGRW folder (settings on lower bar of screen), the data displayed in PFPX is then automatically refreshed each time the file is updated.


### How to use :

Open the script by double clicking on wx2pfpx.exe or the created shortcut on the Desktop. 

The script keeps track of last downloaded data and they can be directly browsed, if available, by using the cursor on the right to get through the different forecast times and display them in PFPX.

To download new data, select a starting time (up to 24 hours in the future) and the number of forecasts you want to fetch. Then click on the download button. This will generate a new dataset that will be saved on the Hard Drive and replace the previous one.

When available for an airport, the METAR and TAF data is displayed. Please note that the TAF data is shown in the METAR section and signaled as unavailable by PFPX.

Keep in mind that the weather data source is a free, but limited service. It is designed to prevent abuse and making a lot of requests will increase downloading time or make it fail.


### How it works :

The script fetches raw weather data, METAR and TAF data from the NOAA, US national weather service, which is then compiled to a single file that can be imported in PFPX. The data source is updated 4 times a day, and provides forecasts for every 3 following hours up to 16 days. More than 15000 reference stations (airports) from PFPX are used and wind/temperature data is provided for each of them. When available, METAR and TAF data is also provided for more than 5000 airports.


Main differences with official server :

- The weather data is not provided as a grid file covering the whole map, but it's imported for every station and the grid is then extrapolated. Points located far from airports are then potentially less accurate.
- No turbulence data is available.
- Only one single forecast can be displayed and used to compute the whole flight performance.
- When the METAR data is unavailable for an airport, usually the data from the nearest airport is automatically displayed. Here the data is simply not provided.