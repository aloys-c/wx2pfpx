pyinstaller prog.spec

mkdir "wx2pfpx_pack/data"
mkdir "wx2pfpx_pack/output"

copy "data\airports" "wx2pfpx_pack\data\airports"
copy "dist\wx2pfpx.exe" "wx2pfpx_pack\"
copy "src\ReadMe.txt" "wx2pfpx_pack\"
copy "src\wx2pfpx.png" "wx2pfpx_pack\"
del "wx2pfpx1.0.zip"
powershell Compress-Archive -Path 'wx2pfpx_pack' -DestinationPath 'wx2pfpx1.0.zip'


rmdir /s /q "build"