mkdir "wx2pfpx/data"
mkdir "wx2pfpx/output"

copy "data\airports" "wx2pfpx\data\airports"
copy "dist\wx2pfpx.exe" "wx2pfpx\"
copy "src/ReadMe.txt" "wx2pfpx\"
del "wx2pfpx1.0.zip"
powershell Compress-Archive -Path 'wx2pfpx' -DestinationPath 'wx2pfpx1.0.zip'

rmdir /s /q "dist"
rmdir /s /q "build"