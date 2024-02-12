# Wx2fs (wx2pfpx extension) + Autosave function
Simple script to inject weather data in SimConnect(v.10.0.61259.0 or FSX_XPACK) compatible simulator (FSX, P3D) from the output of wx2pfpx. This is a a very basic weather engine solution to allow to get enroute winds and ground weather at airports (for which the METAR is available) for IFR flights where visual realism it not the main concern.

## How to use :
- The executable must be in the same folder as the output folder from wx2pfpx, it will take the selected dataset on the wx2pfpx app.
- Run the script after the simulator is started, but before loading a flight. The window must be kept open (or minimized) to maintain the weather active in the sim.
- Closing the script might make your sim crash, also some short lag is expected at loading (whole map is loaded at once.).
- While the script is open, it can be used to autosave the game at a desired time interval (optionnal).
- When using full grid, set the config to include also the airports data and also set the grid to a resolution of 1 to avoid overloading the map.


## How it works :
- Data used is what is provided from wx2pfpx (METARSs and winds aloft) and is directly injected as is into the sim after a bit of cleaning.
- Weather stations allow the sim to interpolate the data and generate the global weather, some changes on a station can impact the others. Also, a station that is in contrast with neighbour stations will tend to align its values.
- When the script sets a weather station in the sim, it has to provide a METAR AND the winds aloft, what is not provided is reset to zero. This means that setting only the METAR will delete altitude winds. On the other hand, providing only altitude winds (additionnal stations in wx2pfpx) will set ground variables (which are also the only ones generating visuals) to zero, thus extra stations and grid points should ideally be far from airports. That's also why it's important to change the settings to add the wind data to the airports with METARs on the full grid mode. There is a trade off between having a lot of stations for a realistic wind, and fewer stations to avoid impacting the data provided by the METARs and emptying the weather visually.

## Troubleshooting :
- If you get an execution error ("Side-by-side configuration") when launching the script, it means you need to install SimConnect (v.10.0.61259.0 or FSX_XPACK, the installer is in your sim folder).
- SimConnect being forward compatible and since this script uses the popular FSX SP2 version, this means it should work with this version on to the most recent versions of P3D (P3Dv4 64bit tested and functionnal). 
