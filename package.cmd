pyinstaller prog.spec

rmdir /s /q "wx2pfpx_pack"

mkdir "wx2pfpx_pack/data"
mkdir "wx2pfpx_pack/output"
mkdir "wx2pfpx_pack\PFPX_vs_NOAA"

copy "data\airports" "wx2pfpx_pack\data\airports"
copy "dist\wx2pfpx.exe" "wx2pfpx_pack\"
copy "src\ReadMe.txt" "wx2pfpx_pack\"
copy "src\wx2pfpx.png" "wx2pfpx_pack\"
copy "src\PFPX_vs_NOAA\*" "wx2pfpx_pack\PFPX_vs_NOAA"
del "wx2pfpx1.1.zip"
powershell Compress-Archive -Path 'wx2pfpx_pack' -DestinationPath 'wx2pfpx1.1.zip'


rmdir /s /q "build"
rmdir /s /q "dist"