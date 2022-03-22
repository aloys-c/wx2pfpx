pyinstaller prog.spec

rmdir /s /q "wx2pfpx_pack"

mkdir "wx2pfpx_pack/data"
mkdir "wx2pfpx_pack/output"
mkdir "wx2pfpx_pack\wx2pfpx_vs_NOAA"

copy "data\airports" "wx2pfpx_pack\data\airports"
copy "data\grid" "wx2pfpx_pack\data\grid"
copy "data\stations" "wx2pfpx_pack\data\stations"
copy "data\grid.list" "wx2pfpx_pack\data\grid.list"
copy "data\stations.list" "wx2pfpx_pack\data\stations.list"

copy "dist\wx2pfpx.exe" "wx2pfpx_pack\"

copy "src\ReadMe.txt" "wx2pfpx_pack\"
copy "src\wx2pfpx.png" "wx2pfpx_pack\"
copy "src\Stations.png" "wx2pfpx_pack\"
copy "src\Grid.png" "wx2pfpx_pack\"
copy "src\wx2pfpx_vs_NOAA\*" "wx2pfpx_pack\wx2pfpx_vs_NOAA"

del "wx2pfpx2.0.zip"
powershell Compress-Archive -Path 'wx2pfpx_pack' -DestinationPath 'wx2pfpx2.0.zip'


rmdir /s /q "build"
rmdir /s /q "dist"