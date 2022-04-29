pyinstaller prog.spec

rmdir /s /q "wx2pfpx_pack"

mkdir "wx2pfpx_pack/data"
mkdir "wx2pfpx_pack/output"
mkdir "wx2pfpx_pack\images_doc"

copy "data\airports" "wx2pfpx_pack\data\airports"
copy "data\stations" "wx2pfpx_pack\data\stations"

copy "dist\wx2pfpx.exe" "wx2pfpx_pack\"

copy "src\ReadMe.txt" "wx2pfpx_pack\"
copy "src\wx2pfpx.png" "wx2pfpx_pack\"
copy "src\default_network.png" "wx2pfpx_pack\"
copy "src\documentation\*" "wx2pfpx_pack\images_doc"
copy "settings.cfg" "wx2pfpx_pack\"

del "wx2pfpx2.5.zip"
powershell Compress-Archive -Path 'wx2pfpx_pack' -DestinationPath 'wx2pfpx2.5.zip'


rmdir /s /q "build"
rmdir /s /q "dist"